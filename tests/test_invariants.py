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
        self.assertIn("--apply", text)


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


if __name__ == "__main__":
    unittest.main()
