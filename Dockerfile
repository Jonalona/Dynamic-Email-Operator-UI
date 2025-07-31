FROM python:3.12
#used to be 3.9 July 22, 2025
RUN apt-get update && apt-get install -y \
    sudo \
    pandoc \
    # pandoc-citeproc \
    libcurl4-gnutls-dev \
    libcairo2-dev \
    libxt-dev \
    libssl-dev \
    libssh2-1-dev \
    # libssl1.1 \
    curl \
    libv8-dev \
    unixodbc \
    unixodbc-dev \ 
    freetds-dev \
    freetds-bin \
    tdsodbc

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \ 
    apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql17 


COPY requirements.txt /
RUN pip install  --no-cache-dir -r /requirements.txt

ENV ODBCSYSINI /ODBCCONFIG
RUN mkdir /ODBCCONFIG
COPY odbcinst.ini /ODBCCONFIG
EXPOSE 9093

WORKDIR /root/app/


# Copy app directory into the container
COPY app/ .

# Run DB initialization then start the app
CMD ["sh", "-c", "python init.py && python app.py"]
