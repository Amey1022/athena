from athena.importance import ImportanceScorer
from athena.nlp import NLPProcessor

scorer = ImportanceScorer()
processor = NLPProcessor()

def test_high_importance():
    features = processor.extract_features(
        "We implemented the ATHENA memory architecture and completed database refactor"
    )

    assert scorer.score(features) >0.70

def test_low_importance():
    features = processor.extract_features(
        "Hello, thank you and bye."
    )
    score = scorer.score(features)

    assert score < 0.30

def test_score_range():
    features = processor.extract_features("Python")
    score = scorer.score(features)

    assert 0.0 <= score <=1.0

def test_personal_milestone():
    features = processor.extract_features(
        "I accepted an internship offer from Bosch."
    )

    score = scorer.score(features)

    assert score > 0.60