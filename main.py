
import json
import os
import time
from datetime import date
from pathlib import Path

FALLBACKS = [
    {
        "title": "3 أدوات ذكاء اصطناعي توفر وقتك",
        "intro": "بدل ما تضيع ساعات في شغلك، جرب الأدوات دي.",
        "scenes": [
            "استخدم ChatGPT لكتابة الأفكار والنصوص.",
            "استخدم Canva لتصميم صور احترافية.",
            "استخدم CapCut لمونتاج الفيديوهات.",
            "ابدأ بأداة واحدة واتعلم استخدامها كويس."
        ],
        "description": "اكتشف أدوات تقنية توفر وقتك وتساعدك على الإنتاج.",
        "hashtags": "#ذكاء_اصطناعي #تقنية #ModernTechnology"
    },
    {
        "title": "مهارات ممكن تبدأ تتعلمها من البيت",
        "intro": "عايز تتعلم مهارة رقمية؟ ابدأ من هنا.",
        "scenes": [
            "تعلم تصميم الصور باستخدام Canva.",
            "تعلم مونتاج الفيديوهات باستخدام CapCut.",
            "تعلم الترجمة وصناعة المحتوى.",
            "اختار مهارة واحدة وابدأ التدريب يوميا."
        ],
        "description": "مهارات رقمية للمبتدئين.",
        "hashtags": "#العمل_عبر_الإنترنت #مهارات #ModernTechnology"
    },
    {
        "title": "متخليش الذكاء الاصطناعي يضيع وقتك",
        "intro": "الذكاء الاصطناعي أداة، مش بديل عن تفكيرك.",
        "scenes": [
            "حدد المهمة اللي عايز تنفذها.",
            "اكتب طلب واضح ومحدد.",
            "راجع النتيجة وعدل الأخطاء.",
            "استخدم النتيجة في شغلك بشكل احترافي."
        ],
        "description": "نصائح لاستخدام أدوات الذكاء الاصطناعي.",
        "hashtags": "#AI #نصائح_تقنية #ModernTechnology"
    }
]

PROMPT = """
اكتب فكرة فيديو تقني قصير باللغة العربية.
أعد JSON فقط بالشكل التالي:
{
"title": "عنوان جذاب",
"intro": "مقدمة قصيرة",
"scenes": ["مشهد 1", "مشهد 2", "مشهد 3", "مشهد 4"],
"description": "وصف الفيديو",
"hashtags": "#تقنية #ذكاء_اصطناعي"
}
اجعل المعلومات مفيدة وصحيحة ومناسبة لفيديو قصير.
"""

def validate(data):
    required = ["title", "intro", "scenes", "description", "hashtags"]
    if not isinstance(data, dict):
        raise ValueError("Invalid JSON")
    for key in required:
        if key not in data:
            raise ValueError(f"Missing {key}")
    if not isinstance(data["scenes"], list) or len(data["scenes"]) != 4:
        raise ValueError("Expected exactly 4 scenes")
    return data

def gemini():
    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return validate(json.loads(raw))

def sambanova():
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["SAMBANOVA_API_KEY"],
        base_url="https://api.sambanova.ai/v1"
    )
    response = client.chat.completions.create(
        model="Meta-Llama-3.3-70B-Instruct",
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.7
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return validate(json.loads(raw))

def generate():
    if os.getenv("GEMINI_API_KEY"):
        for attempt in range(2):
            try:
                print(f"Gemini attempt {attempt + 1}")
                return gemini()
            except Exception as e:
                print("Gemini error:", str(e)[:300])
                time.sleep(5)

    if os.getenv("SAMBANOVA_API_KEY"):
        try:
            print("Trying SambaNova")
            return sambanova()
        except Exception as e:
            print("SambaNova error:", str(e)[:300])

    print("Using offline fallback content")
    return FALLBACKS[date.today().toordinal() % len(FALLBACKS)]

if __name__ == "__main__":
    content = generate()
    Path("daily_content.json").write_text(
        json.dumps(content, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print("Content saved successfully")

