#!/usr/bin/env python3
"""Run an end-to-end dry-run of the opc-xhs-production skill gates."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "opc-xhs-production"
AUDIT = SKILL_DIR / "scripts" / "audit_episode.py"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_state(root: Path, state: dict) -> None:
    write_text(root / "production-state.json", json.dumps(state, ensure_ascii=False, indent=2))


def run_audit(root: Path, stage: str, expect_ok: bool = True, must_contain: str | None = None) -> None:
    result = subprocess.run(
        [sys.executable, str(AUDIT), str(root), "--stage", stage],
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    ok = result.returncode == 0
    if ok != expect_ok:
        raise AssertionError(f"stage {stage} expected ok={expect_ok}, got {result.returncode}\n{output}")
    if must_contain and must_contain not in output:
        raise AssertionError(f"stage {stage} output missing {must_contain!r}\n{output}")
    status = "PASS" if ok else "BLOCKED"
    print(f"{status}: {stage}")
    if must_contain:
        print(f"  observed gate: {must_contain}")


def make_complete_episode(root: Path) -> dict:
    files = {
        "plan.md": "# 口播规划\n讲清楚 agent 工作流。\n\n# 笔记规划\n拆成标题、正文、标签。",
        "voiceover-analysis.md": "原稿问题：开头不够钩子，口语节奏弱。",
        "voiceover-script.md": "新版口播稿：三秒钩子，然后进入步骤。",
        "recording-guide.md": "录制提示：自然语速，关键句停顿。",
        "poster-titles.md": "海报主标题：别再手搓流程\n海报副标题：让 Skill 自动接力",
        "note-package.md": "主标题：OPC 小红书生产流\n副标题：从 MD 到成片\n内容：...\n标签：#AI #小红书",
        "recordings/talking-head.mov": "dry-run media placeholder",
        "animation-brief.md": "动效方案：HyperFrames，三段结构，字幕安全区，渲染 QA。",
        "animation-project/index.html": "<html><body>dry run animation</body></html>",
        "renders/animation.mp4": "dry-run render placeholder",
        "animation-qa.md": "预览非空，字幕未越界，时长匹配。",
        "cover-interview-log.md": "Q1: 人设？A: 探长式经验分享。",
        "cover-brief.md": "封面方案：3:4，人物大图，超大标题，绿色勾选清单。",
        "cover-prompt.md": "atutun-xhs-cover-v2 prompt placeholder",
        "covers/cover.png": "dry-run image placeholder",
        "cover-qa.md": "3:4，标题可读，未遮挡主体。",
        "final-package.md": "成片、封面、标题、正文、标签、发布检查清单。",
        "worklog.md": "lingzao\nhyperframes\natutun-xhs-cover-v2\n",
    }
    for rel, text in files.items():
        write_text(root / rel, text)

    return {
        "episode": {
            "name": "dry-run",
            "source_plan_md": "plan.md",
            "current_stage": "final",
        },
        "deliverables": {
            "source_plan_md": "plan.md",
            "voiceover_analysis_md": "voiceover-analysis.md",
            "voiceover_script_md": "voiceover-script.md",
            "recording_guide_md": "recording-guide.md",
            "poster_titles_md": "poster-titles.md",
            "note_package_md": "note-package.md",
            "recording_assets": ["recordings/talking-head.mov"],
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
            "animation_plan_approved": False,
            "cover_plan_approved": False,
        },
        "subskills_used": {
            "lingzao": True,
            "remotion_or_hyperframes": True,
            "atutun_xhs_cover_v2": True,
        },
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="opc-xhs-dry-run-") as tmp:
        root = Path(tmp)
        state = make_complete_episode(root)
        write_state(root, state)

        for stage in ("intake", "lingzao", "recording", "animation-plan"):
            run_audit(root, stage)

        run_audit(
            root,
            "animation-generated",
            expect_ok=False,
            must_contain="animation_plan_approved",
        )
        state["confirmations"]["animation_plan_approved"] = True
        write_state(root, state)
        run_audit(root, "animation-generated")

        run_audit(root, "cover-plan")
        run_audit(
            root,
            "cover-generated",
            expect_ok=False,
            must_contain="cover_plan_approved",
        )
        state["confirmations"]["cover_plan_approved"] = True
        write_state(root, state)
        run_audit(root, "cover-generated")
        run_audit(root, "final")

        print(f"DRY_RUN_EPISODE={root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
