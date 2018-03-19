FROM registry.esav.fi/base/python3

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
