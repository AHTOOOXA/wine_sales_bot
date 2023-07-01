FROM python:3.8
ENV TOKEN # your token
ENV CHANNEL # @your_channel
COPY /requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r /app/requirements.txt
COPY . /app
CMD python /app/main.py
