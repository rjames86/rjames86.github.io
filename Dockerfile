FROM python:3.8.0-alpine

RUN apk update && apk add \
	bash \
	git \
	git-fast-import \
	make \
	openssh \ 
    gcc \ 
    linux-headers

RUN mkdir /website && chmod 777 /website
COPY . /website

WORKDIR /website

VOLUME output /website/output

# prevent writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip && \
	pip install -r requirements.txt

RUN make html
