import pandas as pd

COLUNAS_IDENTIFICAVEIS = ["code", "name", "name_short", "name_tv", "birth_date"]

def load_data(path="data/clean/dataset.csv"):
    """Remove identificadores pessoais antes de devolver os dados ao app."""
    df = pd.read_csv(path)
    return df.drop(columns=COLUNAS_IDENTIFICAVEIS, errors="ignore")
