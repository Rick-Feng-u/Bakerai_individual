# %%
import os
import json
import gzip
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

pd.options.mode.chained_assignment = None
# %%
#import data
def parse(path):
    g = gzip.open(path, 'rb')
    for l in g:
        yield json.loads(l)

def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')

#%%
#subset dataframe to only relevant.
df = getDF('./data/Grocery_and_Gourmet_Food_5.json.gz')

dg = df[['overall', 'reviewText']]
dg

#clean data remove nulls.
df.isnull().sum()
dg.dropna(inplace=True)

#assign each review with more than 3 stars as positive and the rest as negative.
dg.loc[dg['overall'] >=   3.0, 'sentiment'] = 'POSITIVE'
dg.loc[dg['overall'] < 3.0, 'sentiment'] = 'NEGATIVE' 
dg.head()

#more cleaning data and make everything lower case.  
dg.dropna(axis=0, how='any', inplace=True)
dg['reviewText'] = dg['reviewText'].map(lambda x: x.lower())

#sample data such that both negative and positive reviews have equal propotion.
g = dg.groupby('sentiment')
dg = pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True)))

# %%
# change the reviews to bow vectorizer.
vectorizer = CountVectorizer()
X = [x for x in dg['reviewText']]
y = [x for x in dg['sentiment']]
#split data using pandas train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=500, random_state=42, train_size=10000)


X_train_bow, X_test_bow = vectorizer.fit_transform(X_train), vectorizer.transform(X_test)

# %%
# gradient boost classifier from scikit learn.
clf = GradientBoostingClassifier(n_estimators=4000, learning_rate=0.5,
                                 max_depth=2, random_state=42, warm_start=True).fit(X_train_bow, y_train)
# score on test data.
clf.score(X_test_bow, y_test)

# %%
# testing model. 
test_set = ['good', "terrible ", 'waste of time','I hate this product']
new_test = vectorizer.transform(test_set)
clf.predict(new_test)
#%% 
# save model to be used in bot.
with open('./sentiment_models/sentiment_model.pkl', 'wb') as f:
    pickle.dump(clf, f)
# save vectorizer
with open('./sentiment_models/vectorizer.pkl', 'wb') as f:
  pickle.dump(vectorizer, f)

# %%
