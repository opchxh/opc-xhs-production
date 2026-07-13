#!/usr/bin/env python3
"""Audit an OPC XHS episode workspace for required stage gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


STAGES = {
    "intake",
    "lingzao",
    "recording",
    "animation-plan",
    "animation-generated",
    "cover-plan",
    "cover-generated",
    "final",
}

TEXT_SUFFIXES = {".md", ".txt", ".json", ".html", ".css", ".js", ".ts", ".tsx"}
PLACEHOLDER_TOKENS = ("TODO", "TBD", "path/to/", "example.com", "<INSERT", "<FILL")


class Auditor:
    def __init__(self, root: Path, stage: str):
        self.root = root
        self.stage = stage
        self.errors: list[str] = []
        self.state = self._load_state()

    def run(self) -> int:
        if self.stage not in STAGES:
            self.errors.append(f"Unknown stage: {self.stage}")
        if self.state:
            self._check_stage()
            self._check_placeholders()

        if self.errors:
            print("FAIL")
            for error in self.errors:
                print(f"- {error}")
            return 1

        print(f"OK: {self.stage}")
        return 0

    def _load_state(self) -> dict:
        state_path = self.root / "production-state.json"
        if not state_path.exists():
            self.errors.append("Missing production-state.json")
            return {}
        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.errors.append(f"Invalid production-state.json: {exc}")
            return {}

    @property
    def deliverables(self) -> dict:
        value = self.state.get("deliverables", {})
        if not isinstance(value, dict):
            self.errors.append("deliverables must be an object")
            return {}
        return value

    @property
    def confirmations(self) -> dict:
        value = self.state.get("confirmations", {})
        return value if isinstance(value, dict) else {}

    @property
    def subskills(self) -> dict:
        value = self.state.get("subskills_used", {})
        return value if isinstance(value, dict) else {}

    def _check_stage(self) -> None:
        if self.stage in {"intake", "lingzao", "recording", "animation-plan", "animation-generated", "cover-plan", "cover-generated", "final"}:
            self._check_intake()
        if self.stage in {"lingzao", "recording", "animation-plan", "animation-generated", "cover-plan", "cover-generated", "final"}:
            self._check_lingzao()
        if self.stage in {"recording", "animation-plan", "animation-generated", "final"}:
            self._check_recording()
        if self.stage in {"animation-plan", "animation-generated", "final"}:
            self._check_animation_plan()
        if self.stage in {"animation-generated", "final"}:
            self._check_animation_generated()
        if self.stage in {"cover-plan", "cover-generated", "final"}:
            self._check_cover_plan()
        if self.stage in {"cover-generated", "final"}:
            self._check_cover_generated()
        if self.stage == "final":
            self._check_path_field("final_package_md", kind="file")

    def _check_intake(self) -> None:
        plan_value = self.deliverables.get("source_plan_md")
        brief_value = self.deliverables.get("source_brief_md")
        if isinstance(plan_value, str) and plan_value.strip():
            path = self._check_relative_path(plan_value, "source_plan_md", kind="file")
            if path and path.exists():
                text = path.read_text(encoding="utf-8", errors="ignore")
                if "口播" not in text:
                    self.errors.append("source_plan_md must contain 口播 planning")
                if "笔记" not in text:
                    self.errors.append("source_plan_md must contain 笔记 planning")
            return
        if isinstance(brief_value, str) and brief_value.strip():
            self._check_relative_path(brief_value, "source_brief_md", kind="file")
            return
        self.errors.append("Either source_plan_md or source_brief_md is required")

    def _check_lingzao(self) -> None:
        for field in (
            "topic_angle_md",
            "voiceover_analysis_md",
            "voiceover_script_md",
            "recording_guide_md",
            "poster_titles_md",
            "note_package_md",
        ):
            self._check_path_field(field, kind="file")
        self._check_subskill("lingzao")
        self._check_worklog_mentions("lingzao")

    def _check_recording(self) -> None:
        audio_assets = self.deliverables.get("audio_assets")
        if not isinstance(audio_assets, list) or not audio_assets:
            self.errors.append("audio_assets must contain at least one uploaded audio path")
        else:
            for item in audio_assets:
                self._check_relative_path(str(item), "audio_assets", kind="file")

        for optional_field in ("video_assets", "auxiliary_assets"):
            assets_by_type = self.deliverables.get(optional_field)
            if not isinstance(assets_by_type, list):
                self.errors.append(f"{optional_field} must be a list")
                continue
            for item in assets_by_type:
                self._check_relative_path(str(item), optional_field, kind="file")

        assets = self.deliverables.get("recording_assets")
        if not isinstance(assets, list) or not assets:
            self.errors.append("recording_assets must contain at least one uploaded file path")
            return
        for item in assets:
            self._check_relative_path(str(item), "recording_assets", kind="file")

    def _check_animation_plan(self) -> None:
        self._check_path_field("animation_brief_md", kind="file")

    def _check_animation_generated(self) -> None:
        if self.confirmations.get("animation_plan_approved") is not True:
            self.errors.append("animation_plan_approved must be true before animation generation")
        self._check_path_field("animation_project_dir", kind="dir")
        self._check_path_field("animation_render_path", kind="file")
        self._check_path_field("animation_qa_md", kind="file")
        self._check_subskill("remotion_or_hyperframes")
        if not self._worklog_contains_any(("remotion", "hyperframes")):
            self.errors.append("worklog.md must mention remotion or hyperframes")

    def _check_cover_plan(self) -> None:
        self._check_path_field("cover_interview_log_md", kind="file")
        self._check_path_field("cover_brief_md", kind="file")

    def _check_cover_generated(self) -> None:
        if self.confirmations.get("cover_plan_approved") is not True:
            self.errors.append("cover_plan_approved must be true before cover generation")
        self._check_path_field("cover_prompt_md", kind="file")
        self._check_path_field("cover_output_path", kind="file")
        self._check_path_field("cover_qa_md", kind="file")
        self._check_subskill("atutun_xhs_cover_v2")
        self._check_worklog_mentions("atutun-xhs-cover-v2")

    def _check_path_field(self, field: str, kind: str) -> Path | None:
        value = self.deliverables.get(field)
        if not isinstance(value, str) or not value.strip():
            self.errors.append(f"{field} is required")
            return None
        return self._check_relative_path(value, field, kind=kind)

    def _check_relative_path(self, value: str, field: str, kind: str) -> Path | None:
        rel = Path(value)
        if rel.is_absolute():
            self.errors.append(f"{field} must be relative to the episode folder")
            return None
        path = self.root / rel
        if kind == "file" and not path.is_file():
            self.errors.append(f"{field} file does not exist: {value}")
        if kind == "dir" and not path.is_dir():
            self.errors.append(f"{field} directory does not exist: {value}")
        return path

    def _check_subskill(self, name: str) -> None:
        if self.subskills.get(name) is not True:
            self.errors.append(f"subskills_used.{name} must be true")

    def _worklog_text(self) -> str:
        path = self.root / "worklog.md"
        if not path.exists():
            self.errors.append("Missing worklog.md")
            return ""
        return path.read_text(encoding="utf-8", errors="ignore").lower()

    def _check_worklog_mentions(self, token: str) -> None:
        if token.lower() not in self._worklog_text():
            self.errors.append(f"worklog.md must mention {token}")

    def _worklog_contains_any(self, tokens: tuple[str, ...]) -> bool:
        text = self._worklog_text()
        return any(token.lower() in text for token in tokens)

    def _check_placeholders(self) -> None:
        for path in self.root.rglob("*"):
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in PLACEHOLDER_TOKENS:
                if token in text:
                    rel = path.relative_to(self.root)
                    self.errors.append(f"Placeholder token {token!r} found in {rel}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit an OPC XHS episode workspace.")
    parser.add_argument("episode_folder", help="Folder containing production-state.json")
    parser.add_argument("--stage", required=True, choices=sorted(STAGES))
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.episode_folder).resolve()
    if not root.is_dir():
        print("FAIL")
        print(f"- Episode folder does not exist: {root}")
        return 1
    return Auditor(root, args.stage).run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
