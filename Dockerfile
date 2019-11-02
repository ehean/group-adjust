FROM ubuntu:latest

RUN apt-get update && apt-get install -y  \
    python3.7 \
    python3-pip \
#    vim

RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.7 /usr/bin/python3
RUN pip3 install pytest numpy

RUN mkdir /apps
COPY /main.py /apps/main.py

#RUN echo "set expandtab tabstop=4 softtabstop=4 shiftwidth=4" > ~/.vimrc
WORKDIR /apps
ENTRYPOINT ["python3", "main.py"]
