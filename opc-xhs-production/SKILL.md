---
name: opc-xhs-production
description: Use when producing OPC 碎碎念探长小红书 content, 小红书 or short-video content from a markdown publishing plan, especially when the user says "使用OPC 碎碎念探长小红书 skill", or mentions 口播规划, 笔记规划, 灵造, Remotion, HyperFrames, 小红书封面, 动效, 成片.
---

# OPC XHS Production

## Overview

Coordinate one 小红书/short-video episode from publishing-plan MD to voiceover, animation, cover, and final delivery package. This is an orchestration skill: use the required sub-skills at the correct stage, preserve approvals, and run the audit script before claiming a stage is complete.

## Required Sub-Skills

- **REQUIRED SUB-SKILL:** Use `lingzao` for plan analysis, voiceover rewriting, poster-title ideas, and note-package generation.
- **REQUIRED SUB-SKILL:** Use `remotion:remotion-best-practices` when building Remotion animation code.
- **REQUIRED SUB-SKILL:** Use `hyperframes:hyperframes` and `hyperframes:hyperframes-cli` when building HyperFrames animation.
- **REQUIRED SUB-SKILL:** Use `atutun-xhs-cover-v2` for cover creation. Use `atutun-xhs-cover` only if v2 is unavailable.

If a required sub-skill is unavailable, say exactly which one is unavailable and ask before continuing with a fallback.

## Episode Workspace

For each episode, create or maintain an episode folder with:

```text
production-state.json
worklog.md
```

Use `assets/episode-template/` as the starting point. Update `production-state.json` after each stage and log every required sub-skill call in `worklog.md`.

Run:

```bash
python scripts/audit_episode.py <episode-folder> --stage <stage>
```

Stages: `intake`, `lingzao`, `recording`, `animation-plan`, `animation-generated`, `cover-plan`, `cover-generated`, `final`.

## Workflow

1. **Intake**
   - Read the publishing-plan MD.
   - Confirm it contains both 口播规划 and 笔记规划.
   - Ask only blocking questions. Do not rewrite content yet.
   - Run audit stage `intake`.

2. **Lingzao Content Package**
   - Call `lingzao`.
   - Produce this exact package:
     - 原口播问题分析
     - 新版口播稿
     - 录制/拍摄提示
     - 海报主标题
     - 海报副标题
     - 笔记正文主标题
     - 笔记正文副标题
     - 笔记内容
     - 笔记标签
   - Save the outputs as separate or clearly sectioned files and record paths in `production-state.json`.
   - Run audit stage `lingzao`.

3. **Recording Wait**
   - Tell the user what to record or shoot.
   - Wait for uploaded audio/video files.
   - Do not invent file paths, durations, transcripts, or camera details.
   - Register received files in `recording_assets`.
   - Run audit stage `recording`.

4. **Animation Plan Before Generation**
   - Inspect the uploaded素材.
   - If useful, search the web for high-quality visual references or supplement material. Record source URLs, licensing assumptions, and planned use in the animation brief.
   - Choose Remotion or HyperFrames based on the requested effect, asset type, and rendering needs.
   - Present an animation plan before generating:
     - goal and viewer feeling
     - tool choice and reason
     - scene structure and timing
     - asset list, including user assets and web-sourced candidates
     - subtitle/text strategy
     - render and QA plan
   - Ask whether to generate the animation. Wait for approval.
   - Save the plan and run audit stage `animation-plan`.

5. **Animation Generation**
   - Generate animation only after the user approves the animation plan.
   - Use the selected animation sub-skill.
   - Render or preview-check the result with the appropriate CLI/browser workflow.
   - Record project directory, render path, QA notes, and sub-skill usage.
   - Run audit stage `animation-generated`.

6. **Cover Interview And Plan**
   - Start the cover Q&A loop while the user edits video if appropriate.
   - Ask one focused question at a time and collect素材、标题偏好、人设、禁忌、参考风格.
   - Use `atutun-xhs-cover-v2`.
   - Before generation, present a cover plan:
     - 主标题/副标题
     - 3:4 first-pass composition
     -人物/产品/素材使用方式
     - color, stickers, arrows, checklist elements
     - typography and hierarchy
     - variants to generate
   - Ask whether to generate the cover. Wait for approval.
   - Save the plan and run audit stage `cover-plan`.

7. **Cover Generation**
   - Generate cover only after the user approves the cover plan.
   - Default first output is 3:4. Expand to 4:3 or 16:9 only after the 3:4 direction is accepted or the user asks.
   - Record prompt, output path, QA notes, and sub-skill usage.
   - Run audit stage `cover-generated`.

8. **Final Package**
   - Collect final video, animation render, cover, titles, note content, tags, and publish checklist.
   - Run audit stage `final`.
   - If audit fails, fix the missing stage artifacts before saying the episode is complete.

## Quality Gates

Read `references/stage-rubrics.md` before evaluating a stage output. Read `references/known-failures.md` whenever an audit fails or before final delivery.

Hard gates:

- No Lingzao stage completion without all nine content-package fields.
- No animation generation before an approved animation plan.
- No cover generation before an approved cover plan.
- No final completion without passing `scripts/audit_episode.py`.
- No fabricated素材 paths, web sources, render files, or user confirmations.

## GitHub Sharing Hygiene

Keep this skill shareable:

- Do not commit episode media, renders, private drafts, API keys, cookies, or `.env` files.
- Keep reusable instructions in `SKILL.md` and `references/`.
- Keep deterministic checks in `scripts/`.
- Keep only generic templates in `assets/`.
