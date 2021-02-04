FROM %BUILD_IMAGE%

USER root

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install

ENV PROJECT_DIR /app

WORKDIR ${PROJECT_DIR}/

COPY requirements.txt ${PROJECT_DIR}/

USER %END_USER%

# install Pip modules
RUN pip install --upgrade pip && pip install -r requirements.txt

