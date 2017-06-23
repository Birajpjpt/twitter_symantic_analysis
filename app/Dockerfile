FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python-libsvm
RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./ /app/
RUN cd /app
ENTRYPOINT [ "python", "app.py" ]