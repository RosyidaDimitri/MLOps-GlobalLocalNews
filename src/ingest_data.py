import argparse
import time
from datetime import datetime

import pandas as pd
import requests


GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_gdelt(query, timespan="1h", maxrecords=100):
    # Mengambil data artikel terbaru dari GDELT DOC API.

    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": maxrecords,
        "format": "json",
        "timespan": timespan,
    }

    max_retries = 3
    wait_seconds = 5

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                GDELT_URL,
                params=params,
                timeout=30,
            )

            if response.status_code == 429:
                print(
                    f"Rate limit GDELT (429). "
                    f"Percobaan {attempt}/{max_retries}."
                )

                if attempt < max_retries:
                    print(f"Menunggu {wait_seconds} detik...")
                    import time
                    time.sleep(wait_seconds)
                    wait_seconds *= 2
                    continue

                print("Gagal setelah beberapa kali percobaan.")
                return None

            response.raise_for_status()
            data = response.json()

            articles = data.get("articles", [])

            if not articles:
                print("Tidak ada artikel yang ditemukan.")
                return None

            return articles

        except requests.exceptions.Timeout:
            print(
                f"Request timeout. "
                f"Percobaan {attempt}/{max_retries}."
            )

        except requests.exceptions.RequestException as error:
            print(f"Gagal mengambil data dari GDELT: {error}")
            return None

        except ValueError:
            print("Response dari GDELT bukan JSON yang valid.")
            return None

    return None


def save_raw_data(articles):
    # Menyimpan data raw ke CSV dengan nama berdasarkan waktu ingestion.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"data/raw/gdelt_articles_{timestamp}.csv"

    df = pd.DataFrame(articles)
    df.to_csv(output_path, index=False)

    print(f"Berhasil menyimpan {len(df)} artikel.")
    print(f"File: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Mengambil data artikel dari GDELT."
    )

    parser.add_argument(
        "--query",
        default="climate change",
        help="Topik atau kata kunci yang dicari.",
    )

    parser.add_argument(
        "--timespan",
        default="1h",
        help="Rentang waktu data, contoh: 1h, 6h, 1d.",
    )

    parser.add_argument(
        "--maxrecords",
        type=int,
        default=100,
        help="Jumlah maksimum artikel.",
    )

    args = parser.parse_args()

    articles = fetch_gdelt(
        query=args.query,
        timespan=args.timespan,
        maxrecords=args.maxrecords,
    )

    if articles is not None:
        save_raw_data(articles)


if __name__ == "__main__":
    main()