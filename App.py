import pandas as pd
import json
import os

INPUT_FILE = "data/microdados_ed_basica_2024.csv"
OUTPUT_FILE = "output/ies_paraiba_top3.json"

def gerar_json():
    
    df = pd.read_csv(INPUT_FILE, sep=";", encoding="latin1", low_memory=False) # Lê o CSV

    df_pb = df[df["SG_UF"] == "PB"] # Filtra somente Paraíba (PB)
    
    cols = [
        "NO_ENTIDADE", "CO_ENTIDADE", "NO_UF", "SG_UF", "CO_UF",
        "NO_MUNICIPIO", "CO_MUNICIPIO",
        "NO_MESORREGIAO", "CO_MESORREGIAO",
        "NO_MICRORREGIAO", "CO_MICRORREGIAO",
        "NU_ANO_CENSO", "NO_REGIAO", "CO_REGIAO",
        "QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_FUND", "QT_MAT_MED",
        "QT_MAT_PROF", "QT_MAT_EJA", "QT_MAT_ESP"
    ]  
    
    df_pb = df_pb[cols] # Mantém apenas colunas de interesse

    df_pb["TOTAL_MATRICULAS"] = (
        df_pb["QT_MAT_BAS"] + df_pb["QT_MAT_INF"] +
        df_pb["QT_MAT_FUND"] + df_pb["QT_MAT_MED"] +
        df_pb["QT_MAT_PROF"] + df_pb["QT_MAT_EJA"] +
        df_pb["QT_MAT_ESP"]
    )  # Soma as matrículas

    df_top3 = df_pb.sort_values(by="TOTAL_MATRICULAS", ascending=False).head(3) # Top 3 instituições

    json_data = df_top3.to_dict(orient="records") # Converte para JSON

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True) # Garante pasta /output

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4) # Salva JSON

    print(f"Arquivo JSON gerado em {OUTPUT_FILE}")

if __name__ == "__main__":
    gerar_json()
