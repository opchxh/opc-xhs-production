# Known Failures

Use this file as a preflight checklist before final delivery and whenever an audit fails.

## Process Failures

- Starting rewriting before reading the plan MD.
- Treating 口播规划 as the whole plan and ignoring 笔记规划.
- Skipping `lingzao` and doing ordinary rewriting.
- Forgetting Lingzao must also output poster titles and note-package fields.
- Inventing uploaded file paths or claiming files were received when they were not.
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
- Adding web素材 without source URLs or licensing assumptions.
- No scene timing, subtitle strategy, or render QA plan.
- Render is blank, incorrectly framed, or not checked.
- Text or subtitles overflow mobile safe areas.

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
