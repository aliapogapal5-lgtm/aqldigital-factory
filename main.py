
import os
import json
from google import genai

CHANNEL_NAME = "Modern Technology"

def generate_daily_script():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)

    prompt = """
    أنت كاتب محتوى محترف لقناة Modern Technology.
    أنشئ فكرة فيديو YouTube Shorts جديدة باللغة العربية المصرية.
    
    المجال: أدوات الذكاء الاصطناعي ومواقع الربح والعمل الحر.
    المدة: 20 إلى 30 ثانية.
    اكتب:
    1. عنوان جذاب.
    2. مقدمة تشد الانتباه.
    3. نص مختصر مقسم إلى 4 مشاهد.
    4. وصف الفيديو.
    5. خمسة هاشتاجات.

    الفيديو بدون تعليق صوتي، يعتمد على النصوص الظاهرة
    على الشاشة والموسيقى فقط.

    أعد النتيجة بصيغة JSON فقط.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    result = response.text.strip()
    result = result.replace("```json", "").replace("```", "").strip()

    data = json.loads(result)

    with open("daily_content.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print("New content generated successfully!")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    generate_daily_script()
