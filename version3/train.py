from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn import metrics

df = pd.read_csv('C:\\Users\\styxm\\Desktop\\models\\version3\\processed_data.csv')
X = df.iloc[: , :-1]
y = df.iloc[: , -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

features_train = X_train
labels_train = y_train
features_test=X_test
labels_test=y_test

print(X_train.head())
# print("\n\n "" XGBoost Algorithm Results"" ")
# # clf4 = RandomForestClassifier(min_samples_split=7, verbose=True)
# # clf4.fit(features_train, labels_train)
# clf4 = GradientBoostingClassifier(n_estimators=500, learning_rate=0.01,
#      max_depth=6, random_state=42).fit(X_train, y_train)
# try:
#     importances = clf4.feature_importances_
#     std = np.std([tree.feature_importances_ for tree in clf4.estimators_], axis=0)
#     indices = np.argsort(importances)[::-1]
#     # Print the feature ranking
#     print("Feature ranking:")
#     for f in range(features_train.shape[1]):
#         print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
# except:
#     pass

# pred4=clf4.predict(features_test)
# print(classification_report(labels_test, pred4))
# print ('The accuracy is:', accuracy_score(labels_test, pred4))
# print (metrics.confusion_matrix(labels_test, pred4))

# pickle.dump(clf4, open('xgb_version1_.pkl', 'wb'))