import os
import json
import pandas as pd

class DataAggregator:
    def __init__(self, processed_path="./data/processed", output_path="./data/analytics"):
        self.processed_path = processed_path
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def generate_metrics(self):
        data = []
        files = [f for f in os.listdir(self.processed_path) if f.endswith('.json')]
        
        if not files:
            print("No data to process.")
            return

        for file in files:
            with open(os.path.join(self.processed_path, file), 'r') as f:
                data.append(json.load(f))
        
        df = pd.DataFrame(data)
        
        # 1: Number of websites with case studies
        case_studies = df[(df['section'] == 'case_study') & (df['isActive'] == True)]
        total_case_studies = case_studies['website'].nunique()

        # 2: Content length stats
        df['content_length'] = df['content'].apply(len)
        stats = df.groupby('section')['content_length'].describe()

        # Save Metrics
        with open(os.path.join(self.output_path, "summary_metrics.txt"), 'w') as f:
            f.write(f"Total Websites with Case Studies: {total_case_studies}\n")
            f.write("\nContent Length Statistics:\n")
            f.write(stats.to_string())
            
        print("Metrics generated successfully.")