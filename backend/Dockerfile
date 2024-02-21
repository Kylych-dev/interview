FROM python:3.11.4-slim-buster

WORKDIR /usr/src/backend


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip


COPY ./requirements.txt /usr/src/backend/requirements.txt
RUN pip install -r /usr/src/backend/requirements.txt


COPY ./entrypoint.sh /usr/src/backend/entrypoint.sh

RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh

RUN chmod +x /usr/src/backend/entrypoint.sh


COPY . /usr/src/backend/


ENTRYPOINT ["/usr/src/backend/entrypoint.sh"]


