# import numpy as np
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, classification_report
# from sklearn import metrics
# import os.path
# from os import path
# import os
# import shutil





# def Train(dataset=[], test_size=0.33, random_state_data_split=42, min_samples_split=7, verbose=True, max_depth=7, random_state_model=42):

#     key = False

#     try:

#         # data split
#         df = pd.DataFrame(dataset)


#         df = df.iloc[: , 1:]
#         X = df.iloc[: , :-1]
#         y = df.iloc[: , -1]

#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state_data_split)

#         features_train = X_train
#         labels_train = y_train
#         features_test=X_test
#         labels_test=y_test

#     except:
#         print ('DATA SPLIT FAILED')


#     try:

#         # train model
#         clf4 = RandomForestClassifier(min_samples_split=min_samples_split, verbose=verbose, max_depth=max_depth, random_state=random_state_model)
#         clf4.fit(features_train, labels_train)

#         # # feature importance
#         # importances = clf4.feature_importances_
#         # std = np.std([tree.feature_importances_ for tree in clf4.estimators_], axis=0)
#         # indices = np.argsort(importances)[::-1]
#         # Print the feature ranking
#         # print("Feature ranking:")
#         # for f in range(features_train.shape[1]):
#         #     print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

#         # model evaluation
#         pred4=clf4.predict(features_test)
#         print(classification_report(labels_test, pred4))
#         print ('The accuracy is:', accuracy_score(labels_test, pred4))
#         print (metrics.confusion_matrix(labels_test, pred4))

#         key = True

#     except:
#         print ('MODEL TRAINING FAILED')



#     try:
#         # save model
#         if path.exists('clf4.pkl'):
            
#             # absolute path
#             src_path = "clf4.pkl"
#             dst_path = "old_models\\clf4.pkl"
#             shutil.move(src_path, dst_path)


#         if key:
#             pickle.dump(clf4, open('clf4.pkl', 'wb'))
#         else:
#             return 'SAVE MODEL FAILED'

#     except:

#         return 'SAVE MODEL FAILED'
    


# # print(Train())



