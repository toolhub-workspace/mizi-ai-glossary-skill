#!/usr/bin/env python3
"""Render one approved six-page issue with deterministic typography.

The script intentionally draws text only. It never creates arrows, doodles,
corner metadata, cards, or repeated page chrome.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


CANVAS = (3000, 4000)
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TITLE = "/System/Library/Fonts/MarkerFelt.ttc"
DEFAULT_COVER = "/System/Library/Fonts/PingFang.ttc"
FALLBACK_BODY = str(SKILL_ROOT / "assets/fonts/XiaolaiSC-Regular.ttf")
DEFAULT_COLORS = {
    "charcoal": "#3e3e3b",
    "gray": "#656460",
    "orange": "#e7650e",
}
FORBIDDEN_LINE_START = set("，。；：、？！）》】」』…,.!?;:%")


def default_body_font() -> str:
    """Prefer the user's macOS Wawati SC font without redistributing it."""
    direct_candidates = [
        Path("/System/Library/Fonts/WawaSC-Regular.otf"),
        Path("/System/Library/Fonts/Supplemental/WawaSC-Regular.otf"),
        Path("/Library/Fonts/WawaSC-Regular.otf"),
        Path.home() / "Library/Fonts/WawaSC-Regular.otf",
    ]
    asset_candidates = sorted(
        Path("/System/Library/AssetsV2/com_apple_MobileAsset_Font7").glob(
            "*/AssetData/WawaSC-Regular.otf"
        )
    )
    for candidate in [*direct_candidates, *asset_candidates]:
        if candidate.is_file():
            return str(candidate)
    return FALLBACK_BODY


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to an issue JSON config")
    return parser.parse_args()


