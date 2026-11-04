

import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1920
SCENE_DURATION = 5
FPS = 30

ASSETS = "assets"
LOGO = os.path.join(ASSETS, "logo.jpg")
MUSIC = os.path.join(ASSETS, "background.mp3")


def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf"
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def create_scene(text, number):
    image = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # خلفية متدرجة
    for y in range(HEIGHT):
        shade = int(12 + (y / HEIGHT) * 30)
        draw.line(
            (0, y, WIDTH, y),
            fill=(shade, 20, shade + 35)
        )

    # الشعار واسم القناة
    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((115, 115))
        image.paste(logo, (65, 65), logo)

    draw.text(
        (205, 105),
        "MODERN TECHNOLOGY",
        font=get_font(38),
        fill=(80, 190, 255),
        anchor="lm"
    )

    # خط ديكوري
    draw.rounded_rectangle(
        (80, 230, 1000, 240),
        radius=5,
        fill=(40, 150, 255)
    )

    # كتابة النص
    font = get_font(70)
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word

        if draw.textbbox((0, 0), test, font=font)[2] > 850:
            if current:
                lines.append(current)
            current = word
        else:
            current = test

    if current:
        lines.append(current)

    y = 800 - (len(lines) * 65)

    for line in lines:
        draw.text(
            (WIDTH // 2, y),
            line,
            font=font,
            fill="white",
            anchor="mm",
            direction="rtl"
        )
        y += 135

    # رقم المشهد
    draw.text(
        (WIDTH // 2, 1650),
        f"{number:02d} / 04",
        font=get_font(38),
        fill=(100, 190, 255),
        anchor="mm"
    )

    return image


def make_video():
    with open("daily_content.json", encoding="utf-8") as f:
        data = json.load(f)

    scenes = data.get("scenes", [])

    if not scenes:
        raise ValueError("No scenes found")

    os.makedirs("frames", exist_ok=True)

    # حذف ملفات المشاهد القديمة
    for filename in os.listdir("frames"):
        if filename.endswith((".png", ".mp4")):
            os.remove(os.path.join("frames", filename))

    # إنشاء صور المشاهد
    frame_files = []

    for index, scene in enumerate(scenes, start=1):
        if isinstance(scene, dict):
            text = scene.get("text", scene.get("description", ""))
        else:
            text = str(scene)

        if not text.strip():
            continue

        image = create_scene(text, index)
        filename = f"frames/scene_{index:02d}.png"
        image.save(filename)
        frame_files.append(filename)

    if not frame_files:
        raise ValueError("No valid scenes")

    # تحويل كل مشهد إلى فيديو متحرك
    video_files = []

    for index, filename in enumerate(frame_files, start=1):
        output = f"frames/clip_{index:02d}.mp4"

        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", filename,
            "-t", str(SCENE_DURATION),
            "-vf",
            "zoompan=z='min(zoom+0.0005,1.08)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            "d=1:s=1080x1920:fps=30,"
            "format=yuv420p",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output
        ], check=True)

        video_files.append(output)

    # دمج المشاهد
    with open("frames.txt", "w", encoding="utf-8") as f:
        for filename in video_files:
            f.write(f"file '{filename}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "frames.txt",
        "-c", "copy",
        "joined.mp4"
    ], check=True)

    # إضافة الموسيقى
    if os.path.exists(MUSIC):
        subprocess.run([
            "ffmpeg", "-y",
            "-i", "joined.mp4",
            "-stream_loop", "-1",
            "-i", MUSIC,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            "modern_technology.mp4"
        ], check=True)
    else:
        os.replace("joined.mp4", "modern_technology.mp4")

    print("Video created successfully!")


if __name__ == "__main__":
    make_video()

