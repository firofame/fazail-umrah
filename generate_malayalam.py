#!/usr/bin/env python3
"""Validate the reviewed Malayalam script and render it with sibling tools."""

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent
TTS_PROJECT = ROOT.parent / "google-docs-tts"
TRANSCRIBE_PROJECT = ROOT.parent / "transcribe"
FULL_STEM = "fazail_umrah_malayalam_full"
CHAPTER_SOURCES = {
    "00_intro": [],
    "01_expiation_of_sins": ["bukhari:1773", "muslim:1349a"],
    "02_removal_of_poverty": ["tirmidhi:810", "nasai:2631", "ibnmajah:2887"],
    "03_umrah_in_ramadan": [
        "bukhari:1782", "bukhari:1863", "muslim:1256", "tirmidhi:939",
    ],
    "04_guests_of_allah": ["ibnmajah:2893", "nasai:2625"],
    "05_jihad_of_women": ["bukhari:1520", "ibnmajah:2901", "nasai:2626"],
    "06_reward_by_hardship": ["bukhari:1787", "ibnmajah:3000"],
    "07_virtues_of_tawaf": ["tirmidhi:959", "nasai:2919"],
    "08_supplication_return": ["bukhari:1797", "muslim:1342"],
    "09_conclusion": [],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe_audio(path: Path, codec: str) -> dict:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=codec_name,sample_rate,channels",
            "-of", "json", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    metadata = json.loads(result.stdout)
    streams = metadata["streams"]
    duration = float(metadata["format"]["duration"])
    if len(streams) != 1 or streams[0]["codec_name"] != codec or duration <= 0:
        raise RuntimeError(f"Invalid {codec} audio: {path}")
    if codec == "opus" and (
        streams[0]["channels"] != 1 or streams[0]["sample_rate"] != "48000"
    ):
        raise RuntimeError(f"Opus output must be mono at 48 kHz: {path}")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"],
        check=True,
    )
    return {
        "duration_seconds": duration,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        **streams[0],
    }


