from fitness_tracker import FitnessTracker

def main():
    app = FitnessTracker()
    plan = app.start_session()
    results = app.record_workout(plan)
    app.analyze_session(results)

if __name__ == "__main__":
    main()
