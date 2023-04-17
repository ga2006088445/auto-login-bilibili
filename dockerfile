FROM python
RUN pip install requests

COPY bilibili.py /app/

CMD ["python", "/app/bilibili.py"]