FROM python:3.11

WORKDIR /opt/mojang2rss

COPY mojang2rss.py requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["uvicorn"]
CMD ["mojang2rss:app", "--host", "0.0.0.0", "--port", "80"]
