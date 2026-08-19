from athena.models import NLPFeatures

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ImportanceScorer:
    """
    Scores how important a completed conversation is.
    Returns a value between 0.0 and 1.0.
    """
    IMPORTANT = [
        "implement semantic memory architecture",
        "complete database refactor repository",
        "design modular software system",
        "finish project milestone testing",
        "accept internship offer career achievement",
    ]
    TRIVIAL = [
        "hello hi how are you",
        "thank you goodbye bye",
        "nice talking see later",
        "okay sure thanks",
    ]

    def __init__(self):
        corpus = self.IMPORTANT + self.TRIVIAL
        self.vectorizer = TfidfVectorizer()
        self.prototype_matrix = self.vectorizer.fit_transform(corpus)

    def score(self, features: NLPFeatures)-> float:
        document = " ".join(features.lemmas)
        if not document:
            return 0.0
        query = self.vectorizer.transform([document])
        similarities = cosine_similarity(query, self.prototype_matrix)[0]
        important = similarities[:len(self.IMPORTANT)].max()
        trivial = similarities[len(self.IMPORTANT):].max()

        cosine_score = (
            important / (important + trivial + 1e-6)
        )
        info_density = (
            0.7 * features.noun_ratio +
            0.3 * features.verb_ratio           # INFORMATION DENSITY
        )

        final = (
            0.8 * cosine_score +
            0.2 * info_density
        )

        return round(final,3)