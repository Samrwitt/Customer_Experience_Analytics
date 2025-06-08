import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Load themed reviews
df = pd.read_csv("data/processed/themed_reviews.csv")

# Convert stringified list to real list (if needed)
import ast
df['themes'] = df['themes'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Make sure output folder exists
os.makedirs("reports/figures", exist_ok=True)

# 1. Sentiment distribution per bank
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="bank", hue="sentiment_label")
plt.title("Sentiment Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("reports/figures/sentiment_by_bank.png")
plt.close()

# 2. Most common themes overall
from collections import Counter
all_themes = [theme for sublist in df['themes'] for theme in sublist]
theme_counts = Counter(all_themes)
theme_df = pd.DataFrame(theme_counts.items(), columns=['Theme', 'Count']).sort_values(by='Count', ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(data=theme_df, x="Theme", y="Count")
plt.title("Most Frequent Themes Across All Reviews")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("reports/figures/theme_distribution.png")
plt.close()

# 3. Heatmap of Theme × Sentiment
theme_sentiment = []

for _, row in df.iterrows():
    for theme in row['themes']:
        theme_sentiment.append((theme, row['sentiment_label']))

theme_sentiment_df = pd.DataFrame(theme_sentiment, columns=['Theme', 'Sentiment'])
pivot = theme_sentiment_df.value_counts().unstack().fillna(0)

plt.figure(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="coolwarm")
plt.title("Theme vs Sentiment Heatmap")
plt.tight_layout()
plt.savefig("reports/figures/theme_sentiment_heatmap.png")
plt.close()

# 4. Word Cloud from all cleaned reviews
text_blob = " ".join(df['cleaned_review'].dropna().tolist())

wc = WordCloud(width=1000, height=400, background_color='white').generate(text_blob)
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Review Keywords")
plt.tight_layout()
plt.savefig("reports/figures/wordcloud_keywords.png")
plt.close()

print("All plots saved in: reports/figures/")
