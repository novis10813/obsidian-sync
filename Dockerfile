# 使用 Python 3.13 slim 版本作為基礎映像
FROM python:3.13-slim

# 設置標籤資訊（適合 DockerHub）
LABEL maintainer="zhizhongz895253@gmail.com"
LABEL description="Obsidian Sync API Service"
LABEL version="1.0.0"

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安裝 uv
RUN pip install --no-cache-dir uv

# 複製依賴檔案
COPY pyproject.toml uv.lock ./

# 安裝 Python 依賴
RUN uv sync --no-dev

# 複製應用程式程式碼
COPY app/ ./app/

# 建立必要的目錄
RUN mkdir -p /app/content /app/static

# 設置環境變數
ENV OBSIDIAN_SYNC_HOST=0.0.0.0
ENV OBSIDIAN_SYNC_PORT=1312
ENV OBSIDIAN_SYNC_LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 1312

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:${OBSIDIAN_SYNC_PORT:-1312}/health || exit 1

# 啟動命令
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1312"]
