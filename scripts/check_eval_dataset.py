import pandas as pd

df = pd.read_csv("data/evaluation/rag_queries.csv")

print("Total queries:", len(df))
print("Unique topics:", df["expected_source"].nunique())

assert len(df) >= 15
assert df["expected_source"].notna().all()

print("Evaluation dataset is ready.")