"""Zhuomo behavior invariants — unittest, no LLM."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = (REPO / "SKILL.md").read_text(encoding="utf-8")
REFERENCES = REPO / "references"


class TestSkillStructure(unittest.TestCase):
    def test_references_exist(self):
        required = [
            "concept-claim-rubric.md",
            "lint-interpretation.md",
            "study-diagnosis.md",
            "query-think-and-apply.md",
            "external-fact-check.md",
            "ingest-depth-and-resume.md",
            "bootstrap-adopt.md",
            "transcript-ingest.md",
            "explain-back-modes.md",
            "continuous-study.md",
            "model-agnostic-playbook.md",
        ]
        for name in required:
            self.assertTrue((REFERENCES / name).is_file(), f"missing references/{name}")

    def test_intent_router_has_adopt_and_continue(self):
        self.assertIn("Adopt vault", SKILL)
        self.assertIn("Study continue", SKILL)
        self.assertIn("transcript", SKILL.lower())

    def test_external_claim_confirmation_gate(self):
        self.assertIn("确认 Claim", SKILL)
        self.assertIn("references/external-fact-check.md", SKILL)


class TestCorpusBoundary(unittest.TestCase):
    def test_ingest_reference_forbids_notes_corpus(self):
        text = (REFERENCES / "ingest-depth-and-resume.md").read_text(encoding="utf-8")
        self.assertIn("wiki/concepts/", text)
        self.assertIn("never", text.lower())
        self.assertIn("notes/", text)

    def test_lint_never_touch_notes(self):
        text = (REFERENCES / "lint-interpretation.md").read_text(encoding="utf-8")
        self.assertIn("Never", text)
        self.assertIn("notes/", text)


class TestExplainBackCoverage(unittest.TestCase):
    def test_claim_rubric_requires_subsections(self):
        text = (REFERENCES / "concept-claim-rubric.md").read_text(encoding="utf-8")
        self.assertIn("###", text)
        self.assertIn("Explain-back", text)

    def test_lint_points_to_revise_not_enrich_apply(self):
        text = (REFERENCES / "lint-interpretation.md").read_text(encoding="utf-8")
        self.assertIn("Revise", text)
        self.assertIn("batch-revise", text)

    def test_model_agnostic_doctor_and_playbook(self):
        self.assertTrue((REPO / "scripts" / "zhuomo-doctor.py").is_file())
        text = (REFERENCES / "model-agnostic-playbook.md").read_text(encoding="utf-8")
        self.assertIn("zhuomo-doctor.py", text)
        self.assertIn("Scripts-first", SKILL)


class TestAdoptSafety(unittest.TestCase):
    def test_vault_adopt_check_script_exists(self):
        self.assertTrue((REPO / "scripts" / "vault-adopt-check.py").is_file())

    def test_adopt_reference_refuses_overwrite(self):
        text = (REFERENCES / "bootstrap-adopt.md").read_text(encoding="utf-8")
        self.assertIn("non-destructive", text.lower())
        self.assertIn("vault-adopt-check", text)


class TestExternalTemplate(unittest.TestCase):
    def test_three_part_summary(self):
        text = (REFERENCES / "external-fact-check.md").read_text(encoding="utf-8")
        self.assertIn("事实", text)
        self.assertIn("判断", text)
        self.assertIn("未知", text)


class TestIngestBatchChapters(unittest.TestCase):
    @staticmethod
    def _load_ingest_batch():
        import importlib.util
        import sys

        name = "ingest_batch_chapters_test"
        path = REPO / "scripts" / "ingest-batch-chapters.py"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    def test_chapter_key_extraction(self):
        mod = self._load_ingest_batch()
        self.assertEqual(mod.chapter_key_from_row("Ch3 Eval tools", "part-009"), "Ch3")
        self.assertEqual(mod.chapter_key_from_row("Appendix Local deploy", "part-016"), "Appendix")
        self.assertEqual(mod.chapter_key_from_row("Misc topic", "part-012"), "part-012")

    def test_parse_topic_map(self):
        mod = self._load_ingest_batch()
        body = """
## Topic map — Demo

| Topic | Evidence | Existing | Action |
|-------|----------|----------|--------|
| Ch1 Intro | part-001 | — | Create [[foo-intro]] |
| Ch2 Core | part-002 | [[bar]] | [[foo-core]] |
"""
        rows = mod.parse_topic_map(body)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].chapter_key, "Ch1")
        self.assertIn("foo-intro", rows[0].concept_slugs)


if __name__ == "__main__":
    unittest.main()
