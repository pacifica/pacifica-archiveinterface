from centos:centos6

RUN yum -y update && \
    yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
    yum -y install python-wsgi python-pip wget curl unzip gcc glibc-devel python-devel python-argparse && \
    yum -y clean all
RUN mkdir /app
COPY . /app
RUN chmod +x /app/runit.sh
WORKDIR /app
RUN python ./setup_nohpss.py install
ENV PACIFICA_AAPI_BACKEND_TYPE posix
ENV PACIFICA_AAPI_ADDRESS 0.0.0.0
ENV PACIFICA_AAPI_PORT 8080
ENV PACIFICA_AAPI_PREFIX /srv
EXPOSE 8080
CMD '/app/runit.sh'
