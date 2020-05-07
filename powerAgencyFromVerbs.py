import pandas as pd
from util import pa_dataframe_from_verbs
    
if __name__ == "__main__":
    df = pa_dataframe_from_verbs('vmaps/cv.json', verbose=True)
    df = df.fillna(0)
    df.to_csv('vmaps/pa_from_vmaps.csv')
