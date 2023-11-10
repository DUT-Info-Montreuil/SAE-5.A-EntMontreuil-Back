FROM python:3.8
COPY . /SAE-5.A-EntMonreuil-Back
WORKDIR /SAE-5.A-EntMonreuil-Back
RUN pip install -r requirements.txt
RUN mkdir -p /usr/src/modules/logs
CMD ["python3", "rest_api.py", "--host", "0.0.0.0", "--port", "5050"]