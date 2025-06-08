#  Customer Experience Analytics – Mobile Banking Apps (Week 2 Challenge)

This repository contains the full pipeline for collecting, processing, analyzing, and storing customer reviews from Google Play Store for three major Ethiopian banks: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank**.

##  Business Objective

Omega Consultancy aims to help banks retain users and improve mobile banking experiences by analyzing real user feedback. This project supports that goal through:

- Scraping app reviews from Google Play Store
- Performing sentiment and theme analysis using NLP
- Storing structured insights into an Oracle database

---

##  Task 1: Data Collection & Preprocessing

### Description:
We collected 400+ reviews per bank using the `google-play-scraper` library and saved them into structured CSV files for further processing.

### Activities:
- Created a modular scraping script (`scrape_reviews.py`)
- Verified actual Google Play Store App IDs:
  - CBE: `com.combanketh.mobilebanking`
  - BOA: `com.boa.boaMobileBanking`
  - Dashen: `com.dashen.dashensuperapp`
- Scraped fields: `review`, `rating`, `date`, `bank`, and `source`
- Saved raw reviews to `data/raw/clean_reviews.csv`

### Preprocessing:
- Removed duplicates and empty/short reviews
- Normalized date format to `YYYY-MM-DD`
- Output cleaned data to `data/processed/cleaned_reviews.csv`

---

##  Task 2: Sentiment & Thematic Analysis

### Sentiment Analysis:
- Used `distilbert-base-uncased-finetuned-sst-2-english` from Hugging Face (with fallback to TextBlob if offline)
- Annotated each review with:
  - `sentiment_label` (POSITIVE / NEGATIVE / NEUTRAL)
  - `sentiment_score` (0 to 1)
- Output saved to `data/processed/sentiment_reviews.csv`

### Thematic Analysis:
- Cleaned reviews using SpaCy (tokenization, lemmatization)
- Extracted top n-grams using TF-IDF (1–2 grams)
- Manually defined and applied 5 theme groups:
  - Login/Access Issues
  - Transfer/Speed Problems
  - UI/UX
  - Features
  - Crashes/Bugs
- Assigned themes to each review and saved final dataset to `data/processed/themed_reviews.csv`

---

##  Task 3: Oracle Database Engineering (In Progress)

### Planned Schema:

**Banks Table**
| Column     | Type        | Description           |
|------------|-------------|------------------------|
| bank_id    | NUMBER      | Primary key            |
| name       | VARCHAR2(100) | Bank name (unique)    |

**Reviews Table**
| Column          | Type        | Description                         |
|------------------|-------------|-------------------------------------|
| review_id        | NUMBER      | Primary key                         |
| review_text      | CLOB        | Full user review                    |
| rating           | NUMBER      | 1–5 stars                           |
| review_date      | DATE        | Review date                         |
| bank_id          | NUMBER      | Foreign key to `banks`              |
| sentiment_label  | VARCHAR2(10)| POSITIVE / NEGATIVE / NEUTRAL       |
| sentiment_score  | FLOAT       | Model confidence                    |
| theme            | VARCHAR2(200) | Comma-separated theme labels      |
| source           | VARCHAR2(50) | Review source (Google Play)        |

### Insert Script (Planned):
- Read cleaned data from `themed_reviews.csv`
- Insert into Oracle using `oracledb` Python client
- Connection string: `localhost/XEPDB1` (customizable)

