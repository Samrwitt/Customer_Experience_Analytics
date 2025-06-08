import pandas as pd
import os

INPUT_PATH = "data/raw/clean_reviews.csv"
OUTPUT_PATH = "data/processed/cleaned_reviews.csv"

def preprocess_reviews(input_file, output_file):
    if not os.path.exists(input_file):
        print(f" File not found: {input_file}")
        return

    df = pd.read_csv(input_file)

    print(f" Loaded {len(df)} reviews")

    df.drop_duplicates(subset=["review", "date"], inplace=True)

    df['review'] = df['review'].astype(str)
    df = df[df['review'].str.strip().str.len() > 5]

    required = {"review", "rating", "date", "bank", "source"}
    if not required.issubset(df.columns):
        print(f" Missing columns: {required - set(df.columns)}")
        return

    print(f" After cleaning: {len(df)} reviews remain")

    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f" Saved cleaned data to: {output_file}")


if __name__ == "__main__":
    preprocess_reviews(INPUT_PATH, OUTPUT_PATH)
