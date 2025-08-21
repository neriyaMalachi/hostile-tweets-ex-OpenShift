import pandas as pd
from fetcher import MongoFetcher
from processor import TextProcessor
from config import WEAPONS_FILE  # ← חדש


class PipelineManager:

    def __init__(self, weapons_file: str = "/app/data/weapons.txt"):
        self.weapons_file = weapons_file or WEAPONS_FILE

    def run(self) -> pd.DataFrame:
        fetcher = MongoFetcher()
        raw_df = fetcher.fetch_all()
        proc = (
            TextProcessor(raw_df, weapons_file=self.weapons_file)
            .add_rarest_word()
            .add_sentiment()
            .add_weapons_detected()
        )
        return proc.current()

    def as_records(self) -> list[dict]:
        df = self.run()
        out = []
        for _, row in df.iterrows():
            out.append({
                "id": row.get("id", ""),
                "original_text": row.get("original_text", ""),
                "rarest_word": row.get("rarest_word", ""),
                "sentiment": row.get("sentiment", ""),
                "weapons_detected": row.get("weapons_detected", "")
            })
        return out
