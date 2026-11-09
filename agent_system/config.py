"""Configuration for the hybrid agent system (local Llama3 via Ollama)."""
import os

# Ollama (OpenAI-compatible) endpoint
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
# OpenAI-compatible v1 endpoint
OLLAMA_V1_URL = f"{OLLAMA_BASE_URL.rstrip('/')}/v1"

# LLM sampling
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# SQLite checkpointer path
CHECKPOINT_DB = os.getenv("CHECKPOINT_DB", "/home/sam/代理人/agent_checkpoints.sqlite")

# Guardrail thresholds (from skill.md)
TARGET_ZO = float(os.getenv("TARGET_ZO", "50.0"))
ZO_TOL = float(os.getenv("ZO_TOL", "1.0"))
MIN_THICKNESS_MIL = float(os.getenv("MIN_THICKNESS_MIL", "4.0"))

# Optimization limits
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
SOLUTION_POOL_TARGET = int(os.getenv("SOLUTION_POOL_TARGET", "3"))