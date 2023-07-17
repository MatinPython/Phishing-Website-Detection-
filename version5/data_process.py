import pandas as pd
import numpy as np
from feature_extrafction import *
import os, glob


df = pd.read_csv('F:\\DataProcessing\\ID__URLs_labell.csv')
path = 'F:\\DataProcessing\\Dataset(D1)\\sourc_Data(D1)'
counter = 1
extracted_features = []
for filename in glob.glob(os.path.join(path, '*.txt')):
    filename = filename.replace('\\', '\\\\')
    id = int((filename.split('\\')[-1]).split('.')[0])
    if counter % 500 == 0:
        print(extracted)
        print(counter)
    url = 'https://' + df[df['id'] == id].url.values[0]
    label = df[df['id'] == id].typ.values[0]
    extracted = feature_extraction(filename, url, label)
    extracted_features.append(extracted)
    counter += 1

df_f = pd.DataFrame(extracted_features)
df_f.to_csv('new_approach.csv', index=False)

