from time import time
import matplotlib.pyplot as plt
import os
import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups


def modify(df, n_features, n_components = 20):


    data = list(df["Abstract Text"])

    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=n_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(data)

    lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)

    lda.fit(tf)
    prediction = lda.transform(tf)

    for col, contents in enumerate(np.transpose(prediction)):
        df[f"Topic {col+1}"] = contents

    return df

def run():
    df = pd.read_csv("data.csv")
    times = []
    for n in [5, 10, 20, 50]:
        t0 = time.time()
        modified_df = modify(df, n, n)
        modified_df.to_csv(f"output_data_{n}_topics.csv")
        times.append(time.time()-t0)
    print(times)


if __name__ == "__main__":
    run()