import time
from pathlib import Path

import pandas as pd
import requests

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

TOPICS = {
    "climate_change": "climate change",
    "energy": "energy",
    "artificial_intelligence": "artificial intelligence",
}

TIMESPAN = "7d"
WAIT_SECONDS = 12

RAW_DIR = Path("data/raw/lk06_timeline")
PROCESSED_DIR = Path("data/processed")


def fetch_timeline(query):
    params = {
        "query": query,
        "mode": "timelinevol",
        "format": "json",
        "timespan": TIMESPAN,
    }

    for attempt in range(3):
        try:
            response = requests.get(
                GDELT_URL,
                params=params,
                timeout=30,
            )

            if response.status_code == 200:
                payload = response.json()
                timeline = payload.get("timeline", [])

                if not timeline:
                    print(f"Tidak ada timeline: {query}")
                    return None

                rows = timeline[0].get("data", [])
                if not rows:
                    print(f"Tidak ada data volume: {query}")
                    return None

                return pd.DataFrame(rows)

            if response.status_code == 429:
                wait = 20 * (attempt + 1)
                print(
                    f"Rate limit untuk '{query}'. "
                    f"Tunggu {wait} detik..."
                )
                time.sleep(wait)
                continue

            print(
                f"HTTP {response.status_code} untuk '{query}'."
            )
            return None

        except requests.RequestException as error:
            print(f"Request error: {error}")
            time.sleep(WAIT_SECONDS)

    print(f"Gagal mengambil: {query}")
    return None


def collect_topic(topic_name, query):
    print(f"\n=== TOPIK: {topic_name} ===")

    global_df = fetch_timeline(query)

    if global_df is None:
        print(f"Global gagal: {topic_name}")
        return None

    global_df = global_df.rename(
        columns={
            "date": "timestamp",
            "value": "global_volume",
        }
    )

    print(f"Global berhasil: {len(global_df)} interval")

    time.sleep(WAIT_SECONDS)

    indonesia_query = f"{query} sourcecountry:indonesia"
    indonesia_df = fetch_timeline(indonesia_query)

    if indonesia_df is None:
        print(f"Indonesia gagal: {topic_name}")
        return None

    indonesia_df = indonesia_df.rename(
        columns={
            "date": "timestamp",
            "value": "indonesia_volume",
        }
    )

    print(
        f"Indonesia berhasil: "
        f"{len(indonesia_df)} interval"
    )

    data = pd.merge(
        global_df,
        indonesia_df,
        on="timestamp",
        how="outer",
    )

    data["topic"] = topic_name
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        utc=True,
    )

    data["global_volume"] = data["global_volume"].fillna(0)
    data["indonesia_volume"] = data["indonesia_volume"].fillna(0)

    return data


def create_features(data):
    data = data.sort_values(
        ["topic", "timestamp"]
    ).copy()

    data["global_growth"] = (
        data.groupby("topic")["global_volume"]
        .pct_change()
    )

    data["indonesia_growth"] = (
        data.groupby("topic")["indonesia_volume"]
        .pct_change()
    )

    data["global_indonesia_ratio"] = (
        data["global_volume"]
        / data["indonesia_volume"].replace(0, pd.NA)
    )

    previous_24h = (
        data.groupby("topic")["indonesia_volume"]
        .transform(
            lambda x: x.rolling(
                24,
                min_periods=24,
            ).sum()
        )
    )

    next_24h = (
        data.groupby("topic")["indonesia_volume"]
        .transform(
            lambda x: x.shift(-24).rolling(
                24,
                min_periods=24,
            ).sum()
        )
    )

    data["previous_24h"] = previous_24h
    data["next_24h"] = next_24h

    growth_24h = (
        (data["next_24h"] - data["previous_24h"])
        / data["previous_24h"]
    )

    data["label"] = (growth_24h >= 0.10).astype("Int64")

    data = data.dropna(
        subset=[
            "global_growth",
            "indonesia_growth",
            "label",
        ]
    )

    return data


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    successful_topics = []

    for index, (topic_name, query) in enumerate(TOPICS.items()):
        topic_data = collect_topic(
            topic_name,
            query,
        )

        if topic_data is not None:
            output = RAW_DIR / f"{topic_name}.csv"
            topic_data.to_csv(output, index=False)
            successful_topics.append(topic_data)

            print(f"Disimpan: {output}")

        if index < len(TOPICS) - 1:
            print(
                f"\nTunggu {WAIT_SECONDS} detik "
                "sebelum topik berikutnya..."
            )
            time.sleep(WAIT_SECONDS)

    if not successful_topics:
        raise RuntimeError(
            "Tidak ada topik yang berhasil diambil."
        )

    combined = pd.concat(
        successful_topics,
        ignore_index=True,
    )

    final_data = create_features(combined)

    output_file = (
        PROCESSED_DIR / "lk06_training_dataset.csv"
    )

    final_data.to_csv(
        output_file,
        index=False,
    )

    print("\n=== DATASET LK-06 ===")
    print(f"File: {output_file}")
    print(f"Rows: {len(final_data)}")
    print(f"Columns: {list(final_data.columns)}")
    print("\nTopik:")
    print(final_data["topic"].value_counts())
    print("\nLabel:")
    print(final_data["label"].value_counts())


if __name__ == "__main__":
    main()
