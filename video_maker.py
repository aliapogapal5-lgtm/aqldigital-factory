
import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from video_library import download_video

WIDTH = 1080
HEIGHT = 1920
FPS = 30

LOGO = "assets/logo.jpg"
MUSIC = "assets/background.mp3"


def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf"
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def create_overlay(text, number):
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # شريط علوي
    draw.rectangle((0, 0, WIDTH, 190), fill=(0, 0, 0, 150))

    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((110, 110))
        image.alpha_composite(logo, (45, 35))

    draw.text(
        (190, 90),
        "MODERN TECHNOLOGY",
        font=get_font(38),
        fill=(80, 190, 255, 255),
        anchor="lm"
    )

    # خلفية النص
    draw.rounded_rectangle(
        (55, 650, 1025, 1240),
        radius=35,
        fill=(0, 0, 0, 175)
    )

    font = get_font(65)
    words = str(text).split()
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

    y = 900 - len(lines) * 65

    for line in lines:
        draw.text(
            (540, y),
            line,
            font=font,
            fill="white",
            anchor="mm",
            direction="rtl"
        )
        y += 130

    draw.text(
        (540, 1770),
        f"MODERN TECHNOLOGY  |  {number:02d}",
        font=get_font(30),
        fill=(100, 200, 255, 255),
        anchor="mm"
    )

    return image


def run_ffmpeg(args):
    subprocess.run(args, check=True)


def make_video():
    with open("daily_content.json", encoding="utf-8") as f:
        data = json.load(f)

    scenes = data.get("scenes", [])

    if not scenes:
        raise ValueError("No scenes found")

    os.makedirs("frames", exist_ok=True)

    clips = []

    for index, scene in enumerate(scenes, start=1):

        if isinstance(scene, dict):
            text = scene.get("text", scene.get("description", ""))
        else:
            text = str(scene)

        if not text.strip():
            continue

        print("Preparing scene:", index)

        video_path = f"frames/video_{index}.mp4"
        overlay_path = f"frames/overlay_{index}.png"
        output_path = f"frames/final_{index}.mp4"

        overlay = create_overlay(text, index)
        overlay.save(overlay_path)

        downloaded = False

        try:
            downloaded = download_video(text, video_path)
        except Exception as error:
            print("Video download failed:", error)

        if not downloaded:
            raise RuntimeError(
                f"No suitable video downloaded for scene {index}"
            )

        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", overlay_path,
            "-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,fps=30,setsar=1[bg];"
            "[bg][1:v]overlay=0:0",
            "-t", "5",
            "-an",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            output_path
        ])

        clips.append(output_path)

    if not clips:
        raise RuntimeError("No video clips created")

    with open("frames.txt", "w", encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    run_ffmpeg([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "frames.txt",
        "-c", "copy",
        "joined.mp4"
    ])

    if os.path.exists(MUSIC):
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", "joined.mp4",
            "-stream_loop", "-1",
            "-i", MUSIC,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "-movflags", "+faststart",
            "modern_technology.mp4"
        ])
    else:
        os.replace("joined.mp4", "modern_technology.mp4")

    print("Video created successfully!")


if __name__ == "__main__":
    make_video()
