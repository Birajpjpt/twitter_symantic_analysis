FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libsvm-tools

# We copy just the requirements.txt first to leverage Docker cache
RUN mkdir /twitter_symantic_analysis
COPY ./requirements.txt /twitter_symantic_analysis/requirements.txt

WORKDIR /twitter_symantic_analysis

RUN pip install -r requirements.txt



COPY ./ /twitter_symantic_analysis/
RUN cd /twitter_symantic_analysis
RUN

ENTRYPOINT [ "python" ]
CMD [ "/twitter_symantic_analysis/Analyser/App_Run.py" ]

