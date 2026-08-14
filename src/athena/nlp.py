import spacy
from typing import cast
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from athena.models import NLPFeatures

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer()

    def lemmatize(self,text:str)-> list[str]:
        doc = self.nlp(text)

        lemmas = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop
            and not token.is_punct
            and not token.is_space
        ]
        return lemmas
    
    def extract_features(self, text:str)-> NLPFeatures:
        doc = self.nlp(text)
        content_tokens = [
            token for token in doc
            if not token.is_stop
            and not token.is_punct
            and not token.is_space
        ]
        token_count = len(content_tokens)
        sentence_count = max(1, len(list(doc.sents)))

        noun = sum(
            token.pos_ in ("NOUN","PROPN")
            for token in content_tokens
        )

        verb = sum(
            token.pos_ == "VERB"
            for token in content_tokens
        )
        noun_ratio = noun/ token_count if token_count else 0.0
        verb_ratio = verb/ token_count if token_count else 0.0

        return NLPFeatures(
            token_count=token_count,
            sentence_count=sentence_count,
            noun_ratio=noun_ratio,
            verb_ratio=verb_ratio,
            entity_count=len(doc.ents),
            tfidf_mean=self.tfidf_score(text),
        )

    def tfidf_score(self, text:str) -> float:
        lemmas = self.lemmatize(text)

        if not lemmas:
            return 0.0

        matrix = cast(
            csr_matrix,
            self.vectorizer.fit_transform([" ".join(lemmas)])
        )
        if matrix.nnz == 0:
            return 0.0
        
        return float(matrix.data.mean())
    