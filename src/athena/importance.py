from athena.models import NLPFeatures

class ImportanceScorer:
    """
    Scores how important a completed conversation is.
    Returns a value between 0.0 and 1.0.
    """
    def score(self, features: NLPFeatures)-> float:
        info_density = (
            0.7 * features.noun_ratio +
            0.3 * features.verb_ratio           # INFORMATION DENSITY
        )
        entity_score = min(features.entity_count/2 , 1.0) #Named entities
        tfidf_score = min(features.tfidf_mean * 12, 1.0)
        length_score = min(features.token_count/10, 1.0)

        score = (
            0.15 * length_score +
            0.40 * info_density +
            0.20 * entity_score + 
            0.25 * tfidf_score
        )

        return round(max(0.0, min(score,1.0)),3)