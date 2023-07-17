import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn import metrics


df = pd.read_csv('processed_data.csv')
X = df.iloc[: , :-1]
y = df.iloc[: , -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

features_train = X_train
labels_train = y_train
features_test=X_test
labels_test=y_test

print("\n\n ""Random Forest Algorithm Results"" ")
clf4 = RandomForestClassifier(min_samples_split=7, verbose=True)
clf4.fit(features_train, labels_train)
importances = clf4.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf4.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
# Print the feature ranking
print("Feature ranking:")
for f in range(features_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

pred4=clf4.predict(features_test)
print(classification_report(labels_test, pred4))
print ('The accuracy is:', accuracy_score(labels_test, pred4))
print (metrics.confusion_matrix(labels_test, pred4))

pickle.dump(clf4, open('clf4_version2_.pkl', 'wb'))



