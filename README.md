# Jacobs VAULT



VAULT contains scripts and notebooks that (a) ingest and characterize the provided AIS shipping tracks and satellite TLE data, (b) find "hits" - satellites are visible for a given ship position, and (c) highlight coverage gaps / flaws in the data.  Here is an example starmap showing satellites visible from one point on track, colored by quality of the satellite's TLE data. 
<table>
    <tr style="background-color:#EEEEEE">
        <td ><img src="images/Jacobs_logo_rgb_black.svg" width="200"/></td>
        <td><img alt="Satellites Visible" src="images/polar_plot2.png" width="300"></td>
    </tr>
</table>
(For demo purposes, we treat all entries in the TLE file as viable satellites, when in reality most are space junk.)

## Installing

These instructions require Docker [(obtained here)](https://docs.docker.com/get-docker/) and a DockerHub account [(obtained here)](https://hub.docker.com/). 

Once docker is installed and the DockerHub account is established, in your operating system command line run:
```bash
docker login
docker pull ke2jacobs/jacobs-vault-nb-with-data:latest
docker run --rm -it -p 2080:2080 ke2jacobs/jacobs-vault-nb-with-data:latest
```

The container will present a message:
```
To access the notebook, open this file in a browser:         
file:///root/.local/share/jupyter/runtime/nbserver-1-open.html    
Or copy and paste one of these URLs:       
http://d20796a21c64:2080/?token=455d272e289a90dbc2533de2cb7ddec9a5574dc3fac5ef66
     or     
http://127.0.0.1:2080/?token=455d272e289a90dbc2533de2cb7ddec9a5574dc3fac5ef66
```
Open a browser window and paste the URL into the browser (http://127.0.0.1: … is usually the best choice)

The main Jupyter page will be displayed.
 
* Click on the folder named "demo"
* Click on the file named "VAULT_Demo.ipynb"
* Click on the "Cell" menu item and choose "Run All"


## Exploring More

If you are familiar with `git`, then you can `git clone` this repository into say `jacobs-vault`. 
* Change to that folder
* VAULT data has to be obtained separately. ETL'ed data must be available via `data/`.

### Demo
Once data are in place, the demo can be run like this:
```bash
cd demo
ln -s ../data ./
. run.sh
```
The `ln` line just makes ETL'd data visible from `demo/data`. Use other techniques if you prefer.


## About jacobs-vault

Jacobs-VAULT is the result of a hackathon challenge, so in addition to a working demo and analysis notebooks, it still has exploratory paths and alternate approaches. Folders are in three rough groups:

### ETL Folders
* `etl` - Original ETL scripts, mostly Spark SQL and Hive.
* `ais-analytics` - Subproject Spark to analyze AIS data. Alternate ETL.
* `geotransformer` - Subproject using Spark to analyze TLE data. Alternate ETL. Directly calls `sgp4` and the `astropy` package, instead of `skyfield`.

### nbdev Folders
A mix of exploratory notebooks and literate programming notebooks that generate Python modules and documentation (including this README) via the `nbdev` package. Controlled by the toplevel `Makefile`, using the `vault` virtual environment captured in `environment.yml`.  
* `nbs` - Toplevel notebooks, generate docs, modules, and README.
* `jacobs_vault` - Python modules generated from `nbs/` by `nbdev` package
* `docs` - Documentation generated from `nbs/` by `nbdev` package
* `data` - (See "Demo Folders".)

To run the notebooks in the `nbs/` folder, 
activate the `vault` Python virtual environment and start a new jupyter kernel.
```bash
conda env -f environment.yml
conda activate vault
jupyter notebook
```
That should start a jupyter session in your browser. You can now explore and run the notebooks in the `nbs/` folder.

### Demo Folders
The demo supports a notebook with an interactive map-based walktrhough of getting AIS tracks, and querying a track for satellite coverage, using the `Skyfield` package for ephemeris calculations.  
* `demo` - As much of the demo as possible lives under here, for completeness.
* `data` - Daily satellite files stored (or linked) as`data/VAULT_Data/TLE_daily/`_year_`/`_MM_`/`_nn_`.tab.gz`. Used by the demo *and* other notebooks & scripts.  


### Other folders
* `autoencoder` - Exploratory work using a PyTorch deep network to discover high-level features and pattersn in the AIS data.
* `ais-kml` - Concurrent visualization attempt using OpenSphere.
* `hitttestservice` - First attempt to wrap HitTest code into a web service.
* `scripts` - A collection of scripts, esp. SQL queries.


### A note on Spark
Some code expects an Apache Spark setup with Hive and Hadoop available. The `ais-analytics` and `geotransformer` folders contain `cookie-cutter` setups with scripts that 
will start Spark-enabled jupyter notebooks, or launch a spark job with the required virtual environment.

## Key Required Packages

After cloning the repository, use the `conda` package manager to install the main dependencies. (We provide files for `pip`, but we recommend conda.)
```bash
conda env create -f environment.yml
```
Key top-level packages fall in three broad categories:

### Scientific Python Ecosystem:
* Core: [numpy](https://numpy.org), [pandas](https://pandas.pydata.org)
* Astronomy: [Skyfield](https://rhodesmill.org/skyfield/), [astropy](https://www.astropy.org), [GDAL](https://gdal.org), (pyorbital??)
* Clustering: [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/index.html)
* Notebooks:  [ipython](https://ipython.org), [jupyter](https://jupyter.org) notebooks.

### Cloud Computing
* [Spark](https://spark.apache.org) including PySpark, [Hive](https://hive.apache.org), [Hadoop](https://hadoop.apache.org)
* (Other database as req'd)
* Map support: geopandas, ...
* Visualization: plotly, (matplotlib?), (leaflet?), (opensphere?)

### Literate Programming: 
* [nbdev](https://nbdev.fast.ai), [cookie-cutter](https://cookiecutter.readthedocs.io/en/latest/README.html)


## Tests

Tests are automatically extracted from notebooks in `nbs/`. To run the tests in parallel, launch:

`nbdev_test_nbs` or `make test`

For all the tests to pass, you'll need to install the following optional dependencies:

```
pip install ...
```

Tests are written using <code>nbdev</code>, for example see the documentation for `hit_quality` or `viz`.

## Contributing

You can clone the repository and install dependencies with ...

``` 
git clone https://github.com/cmorris-jacobs/jacobs-vault
pip install -e "jacobs-vault[dev]"
``` 

After you clone this repository, please run `nbdev_install_git_hooks` in your terminal. This sets up git hooks, which clean up the notebooks to remove the extraneous stuff stored in the notebooks (e.g. which cells you ran) which causes unnecessary merge conflicts.

Before submitting a PR, check that the local library and notebooks match. The script `nbdev_diff_nbs` can let you know if there is a difference between the local library and the notebooks.

- If you made a change to the *notebooks* in one of the exported cells, you can export it to the library with `nbdev_build_lib` or `make jacobs-vault`.
- If you made a (small) change to the *library*, you can export it back to the notebooks with `nbdev_update_lib`.

## Docker Containers

We do not yet have official docker containers, but when done they should be available from [the github site](https://github.com/cmorris-jacobs/docker-containers#jacobs-vault).
