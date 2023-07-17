























import numpy as np
import pickle
from feature_extraxtion import *


# url = 'https://www.tutorialspoint.com/beautiful_soup/index.htm'

# feautres = featureExtractionURL(url)

# print(feautres)

features = [1, 1, 3, 22, 0, 25, 0.6636511854151482, 0.6318181818181818, 0.7863636363636363, 0.9261511216056671, 0.23404255319148937, 0.25, 0.0, 0.18181818181818182]
new_features = []
for i in features:
    new_features.append(round(i, 3))

new = np.array(new_features).reshape(1, -1)
# Prediction


pickled_model = pickle.load(open('clf4_version2_.pkl', 'rb'))
pred = pickled_model.predict(new)[0]
pred_proba = pickled_model.predict_proba(new)[0]

print(pred)
print(pred_proba)