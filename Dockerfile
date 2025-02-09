# 使用官方 Python 運行時作為父鏡像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 暴露端口
EXPOSE 8080

# 運行應用
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app 