import logging
import string

import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__file__)


class AmiNLP:

    def __init__(self):
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        self.vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')

        nltk.download('punkt')  # if necessary...

    def stem_tokens(self, tokens):
        return [self.stemmer.stem(item) for item in tokens]

    '''remove punctuation, lowercase, stem'''

    def normalize(self, text):
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punctuation_map)))

    def cosine_sim(self, text1, text2):
        try:
            tfidf = self.vectorizer.fit_transform([text1, text2])
        except Exception as e:
            logger.error(f"cannot parse {text1} \n.......\n{text2}")
            return None
        return ((tfidf * tfidf.T).A)[0, 1]

    def find_similarities(self, texts, maxt=10000, min_sim=0.25):
        """
        find simiarities in list of text objects
        :param list of texts
        """
        texts = [str(t) for t in texts[:maxt] if t]
        print(f"texts:\n{texts}")
        for i, t0 in enumerate(texts[:maxt]):
            # print(f"--------{i}--------\n{t0}\n..")

            for ii, t1 in enumerate(texts[i + 1 : maxt]):
                j = i + ii + 1
                # print(f"{i} .. {j} ...{t0[:30]} ||| {t1[:30]}")
                sim = self.cosine_sim(t0, t1)
                if sim > min_sim:
                    sim = {round(sim, 3)}
                    print(f"\n{i}=>{j}  s={sim}\n{t0}\n{t1}")

    @classmethod
    def find_text_similarities(cls, csv_path, maxt=10000, min_sim=0.25):
        print(f"============{csv_path}=============")
        data = pd.read_csv(str(csv_path))
        data.drop_duplicates(inplace=True, subset=["a_text"])

        try:
            data = data[~data['a_text'].str.contains('See |see ')]
            data = data[~data['t_text'].str.contains('See |see ')]
        except Exception as e:
            logger.error(f"cannot read data into pandas {e}")
        a_text = data.get("a_text")
        a_id = data.get("a_id")
        # a_id = [ai.lower() for ai in set(table.get("a_id"))]
        ami_nlp = AmiNLP()
        simmat = ami_nlp.find_similarities(a_text, maxt=maxt, min_sim=min_sim)

# ski-kit learn pairwise distances
