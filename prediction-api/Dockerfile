FROM python:3.10.7-slim
WORKDIR /usr/src/myapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV MODEL_REPO=/usr/src/myapp
CMD ["python3", "app.py"]
