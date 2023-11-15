FROM python:slim
COPY app /app
WORKDIR /app
RUN apt-get update && \
    apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 CMD curl -f http://localhost:5000/health || exit 1