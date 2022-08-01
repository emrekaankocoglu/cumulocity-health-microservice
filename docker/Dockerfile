FROM python:alpine3.6

COPY . /app
WORKDIR /app
RUN pip3 install flask 
RUN pip3 install requests

ENTRYPOINT ["python3"]
CMD ["-u", "app.py"]