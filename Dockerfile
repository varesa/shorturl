FROM registry.esav.fi/base/python3

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY ./ /app
WORKDIR /app

ENV LANG=en_US.utf-8
ENV LC_ALL=en_US.utf-8

ENV FLASK_APP=main.py

CMD ["sh", "start.sh"]
