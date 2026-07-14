# ⚡️ OpenClaw Token Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OS: Windows | macOS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS-blue)](#-installation-and-usage)
[![API: Anthropic / OpenAI](https://img.shields.io/badge/API-Anthropic%20%7C%20OpenAI-success)](#)

**OpenClaw Token Optimizer** 是一个开源的本地技能补丁程序，专为自主 AI 代理 **OpenClaw** 设计。

该工具解决了代理在活跃使用中的主要问题——令牌 (Token) 成本的指数级增长和上下文窗口溢出。我们重写了基础技能模式和代理的系统提示，引入了对 **提示缓存 (Prompt Caching)** 和基于 **MCP (模型上下文协议)** 的动态工具加载的原生支持。这使 API 成本 (Claude / OpenAI) 降低了 **高达 90%**，同时不会损失自主性。

⚠️ **重要提示：** 这不是代理服务器，也不是后台进程。该实用程序是一个轻量级的可执行文件，只需运行一次即可更新您的 OpenClaw 目录中的配置和 TypeScript/Python 技能文件，然后就会退出。完全保护隐私，零系统开销。

---

## ⚙️ 优化架构

标准的开箱即用的 OpenClaw 会向 LLM 发送一个庞大的单一上下文。我们在 API 负载生成层面解决了这个问题。

### 1. 🧠 原生提示缓存 (上下文缓存)

我们修改了 OpenClaw 的提示生成器以支持现代提供商的缓存机制：

* **对于 Anthropic API (Claude)：** 系统提示和大型附件（如源代码或日志）与 `{"cache_control": {"type": "ephemeral"}}` 标记集成在一起。我们对请求进行了结构化处理，使静态上下文始终处于 `messages` 数组的开头，从而允许 Claude API 在其服务器端对其进行缓存（缓存生命周期为 5 分钟）。您只需支付 `cache_read` 令牌的费用，比基准费率便宜 90%。
* **对于 OpenAI API (GPT-4o / o系列)：** 补丁程序针对*前缀缓存 (Prefix Caching)* 算法优化了消息结构。我们严格固定了系统指令和加载的 RAG 文档（前缀 > 1024 个令牌）的顺序，以便在代理的每一个后续步骤中，OpenAI 都会自动对缓存的输入令牌应用折扣。

### 2. 🛠 动态工具搜索 (通过 MCP 进行延迟加载)

原始的 OpenClaw 使用静态注入：将*所有* 50 多个可用工具的 JSON 模式包含在每次请求的 `tools` 数组中传递。这浪费了数以千计的令牌。

我们引入了与模型上下文协议 (Model Context Protocol) 逻辑兼容的“工具发现 (Tool Discovery)”模式：

1. 基础的 `tools` 数组中只保留 **一个** 供 LLM 使用的元工具：`search_available_tools(query: string)`。
2. 当代理需要执行特定任务（例如解析 DOM）时，它会调用 `search_available_tools("web parsing")`。
3. 本地处理程序返回所需工具的确切模式（例如，`read_dom_tree`）。
4. 在下一个生成步骤中，代理将获得所请求工具的访问权限并执行它。

*结果：上下文窗口保持整洁。工具仅在需要时才被加载到上下文中（并计费），实现严格的按需加载 (延迟加载)。*

---

## 🚀 安装与使用

该实用程序基于“下载、修补、忘记”的原则工作。

1. 前往 [Releases](../../releases) 部分。
2. 下载适用于您操作系统的可执行文件：
* **Windows:** `OpenClaw_Optimizer_x64.exe`
* **macOS:** `OpenClaw_Optimizer_macOS.dmg` (ARM)


3. 如果 OpenClaw 进程正在运行，请将其终止。
4. 运行更新程序。它将自动找到标准安装目录：
* *Windows:* `%LOCALAPPDATA%\OpenClaw\skills`
* *macOS:* `~/.config/openclaw/skills` (或 `~/.openclaw`)


5. 点击 **"Patch & Optimize"** (修补并优化)。
6. 启动 OpenClaw。代理将自动开始使用优化后的架构。

---

## 🔍 安全与更新流程

为了完全透明，以下是补丁程序启动时执行的操作：

1. 将您当前的 `skills` 文件夹打包成名为 `skills_backup_[timestamp].zip` 的 ZIP 压缩包进行备份。
2. 将 `system_prompt.md` 替换为支持缓存的版本。
3. 在 `tools/` 目录中注入工具注册表 (Tool Registry) 层，将静态调用替换为动态调用。
4. 修改代理的 `.env` 文件（例如，启用必要的 `anthropic-version` 请求头）。

更新逻辑的源代码完全开源，位于此存储库的 `/src` 目录中。

---

## 🛡 许可证

MIT 许可证。请随意使用、修改并将其集成到您的 OpenClaw 分支中。
