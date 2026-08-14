from athena.nlp import NLPProcessor

processor = NLPProcessor()

def test_lemmatization():
    lemmas = processor.lemmatize(
        "Implemented databases and implementing architecture."
    )
    assert "implement" in lemmas
    assert "database" in lemmas

def test_stopwords_removed():
    lemmas = processor.lemmatize(
        "This is a very important project"
    )
    assert "is" not in lemmas
    assert "a" not in lemmas

def test_entity_detection():
    features = processor.extract_features(
        "Amey joined Bosch in August"
    )
    assert features.entity_count >=2
    