# Jacobs VAULT



VAULT converts AIS ship records into clickable tracks that show satellite coverage for the location clicked. The demo shows both Jupyter maps (via iPyLeaflet) and Google-Earth style maps (using OpenSphere).  

<img src="nbs/images/vault-demo-3.gif">

For demo purposes, we treat all entries in the TLE file as viable satellites. In reality most of these are space junk, but within 10 years there could be over 10,000 cubesats. 

The project also contains scripts & notebooks to ingest, characterize, and clean the AIS & TLE data, detect outliers, and cluster tracks. 

<table>
    <tr style="background-color:#FFFFFF">
        <td style="background-color:#FFFFFF">
<img src="nbs/images/Jacobs_logo_rgb_black.svg" width="200" style="max-width: 200px">
        </td>
        <td>
<img alt="Satellites Visible" src="nbs/images/starmap_new.png" width="300" style="max-width: 300px">
        </td>
    </tr>
</table>



## Documentation
Further documents are hosted on [GitHub Pages](https://cmorris-jacobs.github.io/jacobs-vault/).

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


## Contributing and Exploring

To explore further, 

1. Clone the repository with ...

```bash
git clone https://github.com/cmorris-jacobs/jacobs-vault
cd jacobs-vault
``` 

2. Obtain a copy of the VAULT data, and put it in `jacobs-vault/data`, for example with :
```bash
ln -s path/to/data data
```

3. Using either conda or pip, create the vault virtual environment so you have the required packages. Using conda, that would be:
```bash
conda create -f environment.yml
```
Wait while it installs packages...

4. Activate the vault virtual environment.
```bash
conda activate vault
```

5. To run the **demo** from here:
```bash
cd demo
ln -s ../data ./
. run.sh
```
The `ln` line just makes ETL'd data visible from `demo/data`. Use other techniques if you prefer.

5. If you plan to be pushing to git, then use nbdev to install git hooks - mostly relevant to notebooks in `nbs/`:
```bash
nbdev_install_git_hooks
```
If you will be modifying notebooks in that folder, familiarize yourself with fastai's nbdev, and do a `make` before commit/push to update associated modules and docs.


## Folders

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
* `hittestservice` - First attempt to wrap HitTest code into a web service.
* `scripts` - A collection of scripts, esp. SQL queries.


### A note on Spark
Some code expects an Apache Spark setup with Hive and Hadoop available. The `ais-analytics` and `geotransformer` folders contain `cookie-cutter` setups with scripts that 
will start Spark-enabled jupyter notebooks, or launch a spark job with the required virtual environment.

## Key Required Packages

The `environment.yml` file invoked above has the full package list, but key top-level packages fall in three broad categories:

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
