FROM alpine:latest

RUN apk add  \
    python3 \
    py-pip \
    vim

RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.7 /usr/bin/python3
RUN pip3 install pytest numpy

RUN mkdir /apps
COPY /main.py /apps/main.py

WORKDIR /apps
ENTRYPOINT ["python", "main.py"]
