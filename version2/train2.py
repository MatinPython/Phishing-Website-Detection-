
#importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import accuracy_score, classification_report
from sklearn import metrics



df = pd.read_csv('C:\\Users\styxm\\Desktop\\models\\version2\\processed_data.csv')
df = df.iloc[: , 1:]
X = df.iloc[: , :-1]
y = df.iloc[: , -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

features_train = X_train
labels_train = y_train
features_test=X_test
labels_test=y_test

#fitting logistic regression 
clf4 = LogisticRegression(random_state = 0)
clf4.fit(X_train, y_train)


pred4=clf4.predict(features_test)
print(classification_report(labels_test, pred4))
print ('The accuracy is:', accuracy_score(labels_test, pred4))
print (metrics.confusion_matrix(labels_test, pred4))

pickle.dump(clf4, open('logisticRegression.pkl', 'wb'))