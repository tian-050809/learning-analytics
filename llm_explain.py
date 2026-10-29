import json
from openai import OpenAI

SYSTEM_PROMPT = """你是资深教研员。请基于提供的学生学情数据，输出一段JSON格式的分析。
规则：
1. 必须区分“事实”和“可能的原因”。
2. 事实必须有数据支撑，原因使用“可能/也许”表述。
3. 不得贴标签。
返回格式：{"facts":["事实1","事实2"], "causes":["原因1","原因2"]}"""

def call_real_llm(api_key, base_url, model_name, stu_data, cls_data):
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    prompt = f"""
    学生个人数据：{json.dumps(stu_data, ensure_ascii=False)}
    班级整体数据：{json.dumps(cls_data, ensure_ascii=False)}
    """
    
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content), None
    except Exception as e:
        return None, str(e)
