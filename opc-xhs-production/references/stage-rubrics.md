# Stage Rubrics

## Intake

- Publishing-plan MD contains both 口播规划 and 笔记规划.
- Blocking gaps are asked as questions before creative rewriting.
- `production-state.json` records the source MD path.

## Lingzao Content Package

The Lingzao package must include:

- 原口播问题分析: concrete issues, not generic praise.
- 新版口播稿: spoken, shootable, paced for the target video length.
- 录制/拍摄提示: tone, shot, pause, expression, and retake notes.
- 海报主标题 and 海报副标题: short, high-contrast, cover-friendly.
- 笔记正文主标题 and 笔记正文副标题: searchable and curiosity-driven.
- 笔记内容: structured for 小红书 reading, with useful detail.
- 笔记标签: relevant tags, no spammy stuffing.

## Animation Plan

Before generation, the animation plan must state:

- viewer feeling and content goal
- Remotion vs HyperFrames choice and reason
- scene-by-scene structure with rough timing
- user素材 and any web-sourced素材 candidates
- source URLs and licensing assumptions for web素材
- subtitle and text hierarchy strategy
- render, preview, and QA checks

## Animation QA

- Render or preview is nonblank and correctly framed.
- Audio/video timing matches the script or edit plan.
- Text/subtitles stay inside safe areas.
- Web素材 use is recorded and appropriate.
- Render path and project path exist.

## Cover Plan

Before generation, the cover plan must state:

- main title and subtitle
- 3:4 first-pass layout
- subject/material placement
- color, typography, stickers, arrows, checklist usage
- variants to generate
- unresolved questions, if any

## Cover QA

- First pass is 3:4 unless user requested otherwise.
- Title is readable at phone-feed size.
- Text does not overlap faces or key objects.
- Style follows `atutun-xhs-cover-v2` conventions unless user changes direction.
- Output path exists.

## Final Package

- Final package includes final video path, animation render path, cover path, title options, note content, tags, and publish checklist.
- `scripts/audit_episode.py` passes for `--stage final`.
