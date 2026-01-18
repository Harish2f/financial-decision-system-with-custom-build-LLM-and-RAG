from decision.pipeline import DecisionPipeline

def main():
    results = DecisionPipeline().run_ml()
    print("ML decisions completed")

if __name__ == "__main__":
    main()