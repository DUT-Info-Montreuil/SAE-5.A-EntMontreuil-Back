FROM python:3.9
WORKDIR /app
EXPOSE 5050
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /usr/src/modules/logs
ENTRYPOINT [ "python3" ]
CMD ["rest_api.py"]
