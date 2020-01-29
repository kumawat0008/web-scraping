FROM ubuntu:16.04
FROM python:3.6


RUN pip install html5lib boto3 bs4 pandas requests fastparquet s3fs

RUN mkdir ~/src
ADD . ~/src
WORKDIR ~/src
CMD ["python", "main.py"]