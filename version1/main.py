""" Subnet Overlap Checker """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from feature_extraction import *
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class request_body(BaseModel):
    """Meh"""

    ip1: str



@app.post("/v1/check-ip/")
async def check_for_conflicts(veri_data: request_body) -> dict:
    """Meh"""
    subs = veri_data.ip1
    url = str(subs)
    featureClass = FeatureExtraction(url)
    features = np.array(featureClass.getFeaturesList()).reshape(1, -1)
    # print(features)
    pickled_model = pickle.load(open('clf4.pkl', 'rb'))
    if pickled_model.predict(features)[0] == 1:
        return('Legitimate')
    elif pickled_model.predict(features)[0] == -1:
        return('Phishing')