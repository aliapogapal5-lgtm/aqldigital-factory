
import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1920

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
    image = Image.new("RGB", (WIDTH, HEIGHT), (12, 18, 38))
    draw = ImageDraw.Draw(image)

    # خلفية تقنية متدرجة
    for y in range(HEIGHT):
        shade = int(18 + (y / HEIGHT) * 35)
        draw.line((0, y, WIDTH, y), fill=(shade, 20, shade + 35))

    # اسم القناة
    draw.text(
        (WIDTH - 70, 100),
        "MODERN TECHNOLOGY",
        font=get_font(43),
        fill=(80, 190, 255),
        anchor="ra"
    )

    # خط ديكوري
    draw.rounded_rectangle(
        (100, 250, 980, 260),
        radius=5,
        fill=(40, 150, 255)
    )

    # نص المشهد
    font = get_font(72)
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word
        if draw.textbbox((0, 0), test, font=font)[2] > 850:
            lines.append(current)
            current = word
        else:
            current = test

    if current:
        lines.append(current)

    y = 750 - (len(lines) * 55)

    for line in lines:
        draw.text(
            (WIDTH // 2, y),
            line,
            font=font,
            fill="white",
            anchor="mm",
            direction="rtl"
        )
        y += 125

    # رقم المشهد
    draw.text(
        (WIDTH // 2, 1600),
        f"SCENE {number}",
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
        raise ValueError("No scenes found in daily_content.json")

    os.makedirs("frames", exist_ok=True)

    for index, scene in enumerate(scenes, start=1):
        if isinstance(scene, dict):
            text = scene.get("text", scene.get("description", ""))
        else:
            text = str(scene)

        if not text.strip():
            continue

        image = create_scene(text, index)
        image.save(f"frames/scene_{index:02d}.png")

    frame_files = sorted(
        f for f in os.listdir("frames") if f.endswith(".png")
    )

    if not frame_files:
        raise ValueError("No valid scenes to render")

    with open("frames.txt", "w", encoding="utf-8") as f:
        for filename in frame_files:
            f.write(f"file 'frames/{filename}'\n")
            f.write("duration 5\n")
        f.write(f"file 'frames/{frame_files[-1]}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "frames.txt",
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264",
        "-movflags", "+faststart",
        "modern_technology.mp4"
    ], check=True)

    print("Video created: modern_technology.mp4")

if __name__ == "__main__":
    make_video()
