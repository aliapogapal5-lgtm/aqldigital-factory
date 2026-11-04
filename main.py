
import os
import json
import time
from google import genai
from openai import OpenAI

CHANNEL_NAME = "Modern Technology"

PROMPT = """
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

أعد النتيجة بصيغة JSON فقط بهذا الشكل:
{
  "title": "العنوان",
  "intro": "المقدمة",
  "scenes": ["المشهد الأول", "المشهد الثاني", "المشهد الثالث", "المشهد الرابع"],
  "description": "الوصف",
  "hashtags": ["#ذكاء_اصطناعي"]
}
"""

def clean_json(result):
    result = result.strip()
    result = result.replace("```json", "").replace("```", "").strip()
    return json.loads(result)

def generate_with_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=PROMPT
    )
    return clean_json(response.text)

def generate_with_sambanova():
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        raise RuntimeError("SAMBANOVA_API_KEY is missing")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.sambanova.ai/v1"
    )

    response = client.chat.completions.create(
        model="Meta-Llama-3.3-70B-Instruct",
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.7
    )

    return clean_json(response.choices[0].message.content)

def generate_daily_script():
    data = None

    for attempt in range(1):
        try:
            print(f"Trying Gemini (attempt {attempt + 1})...")
            data = generate_with_gemini()
            print("Gemini succeeded!")
            break
        except Exception as error:
            print(f"Gemini failed: {error}")
            if attempt == 0:
                time.sleep(5)

    if data is None:
        try:
            print("Switching to SambaNova...")
            data = generate_with_sambanova()
            print("SambaNova succeeded!")
        except Exception as error:
            print(f"SambaNova failed: {error}")
            raise RuntimeError("Both AI providers failed") from error

    with open("daily_content.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print("New content generated successfully!")
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    generate_daily_script()

