FROM python:3.10.7-slim
WORKDIR /usr/src/myapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV PREDICTOR_API=http://predictor-api-server:5000/phishing_predictor
LABEL prediction="0.0.1-beta"
CMD ["python3", "app.py"]
