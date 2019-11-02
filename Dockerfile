FROM ubuntu:latest

RUN apt-get update && apt-get install -y  \
    python3.7 \
    python3-pip \
#    vim

RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.7 /usr/bin/python3
RUN pip3 install pytest numpy

RUN mkdir /apps
COPY /pure_python_implementation.py /apps/pure_python_implementation.py                                                               
COPY /numpy_implementation.py /apps/numpy_implementation.py 

#RUN echo "set expandtab tabstop=4 softtabstop=4 shiftwidth=4" > ~/.vimrc
WORKDIR /apps
ENTRYPOINT ["python3", "main.py"]
