import pandas as pd
import json

def read_csv(filename):
    matrix = pd.read_csv(filename)
    matrix.index = matrix.columns
    return matrix


def read_json(filename:str) -> dict:
    with open(filename) as f:
        data = json.load(f)

    return data