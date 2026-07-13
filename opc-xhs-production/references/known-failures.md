# Known Failures

Use this file as a preflight checklist before final delivery and whenever an audit fails.

## Process Failures

- Starting rewriting before reading the plan MD.
- Assuming a publishing-plan MD is required when the user only wants Lingzao to handle topic and script work.
- Treating 口播规划 as the whole plan and ignoring 笔记规划.
- Skipping `lingzao` and doing ordinary rewriting.
- Asking the user to do选题、脚本、口播改写 manually instead of routing that work to `lingzao`.
- Forgetting Lingzao must also output poster titles and note-package fields.
- Inventing uploaded file paths or claiming files were received when they were not.
- Asking for all素材 at once instead of audio first, video second, auxiliary素材 third.
- Asking the user to record a full真人口播 video when only开头出镜、强调观点、总结收口 clips are needed.
- Generating animation before the user approves the animation plan.
- Generating cover before the user approves the cover plan.
- Saying "done" without running the audit script.

## Voiceover Failures

- Script is too written, too abstract, or not speakable.
- No opening hook in the first seconds.
- No recording guidance for tone, pause, expression, or shot.
- The revised script drifts away from the original topic.

## Animation Failures

- Choosing Remotion or HyperFrames without explaining why.
- Ignoring OPC 碎碎念探长标准剪辑风格 when the user has not provided a new style reference.
- Making the video all motion graphics or all真人 footage instead of mixing真人、动效、截图/B-roll according to the standard style.
- Adding web素材 without source URLs or licensing assumptions.
- No scene timing, subtitle strategy, or render QA plan.
- Render is blank, incorrectly framed, or not checked.
- Text or subtitles overflow mobile safe areas.
- Not inspecting representative still frames for alignment, overflow, and crowded graphics.

## Cover Failures

- Not doing the Q&A loop.
- Not using `atutun-xhs-cover-v2`.
- Generating before presenting the cover plan.
- First output is not 3:4.
- Main title is too small, low-contrast, or buried.
- Too many unrelated decorative elements.

## GitHub Sharing Failures

- Committing real episode media, private drafts, API keys, cookies, or `.env`.
- Making the skill depend on absolute local paths.
- Putting reusable process knowledge only in a chat instead of `SKILL.md` or `references/`.
