FROM ubuntu:24.04

# Install Python and build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY bot/ ./bot/

# Install uv package manager using the official installer
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies and build executable
RUN uv sync && uvx pyinstaller --onefile bot/python/bot.py

# The executable will be in dist/bot
CMD ["ls", "-la", "dist/"]