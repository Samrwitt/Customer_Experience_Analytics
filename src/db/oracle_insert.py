"""
oracle_insert.py

This script connects to an Oracle XE database and inserts cleaned mobile banking
app review data into two relational tables: banks and reviews.

Usage:
    Ensure Oracle DB is running and themed_reviews.csv exists at:
    data/processed/themed_reviews.csv

    Then run:
        python3 src/db/oracle_insert.py
"""

import os
import oracledb
import pandas as pd
import ast
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

USERNAME = os.getenv("ORACLE_USERNAME")
PASSWORD = os.getenv("ORACLE_PASSWORD")
DSN = os.getenv("ORACLE_DSN")

# === Load and prepare data ===
DATA_PATH = "data/processed/themed_reviews.csv"
df = pd.read_csv(DATA_PATH)

# Convert themes column from stringified list to comma-separated string
df['theme'] = df['themes'].apply(lambda x: ", ".join(ast.literal_eval(x)) if isinstance(x, str) else "")

# === Connect to Oracle ===
print("🔌 Connecting to Oracle XE...")
conn = oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN)
cursor = conn.cursor()

# === Insert unique banks ===
print("🏦 Inserting banks...")
bank_ids = {}
for bank_name in df['bank'].unique():
    try:
        bank_id_var = cursor.var(int)
        cursor.execute(
            "INSERT INTO banks (name) VALUES (:1) RETURNING bank_id INTO :2",
            [bank_name, bank_id_var]
        )
        bank_id = bank_id_var.getvalue()[0]
    except oracledb.IntegrityError:
        cursor.execute("SELECT bank_id FROM banks WHERE name = :1", [bank_name])
        bank_id = cursor.fetchone()[0]
    bank_ids[bank_name] = bank_id

# === Insert reviews ===
print("📝 Inserting reviews...")
for _, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO reviews (
                review_text, rating, review_date,
                bank_id, sentiment_label, sentiment_score,
                theme, source
            ) VALUES (
                :review, :rating, TO_DATE(:date, 'YYYY-MM-DD'),
                :bank_id, :sentiment, :score,
                :theme, :source
            )
        """, {
            "review": row['review'],
            "rating": row['rating'],
            "date": row['date'],
            "bank_id": bank_ids[row['bank']],
            "sentiment": row['sentiment_label'],
            "score": row['sentiment_score'],
            "theme": row['theme'],
            "source": row['source']
        })
    except Exception as e:
        print(f"⚠️ Skipping row due to error: {e}")
        continue

# === Commit and close ===
conn.commit()
cursor.close()
conn.close()
print("✅ All data inserted successfully into Oracle DB.")
