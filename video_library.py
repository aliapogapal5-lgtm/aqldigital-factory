import os
import re
import random
import requests

API_KEY = os.getenv("PIXABAY_API_KEY")
API_URL = "https://pixabay.com/api/videos/"

# تحويل الكلمات العربية إلى كلمات بحث مناسبة للفيديوهات
KEYWORDS = {
    "ذكاء اصطناعي": "artificial intelligence computer",
    "شات جي بي تي": "chatgpt computer typing",
    "برمجة": "programming coding computer",
    "تصميم": "graphic design computer",
    "مونتاج": "video editing computer",
    "ربح": "freelancer working laptop",
    "عمل": "remote work laptop",
    "يوتيوب": "youtube content creator",
    "هاتف": "smartphone technology",
    "تطبيق": "mobile app smartphone",
    "موقع": "website computer",
    "كمبيوتر": "computer technology",
    "أمان": "cyber security computer",
}

def search_query(text):
    text = str(text).lower()

    for arabic, english in KEYWORDS.items():
        if arabic in text:
            return english

    return "technology computer laptop"

def download_video(text, output_path):
    if not API_KEY:
        raise ValueError("PIXABAY_API_KEY is missing")

    query = search_query(text)

    response = requests.get(
        API_URL,
        params={
            "key": API_KEY,
            "q": query,
            "per_page": 20,
            "safesearch": "true"
        },
        timeout=30
    )
    response.raise_for_status()

    videos = response.json().get("hits", [])

    if not videos:
        print("No videos found:", query)
        return False

    video = random.choice(videos)
    files = video.get("videos", {})

    selected = files.get("medium") or files.get("small")

    if not selected or not selected.get("url"):
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    clip = requests.get(selected["url"], timeout=90)
    clip.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(clip.content)

    print("Video downloaded:", output_path)
    return True
