From pyiron/md:2020-10-30

RUN rm ${HOME}/*.ipynb

USER root
RUN apt-get update && \
    apt install -y nano \
    vim \
    build-essential \
    curl && \
    apt-get clean && \
    fix-permissions ${HOME}/ && \
    mkdir ${HOME}/studentRepo/ && \
    mkdir ${HOME}/studentRepo/pyiron && \
    mkdir ${HOME}/studentRepo/pyiron_contrib/ && \
    mkdir ${HOME}/studentRepo/custom_code/ && \
    chmod -R 775 ${HOME}/studentRepo/
ENV PYTHONPATH="${HOME}/studentRepo/pyiron/:$PYTHONPATH"
ENV PYTHONPATH="${HOME}/studentRepo/pyiron_contrib/:$PYTHONPATH"
ENV PYTHONPATH="${HOME}/studentRepo/custom_code/:$PYTHONPATH"
USER $DOCKER_UID