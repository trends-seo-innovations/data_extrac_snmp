FROM python:3.7
 
WORKDIR /srv
ADD . .
#for pymssql
RUN pip install --upgrade pip
 
# RUN sh installodbc.sh
# ADD odbcinst.ini /etc/odbcinst.ini
# for pyodbc
RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y
 
# populate "ocbcinst.ini"
RUN echo "[FreeTDS]\n\
    Description = FreeTDS unixODBC Driver\n\
    Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
    Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini
 
# install pyodbc (and, optionally, sqlalchemy)
RUN pip install --trusted-host pypi.python.org pyodbc==4.0.26 sqlalchemy==1.3.5
 
# RUN wget https://gallery.technet.microsoft.com/ODBC-Driver-13-for-Ubuntu-b87369f0/file/154097/2/installodbc.sh
# RUN apt-get update
# RUN apt-get install -y tdsodbc unixodbc-dev
# RUN apt install libssl1.0.0 libssl-dev
# RUN apt install unixodbc-bin -y
# RUN apt-get clean -y
 
# Add ./requirements.txt ./requirements.txt
 
# RUN python3 -m pip install -r requirements.txt
 
RUN pip install Flask==1.1.1
RUN pip install Flask-Cors==3.0.8
RUN pip install Flask-JWT==0.3.2
RUN pip install Flask-JWT-Extended==3.20.0
RUN pip install flask-marshmallow==0.10.1
RUN pip install Flask-RESTful==0.3.7
RUN pip install Flask-SQLAlchemy==2.4.0
RUN pip install marshmallow==3.0.0rc8
RUN pip install PyJWT==1.7.1
RUN pip install pyodbc
RUN pip install pyOpenSSL==19.0.0
RUN pip install scapy==2.4.3
RUN pip install pysnmp==4.4.12
RUN pip install requests==2.22.0
RUN pip install datetime==4.3
RUN pip install psutil==5.6.3
RUN pip install jinjasql==0.1.7
RUN pip install pymssql==2.1.4
 
ENV DB_CONN localhost
ENV DB_PORT 1433
ENV DB_PASSWORD p@ssw0rd
ENV DB_NAME source_extractor_engine
ENV DB_USER sa
ENV API_PORT 4044
 
EXPOSE 4044 
ADD . /srv
 
ENTRYPOINT [ "python" ] 
CMD [ "/srv/pollerapi.py" ]