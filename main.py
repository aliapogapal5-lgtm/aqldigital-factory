
import os
import json
import re
from pathlib import Path

# =====================================
# 90 فكرة احتياطية
# =====================================

FALLBACK_TOPICS = [
    "5 أدوات ذكاء اصطناعي مجانية تستحق التجربة",
    "كيف تستخدم ChatGPT في تنظيم يومك",
    "كيف تحول فكرة إلى تصميم بالذكاء الاصطناعي",
    "أفضل استخدامات Gemini للمبتدئين",
    "كيف تكتب برومبت احترافي",
    "أخطاء شائعة عند استخدام الذكاء الاصطناعي",
    "كيف تلخص ملف PDF باستخدام AI",
    "كيف تنشئ عرضًا تقديميًا بالذكاء الاصطناعي",
    "كيف تحسن جودة الصور بالذكاء الاصطناعي",
    "كيف تزيل خلفية الصور بسهولة",
    "كيف تصنع شعارًا احترافيًا",
    "كيف تحول النص إلى صورة",
    "كيف تنظم أفكارك باستخدام أدوات AI",
    "هل الذكاء الاصطناعي سيغير سوق العمل",
    "5 مهام يوفر فيها الذكاء الاصطناعي وقتك",
    "كيف تبدأ العمل الحر من الصفر",
    "الفرق بين Fiverr وUpwork",
    "كيف تنشئ حسابًا احترافيًا على Fiverr",
    "كيف تكتب وصف خدمة يجذب العملاء",
    "كيف تحصل على أول عميل عبر الإنترنت",
    "أخطاء المبتدئين في العمل الحر",
    "مهارات رقمية يمكنك تعلمها مجانًا",
    "كيف تنشئ معرض أعمال بدون خبرة",
    "كيف تسعر خدماتك كمستقل",
    "كيف تتجنب عمليات النصب في العمل الحر",
    "هل تحتاج الإنجليزية للعمل عبر الإنترنت",
    "كيف تقدم خدمة ترجمة فيديو",
    "كيف تبدأ في تصميم الصور",
    "كيف تبدأ في مونتاج الفيديو",
    "كيف تنظم وقتك كمستقل",
    "أسرار مفيدة في CapCut",
    "5 اختصارات توفر وقتك في Windows",
    "كيف تسجل شاشة الكمبيوتر",
    "كيف تضغط حجم الفيديو",
    "كيف تحول الفيديو إلى صيغة MP4",
    "كيف تصمم صورة مصغرة جذابة",
    "كيف تضيف ترجمة تلقائية للفيديو",
    "كيف تحسن الصوت في الفيديو",
    "كيف تصنع فيديو عمودي احترافي",
    "كيف تستخدم Canva للمبتدئين",
    "أدوات مجانية لإزالة خلفية الصور",
    "كيف تحول الصور إلى PDF",
    "كيف تدمج ملفات PDF",
    "كيف تستخرج النص من الصور",
    "كيف تحمي ملفاتك المهمة",
    "كيف تحمي حسابك من الاختراق",
    "علامات تدل على أن موقعًا إلكترونيًا مزيف",
    "كيف تنشئ كلمة مرور قوية",
    "لماذا يجب تفعيل المصادقة الثنائية",
    "كيف تتجنب الروابط المشبوهة",
    "أخطاء تضعف أمان هاتفك",
    "كيف تعرف التطبيقات التي تستهلك الإنترنت",
    "كيف توفر مساحة على هاتفك",
    "كيف تحسن أداء هاتف Android",
    "كيف تنقل الملفات بين الهاتف والكمبيوتر",
    "كيف تربط هاتفك بالكمبيوتر لاسلكيًا",
    "أهم إعدادات Windows التي يجب معرفتها",
    "كيف تحدث برامج الكمبيوتر بأمان",
    "كيف تتعامل مع الملفات المضغوطة",
    "أدوات مجانية لفحص الملفات",
    "كيف تبدأ قناة يوتيوب بدون ظهور وجهك",
    "أخطاء تقلل مشاهدات YouTube Shorts",
    "كيف تختار عنوانًا جذابًا للفيديو",
    "كيف تصمم صورة مصغرة تلفت الانتباه",
    "ما أهمية أول 3 ثوانٍ في الفيديو",
    "كيف تحافظ على انتباه المشاهد",
    "الفرق بين المشاهدات ووقت المشاهدة",
    "كيف تقرأ إحصائيات YouTube Studio",
    "كيف تختار فكرة فيديو ناجحة",
    "كيف تخطط لمحتوى شهر كامل",
    "كيف تستخدم الموسيقى في فيديوهاتك",
    "كيف تضيف شعار قناتك للفيديو",
    "كيف تنشر الفيديو في الوقت المناسب",
    "لماذا لا تحصل بعض الفيديوهات على مشاهدات",
    "كيف تحسن جودة فيديوهات Shorts",
    "5 مواقع مفيدة للطلاب",
    "أفضل أدوات مجانية لتنظيم المهام",
    "كيف تتعلم مهارة جديدة عبر الإنترنت",
    "كيف تبحث عن معلومات موثوقة على الإنترنت",
    "كيف تستخدم Google Drive",
    "كيف تنظم ملفاتك على الكمبيوتر",
    "كيف تنشئ بريدًا إلكترونيًا احترافيًا",
    "كيف تستخدم Google Docs",
    "كيف تنشئ جدولًا باستخدام Google Sheets",
    "كيف تحول هاتفك إلى ماسح ضوئي",
    "كيف تتعلم أساسيات البرمجة",
    "ما الفرق بين الموقع والتطبيق",
    "ما هو التخزين السحابي",
    "ما هو VPN ومتى تحتاجه",
    "5 نصائح تجعل استخدامك للتكنولوجيا أذكى"
]

