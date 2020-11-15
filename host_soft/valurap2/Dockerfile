FROM valurap-base:latest

COPY setup.py /code/setup.py
COPY valurap2 /code/valurap2

RUN pip install -e /code[hw]

LABEL org.opencontainers.image.source https://github.com/sevikkk/valurap
