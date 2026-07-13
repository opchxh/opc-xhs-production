---
name: opc-xhs-production
description: Use when producing OPC 碎碎念探长小红书 content or short-video episodes end to end, including topic ideation, voiceover/script planning through lingzao, recording intake, Remotion/HyperFrames animation, editing-style planning, 小红书 cover, note package, and final delivery. Trigger when the user says "使用OPC 碎碎念探长小红书 skill", "OPC 碎碎念探长标准剪辑风格", or mentions 小红书选题、口播规划、笔记规划、灵造、录音、真人视频、辅助素材、Remotion、HyperFrames、动效、成片、封面.
---

# OPC XHS Production

## Overview

Coordinate one 小红书/short-video episode from topic direction or publishing-plan MD to voiceover, recording, edit-ready animation, cover, note package, and final delivery package. This is an orchestration skill: use the required sub-skills at the correct stage, preserve approvals, and run the audit script before claiming a stage is complete.

## Required Sub-Skills

- **REQUIRED SUB-SKILL:** Use `lingzao` for topic ideation, plan analysis, voiceover/script creation or rewriting, recording guidance, poster-title ideas, and note-package generation.
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

## Standard Editing Style

Default to **OPC 碎碎念探长标准剪辑风格** unless the user provides a new finished reference video and asks to change style.

Style rules:

- Use真人画面 to establish trust and emphasize key观点, not as the whole video.
- Ask the user to record only: (a) 开头出镜, (b) 强调观点的地方, (c) 总结收口.
- Use motion graphics for concept explanation, structure, comparisons, cases, and key takeaways.
- Use screenshots, screen recordings, photos, web references, or B-roll as proof/context layers when useful.
- Keep the default ratio around真人 25-40%, 动效 40-55%, 截图/B-roll/辅助素材 10-25%, then adapt to available素材.
- Use clear chapter progress, large section titles, bottom key-line subtitles, and restrained full-sentence captions.
- Maintain strict 1080x1920 safe-area layout. Inspect representative frames for text overflow, bad alignment, and graphic crowding.
- Default render target for intermediate delivery is 1080x1920, 30fps, high-bitrate MP4/H.264 with AAC audio when recorded audio exists. Do not default to transparent MOV.

## Workflow

1. **Intake**
   - Accept either a publishing-plan MD or a loose topic direction.
   - If a publishing-plan MD is provided, read it and check whether it contains 口播规划 and 笔记规划.
   - If no publishing-plan MD is provided, create an intake brief from the user's topic, audience, constraints, and any account context. Ask only blocking questions.
   - Do not make the user perform topic or script work manually; route that work into the Lingzao stage.
   - Run audit stage `intake`.

2. **Lingzao Content Package**
   - Call `lingzao`.
   - Produce this exact package:
     - 选题方向与切入角度
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
   - Ask for素材 in this exact order, one category at a time:
     1. Ask how many audio recordings there are and request the audio files.
     2. After audio files are received, ask how many video clips there are and request the video files.
     3. After video files are received, ask how many auxiliary素材 items there are and request them.
   - For video recording guidance, request only: 开头出镜, 强调观点, 总结收口. Do not ask the user to record the whole口播 unless they explicitly want that.
   - Do not invent file paths, durations, transcripts, or camera details.
   - Register received files by category in `audio_assets`, `video_assets`, and `auxiliary_assets`; also keep `recording_assets` as the combined list for audit compatibility.
   - Run audit stage `recording`.

4. **Animation Plan Before Generation**
   - Inspect the uploaded audio, video, and auxiliary素材.
   - If useful, search the web for high-quality visual references or supplement material. Record source URLs, licensing assumptions, and planned use in the animation brief.
   - Choose Remotion or HyperFrames based on the requested effect, asset type, and rendering needs.
   - Present an animation plan before generating:
     - goal and viewer feeling
     - tool choice and reason
     - scene structure and timing
     - asset list, including user assets and web-sourced candidates
     - how the OPC 碎碎念探长标准剪辑风格 will be applied
     - subtitle/text strategy
     - render and QA plan
   - Ask whether to generate the animation. Wait for approval.
   - Save the plan and run audit stage `animation-plan`.

5. **Animation Generation**
   - Generate animation only after the user approves the animation plan.
   - Use the selected animation sub-skill.
   - When真人 clips are provided, edit them into the planned places according to the standard style instead of leaving all真人 placement to the user.
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

- No Lingzao stage completion without all ten content-package fields.
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
