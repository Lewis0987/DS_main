//go:build e2e

package e2e

// Story 09: Long-term Event - 基本流程
//
// 目的：驗證 Long-term 活動從建立到結算的完整 E2E 流程。
//
// Long-term vs Quick Match 的差異：
//   - 沒有房間概念：虛擬房間 ID = Tournament ID
//   - 玩家透過 MQ 加入活動（不需要 match service 配對）
//   - NotifyBet 的 RoomId = TournamentId
//   - 可多次投注，分數累積（期間排名持續更新）
//   - 結算時機：活動 end_time 到期後，EventStatusScheduler 觸發 PerformSettlement
//
// 流程：
//  1. 建立 long_term 活動（end_time = now+30s，score_mode=bet_amount，固定獎金）
//  2. 等待活動狀態 → running（ensureLongTermRoomHistory 同時建立虛擬房間）
//  3. 送 2 位玩家加入 MQ 請求
//  4. 等待玩家出現在 participation 表（WaitForRoom → room_id = tournament_id）
//  5. 多次 gRPC NotifyBet（RoomId = TournamentId）→ 分數累積
//  6. 等待活動結束 (end_time) + 調度器觸發結算（docker-compose SCHEDULER_INTERVAL=5s）
//  7. 等待 tournament_settlement.status = completed
//  8. 驗證排名與獎金（依累積 bet_amount 排名）
//
// 投注明細：
//   P1: 3000 + 2000 = 5000（rank=1 預期）
//   P2: 1000 + 1000 = 2000（rank=2 預期）
//
// 金額單位：內部 × 10000，$0.30=3000，$0.20=2000，$0.10=1000

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	pb "tournament-core-service/proto"

	"tournament-e2e/testutil"
)

