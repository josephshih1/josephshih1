import os
import time
import matplotlib.pyplot as plt

class FitnessTracker:
    def __init__(self):
        self.preset_workout = {
            "深蹲": {"sets": 3, "target_reps": 5, "target_weight": 100},
            "臥推": {"sets": 3, "target_reps": 8, "target_weight": 60}
        }
        self.personal_records = {"深蹲": 110, "臥推": 70}
        self.history_volumes = [2500, 2600, 2450, 2700]
        
        self.is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'

    # === A. 訓練前 ===
    def start_session(self):
        print("=== A. 訓練前：計畫與準備 ===")
        if self.is_github_actions:
            print("[CI 模式] 自動選擇模式 1：按計畫訓練")
            return self.preset_workout.copy()
            
        print("1. 按計畫訓練")
        print("2. 自由訓練")
        mode = input("請選擇模式 (1 或 2): ")
        
        current_workout = {}
        if mode == "1":
            print("\n[系統提示] 已載入今日預設計畫：")
            for exercise, details in self.preset_workout.items():
                print(f"- {exercise}: {details['target_weight']}kg x {details['sets']}組")
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
            easy_streak = 0
            
            for s in range(1, target["sets"] + 1):
                print(f"\n>> 第 {s} 組 (目標: {target['target_weight']}kg x {target['target_reps']}下)")
                
                # 如果是 GitHub Actions，自動餵入完美達標數據，不呼叫 input()
                if self.is_github_actions:
                    actual_weight = target['target_weight']
                    actual_reps = target['target_reps']
                    print(f"[CI 自動輸入] 重量: {actual_weight}kg, 次數: {actual_reps}下")
                else:
                    actual_weight = float(input(f"請輸入實際重量 (kg): "))
                    actual_reps = int(input(f"請輸入實際完成次數: "))
                    
                session_results[exercise].append({"weight": actual_weight, "reps": actual_reps})
                
                if actual_weight >= target["target_weight"] and actual_reps >= target["target_reps"]:
                    easy_streak += 1
                else:
                    easy_streak = 0
                    
                if easy_streak >= 2:
                    print("💡 [動態回饋] 偵測到表現良好，建議下一組增加 2.5kg！")
                
                print("⏱️ [系統提示] 啟動組間休息計時器...")
                if not self.is_github_actions:
                    time.sleep(1) # Colab 稍等一下增加儀式感
                print("⏳ 休息時間結束！")
                
        return session_results

    # === C. 訓練後 ===
    def analyze_session(self, session_results):
        print("\n=== C. 訓練後：總結與分析 ===")
        if not self.is_github_actions:
            input("按 Enter 鍵結束訓練以生成報告...")
        
        total_volume = 0
        new_prs = []
        
        for exercise, sets_data in session_results.items():
            max_weight_today = 0
            for set_data in sets_data:
                total_volume += set_data["weight"] * set_data["reps"]
                if set_data["weight"] > max_weight_today:
                    max_weight_today = set_data["weight"]
            
            history_pr = self.personal_records.get(exercise, 0)
            if max_weight_today > history_pr:
                new_prs.append((exercise, max_weight_today))
                self.personal_records[exercise] = max_weight_today
                
        print(f"\n📊 本次訓練總負荷量 (Total Volume): {total_volume} kg")
        
        if new_prs:
            print("🎉 [PR 突破提醒] 太棒了！你創下了新的個人紀錄！")
            
        print("\n[疲勞評估]")
        if self.is_github_actions:
            rpe = "8"
            print(f"[CI 自動輸入] 自覺強度 RPE: {rpe}")
        else:
            rpe = input("請輸入本次訓練的自覺強度 RPE (1-10分): ")
            
        self.history_volumes.append(total_volume)
        self.plot_trend()

    def plot_trend(self):
        print("\n📈 正在生成訓練強度趨勢圖表...")
        plt.figure(figsize=(8, 4))
        plt.plot(self.history_volumes, marker='o', color='b', linestyle='-')
        plt.title("Weekly/Monthly Training Volume Trend")
        plt.xlabel("Sessions")
        plt.ylabel("Total Volume (kg)")
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # GitHub 模式下存成圖片，Colab/本機模式下直接秀在畫面上
        plt.savefig("workout_trend.png")
        if not self.is_github_actions:
            plt.show()
        else:
            print("💾 圖片已儲存 (GitHub 模式)")
