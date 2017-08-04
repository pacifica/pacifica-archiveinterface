from python:2

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi
COPY . .
RUN python ./setup.py install
ENV PAI_BACKEND_TYPE posix
ENV PAI_PREFIX /srv
ENV ARCHIVEI_CONFIG /usr/src/app/config.cfg
ENTRYPOINT [ "/bin/bash", "/usr/src/app/entrypoint.sh" ]
