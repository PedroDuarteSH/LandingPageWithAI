import pandas as pd

if __name__ == "__main__":
    file_pt = "data/conversations_pt.parquet"
    file_en = "data/conversations_en.parquet"
    
    df_pt = pd.read_parquet(file_pt)
    df_en = pd.read_parquet(file_en)
    
    df = pd.concat([df_pt, df_en])
    
    df.to_parquet("data/conversations.parquet", index=False)
    
    