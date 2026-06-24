# ci_test.py
from fitness_tracker import FitnessTracker

def run_ci_test():
    print("開始執行 CI 自動化測試（無人互動版）...")
    app = FitnessTracker()
    
    # 模擬 B 階段傳入的訓練結果（跳過 input 互動）
    mock_results = {
        "深蹲": [
            {"weight": 100.0, "reps": 5},
            {"weight": 100.0, "reps": 5}, # 連續兩組達成
            {"weight": 102.5, "reps": 5}
        ]
    }
    
    # 直接執行 C 階段的分析與畫圖 (我們手動把 RPE 的 input 模擬掉)
    # 為了防止 analyze_session 裡面的 input() 報錯，我們直接呼叫裡面的計算與畫圖
    total_volume = 0
    for exercise, sets_data in mock_results.items():
        for set_data in sets_data:
            total_volume += set_data["weight"] * set_data["reps"]
            
    print(f"自動計算總負荷: {total_volume} kg")
    app.history_volumes.append(total_volume)
    app.plot_trend() # 呼叫畫圖
    print("CI 測試成功生成圖表！")

if __name__ == "__main__":
    run_ci_test()