def hex_color(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Expected six-digit hex color, got {value!r}")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def load_font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    font_path = Path(path)
    if not font_path.is_file():
        raise FileNotFoundError(f"Font not found: {font_path}")
    return ImageFont.truetype(str(font_path), size=size, index=index)


def resolve_path(value: str, config_dir: Path) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else (config_dir / path).resolve()


def wrap_chars(
    draw: ImageDraw.ImageDraw,
    text: str,
    face: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        too_wide = current and draw.textlength(candidate, font=face) > max_width
        if too_wide and char not in FORBIDDEN_LINE_START:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_multiline(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: list[int],
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int,
) -> int:
    x, y = xy
    bbox = face.getbbox("咪API")
    line_height = bbox[3] - bbox[1] + line_gap
    for line in wrap_chars(draw, text, face, max_width):
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height
    return y


def paste_rotated_text(
    canvas: Image.Image,
    text: str,
    xy: list[int],
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    angle: float,
) -> None:
    probe = ImageDraw.Draw(canvas)
    bbox = probe.textbbox((0, 0), text, font=face)
    width = bbox[2] - bbox[0] + 180
    height = bbox[3] - bbox[1] + 180
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    layer_draw = ImageDraw.Draw(layer)
    layer_draw.text((90 - bbox[0], 70 - bbox[1]), text, font=face, fill=fill + (255,))
    layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    canvas.paste(layer, tuple(xy), layer)


def check_source_ratio(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    ratio = image.width / image.height
    if abs(ratio - 0.75) > 0.005:
        raise ValueError(f"Source must be 3:4 without cropping: {path} is {image.width}x{image.height}")
    return image.resize(CANVAS, Image.Resampling.LANCZOS)


def ensure_no_unapproved_metadata(config: dict[str, Any]) -> None:
    if config.get("allow_page_metadata", False):
        return
    visible: list[str] = []
    for page in config["pages"]:
        visible.extend([page.get("term", ""), page.get("definition", ""), page.get("analogy", "")])
        visible.extend(line.get("text", "") for line in page.get("cover_lines", []))
    combined = "\n".join(visible)
    if "咪子分享" in combined or re.search(r"第\s*\d+\s*期", combined):
        raise ValueError("Recurring series/issue metadata is disabled for page artwork")


def render_page(
    page: dict[str, Any],
    config: dict[str, Any],
    config_dir: Path,
) -> Image.Image:
    source = resolve_path(page["source_image"], config_dir)
    if not source.is_file():
        raise FileNotFoundError(f"Art base not found: {source}")
    canvas = check_source_ratio(source)
    draw = ImageDraw.Draw(canvas)

    fonts = config["fonts"]
    colors = {name: hex_color(value) for name, value in config["colors"].items()}

    if page["kind"] == "cover":
        for line in page["cover_lines"]:
            role = line.get("font_role", "cover")
            face = load_font(fonts[role], line["size"], line.get("font_index", 0))
            paste_rotated_text(
                canvas,
                line["text"],
                line["xy"],
                face,
                colors[line["color"]],
                line.get("angle", 0.0),
            )
        return canvas

    layout = page["layout"]
    title_face = load_font(fonts["title"], layout["term_size"], layout.get("title_font_index", 0))
    paste_rotated_text(
        canvas,
        page["term"],
        layout["term_xy"],
        title_face,
        colors[layout.get("term_color", "charcoal")],
        layout.get("term_angle", 0.8),
    )

    definition_face = load_font(fonts["body"], layout["definition_size"])
    definition_end = draw_multiline(
        draw,
        page["definition"],
        layout["definition_xy"],
        definition_face,
        colors[layout.get("definition_color", "gray")],
        layout["definition_width"],
        layout.get("definition_gap", 40),
    )

    analogy_xy = layout.get("analogy_xy") or [layout["definition_xy"][0], definition_end + 130]
    analogy_face = load_font(fonts["body"], layout["analogy_size"])
    draw_multiline(
        draw,
        page["analogy"],
        analogy_xy,
        analogy_face,
        colors[layout.get("analogy_color", "orange")],
        layout["analogy_width"],
        layout.get("analogy_gap", 38),
    )
    return canvas


def output_stem(issue_number: str, page: dict[str, Any]) -> str:
    order = int(page["order"])
    label = page["label"]
    return f"咪子分享第{issue_number}期-{order:02d}-{label}"


def make_contact_sheet(png_files: list[Path], output: Path) -> None:
    thumb_w, thumb_h, gap = 600, 800, 24
    sheet = Image.new("RGB", (thumb_w * 3 + gap * 4, thumb_h * 2 + gap * 3), (239, 237, 232))
    for index, path in enumerate(png_files):
        image = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = gap + (index % 3) * (thumb_w + gap)
        y = gap + (index // 3) * (thumb_h + gap)
        sheet.paste(image, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="JPEG", quality=92)


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    config_dir = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))

    if len(config.get("pages", [])) != 6:
        raise ValueError("An issue must contain exactly one cover and five term pages")
    orders = sorted(int(page["order"]) for page in config["pages"])
    if orders != [1, 2, 3, 4, 5, 6]:
        raise ValueError("Page orders must be exactly 1 through 6")

    config.setdefault("fonts", {})
    config["fonts"].setdefault("title", DEFAULT_TITLE)
    config["fonts"].setdefault("cover", DEFAULT_COVER)
    config["fonts"].setdefault("body", default_body_font())
    config.setdefault("colors", {})
    for name, value in DEFAULT_COLORS.items():
        config["colors"].setdefault(name, value)

    ensure_no_unapproved_metadata(config)

    output_dir = resolve_path(config["output_dir"], config_dir)
    png_dir = output_dir / "PNG"
    jpg_dir = output_dir / "JPG"
    source_dir = output_dir / "source"
    png_dir.mkdir(parents=True, exist_ok=True)
    jpg_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    issue_number = str(config["issue_number"])
    targets: list[tuple[dict[str, Any], Path, Path]] = []
    for page in sorted(config["pages"], key=lambda item: int(item["order"])):
        stem = output_stem(issue_number, page)
        png = png_dir / f"{stem}.png"
        jpg = jpg_dir / f"{stem}.jpg"
        if png.exists() or jpg.exists():
            raise FileExistsError(f"Refusing to overwrite existing page: {stem}")
        targets.append((page, png, jpg))

    written_png: list[Path] = []
    for page, png, jpg in targets:
        image = render_page(page, config, config_dir)
        image.save(png, format="PNG", optimize=True)
        image.save(jpg, format="JPEG", quality=94, optimize=True, progressive=True)
        written_png.append(png)

    make_contact_sheet(written_png, source_dir / "contact-sheet.jpg")
    for path in written_png:
        with Image.open(path) as image:
            if image.size != CANVAS:
                raise RuntimeError(f"Unexpected final size for {path}: {image.size}")

    print(f"Rendered six PNG and six JPG pages under {output_dir}")


if __name__ == "__main__":
    main()