# =====================================
# تعليمات الذكاء الاصطناعي
# =====================================

PROMPT = """
أنت صانع محتوى محترف لقناة Modern Technology.

اكتب فيديو YouTube Shorts باللغة العربية المصرية.
مدة الفيديو 20 إلى 30 ثانية.

المطلوب:
- عنوان جذاب.
- مقدمة تشد الانتباه.
- أربعة مشاهد قصيرة ومفيدة.
- معلومات صحيحة وعملية.
- لا تخترع معلومات أو مواقع.

أعد JSON فقط بهذا الشكل:

{
"title": "عنوان الفيديو",
"intro": "مقدمة الفيديو",
"scenes": [
"المشهد الأول",
"المشهد الثاني",
"المشهد الثالث",
"المشهد الرابع"
],
"description": "وصف الفيديو",
"hashtags": "#تقنية #تكنولوجيا"
}
"""

# =====================================
# فحص المحتوى
# =====================================

def validate_content(data):
    required = [
        "title",
        "intro",
        "scenes",
        "description",
        "hashtags"
    ]

    if not isinstance(data, dict):
        raise ValueError("Invalid JSON")

    for key in required:
        if key not in data or not data[key]:
            raise ValueError(f"Missing or empty field: {key}")

    if not isinstance(data["scenes"], list):
        raise ValueError("Scenes must be a list")

    if len(data["scenes"]) != 4:
        raise ValueError("Exactly four scenes are required")

    return data


def parse_json(raw):
    raw = raw.strip()

    raw = re.sub(
        r"^```(?:json)?\s*",
        "",
        raw,
        flags=re.IGNORECASE
    )

    raw = re.sub(r"\s*```$", "", raw)

    return validate_content(json.loads(raw))


# =====================================
# Gemini - محاولة واحدة فقط
# =====================================

def generate_with_gemini():
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key missing")

    client = genai.Client(
        api_key=api_key,
        http_options={"timeout": 20000}
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT
    )

    if not response.text:
        raise ValueError("Gemini returned empty response")

    return parse_json(response.text)


# =====================================
# SambaNova
# =====================================

def generate_with_sambanova():
    from openai import OpenAI

    api_key = os.environ.get("SAMBANOVA_API_KEY")

    if not api_key:
        raise ValueError("SambaNova API key missing")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.sambanova.ai/v1",
        timeout=30,
        max_retries=0
    )

    response = client.chat.completions.create(
        model="Meta-Llama-3.3-70B-Instruct",
        messages=[
            {
                "role": "user",
                "content": PROMPT
            }
        ],
        temperature=0.7,
        max_tokens=1200
    )

    raw = response.choices[0].message.content

    if not raw:
        raise ValueError("SambaNova returned empty response")

    return parse_json(raw)


# =====================================
# بنك المحتوى الاحتياطي
# =====================================

def make_fallback(topic):
    return {
        "title": topic,
        "intro": "في الفيديو ده هنتعرف على معلومة تقنية مهمة.",
        "scenes": [
            f"موضوعنا النهارده هو: {topic}",
            "تعرف على أهم استخداماته وفوائده.",
            "ابدأ بالتجربة والتطبيق خطوة بخطوة.",
            "تابع Modern Technology للمزيد من الشروحات."
        ],
        "description": (
            topic
            + " | تابع Modern Technology للمزيد من المحتوى التقني."
        ),
        "hashtags": (
            "#تقنية #تكنولوجيا #ذكاء_اصطناعي "
            "#ModernTechnology #Shorts"
        )
    }


FALLBACKS = [
    make_fallback(topic)
    for topic in FALLBACK_TOPICS
]


def generate_fallback():
    run_number = int(os.getenv("GITHUB_RUN_NUMBER", "1"))
    index = (run_number - 1) % len(FALLBACKS)

    print(
        f"Using fallback idea {index + 1} "
        f"of {len(FALLBACKS)}"
    )

    return FALLBACKS[index]


# =====================================
# اختيار مصدر المحتوى
# =====================================

def generate_daily_content():

    # Gemini مرة واحدة فقط
    if os.getenv("GEMINI_API_KEY"):
        try:
            print("Trying Gemini once...")
            content = generate_with_gemini()
            print("Gemini succeeded")
            return content

        except Exception as error:
            print(
                "Gemini failed. Switching immediately:",
                str(error)[:300]
            )

    # الانتقال إلى SambaNova
    if os.getenv("SAMBANOVA_API_KEY"):
        try:
            print("Trying SambaNova...")
            content = generate_with_sambanova()
            print("SambaNova succeeded")
            return content

        except Exception as error:
            print(
                "SambaNova failed:",
                str(error)[:300]
            )

    # المحتوى الاحتياطي
    print("Both AI providers failed.")
    print("Using offline fallback content.")

    return generate_fallback()


# =====================================
# حفظ النتيجة
# =====================================

if __name__ == "__main__":

    content = generate_daily_content()

    Path("daily_content.json").write_text(
        json.dumps(
            content,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("CONTENT GENERATED SUCCESSFULLY")
    print("Title:", content["title"])
    print("Number of scenes:", len(content["scenes"]))

