from centos:centos6

RUN yum -y update && \
    yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && \
    yum -y install wget unzip autoconf automake make gcc gcc-c++ libtool-devel libtool && \
    yum -y install libtool-ltdl-devel libtool-ltdl file glib2 glib2-devel doxygen && \
    yum -y install texlive-latex texlive texlive-dvips graphviz which fcgi fcgi-devel && \
    yum -y install mod_fcgid spawn-fcgi && \
    wget -O /srv/foo.zip 'https://jenkins.emsl.pnl.gov/view/HPSS%20Software/job/hpss-client-7.4.1p2/DIST=epel-6-x86_64,label=el6/lastSuccessfulBuild/artifact/*zip*/archive.zip' && \
    cd /srv && \
    unzip foo.zip && \
    yum -y localinstall archive/hpss-client/output/*.x86_64.rpm && \
    yum -y clean all
RUN mkdir /app
COPY . /app
ENV PKG_CONFIG_PATH /opt/hpss/lib/pkgconfig
RUN cd /app && \
    touch * && \
    bash -xe autogen.sh && \
    ./configure --enable-doxygen-dot --enable-doxygen-man --disable-doxygen-html --disable-doxygen-pdf && \
    make && \
    make check
