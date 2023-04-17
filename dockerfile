FROM python:3.10
RUN pip install requests

COPY bilibili.py /app/

CMD ["python", "/app/bilibili.py"]