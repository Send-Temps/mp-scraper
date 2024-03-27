FROM python:3.10

ADD . mp-scraper/
WORKDIR mp-scraper/
RUN pip install -r requirements.txt
USER root

CMD ["python3", "main.py"]