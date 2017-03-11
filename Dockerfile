from centos:centos6

RUN yum -y update && \
    yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
    yum -y install MySQL-python && \
    yum -y install python-wsgi python-pip wget curl unzip gcc glibc-devel python-devel python-argparse && \
    yum -y clean all
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN python ./setup.py install
ENV PACIFICA_AAPI_BACKEND_TYPE posix
ENV PACIFICA_AAPI_ADDRESS 0.0.0.0
ENV PACIFICA_AAPI_PORT 8080
ENV PACIFICA_AAPI_PREFIX /srv
EXPOSE 8080
ENTRYPOINT [ "/bin/bash", "/app/entrypoint.sh" ]