func TestStory09_LongTerm_BasicFlow(t *testing.T) {
	now := time.Now().UTC()
	runID := now.UnixMilli()
	p1ID := fmt.Sprintf("s09p1-%d", runID)
	p2ID := fmt.Sprintf("s09p2-%d", runID)
	ticketBase := fmt.Sprintf("S09-%d", runID)

	// 步驟 1：建立 long_term 活動（end_time = now+30s，scheduler 5s poll → 最多 35s 後結算）
	eventEndTime := now.Add(30 * time.Second)
	tournamentID, err := adminClient.CreateEvent(map[string]interface{}{
		"name":              map[string]string{"en": "S09 LongTerm Basic Test"},
		"event_type":        "long_term",
		"begin_time":        now.Add(-1 * time.Minute).Format(time.RFC3339),
		"end_time":          eventEndTime.Format(time.RFC3339),
		"timezone":          "UTC",
		"min_players":       1, // long_term 不需要配對，min=1 表示無門檻
		"max_players":       100,
		"score_mode":        "bet_amount",
		"score_coefficient": 1,
		"base_currency":     "USD",
		"pool_ratio":        0.5,
		"system_ratio":      0.5,
		"total_budget":      1000.0,
		"allowed_games":     []string{"10001"},
		"platforms": []map[string]string{
			{"platform_code": "TEST", "brand_code": "BRAND1", "site_code": "SITE1"},
		},
		"exchange_rates": []map[string]string{
			{"currency_code": "USD", "ratio": "1"},
		},
		"tiers": []map[string]interface{}{
			{
				"tier_id":        "default",
				"tier_name_i18n": map[string]string{"en": "Default"},
				"tier_order":     1,
				"pool_distribution": []map[string]interface{}{
					{"rank_from": 1, "rank_to": 99, "percentage": "0"},
				},
				"fixed_prizes": []map[string]interface{}{
					{"rank": 1, "amount": "10"},
					{"rank": 2, "amount": "5"},
				},
				"currencies": []map[string]string{
					{"currency": "USD", "min_stake_amount": "0.01", "min_player_balance": "0.01"},
				},
			},
		},
	})
	require.NoError(t, err, "建立 long_term 活動失敗")
	_ = redisClient.InvalidateAvailableEventsCache("TEST", "BRAND1", "SITE1")
	testutil.RegisterCleanup(t, testDB, tournamentID, redisClient)
	t.Logf("✅ Long-term 活動已建立: %s（end_time=%s）", tournamentID, eventEndTime.Format(time.RFC3339))

	// 步驟 2：等待活動 running（同時 ensureLongTermRoomHistory 建立虛擬房間）
	testutil.WaitForEventStatus(t, adminClient, tournamentID, "running", 30*time.Second)
	t.Log("✅ 活動狀態: running，虛擬房間已建立")

	testutil.RegisterPlayersOnline(t, "TEST", "BRAND1", "SITE1", p1ID, p2ID)

	// 步驟 3：兩位玩家加入
	err = mqClient.SendPlayerJoin("TEST", "BRAND1", "SITE1", p1ID, tournamentID, "USD","p1", 10000)
	require.NoError(t, err, "p1 加入失敗")
	err = mqClient.SendPlayerJoin("TEST", "BRAND1", "SITE1", p2ID, tournamentID, "USD","p2", 10000)
	require.NoError(t, err, "p2 加入失敗")
	t.Logf("✅ 已送出 2 位玩家加入請求（p1=%s, p2=%s）", p1ID, p2ID)

	// 步驟 4：等待玩家出現在 participation 表
	// Long-term: room_id = tournament_id（虛擬房間）
	roomID := testutil.WaitForRoom(t, testDB, tournamentID, 30*time.Second)
	// 對於 long_term，虛擬房間 ID 應等於 tournament_id
	assert.Equal(t, tournamentID, roomID, "Long-term 活動的 room_id 應等於 tournament_id")
	t.Logf("✅ 玩家已加入，虛擬房間 ID: %s", roomID)

	// 步驟 5：多次投注（RoomId = tournamentID）
	// P1: 第一次 bet=3000，第二次 bet=2000 → 累積 5000
	// P2: 第一次 bet=1000，第二次 bet=1000 → 累積 2000
	ctx := context.Background()
	betTime := now.Add(5 * time.Second).UnixMilli()

	bets := []struct {
		playerID  string
		ticketSfx string
		amount    int64
		ts        int64
	}{
		{p1ID, "-P1T1", 3000, betTime},
		{p2ID, "-P2T1", 1000, betTime + 100},
		{p1ID, "-P1T2", 2000, betTime + 1000},
		{p2ID, "-P2T2", 1000, betTime + 1100},
	}

	for _, b := range bets {
		betResp, betErr := grpcClient.Client().NotifyBet(ctx, &pb.BetNotification{
			AccountId:    b.playerID,
			TicketNo:     ticketBase + b.ticketSfx,
			Platform:     "TEST", Brand: "BRAND1", Site: "SITE1",
			RoomId:       tournamentID, // Long-term: RoomId = TournamentId
			TournamentId: tournamentID,
			BetAmount:    b.amount,
			Currency:     "USD",
			Timestamp:    b.ts,
			GameCode:     "10001",
			EventType:    "LONG_TERM",
		})
		require.NoError(t, betErr)
		require.True(t, betResp.Success, "NotifyBet 失敗 player=%s ticket=%s: %s",
			b.playerID, ticketBase+b.ticketSfx, betResp.Message)
	}
	t.Log("✅ 多次投注完成（P1 累積 5000，P2 累積 2000）")

	// NotifyWin（bet_amount 模式 win=0）
	winTime := betTime + 2000
	for _, tc := range []struct {
		id       string
		ticketNo string
	}{
		{p1ID, ticketBase + "-P1T1"},
		{p1ID, ticketBase + "-P1T2"},
		{p2ID, ticketBase + "-P2T1"},
		{p2ID, ticketBase + "-P2T2"},
	} {
		winResp, winErr := grpcClient.Client().NotifyWin(ctx, &pb.WinNotification{
			AccountId: tc.id, TicketNo: tc.ticketNo,
			Platform: "TEST", Brand: "BRAND1", Site: "SITE1",
			RoomId: tournamentID, TournamentId: tournamentID,
			WinAmount: 0, Currency: "USD", Timestamp: winTime, GameCode: "10001",
		})
		require.NoError(t, winErr)
		require.True(t, winResp.Success, "%s NotifyWin 失敗: %s", tc.id, winResp.Message)
		winTime++
	}
	t.Log("✅ 所有 NotifyWin 完成")

	// 步驟 6+7：等待 end_time 後結算完成
	// end_time = now+30s，scheduler poll = 5s → 最多 90s 後應完成
	t.Log("⏳ 等待活動 end_time 到期並結算...")
	testutil.WaitForSettlement(t, testDB, tournamentID, roomID, "completed", 120*time.Second)
	t.Log("✅ 結算完成")

	// 步驟 8：驗證 P1（累積 bet=5000 → rank=1）
	rank1, prize1, currency1, err := testDB.GetSettlementDetail(tournamentID, roomID, p1ID)
	require.NoError(t, err, "取得 p1 結算詳情失敗")
	assert.Equal(t, 1, rank1, "P1（累積 5000）應為 rank=1")
	assert.Equal(t, int64(100000), prize1, "P1 prize 應為 100000（rank=1 固定獎金 $10）")
	assert.Equal(t, "USD", currency1, "P1 currency 應為 USD")
	t.Logf("✅ P1: rank=%d prize=%d currency=%s", rank1, prize1, currency1)

	// 驗證 P2（累積 bet=2000 → rank=2）
	rank2, prize2, currency2, err := testDB.GetSettlementDetail(tournamentID, roomID, p2ID)
	require.NoError(t, err, "取得 p2 結算詳情失敗")
	assert.Equal(t, 2, rank2, "P2（累積 2000）應為 rank=2")
	assert.Equal(t, int64(50000), prize2, "P2 prize 應為 50000（rank=2 固定獎金 $5）")
	assert.Equal(t, "USD", currency2, "P2 currency 應為 USD")
	t.Logf("✅ P2: rank=%d prize=%d currency=%s", rank2, prize2, currency2)

	// 驗證 P1 final_score（應為累積投注 = 5000）
	p1Score, err := testDB.GetPlayerFinalScore(tournamentID, roomID, p1ID)
	require.NoError(t, err, "取得 p1 final_score 失敗")
	assert.Equal(t, int64(5000), p1Score, "P1 累積 final_score 應為 5000")
	t.Logf("✅ P1 final_score=%d（累積投注）", p1Score)

	// 驗證 P2 final_score（應為累積投注 = 2000）
	p2Score, err := testDB.GetPlayerFinalScore(tournamentID, roomID, p2ID)
	require.NoError(t, err, "取得 p2 final_score 失敗")
	assert.Equal(t, int64(2000), p2Score, "P2 累積 final_score 應為 2000")
	t.Logf("✅ P2 final_score=%d（累積投注）", p2Score)

	// 驗證 used_budget（P1 $10 + P2 $5 = $15 = 150000）
	usedBudget, err := testDB.GetEventUsedBudget(tournamentID)
	require.NoError(t, err, "取得 used_budget 失敗")
	assert.Equal(t, int64(150000), usedBudget, "used_budget 應為 150000（$10 + $5）")
	t.Logf("✅ used_budget=%d（rank1 $10 + rank2 $5）", usedBudget)
}
