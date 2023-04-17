FROM python
RUN pip install requests

COPY bilibili.py /app/

RUN python /app/bilibili.py