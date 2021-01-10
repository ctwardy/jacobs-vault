FROM continuumio/anaconda3:2019.10

# FYI: Equivalent conda createL:
#    conda create --name vault python=3.7.4 anaconda=2019.10

WORKDIR /github.com/cmorris-jacobs/
RUN git clone https://github.com/cmorris-jacobs/jacobs-vault.git

# Override this with a local folder to externalize project source for development
#    e.g. if you are in the demo directory:
#       -v "${pwd}/..":/github.com/cmorris-jacobs/jacobs-vault
WORKDIR /github.com/cmorris-jacobs/jacobs-vault

# Load the additional python packages we depend on
WORKDIR /github.com/cmorris-jacobs/jacobs-vault/demo/docker
RUN /opt/conda/bin/pip install -r requirements.txt

# Load data needed for Jupyter Notebook portion of demo

# on Jacobs Silverdale cloud use 
#    -v /share/nas2/data/airforce:/github.com/cmorris-jacobs/jacobs-vault/hittestservice/data
# to override limited data here with full data
WORKDIR /github.com/cmorris-jacobs/jacobs-vault/data
WORKDIR /github.com/cmorris-jacobs/jacobs-vault/data/VAULT_Data/
ADD https://jacobs-vault-2020-12-24--shortterm.s3.amazonaws.com/data/airforce/VAULT_Data/TLE_daily.tar.gz \
    /github.com/cmorris-jacobs/jacobs-vault/data/VAULT_Data/
ADD https://jacobs-vault-2020-12-24--shortterm.s3.amazonaws.com/data/airforce/VAULT_Data/timeseries.tar.gz \
    /github.com/cmorris-jacobs/jacobs-vault/data/VAULT_Data/
ADD https://jacobs-vault-2020-12-24--shortterm.s3.amazonaws.com/data/airforce/VAULT_Data/demo.tar.gz \
   /github.com/cmorris-jacobs/jacobs-vault/data/VAULT_Data/
RUN cd /github.com/cmorris-jacobs/jacobs-vault/data/VAULT_Data/ && \
    tar xzf TLE_daily.tar.gz && rm TLE_daily.tar.gz && \
    tar xzf timeseries.tar.gz && rm timeseries.tar.gz && \
    tar xzf demo.tar.gz && rm demo.tar.gz 

# Move to the directory we run Jupyter out of
WORKDIR /github.com/cmorris-jacobs/jacobs-vault

# Put the hittest service on the Python module path
ENV PYTHONPATH=/github.com/cmorris-jacobs/jacobs-vault/hittestservice

CMD [ "/opt/conda/bin/jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--port=2080"]
