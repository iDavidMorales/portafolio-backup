#!/usr/bin/env python3
"""Genera un QR PNG para Don Mario."""

from io import BytesIO
from pathlib import Path
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageOps


DEFAULT_URL = "https://routicket.com/negocios/don-mario/?menu_light=1"


def build_qr_png(text: str, output: Path, size_px: int = 1024) -> None:
    encoded = urllib.parse.quote(text, safe="")
    url = f"https://api.qrserver.com/v1/create-qr-code/?size={size_px}x{size_px}&data={encoded}"
    with urllib.request.urlopen(url, timeout=30) as response:
        raw = response.read()
    qr_img = Image.open(BytesIO(raw)).convert("RGBA")

    margin = max(28, size_px // 22)
    canvas_size = size_px + margin * 2
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    qr_img = qr_img.resize((size_px, size_px), Image.LANCZOS)
    canvas.paste(qr_img, (margin, margin), qr_img)
    bordered = ImageOps.expand(canvas, border=18, fill="white")
    output.parent.mkdir(parents=True, exist_ok=True)
    bordered.save(output, format="PNG")


def main() -> int:
    text = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    output = Path(__file__).resolve().parents[3] / "output" / "pdf" / "don-mario" / "don-mario-menu-light-qr.png"
    build_qr_png(text, output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
