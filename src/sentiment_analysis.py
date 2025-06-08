import pandas as pd
from transformers import pipeline
from tqdm import tqdm

tqdm.pandas()

# Load cleaned reviews
df = pd.read_csv("data/processed/cleaned_reviews.csv")

# Load Hugging Face sentiment model
print(" Loading sentiment model...")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Run sentiment analysis
print("⚙️ Analyzing sentiments...")
df['sentiment_result'] = df['review'].progress_apply(lambda x: classifier(x[:512])[0])

# Extract sentiment label and score
df['sentiment_label'] = df['sentiment_result'].apply(lambda x: x['label'])
df['sentiment_score'] = df['sentiment_result'].apply(lambda x: x['score'])

# Drop the raw result column
df.drop(columns=['sentiment_result'], inplace=True)

# Save output
output_path = "data/processed/sentiment_reviews.csv"
df.to_csv(output_path, index=False)
print(f" Saved sentiment-labeled data to: {output_path}")
