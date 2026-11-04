
import os
import json
import time
from datetime import date
from google import genai
from openai import OpenAI

CHANNEL_NAME = "Modern Technology"

PROMPT = """
أنت كاتب محتوى محترف لقناة Modern Technology.
أنشئ فيديو YouTube Shorts باللغة العربية المصرية.

المجال: الذكاء الاصطناعي والتكنولوجيا والعمل الحر.
المدة: 20 إلى 30 ثانية.
بدون تعليق صوتي، نصوص على الشاشة وموسيقى فقط.

أعد JSON فقط:
{
  "title": "عنوان جذاب",
  "intro": "مقدمة تشد الانتباه",
  "scenes": ["المشهد الأول", "المشهد الثاني", "المشهد الثالث", "المشهد الرابع"],
  "description": "وصف الفيديو",
  "hashtags": ["#تكنولوجيا"]
}
"""

FALLBACKS = [
    {
        "title": "موقع يوفر عليك وقت التصميم",
        "intro": "لسه بتصمم كل حاجة من الصفر؟",
        "scenes": [
            "في أدوات بتساعدك تبدأ تصميمك بسرعة",
            "اختار قالب مناسب لمشروعك",
            "عدّل الألوان والنصوص والصور",
            "احفظ تصميمك وابدأ شغلك"
        ],
        "description": "نصائح بسيطة لتطوير مهارات التصميم.",
        "hashtags": ["#تصميم", "#تكنولوجيا", "#ModernTechnology"]
    },
    {
        "title": "3 مهارات رقمية اتعلمها",
        "intro": "عايز تبدأ شغل أونلاين؟",
        "scenes": [
            "اتعلم تصميم الصور",
            "اتعلم مونتاج الفيديو",
            "اتعلم استخدام أدوات الذكاء الاصطناعي",
            "ابدأ بمشروع صغير وطور مهاراتك"
        ],
        "description": "مهارات رقمية مفيدة للمبتدئين.",
        "hashtags": ["#العمل_الحر", "#مهارات", "#ModernTechnology"]
    },
    {
        "title": "استغل الذكاء الاصطناعي صح",
        "intro": "الذكاء الاصطناعي ممكن يساعدك في شغلك!",
        "scenes": [
            "استخدمه لتوليد الأفكار",
            "استفد منه في كتابة المحتوى",
            "نظم مهامك ووقتك",
            "راجع النتائج بنفسك قبل النشر"
        ],
        "description": "طرق عملية للاستفادة من الذكاء الاصطناعي.",
        "hashtags": ["#ذكاء_اصطناعي", "#AI", "#ModernTechnology"]
    }
]

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
        model="gemini-2.5-flash",
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

    for attempt in range(3):
        try:
            print(f"Trying Gemini ({attempt + 1}/3)...")
            data = generate_with_gemini()
            print("Gemini succeeded!")
            break
        except Exception as error:
            print(f"Gemini failed: {error}")
            if attempt < 2:
                time.sleep(15)

    if data is None:
        try:
            print("Switching to SambaNova...")
            data = generate_with_sambanova()
            print("SambaNova succeeded!")
        except Exception as error:
            print(f"SambaNova failed: {error}")

    if data is None:
        index = date.today().toordinal() % len(FALLBACKS)
        data = FALLBACKS[index]
        print("Using offline fallback content.")

    with open("daily_content.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print("Content ready!")
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    generate_daily_script()

