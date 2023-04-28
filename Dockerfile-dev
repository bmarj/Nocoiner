# mssql-python3.6-pyodbc
FROM ubuntu:20.04
# apt-get and system utilities
# RUN apt-get update && apt-get install -y \
#     curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5\
#     && rm -rf /var/lib/apt/lists/*
# # adding custom MS repository
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && apt-get install -y curl apt-utils apt-transport-https debconf-utils gcc build-essential
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# # install libssl - required for sqlcmd to work on Ubuntu 18.04
RUN apt-get update && apt-get install -y libssl1.1 libssl-dev
# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
# install SQL Server tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"
# python libraries
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev python3-setuptools \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# # install necessary locales
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen
RUN pip3 install --upgrade pip
# # install SQL Server Python SQL Server connector module - pyodbc
RUN pip3 install pyodbc
# RUN pip3 install setuptools
# RUN pip3 install imutils
# RUN pip3 install flask_restful
# RUN pip3 install flask_sqlalchemy
# RUN pip3 install numpy
# RUN pip3 install flask_httpauth
# RUN pip3 install Flask-JWT
# RUN pip3 install flask_babel
# RUN pip3 install werkzeug
# RUN pip3 install requests
# RUN pip3 install flask_cors
# RUN pip3 install urllib3
# RUN pip3 install bs4
# RUN pip3 install flask_jwt_extended
# RUN pip3 install python-csv
# RUN pip3 install uuid
# RUN pip3 install scipy
# RUN pip3 install flask_httpauth
# RUN pip3 install colorgram.py
# RUN pip3 install opencv-python
# RUN pip3 install pillow
# RUN pip3 install colorthief
# install additional utilities

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN TZ="America/New_York" apt-get update && apt-get install gettext nano vim -y 
# add sample code
RUN mkdir /web
ADD . /web
WORKDIR /web

COPY . /web

RUN pip3 install -r requirements.txt

EXPOSE 8000
ENV FLASK_ENV=production
# ENTRYPOINT ["python3"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "app:application"]