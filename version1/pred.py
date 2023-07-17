import numpy as np
import pickle
from feature_extraction import *


# Feature extraction

# First test Succesful

url = 'https://365careers.com/business-intelligence-courses'
featureClass = FeatureExtraction(url)

features = np.array(featureClass.getFeaturesList()).reshape(1, -1)

print(features)

features = np.array([1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1]).reshape(1, -1)


# Second Test Succesful

url = 'https://www.statology.org/pandas-drop-first-column/'
featureClass = FeatureExtraction(url)

features = np.array(featureClass.getFeaturesList()).reshape(1, -1)

print(features)

# Prediction

pickled_model = pickle.load(open('C:\\Users\\styxm\\Desktop\\models\\version1\\clf4.pkl', 'rb'))

# if pickled_model.predict(features)[0] == 1:
#     print('Legitimate')
# elif pickled_model.predict(features)[0] == -1:
#     print('Phishing')

score = pickled_model.predict_proba(features)
print(score)