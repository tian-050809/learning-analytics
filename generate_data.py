import csv, os, random
from datetime import datetime, timedelta
from collections import Counter

random.seed(20260301)
OUT_DIR = "data"
KNOWLEDGE_POINTS = ["有理数", "整式", "一元一次方程", "几何图形初步"]
PROFILES = {
    "A_稳定优秀": dict(c=(0.8, 0.95), m=(0.9, 1.0), weak=0, late=0.05),
    "B_高完成低正确": dict(c=(0.45, 0.65), m=(0.85, 1.0), weak=2, late=0.1),
    "C_低完成高正确": dict(c=(0.75, 0.9), m=(0.4, 0.6), weak=0, late=0.6),
    "D_波动型": dict(c=(0.4, 0.9), m=(0.6, 0.9), weak=1, late=0.25),
    "E_整体薄弱": dict(c=(0.3, 0.5), m=(0.3, 0.55), weak=3, late=0.4),
}
NAMES = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", "郑一", "王二"]

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    profiles = list(PROFILES.keys()) * 3  # 30 students
    random.shuffle(profiles)
    
    for i in range(30):
        sid = f"S{i+1:03d}"
        name = NAMES[i % len(NAMES)]
        p = PROFILES[profiles[i]]
        weak_kps = random.sample(KNOWLEDGE_POINTS, k=max(1, p['weak']))
        base_c = random.uniform(*p['c'])
        base_m = random.uniform(*p['m'])
        
        for j in range(6):
            kp = random.choice(KNOWLEDGE_POINTS)
            c = base_c - (0.2 if kp in weak_kps else 0) + random.uniform(-0.05, 0.05)
            c = max(0, min(1, c))
            m = max(0, min(1, base_m + random.uniform(-0.05, 0.05)))
            completed = 1 if random.random() < m else 0
            score = round(c * 10, 1) if completed else 0.0
            
            rows.append({
                "student_id": sid, "student_name": name, "class_name": "初一1班",
                "task_id": f"T{j+1:02d}", "knowledge_point": kp, "task_type": "quiz",
                "score": score, "max_score": 10, "completed": completed,
                "submit_time": (datetime(2026, 3, 1) + timedelta(days=j)).strftime("%Y-%m-%d %H:%M")
            })

    with open(f"{OUT_DIR}/sample_data.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("数据已生成到 data/sample_data.csv")

if __name__ == "__main__":
    main()
