# ⚡️ OpenClaw Token Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OS: Windows | macOS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS-blue)](#-installation-and-usage)
[![API: Anthropic / OpenAI](https://img.shields.io/badge/API-Anthropic%20%7C%20OpenAI-success)](#)

**OpenClaw Token Optimizer** is an open-source local skills patcher for the autonomous AI agent **OpenClaw**. 

This tool solves the main problem of active agent usage — the exponential growth of token costs and context window overflow. We rewrote the basic skill schemas and the agent's system prompts, introducing native support for **Prompt Caching** and dynamic tool loading based on **MCP (Model Context Protocol)**. This reduces API costs (Claude / OpenAI) by **up to 90%** without losing autonomy.

⚠️ **Important:** This is NOT a proxy server and NOT a background process. The utility is a lightweight executable that updates the configuration and TypeScript/Python skill files in your OpenClaw directory just once, and then exits. Total privacy and zero overhead.

---

## ⚙️ Optimization Architecture

Standard out-of-the-box OpenClaw sends a monolithic context to the LLM. We solve this problem at the payload generation level for the API.

### 1. 🧠 Native Prompt Caching (Context Caching)

We modified OpenClaw's prompt generator to support modern provider caching mechanisms:

* **For Anthropic API (Claude):** System prompts and large attachments (e.g., source code or logs) are integrated with `{"cache_control": {"type": "ephemeral"}}` markers. We structure the requests so that the static context is always at the beginning of the `messages` array, allowing the Claude API to cache it on its side (cache lifetime is 5 minutes). You only pay for `cache_read` tokens, which is 90% cheaper than the base rate.
* **For OpenAI API (GPT-4o / o-series):** The patcher optimizes the message structure for the *Prefix Caching* algorithm. We strictly fix the order of system instructions and loaded RAG documents (prefix > 1024 tokens) so that with each subsequent agent step, OpenAI automatically applies a discount on cached input tokens.

### 2. 🛠 Dynamic Tool Search (Lazy Loading via MCP)

Vanilla OpenClaw uses static injection: JSON schemas of *all* 50+ available tools are passed in the `tools` array with every request. This wastes thousands of tokens.

We introduced the "Tool Discovery" pattern, compatible with the Model Context Protocol logic:
1. Only **one** meta-tool remains in the base `tools` array for the LLM: `search_available_tools(query: string)`.
2. When the agent needs to perform a specific task (e.g., parse the DOM), it calls `search_available_tools("web parsing")`.
3. The local handler returns the exact schema of the required tool (e.g., `read_dom_tree`).
4. In the next generation step, the agent gets access to the requested tool and executes it.

*Result: The context window remains clean. Tools are loaded into the context (and billed) strictly on demand (Lazy Loading).*

---

## 🚀 Installation and Usage

The utility works on a "download, patch, forget" principle.

1. Go to the [Releases](../../releases) section.
2. Download the executable file for your OS:
   * **Windows:** `OpenClaw_Optimizer_x64.exe`
   * **macOS:** `OpenClaw_Optimizer_macOS.dmg` (ARM)
3. Terminate the OpenClaw process if it is running.
4. Run the updater. It will automatically find the standard installation directory:
   * *Windows:* `%LOCALAPPDATA%\OpenClaw\skills`
   * *macOS:* `~/.config/openclaw/skills` (or `~/.openclaw`)
5. Click **"Patch & Optimize"**. 
6. Launch OpenClaw. The agent will automatically start using the optimized architecture.

---

## 🔍 Security and Update Process

For full transparency, here is what the patcher does upon launch:
1. Creates a ZIP archive of your current `skills` folder in `skills_backup_[timestamp].zip`.
2. Replaces `system_prompt.md` with a version that supports caching.
3. Injects a Tool Registry layer into the `tools/` directory, replacing static calls with dynamic ones.
4. Modifies the agent's `.env` file (e.g., enables necessary `anthropic-version` headers).

The source code of the update logic is fully open in the `/src` directory of this repository.

---

## 🛡 License

MIT License. Feel free to use, modify, and integrate it into your OpenClaw forks.
