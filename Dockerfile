FROM python:3.10-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./runcontainer.sh /code/runcontainer.sh

CMD ["./runcontainer.sh"]