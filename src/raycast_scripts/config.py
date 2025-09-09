"""Configuration management for Raycast scripts."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI settings
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    model: str = Field(default="gpt-4o-mini", description="OpenAI model to use")

    # Ollama settings
    ollama_model: str = Field(default="llama3.1:latest", description="Ollama model to use")
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")

    # JIRA settings
    jira_server: Optional[str] = Field(default=None, description="JIRA server URL")
    jira_email: Optional[str] = Field(default=None, description="JIRA email")
    jira_api_token: Optional[str] = Field(default=None, description="JIRA API token")

    # Application settings
    log_level: str = Field(default="INFO", description="Logging level")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".cache" / "raycast-scripts")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout: int = Field(default=30, description="Request timeout in seconds")

    def __init__(self, **kwargs) -> None:
        """Initialize settings with cache directory creation."""
        super().__init__(**kwargs)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def has_openai_config(self) -> bool:
        """Check if OpenAI configuration is available."""
        return self.openai_api_key is not None

    @property
    def has_jira_config(self) -> bool:
        """Check if JIRA configuration is available."""
        return all([self.jira_server, self.jira_email, self.jira_api_token])

    @property
    def has_ollama_config(self) -> bool:
        """Check if Ollama configuration is available."""
        return self.ollama_base_url is not None


# Global settings instance
settings = Settings()