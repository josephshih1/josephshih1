import time
import matplotlib.pyplot as plt

class FitnessTracker:
    def __init__(self):
        # 模擬資料庫
        self.preset_workout = {
            "深蹲": {"sets": 3, "target_reps": 5, "target_weight": 100},
            "臥推": {"sets": 3, "target_reps": 8, "target_weight": 60}
        }
        self.personal_records = {"深蹲": 110, "臥推": 70} # 歷史 PR
        self.history_volumes = [2500, 2600, 2450, 2700] # 模擬前幾次的總負荷

    # === A. 訓練前 ===
    def start_session(self):
        print("=== A. 訓練前：計畫與準備 ===")
        print("1. 按計畫訓練")
        print("2. 自由訓練")
        mode = input("請選擇模式 (1 或 2): ")
        
        current_workout = {}
        if mode == "1":
            print("\n[系統提示] 已載入今日預設計畫：")
            for exercise, details in self.preset_workout.items():
                print(f"- {exercise}: {details['target_weight']}kg x {details['sets']}組, 目標 {details['target_reps']}下")
            current_workout = self.preset_workout.copy()
        else:
            print("\n[系統提示] 進入自由訓練模式。")
            exercise_name = input("請輸入想訓練的動作名稱: ")
            sets = int(input("請輸入預計組數: "))
            target_weight = float(input("請輸入目標重量 (kg): "))
            target_reps = int(input("請輸入目標次數: "))
            current_workout[exercise_name] = {"sets": sets, "target_reps": target_reps, "target_weight": target_weight}
            
        return current_workout

    # === B. 訓練中 ===
    def record_workout(self, current_workout):
        print("\n=== B. 訓練中：數據錄入與即時回饋 ===")
        session_results = {}
        
        for exercise, target in current_workout.items():
            print(f"\n--- 開始進行【{exercise}】 ---")
            session_results[exercise] = []
            easy_streak = 0 # 紀錄連續輕鬆的組數
            
            for s in range(1, target["sets"] + 1):
                print(f"\n>> 第 {s} 組 (目標: {target['target_weight']}kg x {target['target_reps']}下)")
                
                # 1. 紀錄數據
                actual_weight = float(input(f"請輸入實際重量 (kg): "))
                actual_reps = int(input(f"請輸入實際完成次數: "))
                session_results[exercise].append({"weight": actual_weight, "reps": actual_reps})
                
                # 3. 動態調整邏輯
                if actual_weight >= target["target_weight"] and actual_reps >= target["target_reps"]:
                    easy_streak += 1
                else:
                    easy_streak = 0
                    
                if easy_streak >= 2:
                    print("💡 [動態回饋] 偵測到表現良好，建議下一組增加 2.5kg！")
                
                # 2. 自動計時 (模擬)
                print("⏱️ [系統提示] 點擊「完成」！啟動組間休息計時器 (模擬休息 3 秒)...")
                time.sleep(3)
                print("⏳ 休息時間結束，請準備下一組！")
                
        return session_results

    # === C. 訓練後 ===
    def analyze_session(self, session_results):
        print("\n=== C. 訓練後：總結與分析 ===")
        _ = input("點擊「結束訓練」以生成報告...")
        
        total_volume = 0
        new_prs = []
        
        # 1. 計算總負荷量 & 2. 檢查 PR
        for exercise, sets_data in session_results.items():
            max_weight_today = 0
            for set_data in sets_data:
                volume = set_data["weight"] * set_data["reps"]
                total_volume += volume
                if set_data["weight"] > max_weight_today:
                    max_weight_today = set_data["weight"]
            
            # PR 檢查
            history_pr = self.personal_records.get(exercise, 0)
            if max_weight_today > history_pr:
                new_prs.append((exercise, max_weight_today))
                self.personal_records[exercise] = max_weight_today # 更新 PR
                
        print(f"\n📊 本次訓練總負荷量 (Total Volume): {total_volume} kg")
        
        # 進步提醒
        if new_prs:
            print("🎉 [PR 突破提醒] 太棒了！你創下了新的個人紀錄：")
            for exercise, weight in new_prs:
                print(f"  - {exercise} 突破歷史紀錄，達到 {weight} kg！")
        else:
            print("✨ 穩定輸出！繼續保持，下次再挑戰突破！")
            
        # 疲勞評估 (RPE)
        print("\n[疲勞評估]")
        rpe = input("請輸入本次訓練的自覺強度 RPE (1-10分，10為力竭): ")
        print(f"系統已記錄 RPE: {rpe}，將作為調整下次計畫的依據。")
        
        # 3. 趨勢圖表
        self.history_volumes.append(total_volume) # 將本次結果加入歷史
        self.plot_trend()

    def plot_trend(self):
        print("\n📈 正在生成訓練強度趨勢圖表...")
        plt.figure(figsize=(8, 4))
        plt.plot(self.history_volumes, marker='o', color='b', linestyle='-', linewidth=2)
        plt.title("Weekly/Monthly Training Volume Trend")
        plt.xlabel("Sessions")
        plt.ylabel("Total Volume (kg)")
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # 在 GitHub 執行時可以儲存為圖片，本地執行則直接彈出視窗
        plt.savefig("workout_trend.png")
        print("💾 趨勢圖表已儲存為 'workout_trend.png'")
        plt.show()
