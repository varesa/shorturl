FROM registry.esav.fi/base/python3

COPY ./ /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENV LANG=en_US.utf-8
ENV LC_ALL=en_US.utf-8

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0"]
