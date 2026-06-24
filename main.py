from fitness_tracker import FitnessTracker

def main():
    print("====================================")
    print(" 歡迎使用 健身紀錄反饋 APP (GitHub 版) ")
    print("====================================\n")
    
    app = FitnessTracker()
    
    # A. 訓練前：計畫與準備
    plan = app.start_session()
    
    # B. 訓練中：數據錄入與即時回饋
    results = app.record_workout(plan)
    
    # C. 訓練後：總結與分析
    app.analyze_session(results)
    
    print("\n感謝使用，期待你下次的進步！💪")

if __name__ == "__main__":
    main()
