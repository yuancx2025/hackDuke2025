FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg libsox-dev libsox-fmt-all libsndfile1 libgl1 libglib2.0-0 libgomp1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制你的代码到容器
COPY . .

# 暴露端口
EXPOSE 8000

# 以生产方式启动 FastAPI 应用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]