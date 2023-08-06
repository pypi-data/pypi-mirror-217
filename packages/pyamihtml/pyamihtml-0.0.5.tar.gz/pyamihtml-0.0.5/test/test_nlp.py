from pyamihtml.ami_nlp import AmiNLP
from test.test_all import AmiAnyTest


class NLPTest(AmiAnyTest):
    import nltk, string

    def test_compute_similarity(self):
        ami_nlp = AmiNLP()
        print(f"sim00 {ami_nlp.cosine_sim('a little bird', 'a little bird')}")
        print(f"sim01 {ami_nlp.cosine_sim('a little bird', 'a little bird chirps')}")
        print(f"sim02 {ami_nlp.cosine_sim('a little bird', 'a big dog barks')}")