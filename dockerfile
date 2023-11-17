WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /usr/src/modules/logs
CMD ["python3", "rest_api.py", "--host", "0.0.0.0", "--port", "5050"]
