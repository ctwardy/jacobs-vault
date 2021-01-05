FROM continuumio/anaconda3:2019.10

# FYI: Equivalent conda createL:
#    conda create --name vault python=3.7.4 anaconda=2019.10

# on Jacobs Silverdale cloud use -v /share/nas2/data/airforce:/data
WORKDIR /data

WORKDIR /github.com/cmorris-jacobs/
RUN git clone https://github.com/cmorris-jacobs/jacobs-vault.git

# Override this with a local folder to externalize project source for development
#    e.g. if you are in the demo directory:
#       -v "${pwd}/..":/github.com/cmorris-jacobs/jacobs-vault
WORKDIR /github.com/cmorris-jacobs/jacobs-vault

WORKDIR /github.com/cmorris-jacobs/jacobs-vault/demo/docker

RUN /opt/conda/bin/pip install -r requirements.txt

WORKDIR /github.com/cmorris-jacobs/jacobs-vault/demo

ENV PYTHONPATH=/github.com/cmorris-jacobs/jacobs-vault/hittestservice

ADD java_home.tar.gz /usr/java/
ADD hive_lib.tar.gz /opt/cloudera/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702/lib/hive/

#CMD [ "/opt/conda/bin/jupyter", "notebook", "--ip=0.0.0.0", "--port=2080", "VAULT_Demo.ipynb"]
CMD [ "/opt/conda/bin/jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--port=2080"]
