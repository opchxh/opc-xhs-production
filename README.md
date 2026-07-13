# OPC 碎碎念探长小红书 Skill

这是一个给 Codex 使用的小红书内容生产流程 Skill。它把一条内容从发布计划 MD，推进到口播稿、拍摄提示、动效方案、封面方案、笔记正文、标签和最终发布包。

## 能做什么

- 读取包含口播规划和笔记规划的发布计划 MD。
- 调用灵造 Skill 分析原口播问题，并生成新版口播稿。
- 输出录制/拍摄提示、海报主标题/副标题、笔记主标题/副标题、笔记正文和标签。
- 等待真实录音或口播视频素材，不编造文件路径或素材信息。
- 在生成动效前先给出动效方案，并等待用户确认。
- 根据场景选择 Remotion 或 HyperFrames 制作动效。
- 做封面前持续问答收集素材，再给出封面方案，并等待用户确认。
- 默认先生成 3:4 小红书封面。
- 用自检脚本检查阶段产物，避免跳步骤、漏文件、乱编素材。

## 目录结构

```text
opc-xhs-production/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/audit_episode.py
  assets/episode-template/
skill-dev-tests/
requirements-dev.txt
```

## 安装

把 `opc-xhs-production/` 复制到 Codex 技能目录：

```bash
cp -R opc-xhs-production ~/.codex/skills/opc-xhs-production
```

之后可以用这句话触发：

```text
使用OPC 碎碎念探长小红书 skill
```

## 验证

创建开发环境：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

运行官方 Skill 校验：

```bash
.venv/bin/python /path/to/quick_validate.py opc-xhs-production
```

运行本仓库自带测试：

```bash
python3 -m unittest skill-dev-tests/test_audit_episode.py
python3 skill-dev-tests/run_dry_skill.py
```

## 注意

不要提交真实 episode 素材、成片、账号 cookie、API key、`.env` 文件或私人草稿。仓库里的 `.gitignore` 已经默认排除了这些常见文件。
