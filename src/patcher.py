from pathlib import Path
import logging
from src.payloads import OPTIMIZED_SYSTEM_PROMPT, TOOL_SEARCH_SCHEMA

logger = logging.getLogger("OpenClawUpdater")

def patch_system_prompt(skills_dir: Path) -> None:
    """Overwrites the old system_prompt.md with the prompt-caching optimized version."""
    prompt_path = skills_dir / "system_prompt.md"
    prompt_path.write_text(OPTIMIZED_SYSTEM_PROMPT, encoding="utf-8")
    logger.info("🧠 System prompt patched with Cache-Control markers.")

def patch_tools(skills_dir: Path) -> None:
    """Removes monolithic tools and injects the dynamic Tool Search schema."""
    tools_dir = skills_dir / "tools"
    
    # Create tools directory if it doesn't exist
    tools_dir.mkdir(parents=True, exist_ok=True)
    
    search_tool_path = tools_dir / "search_tools.json"
    search_tool_path.write_text(TOOL_SEARCH_SCHEMA, encoding="utf-8")
    logger.info("🛠 Dynamic Tool Search injected into tools directory.")

def patch_env_file(base_dir: Path) -> None:
    """Appends necessary API headers (e.g., Anthropic beta headers) to the .env file."""
    env_path = base_dir / ".env"
    
    env_data = ""
    if env_path.exists():
        env_data = env_path.read_text(encoding="utf-8")
    
    # Append Anthropic beta header if not present
    if "ANTHROPIC_BETA" not in env_data:
        append_string = "\n# Added by OpenClaw Updater\nANTHROPIC_BETA=prompt-caching-2024-07-31\n"
        with env_path.open("a", encoding="utf-8") as f:
            f.write(append_string)
        logger.info("🌐 .env configured for optimal API requests.")
    else:
        logger.info("🌐 .env already contains necessary API headers. Skipped.")
