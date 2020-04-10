# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM youshumin/python:2.7

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=cute_cmdb Version=0.0.1
EXPOSE 3000

WORKDIR /work_app
ADD . /work_app


# Using pip:
# RUN python3 -m pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple \
    && apk add --no-cache --virtual .install-deps git \
    && git clone https://github.com/cuteboy9201/oslo.git \
    && apk  del .install-deps \
    && cd oslo && python setup.py install && cd .. && rm -rf oslo && pip list
CMD ["python", "run_server.py"]

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "cute_cmdb"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m cute_cmdb"
