# Claude Code + DeepSeek 隔离方案

目标：普通模式开发可以借用 Claude Code CLI 的工程外壳，但模型请求只走 DeepSeek，且不污染当前 Claude Code/Opus 研究环境。

## 官方核实

- DeepSeek 官方 Claude Code 接入方式：`ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic`，`ANTHROPIC_AUTH_TOKEN=$DEEPSEEK_API_KEY`，主模型示例为 `deepseek-v4-pro[1m]`，并可设置 `CLAUDE_CODE_EFFORT_LEVEL=max`。
- Claude Code 官方环境变量说明：用户配置默认在 `$HOME/.claude`、`~/.claude.json`，项目配置在 `.claude/settings.json`，并支持 `ANTHROPIC_MODEL`、`ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`、`CLAUDE_CODE_SUBAGENT_MODEL` 等变量。

参考：

- <https://api-docs.deepseek.com/guides/agent_integrations/claude_code>
- <https://docs.anthropic.com/en/docs/claude-code/settings>
- <https://code.claude.com/docs/en/env-vars>

## 当前状态

- 脚本已创建：`scripts/launch_claude_code_deepseek_isolated.ps1`
- 2026-05-09 干跑已通过：未启动 Claude Code，只生成隔离目录和报告。
- 干跑报告：`runtime_data/claude_deepseek_isolation/deepseek_cc_isolation_dryrun_20260509_202144.json`
- 当前 PowerShell 环境里没有找到 `claude` 命令。
- 当前 PowerShell 环境里没有暴露 `DEEPSEEK_API_KEY`。
- 因此真实启动仍被阻断，这是预期的安全行为。

## 隔离原则

| 风险 | 对策 |
| --- | --- |
| 复用 Claude/Opus 登录态 | 启动子进程前清空 `ANTHROPIC_API_KEY`、`ANTHROPIC_CUSTOM_HEADERS`、`CLAUDE_CODE_OAUTH_TOKEN` 等变量。 |
| 写入默认 Claude Code 用户目录 | 子进程内把 `HOME`、`USERPROFILE`、`APPDATA`、`LOCALAPPDATA`、`TEMP`、`TMP` 全部指到 `E:\AI_Tools\claude-code-deepseek-isolated` 下。 |
| 普通模式高危数据进入 Opus/Claude 账号 | 只设置 DeepSeek 的 Anthropic-compatible endpoint 和 token，不登录 Claude/Opus。 |
| 读取旧 Claude Code 记忆 | 默认设置 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` 和 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`；隔离目录内另写 deny 规则阻止读取原用户 `.claude`、`.claude.json`。 |
| 自动安装、遥测、外部副作用 | 默认关闭非必要流量、自动安装、policy skills、cron、IDE 自动连接、遥测、错误上报。 |
| 普通模式代码污染主工作树 | 推荐给普通模式建独立 worktree 或副本目录；Codex 最后只接收格式校验后的资产和管线文件。 |

## 使用方式

先只干跑：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\launch_claude_code_deepseek_isolated.ps1
```

准备真实启动前需要两件事：

```powershell
$env:DEEPSEEK_API_KEY = "sk-..."
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\launch_claude_code_deepseek_isolated.ps1 `
  -ClaudeCommand "完整的 claude.exe 或 claude.cmd 路径" `
  -Workspace "E:\AI_Projects\xiya-normal-worktree" `
  -IsolatedRoot "E:\AI_Tools\cc-deepseek-normal"
```

确认 dry-run 输出无误后，才加 `-Launch`：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\launch_claude_code_deepseek_isolated.ps1 `
  -ClaudeCommand "完整的 claude.exe 或 claude.cmd 路径" `
  -Workspace "E:\AI_Projects\xiya-normal-worktree" `
  -IsolatedRoot "E:\AI_Tools\cc-deepseek-normal" `
  -Launch
```

默认模型：

| 用途 | 模型 |
| --- | --- |
| 主模型/Opus/Sonnet 映射 | `deepseek-v4-pro[1m]` |
| 子代理/小模型 | `deepseek-v4-flash` |
| effort | `max` |

## 推荐工作流

1. 普通模式建独立 worktree 或目录副本。
2. SFW 侧继续由 Codex 负责完整管线、资产、验收、Discord 实测。
3. 普通模式侧由隔离 Claude Code + DeepSeek 写内容，例如 normal lore、play 条目、NAI normal tag、道具/全局模式映射。
4. Codex 只把普通模式输出当资产包接收，负责格式校验、接线、最小必要验收。
5. 如果隔离实例仍读取或写入默认 Claude Code 配置目录，立即停用，改虚拟机或独立 Windows 用户。

## 不能做

- 不在普通模式任务里登录 Claude/Opus。
- 不把普通模式高危资产放进当前 Claude Code/Opus 研究项目目录。
- 不让第三方 router 保存通用密钥，除非之后确实需要多模型路由且已单独审计配置文件路径。
