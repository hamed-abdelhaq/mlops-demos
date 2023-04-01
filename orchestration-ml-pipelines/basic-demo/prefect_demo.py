
from prefect import task, flow
import pandas as pd

@task
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

@task
def clean_data(df):
    # Apply some data cleaning transformations
    cleaned_df = df.dropna()
    cleaned_df = cleaned_df[cleaned_df["sales"].str.startswith("$")]
    return cleaned_df

@task
def write_csv(cleaned_df):
    cleaned_df.to_csv("cleaned_sales_data.csv", index=False)

@flow(name="Main Sales Data Flow")
def main_flow_sales(file_path: str):
    data = read_csv(file_path)
    cleaned_data = clean_data(data)
    write_csv(cleaned_data)

if __name__ == "__main__":
    main_flow_sales("sales_data.csv")