async def render_chapters(tts, texts: dict[str, str], output_dir: Path) -> None:
    tts.CONFIG["headless"] = True
    credentials = tts.get_google_credentials()
    doc_id = tts.get_doc_id(tts.CONFIG["doc_url"])
    async with tts.async_playwright() as playwright:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(tts.CONFIG["profile_dir"]),
            headless=True,
            bypass_csp=True,
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--mute-audio"],
        )
        try:
            page = await tts.open_tts_page(context)
            for stem, text in texts.items():
                output = output_dir / f"{stem}.mp3"
                if output.exists():
                    probe_audio(output, "mp3")
                    print(f"Resuming verified cached chapter: {stem}", flush=True)
                    continue
                print(f"Generating Malayalam chapter: {stem}", flush=True)
                # Each chapter is validated below the Google Docs limit.
                await tts.process_chunk(page, credentials, doc_id, text, output)
                await tts.close_player(page)
                probe_audio(output, "mp3")
        finally:
            await context.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Validate script and source references without contacting Google.",
    )
    args = parser.parse_args()
    sys.path.insert(0, str(TRANSCRIBE_PROJECT))
    from src.translate import validate_translation

    hadiths = {
        record["id"]: record
        for record in json.loads((ROOT / "data/fazail_umrah.json").read_text())
    }
    texts = {}
    chapters = []
    for stem, source_ids in CHAPTER_SOURCES.items():
        path = ROOT / "data/tts" / f"{stem}.txt"
        text = path.read_text(encoding="utf-8").strip() + "\n"
        issues = validate_translation(text)
        if issues:
            raise ValueError(f"{path}: {'; '.join(issues)}")
        sources = [
            {
                "id": source_id,
                "reference": hadiths[source_id]["reference"],
                "grade_as_stored": hadiths[source_id]["grade"],
                "url": hadiths[source_id]["sunnah_url"],
            }
            for source_id in source_ids
        ]
        texts[stem] = text
        chapters.append({
            "stem": stem,
            "text_sha256": sha256(path),
            "characters": len(text),
            "validation_issues": issues,
            "sources": sources,
        })
        print(f"Validated {stem}: {len(text)} characters", flush=True)
    full_text = "\n".join(texts.values())
    full_path = ROOT / "data/tts" / f"{FULL_STEM}.txt"
    full_path.write_text(full_text, encoding="utf-8")
    if args.validate_only:
        print("All ten chapters passed Malayalam TTS checks. No API calls made.")
        return

    sys.path.insert(0, str(TTS_PROJECT))
    import tts

    render_hash = hashlib.sha256(
        (full_text + sha256(TTS_PROJECT / "tts.py") + sha256(Path(__file__)))
        .encode("utf-8")
    ).hexdigest()
    audio_dir = ROOT / "audio"
    cache_dir = audio_dir / ".malayalam-cache" / render_hash
    cache_dir.mkdir(parents=True, exist_ok=True)
    previous_directory = Path.cwd()
    # The sibling tool resolves its credentials relative to its project.
    os.chdir(TTS_PROJECT)
    try:
        asyncio.run(render_chapters(tts, texts, cache_dir))
    finally:
        os.chdir(previous_directory)

    with TemporaryDirectory(prefix="malayalam-", dir=audio_dir) as temporary:
        staged = Path(temporary)
        for chapter in chapters:
            stem = chapter["stem"]
            mp3 = cache_dir / f"{stem}.mp3"
            ogg = staged / f"{stem}.ogg"
            if not tts.convert_mp3_to_ogg_opus(mp3, ogg):
                raise RuntimeError(f"Opus conversion failed for {stem}")
            chapter["audio"] = {
                "mp3": probe_audio(mp3, "mp3"),
                "ogg": probe_audio(ogg, "opus"),
            }
            shutil.copyfile(mp3, staged / mp3.name)
        full_mp3 = staged / f"{FULL_STEM}.mp3"
        if not tts.concatenate_audio_chunks(
            [staged / f"{stem}.mp3" for stem in texts], full_mp3,
        ):
            raise RuntimeError("Full Malayalam recording concatenation failed")
        full_ogg = full_mp3.with_suffix(".ogg")
        if not tts.convert_mp3_to_ogg_opus(full_mp3, full_ogg):
            raise RuntimeError("Full Malayalam Opus conversion failed")
        full_audio = {
            "mp3": probe_audio(full_mp3, "mp3"),
            "ogg": probe_audio(full_ogg, "opus"),
        }
        expected_duration = sum(
            chapter["audio"]["mp3"]["duration_seconds"] for chapter in chapters
        )
        if abs(full_audio["mp3"]["duration_seconds"] - expected_duration) > 0.1:
            raise RuntimeError("Combined MP3 duration does not match its chapters")
        if abs(
            full_audio["mp3"]["duration_seconds"]
            - full_audio["ogg"]["duration_seconds"]
        ) > 0.1:
            raise RuntimeError("Combined MP3 and Opus durations do not match")
        manifest = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "language": "ml",
            "scope": "Reviewed thematic meaning-summary, not all 37 full hadiths",
            "quality_boundary": (
                "Source/script and media checks passed; pronunciation has not "
                "been independently checked by a Malayalam listener or ASR."
            ),
            "dataset_sha256": sha256(ROOT / "data/fazail_umrah.json"),
            "render_sha256": render_hash,
            "full_text_sha256": sha256(full_path),
            "chapters": chapters,
            "full_audio": full_audio,
        }
        manifest_path = staged / "malayalam_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # Do not replace previous recordings until every new file has passed QA.
        for path in staged.iterdir():
            path.replace(audio_dir / path.name)
    for path in cache_dir.glob("*.mp3"):
        path.unlink()
    debug_dir = cache_dir / "debug"
    if debug_dir.is_dir():
        shutil.rmtree(debug_dir)
    cache_dir.rmdir()
    print(
        f"Saved ten chapters and full MP3/Opus recording "
        f"({full_audio['mp3']['duration_seconds']:.2f} seconds) to {audio_dir}",
        flush=True,
    )


if __name__ == "__main__":
    main()
