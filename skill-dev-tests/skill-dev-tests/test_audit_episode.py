import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "opc-xhs-production" / "scripts" / "audit_episode.py"


def write_text(path, text="ok"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_state(root, state):
    write_text(root / "production-state.json", json.dumps(state, ensure_ascii=False, indent=2))


def run_audit(root, stage):
    return subprocess.run(
        [sys.executable, str(AUDIT), str(root), "--stage", stage],
        text=True,
        capture_output=True,
        check=False,
    )


class AuditEpisodeTests(unittest.TestCase):
    def test_lingzao_stage_requires_expanded_content_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_text(root / "plan.md", "# 口播规划\n...\n# 笔记规划\n...")
            write_text(root / "voiceover-analysis.md")
            write_text(root / "voiceover-script.md")
            write_text(root / "recording-guide.md")
            write_text(root / "worklog.md", "lingzao")
            write_state(root, {
                "deliverables": {
                    "source_plan_md": "plan.md",
                    "voiceover_analysis_md": "voiceover-analysis.md",
                    "voiceover_script_md": "voiceover-script.md",
                    "recording_guide_md": "recording-guide.md",
                    "poster_titles_md": "",
                    "note_package_md": "",
                },
                "subskills_used": {"lingzao": True},
            })

            result = run_audit(root, "lingzao")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("poster_titles_md", result.stdout)
            self.assertIn("note_package_md", result.stdout)

    def test_animation_generation_requires_explicit_plan_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            required = {
                "plan.md": "# 口播规划\n...\n# 笔记规划\n...",
                "voiceover-analysis.md": "ok",
                "voiceover-script.md": "ok",
                "recording-guide.md": "ok",
                "poster-titles.md": "ok",
                "note-package.md": "ok",
                "recordings/a.mov": "media",
                "animation-brief.md": "ok",
                "animation-project/index.html": "ok",
                "renders/animation.mp4": "media",
                "animation-qa.md": "ok",
                "worklog.md": "lingzao\nhyperframes",
            }
            for rel, text in required.items():
                write_text(root / rel, text)
            write_state(root, {
                "deliverables": {
                    "source_plan_md": "plan.md",
                    "voiceover_analysis_md": "voiceover-analysis.md",
                    "voiceover_script_md": "voiceover-script.md",
                    "recording_guide_md": "recording-guide.md",
                    "poster_titles_md": "poster-titles.md",
                    "note_package_md": "note-package.md",
                    "recording_assets": ["recordings/a.mov"],
                    "animation_brief_md": "animation-brief.md",
                    "animation_project_dir": "animation-project",
                    "animation_render_path": "renders/animation.mp4",
                    "animation_qa_md": "animation-qa.md",
                },
                "confirmations": {"animation_plan_approved": False},
                "subskills_used": {"lingzao": True, "remotion_or_hyperframes": True},
            })

            result = run_audit(root, "animation-generated")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("animation_plan_approved", result.stdout)

    def test_final_stage_passes_when_all_gate_artifacts_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            required = {
                "plan.md": "# 口播规划\n...\n# 笔记规划\n...",
                "voiceover-analysis.md": "ok",
                "voiceover-script.md": "ok",
                "recording-guide.md": "ok",
                "poster-titles.md": "ok",
                "note-package.md": "ok",
                "recordings/a.mov": "media",
                "animation-brief.md": "ok",
                "animation-project/index.html": "ok",
                "renders/animation.mp4": "media",
                "animation-qa.md": "ok",
                "cover-interview-log.md": "ok",
                "cover-brief.md": "ok",
                "cover-prompt.md": "ok",
                "covers/cover.png": "image",
                "cover-qa.md": "ok",
                "final-package.md": "ok",
                "worklog.md": "lingzao\nremotion\natutun-xhs-cover-v2",
            }
            for rel, text in required.items():
                write_text(root / rel, text)
            write_state(root, {
                "deliverables": {
                    "source_plan_md": "plan.md",
                    "voiceover_analysis_md": "voiceover-analysis.md",
                    "voiceover_script_md": "voiceover-script.md",
                    "recording_guide_md": "recording-guide.md",
                    "poster_titles_md": "poster-titles.md",
                    "note_package_md": "note-package.md",
                    "recording_assets": ["recordings/a.mov"],
                    "animation_brief_md": "animation-brief.md",
                    "animation_project_dir": "animation-project",
                    "animation_render_path": "renders/animation.mp4",
                    "animation_qa_md": "animation-qa.md",
                    "cover_interview_log_md": "cover-interview-log.md",
                    "cover_brief_md": "cover-brief.md",
                    "cover_prompt_md": "cover-prompt.md",
                    "cover_output_path": "covers/cover.png",
                    "cover_qa_md": "cover-qa.md",
                    "final_package_md": "final-package.md",
                },
                "confirmations": {
                    "animation_plan_approved": True,
                    "cover_plan_approved": True,
                },
                "subskills_used": {
                    "lingzao": True,
                    "remotion_or_hyperframes": True,
                    "atutun_xhs_cover_v2": True,
                },
            })

            result = run_audit(root, "final")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
