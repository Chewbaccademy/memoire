import pandas as pd

def read_csv(filename):
    matrix = pd.read_csv(filename)
    matrix.index = matrix.columns
    return matrix
