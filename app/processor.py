from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import re
import pandas as pd
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import unicodedata


def ensure_vader():
    # ודא שהלקסיקון זמין (למקרה שרץ מחוץ לדוקר)
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')


def normalize_text(s: str) -> str:
    # נרמול קל, שמירה על a-z0-9 ומקף (לזיהוי ak-47)
    s = unicodedata.normalize("NFKC", s)
    return s


TOKEN_RE = re.compile(r"[A-Za-z0-9\-]+")

# סט בסיסי של stopwords כדי לא לבחור מילים שכיחות מדי
BASIC_STOPWORDS = {
    "the","a","an","and","or","but","if","then","so","to","of","in","on","at","for",
    "we","will","is","are","am","be","was","were","it","this","that","with","as","by",
    "due","i","you","he","she","they","them","our","your","their"
}


BASE_DIR = Path(__file__).resolve().parent.parent
WEAPONS_FILE = os.getenv("WEAPONS_FILE", str(BASE_DIR/ "app" / "data" / "weapons.txt"))
class TextProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.weapons = self._load_weapons(WEAPONS_FILE)
        ensure_vader()
        self.sentiment_model = SentimentIntensityAnalyzer()

    def _load_weapons(self, path: str) -> List[str]:
        if not os.path.exists(path):
            print("neeeeeeee")
            return []
        print("qqqqqqqq")
        with open(path, "r", encoding="utf-8") as f:
            words = [w.strip().lower() for w in f if w.strip()]
        words.sort(key=len, reverse=True)
        return words

    def _tokenize(self, text: str) -> List[str]:
        text = normalize_text(text).lower()
        return [t for t in TOKEN_RE.findall(text)]

    def _corpus_counts(self) -> Counter:
        c = Counter()
        for t in self.df["original_text"].fillna(""):
            toks = [w for w in self._tokenize(t) if w not in BASIC_STOPWORDS and len(w) > 2]
            c.update(toks)
        return c

    def add_rarest_word(self) -> "TextProcessor":
        corpus = self._corpus_counts()
        def rarest_for_text(text: str) -> str:
            toks = [w for w in self._tokenize(text) if w not in BASIC_STOPWORDS and len(w) > 2]
            if not toks:
                return ""
            freqs = [(w, corpus.get(w, 0)) for w in toks]
            min_freq = min(f for _, f in freqs)
            for w in toks:
                if corpus.get(w, 0) == min_freq:
                    return w
            return toks[-1]

        self.df["rarest_word"] = self.df["original_text"].fillna("").apply(rarest_for_text)
        return self

    def add_sentiment(self) -> "TextProcessor":
        def label(text: str) -> str:
            s = self.sentiment_model.polarity_scores(text or "")
            c = s.get("compound", 0.0)
            if c >= 0.5:
                return "positive"
            if c <= -0.5:
                return "negative"
            return "neutral"

        self.df["sentiment"] = self.df["original_text"].fillna("").apply(label)
        return self

    def add_weapons_detected(self) -> "TextProcessor":

        def detect(text: str) -> str:
            t = normalize_text(text or "").lower()
            for w in self.weapons:
                pattern = rf"(?<!\w){re.escape(w)}(?!\w)"
                if re.search(pattern, t):
                    return w
            return ""

        self.df["weapons_detected"] = self.df["original_text"].fillna("").apply(detect)
        return self

    def current(self) -> pd.DataFrame:
        return self.df.copy()
