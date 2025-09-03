# Pin to a stable Debian to avoid base-image surprises
FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    sudo \
    pandoc \
    libcurl4-gnutls-dev \
    libcairo2-dev \
    libxt-dev \
    libssl-dev \
    libssh2-1-dev \
    curl \
    libv8-dev \
    unixodbc \
    unixodbc-dev \
    freetds-dev \
    freetds-bin \
    tdsodbc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

ENV ODBCSYSINI=/ODBCCONFIG
RUN mkdir /ODBCCONFIG
COPY odbcinst.ini /ODBCCONFIG

EXPOSE 9093
WORKDIR /root/app/
COPY app/ .

CMD ["sh", "-c", "python init_db.py && python app.py"]
