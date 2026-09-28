from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def preprocess_data():
    # Membaca dan membersihkan seluruh data raw GDELT.

    files = list(RAW_DIR.glob("*.csv"))

    if not files:
        print("Tidak ada file CSV di data/raw/")
        return

    dataframes = []

    for file in files:
        df = pd.read_csv(file)
        dataframes.append(df)

    data = pd.concat(dataframes, ignore_index=True)

    print(f"Data sebelum preprocessing: {len(data)} baris")

    data = data.drop_duplicates(subset="url")

    data = data.dropna(subset=["url", "title"])

    data["seendate"] = pd.to_datetime(
        data["seendate"],
        errors="coerce",
    )

    data = data.dropna(subset=["seendate"])

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / "gdelt_articles_processed.csv"
    data.to_csv(output_file, index=False)

    print(f"Data setelah preprocessing: {len(data)} baris")
    print(f"File processed: {output_file}")


if __name__ == "__main__":
    preprocess_data()
