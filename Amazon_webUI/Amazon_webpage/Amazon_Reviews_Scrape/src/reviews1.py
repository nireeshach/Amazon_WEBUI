import numpy as np
import spacy
from spacy.lang.en import English
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics.pairwise import cosine_similarity
import re

from .rating_calculation import rating_cal
# nltk.download('stopwords')
# nltk.download('punkt')


def similarity_reviews(results):

# def similarity_reviews():

    stop_words = set(stopwords.words("english"))

    data = pd.DataFrame(results)

    # data = pd.read_csv("Curling Iron(Done)checked.csv")
    data = data.fillna(0)
    data["reviews"] = data["Title"].str.cat(data["Body"], sep=",")


    print(data.head())
    #  1. Remove punctuation, numbers
    #  2. Convert to lowercase and tokenize
    #  3. Remove stopwords.

    def train_review_to_words(reviews):
        stem = PorterStemmer()
        letters_only = re.sub("[^a-zA-Z]", " ", reviews)
        words = letters_only.lower().split()
        stops = set(stopwords.words("english"))
        meaningful_train_words = [w for w in words if not w in stops]
        stem_train_words = [stem.stem(w) for w in meaningful_train_words]
        return " ".join(stem_train_words)

    q = (data['ProductTitle'][0]+data['ProductDescription'][0])
    num_tr_reviews = data["reviews"].size
    clean_tr_reviews = []
    for i in range(0, num_tr_reviews):
        clean_tr_reviews.append(train_review_to_words(str(data["reviews"][i])))

    print(clean_tr_reviews[0:2])

    product_descrip = []
    product_descrip.append(train_review_to_words(str(q)))
    # print(product_descrip[0])

    product_description = set(product_descrip[0].split())

    # Building up dictionary of words present in the text corpus using count Vectorizer

    vectorizer = CountVectorizer(
        analyzer="word", tokenizer=None, preprocessor=None, stop_words=None
    )
    reviews_vec = vectorizer.fit_transform(clean_tr_reviews)
    reviews_vec = reviews_vec.toarray()
    tf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    train_tfidf_features = tf_transformer.fit_transform(reviews_vec)
    train_tfidf_features = train_tfidf_features.toarray()

    # convert the description vector by looking each term of description in the corpus
    q_countvec = vectorizer.transform(product_descrip)
    q_countvec.toarray()
    q_tfidf_vec = tf_transformer.transform(q_countvec)
    q_tfidf_vec = q_tfidf_vec.toarray()

    # cosine similarity
    cs = []
    cs = cosine_similarity(q_tfidf_vec, train_tfidf_features, dense_output=False)

    # jaccard similarity
    js = []
    for x in range(0, len(data)):
        review = set(clean_tr_reviews[x].split())
        c = product_description.intersection(review)
        js.append(float(len(c)) / (len(product_description) + len(review) - len(c)))

    print("Product Description: ", q)
    print("")

    reviews = []
    cosinesimilarity = []
    jaccardsimilarity = []
    for i in range(0, len(data)):
        reviews.append(clean_tr_reviews[i])
        cosinesimilarity.append(cs[0][i])
        jaccardsimilarity.append(js[i])
        print("Review:", clean_tr_reviews[i])
        print("Cosine Similarity = ", cs[0][i])
        print("Jaccard Similarity = ", js[i])
        print("")
    output = [reviews, cosinesimilarity, jaccardsimilarity]
    data2 = pd.DataFrame(output).T
    data2["Product Reviews"] = data["Body"]
    data2["Rating"] = data["Rating"]
    data2["Amazon_Rating"] = data["ProductRating"]
    data2.columns = ["reviews", "cosine_similarity", "jaccard", "Product Reviews","Rating","Amazon_Rating"]
    threshold = 0.005
    data2["relevant"] = np.where(data2["cosine_similarity"] >= threshold, 1, 0)
    relevant_reviews_pd = data2[(data2.relevant == 1)]
    irrelevant_reviews_pd = data2[(data2.relevant == 0)]
    rating = rating_cal(relevant_reviews_pd)
    relevant_reviews_pd = relevant_reviews_pd["Product Reviews"].to_frame()
    irrelevant_reviews_pd = irrelevant_reviews_pd["Product Reviews"].to_frame()
    return relevant_reviews_pd, irrelevant_reviews_pd,rating,data2["Amazon_Rating"][0]

# similarity_reviews()
