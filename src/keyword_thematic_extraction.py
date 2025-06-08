import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from tqdm import tqdm

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")
tqdm.pandas()

# Load cleaned sentiment-labeled data
df = pd.read_csv("data/processed/sentiment_reviews.csv")

# Step 1: NLP-based cleaning (lemmatization, stopword removal)
def clean_text(text):
    doc = nlp(str(text).lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha and len(token) > 2]
    return " ".join(tokens)

df['cleaned_review'] = df['review'].progress_apply(clean_text)

# Step 2: TF-IDF keyword extraction
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
X = vectorizer.fit_transform(df['cleaned_review'])
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = X.sum(axis=0).A1

keywords_df = pd.DataFrame({
    'keyword': feature_names,
    'score': tfidf_scores
}).sort_values(by='score', ascending=False)

# Save top 50 keywords
top_keywords_path = "data/processed/top_keywords.csv"
keywords_df.head(50).to_csv(top_keywords_path, index=False)
print(f"Saved top keywords to {top_keywords_path}")

# Step 3: Rule-based theme grouping
theme_rules = {
    "Login/Access Issues": ["login", "password", "failed", "sign", "account", "access", "open"],
    "Transfer/Speed Problems": ["transfer", "slow", "delay", "hang", "loading", "wait"],
    "UI/UX": ["ui", "interface", "layout", "design", "experience", "look", "navigate"],
    "Features": ["fingerprint", "qr", "wallet", "card", "balance", "feature", "add"],
    "Crashes/Bugs": ["crash", "bug", "error", "close", "freeze", "stop"]
}

def assign_themes(text):
    text = str(text).lower()
    matched_themes = []
    for theme, keywords in theme_rules.items():
        if any(keyword in text for keyword in keywords):
            matched_themes.append(theme)
    return matched_themes if matched_themes else ["Other"]

df['themes'] = df['cleaned_review'].progress_apply(assign_themes)

# Save final themed dataset
final_output = "data/processed/themed_reviews.csv"
df.to_csv(final_output, index=False)
print(f"Saved themed reviews to {final_output}")
