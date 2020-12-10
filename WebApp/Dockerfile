FROM tiangolo/uwsgi-nginx:python3.8-2020-05-09

ARG TESTING

COPY ./requirements* /code/

WORKDIR /code

RUN pip install --upgrade pip==20.3.1 && \
    pip install -r /code/requirements.txt

# Install testing requirements when testing
RUN if [ -z "$TESTING" ] ; then echo Not running tests ; else pip install -r /code/requirements_testing.txt ; fi

COPY . /code

ENV FLASK_APP tinifyUrl
ENV FLASK_DEBUG 1

CMD ["flask", "run", "-h", "0.0.0.0"]
