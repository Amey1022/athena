from athena.memory_detector import MemoryDetector

detector = MemoryDetector()

def test_detect_favourite_language():
    result = detector.detect(
        "My favourite programming language is Python."
    )
    assert result == [
        ("favourite_programming_language", "Python")
    ]

def test_detect_cpp():
    result= detector.detect(
        "My favourite programming language is C++"
    )
    assert result == [
        ("favourite_programming_language", "C++")
    ]

def test_ignore_normal_sentance():
    result = detector.detect(
        "I enjoy programming in Python."
    )
    assert result == []