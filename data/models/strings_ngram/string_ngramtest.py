# coding=utf-8
import joblib
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# TFIDF 模型测试
train_data_ = pd.read_csv("raw_train_data.csv")

"""
vectorizer = TfidfVectorizer(max_features=500)
word = train_data_.words.tolist()
train_tfidf_features = vectorizer.fit_transform(train_data_.words.tolist())

"""
try:
    vectorizer = joblib.load('/home/zy/PycharmProjects/virtualenv/Bold-Falcon/data/models/strings_ngram/tfidf_model_test')
except EOFError:
    print(None)

# Import packages
train_tfidf_features = vectorizer.fit_transform(train_data_.words.tolist())

try:
    from sklearn.model_selection import train_test_split
    import numpy as np
    from xgboost import XGBClassifier
except ImportError, e:
    print >> sys.stderr, "Some of the packages required by Detection Modules are not available."
    print >> sys.stderr, e
# loader data
train_data_ = train_tfidf_features
train_labels = train_data_.labels


train_data, test_data, train_label, test_label = train_test_split(train_data_,\
                                                                          train_labels,
                                                                          test_size=0.25,
                                                                          random_state=20)

model = XGBClassifier(max_depth=5, n_estimators=90) #n_estimatores决策树的个数，https://www.cnblogs.com/TMatrix52/p/9623093.html（XGB参数）
model.fit(train_data, train_label)
y_pred = model.predict(test_data)
score = model.score(test_label, y_pred)
print(score)