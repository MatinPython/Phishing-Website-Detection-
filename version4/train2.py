from sklearn.metrics import mean_squared_error 
from sklearn.model_selection import train_test_split 
from xgboost import XGBClassifier
import pandas as pd 
import numpy as np 
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn import metrics
from sklearn.ensemble import GradientBoostingClassifier
import pickle

df = pd.read_csv('processed_data.csv')

X = df.iloc[: , :-1]
y = df.iloc[: , -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

features_train = X_train
labels_train = y_train
features_test=X_test
labels_test=y_test

# fit model no training data
clf = GradientBoostingClassifier(n_estimators=200, learning_rate=0.01,
     max_depth=8, random_state=42).fit(X_train, y_train)
# make predictions for test data
score = clf.score(X_test, y_test)

print(score)

pred4=clf.predict(X_test)
print(classification_report(y_test, pred4))
print ('The accuracy is:', accuracy_score(y_test, pred4))
print (metrics.confusion_matrix(y_test, pred4))

pickle.dump(clf, open('xgb_version4_.pkl', 'wb'))