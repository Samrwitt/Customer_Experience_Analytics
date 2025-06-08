from google_play_scraper import Sort, reviews
import pandas as pd

def fetch_reviews(app_id, bank_name, count=400):
    all_reviews = []
    cursor = None

    while len(all_reviews) < count:
        r, cursor = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=min(100, count - len(all_reviews)),
            continuation_token=cursor
        )
        for entry in r:
            all_reviews.append({
                "review": entry['content'],
                "rating": entry['score'],
                "date": entry['at'].date().isoformat(),
                "bank": bank_name,
                "source": "Google Play"
            })
    return pd.DataFrame(all_reviews)

if __name__ == "__main__":
    apps = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp"
}


    combined_df = pd.DataFrame()

    for bank, app_id in apps.items():
        print(f"Scraping {bank}...")
        df = fetch_reviews(app_id, bank)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df.to_csv("clean_reviews.csv", index=False)
    print("Saved to clean_reviews.csv")
