import asyncio
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generate_malayalam as narration

sys.path.insert(0, str(narration.TRANSCRIBE_PROJECT))
from src.translate import validate_translation


class NarrationTests(unittest.TestCase):
    def test_chapter_order_and_new_source_coverage(self):
        stems = list(narration.CHAPTER_SOURCES)
        self.assertEqual(len(stems), 22)
        self.assertEqual(stems[0], "00_intro")
        self.assertEqual(stems[-1], "09_conclusion")
        self.assertEqual(stems[8], "08_supplication_return")
        self.assertEqual(stems[9], "10_talbiyah")
        new_ids = [
            source_id
            for stem, source_ids in narration.CHAPTER_SOURCES.items()
            if int(stem.split("_", 1)[0]) >= 10
            for source_id in source_ids
        ]
        reviews = json.loads(narration.REVIEW_PATH.read_text())["records"]
        self.assertEqual(len(new_ids), 29)
        self.assertEqual(len(new_ids), len(set(new_ids)))
        self.assertEqual(set(new_ids), set(reviews))
        dataset_ids = {
            record["id"]
            for record in json.loads((ROOT / "data/fazail_umrah.json").read_text())
        }
        self.assertTrue(set(new_ids) <= dataset_ids)
        self.assertEqual(
            sum(r["usage"] == "excluded_unverified" for r in reviews.values()), 4
        )
        self.assertEqual(
            sum(r["usage"] == "qualified_report" for r in reviews.values()), 6
        )

    def test_all_chapters_pass_sibling_tts_validation(self):
        for stem in narration.CHAPTER_SOURCES:
            with self.subTest(stem=stem):
                text = (ROOT / "data/tts" / f"{stem}.txt").read_text()
                self.assertEqual(validate_translation(text), [])

    def test_verified_reviews_have_grade_and_primary_url(self):
        reviews = json.loads(narration.REVIEW_PATH.read_text())["records"]
        for source_id, review in reviews.items():
            with self.subTest(source_id=source_id):
                if review["usage"] != "excluded_unverified":
                    self.assertTrue(review["grade_verified"])
                    self.assertTrue(
                        review["url_verified"].startswith("https://sunnah.com/")
                    )
                    self.assertNotEqual(review["url_verified"], "https://sunnah.com/")

    def test_cached_chapters_do_not_start_browser(self):
        with TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "chapter.mp3").write_bytes(b"cached")
            with patch.object(narration, "probe_audio") as probe:
                asyncio.run(
                    narration.render_chapters(None, {"chapter": "text"}, output)
                )
                probe.assert_called_once_with(output / "chapter.mp3", "mp3")

    def write_published(self, audio_dir):
        mp3 = audio_dir / "chapter.mp3"
        mp3.write_bytes(b"published audio")
        (audio_dir / "malayalam_manifest.json").write_text(json.dumps({
            "render_sha256": "old-renderer",
            "chapters": [{
                "stem": "chapter",
                "text_sha256": "same-text",
                "audio": {"mp3": {"sha256": narration.sha256(mp3)}},
            }],
        }))
        return mp3

    def test_reuse_requires_matching_text_and_audio_hashes(self):
        with TemporaryDirectory() as temporary:
            audio_dir = Path(temporary)
            cache_dir = audio_dir / "cache"
            cache_dir.mkdir()
            mp3 = self.write_published(audio_dir)
            chapters = [{"stem": "chapter", "text_sha256": "same-text"}]
            with patch.object(narration, "probe_audio") as probe:
                narration.reuse_verified_chapters(chapters, audio_dir, cache_dir)
                probe.assert_called_once_with(mp3, "mp3")
            self.assertEqual((cache_dir / mp3.name).read_bytes(), mp3.read_bytes())
            self.assertEqual(chapters[0]["generation"], {
                "method": "reused_verified",
                "previous_render_sha256": "old-renderer",
            })

    def test_changed_text_is_not_reused(self):
        with TemporaryDirectory() as temporary:
            audio_dir = Path(temporary)
            cache_dir = audio_dir / "cache"
            cache_dir.mkdir()
            self.write_published(audio_dir)
            with patch.object(narration, "probe_audio") as probe:
                narration.reuse_verified_chapters(
                    [{"stem": "chapter", "text_sha256": "changed-text"}],
                    audio_dir, cache_dir,
                )
                probe.assert_not_called()
            self.assertEqual(list(cache_dir.iterdir()), [])

    def test_corrupted_published_audio_fails_explicitly(self):
        with TemporaryDirectory() as temporary:
            audio_dir = Path(temporary)
            cache_dir = audio_dir / "cache"
            cache_dir.mkdir()
            mp3 = self.write_published(audio_dir)
            mp3.write_bytes(b"corrupted")
            with self.assertRaisesRegex(RuntimeError, "checksum mismatch"):
                narration.reuse_verified_chapters(
                    [{"stem": "chapter", "text_sha256": "same-text"}],
                    audio_dir, cache_dir,
                )

    def test_reuse_without_manifest_fails_explicitly(self):
        with TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(FileNotFoundError, "requires"):
                narration.reuse_verified_chapters([], Path(temporary), Path(temporary))


if __name__ == "__main__":
    unittest.main()
