import pandas as pd

def process_data(df):
    """清洗与计算规则（对应项目文档R-C与R-D规则）"""
    df = df.copy()
    # 数据清洗
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
    df["max_score"] = pd.to_numeric(df["max_score"], errors="coerce").fillna(10)
    df["completed"] = pd.to_numeric(df["completed"], errors="coerce").fillna(0).astype(int)
    df.loc[df["score"] > df["max_score"], "score"] = df.loc[df["score"] > df["max_score"], "max_score"]
    df = df.drop_duplicates(subset=["student_id", "task_id"], keep="last")
    df["correct_rate"] = df["score"] / df["max_score"]
    return df

def diagnose_student(stu_df):
    n = len(stu_df)
    if n == 0:
        return {"status": "empty"}
        
    overall_c = stu_df["correct_rate"].mean()
    overall_m = stu_df["completed"].mean()
    
    kp_stats = stu_df.groupby("knowledge_point").agg(
        n=("correct_rate", "size"), avg_c=("correct_rate", "mean")
    ).reset_index()

    weak = [{"kp": r["knowledge_point"], "avg_correct": round(r["avg_c"], 3)} 
            for _, r in kp_stats.iterrows() if r["n"] >= 2 and r["avg_c"] < 0.6]

    if overall_c < 0.6 and overall_m < 0.8:
        main, rule = "整体薄弱，需基础补强 + 任务管理", "R-D2"
    elif overall_c >= 0.6 and overall_m < 0.8:
        main, rule = "会做但任务完成不稳定，需任务提醒", "R-D3"
    elif overall_c < 0.6 and overall_m >= 0.8:
        main, rule = "投入充分但知识掌握不足，需针对性补弱", "R-D4"
    else:
        main, rule = "表现稳定，可拓展提升", "R-D5"

    return {
        "status": "ok", "overall_c": overall_c, "overall_m": overall_m,
        "main_diagnosis": main, "main_rule": rule, "weak_kps": weak
    }

def generate_suggestions(diag):
    if diag["status"] != "ok": return []
    mapping = {
        "R-D2": dict(target="整体薄弱", goal="正确率≥60%且完成率≥80%", activity="每日基础题+错题重做", rule="R-S1"),
        "R-D3": dict(target="完成不稳定", goal="完成率≥80%", activity="每日任务清单+放学前自查", rule="R-S2"),
        "R-D4": dict(target="知识掌握不足", goal="薄弱知识点≥60%", activity="分层练习+同伴讲解", rule="R-S3"),
        "R-D5": dict(target="拓展提升", goal="维持并适度拓展", activity="拓展题/同伴互助", rule="R-S4"),
    }
    base = mapping[diag["main_rule"]]
    base["kp"] = "全部"
    suggs = [base]
    for w in diag["weak_kps"]:
        suggs.append({
            "target": "知识点专项", "kp": w["kp"], "rule": "R-S5",
            "goal": f"{w['kp']}正确率≥60%", "activity": f"{w['kp']}基础题+针对性讲解"
        })
    return suggs
