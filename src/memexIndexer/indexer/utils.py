from typing import List
import nltk
from nltk import word_tokenize


try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("stopwords")
except LookupError:
    nltk.download("stopwords")

from nltk.corpus import stopwords


def get_tokens(data: str) -> List[str]:
    stop = set(stopwords.words("english"))
    tokens = word_tokenize(data)
    filtered = [t.lower() for t in tokens if t.lower() not in stop and t.isalnum()]
    return filtered
