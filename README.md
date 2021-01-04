# Jacobs VAULT



## Installing

**TBD:** 

We recommend installing from conda. 

| Conda | Pip | Git |
| ---- | ---- | ---- |
| Full [Anaconda](https://www.anaconda.com/products/individual):
```bash
conda install -c <CONDA CHANNEL> jacobs-vault gh anaconda
```
[Miniconda](https://docs.conda.io/en/latest/miniconda.html)):
```bash
conda install -c <CHANNEL> -c jacobs-vault
```
| ```bash
pip install jacobs-vault
```
| ```bash
git clone git@github.com:cmorris-jacobs/jacobs-vault.git
```
or 
```bash
git clone https://github.com/cmorris-jacobs/jacobs-vault.git
```
|

## Using

Change to the `jacobs-vault` folder and ensure that `data/` contains or points to the VAULT data. (SAY MORE!)  Then explore these options:

### Demo
```bash
cd demo
. run.sh
```
May require linking `demo/data` to the data folder, e.g. `ln -s ../data ./`. 

### Run the notebooks in nbs/
Activate the `vault` Python virtual environment and start a new jupyter kernel.
```bash
conda env -f environment.yml
conda activate vault
jupyter notebook
```
You can now explore and run the notebooks in the `nbs/` folder.

### Notes
* Notebooks in `nbs/` contain `nbdev` markup. The `nbdev` package uses them to generate the project docs (including this README), generate some python modules, run tests, and perform limited Continuous Integration testing upon `git push` events. 
* Some code expects an Apache Spark setup with Hive and Hadoop available, and we have only tested on our cluster. However, our `cookie-cutter` template packages the Spark environments and our run scripts distribute those to the compute nodes for reproducibility. 


## About jacobs-vault

jacobs-vault partitions the data to support either distributed workflows (Spark), or fast single-ship satellite queries. It includes: 

* ETL scripts in the `etl` folder
* Call `skyfield` for ephemeris calculations
* Notebooks folder `nbs/` for exploration.
  * Via the `nbdev` package, notebooks generate modules that can be called by other scripts, and documentation (including this README).
  * `nbs/01_HitTest.ipynb` generates jacobs-vault/hittest.py, used by `hittestservice.py` to display satellite starmaps given queries. 
* `geotransformer`
* `ais-analytics`
* ...

## Key Required Packages

After cloning the repository, use the `conda` package manager to install the main dependencies. (We provide files for `pip`, but we recommend conda.)
```bash
conda env create -f environment.yml
```
Key top-level packages fall in three broad categories:

### Scientific Python Ecosystem:
* Core: numpy, pandas, ipython
* Astronomy: skyfield, astropy, GDAL, pyephem, pyorbital  # <-- do we really use all these still?
* Clustering: [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/index.html)
* Notebooks: jupyter notebook

### Cloud Computing
* Spark, PySpark, Hive, Hadoop
* (Other database as req'd)
* Map support: geopandas, ...
* Visualization: plotly, (matplotlib?), (leaflet?), (opensphere?)

### Literate Programming: 
* nbdev, cookie-cutter


## Tests

To run the tests in parallel, launch:

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
