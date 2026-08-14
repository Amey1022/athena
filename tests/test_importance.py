from athena.importance import ImportanceScorer

scorer = ImportanceScorer()

def test_high_importance():
    score = scorer.score(
        "We implemented the ATHENA memory architecture and completed database refactor"
    )
    assert score >0.7

def test_low_importance():
    score= scorer.score(
        "Hello, thank you and bye."
    )
    assert score < 0.3
