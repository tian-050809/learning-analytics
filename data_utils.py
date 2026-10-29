import pandas as pd
from rules import clean_dataframe

DATA_PATH = "data/sample_data.csv"

def load_clean():
    df = pd.read_csv(DATA_PATH)
    return clean_dataframe(df)

def class_level(df):
    return {
        "total_records": len(df),
        "n_students": df["student_id"].nunique(),
        "avg_correct_rate": round(df["correct_rate"].mean(), 4) if len(df) else 0,
        "completion_rate": round(df["completed"].mean(), 4) if len(df) else 0,
        "by_knowledge_point": df.groupby("knowledge_point").agg(
            n=("correct_rate", "size"), avg_correct=("correct_rate", "mean"), completion=("completed", "mean")
        ).reset_index().round(3).to_dict("records"),
    }

def student_level(df, student_id):
    sub = df[df["student_id"] == student_id]
    if sub.empty: return None
    return {
        "student_id": student_id, "name": sub.iloc[0]["student_name"], "n_records": len(sub),
        "overall_correct": round(sub["correct_rate"].mean(), 4), "overall_completion": round(sub["completed"].mean(), 4),
        "by_knowledge_point": sub.groupby("knowledge_point").agg(
            n=("correct_rate", "size"), avg_correct=("correct_rate", "mean"), completion=("completed", "mean")
        ).reset_index().round(3).to_dict("records"),
        "missing_tasks": sub[sub["completed"] == 0]["task_id"].tolist(),
    }

def list_students(df):
    return df[["student_id", "student_name"]].drop_duplicates().values.tolist()
