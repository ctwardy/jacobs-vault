# Title



<table>
    <tr style="background-color:white">
        <td ><img src="images/Jacobs_logo_rgb_black.svg" width="200"/></td>
        <td><img alt="Satellites Visible" src="images/polar_plot2.png" width="300"></td>
    </tr>
</table>
    
# Welcome to jacobs-vault.
 
> **jacobs-vault** is Jacobs' response to the Air Force VAULT quick-turn data analysis challenge. 

It contains scripts and notebooks to (a) ingest the provided AIS shipping tracks and satellite TLE data, (b) find what satellites are visible for a given ship track position, and (c) highlight coverage gaps / flaws in the data. 

## Installing

We used the `nbdev` and `cookie-cutter` environments to ease packaging and installation, but they haven't been fully integrated.  Many queries expect you to have an Apache Spark environment, though in theory that could be on a single machine.  

**When done, you should be able to install as follows:** 

You can install jacobs-vault on your own machines with conda (highly recommended). If you're using [Anaconda](https://www.anaconda.com/products/individual) then run:
```bash
conda install -c <CONDA CHANNEL> jacobs-vault gh anaconda
```
...or if you're using [miniconda](https://docs.conda.io/en/latest/miniconda.html)) then run:
```bash
conda install -c <CHANNEL> -c jacobs-vault
```
To install with pip, use: `pip install jacobs-vault`. 


If you plan to develop, see below.

## About jacobs-vault

jacobs-vault partitions the data to support either distributed Spark/Dash workflows, or fast single-ship satellite queries. It includes: 

* ETL scripts in the `etl` folder
* Call `skyfield` for ephemeris calculations
* The notebook `nbs/01_HitTest.ipynb` and service `hittestservice/` provide the core functions to read the appropriate TLE file for a given day, and calculate the visible satellites.
* `geotransformer`
* `ais-analytics`
* ...

## Key Required Packages

Required top-level packages must be listed in `settings.ini`, or the GitHub Continuous Integration tests will fail. There are three broad categories:

### Scientific Python Ecosystem:
* Anaconda distribution preferred, though pip should work
* Core: numpy, pandas
* Astronomy: skyfield, ...else?...
* Possibly: scikit-learn (not used yet?)
* Notebooks: jupyter notebook

### Cloud Computing
* Spark, PySpark, Hive, Hadoop
* (Other database as req'd)
* Map support: geopandas, ...
* Visualization: plotly, (matplotlib?), (leaflet?), (opensphere?)

### Literate Programming: 
* nbdev, cookie-cutter

## conda env
You can create the <code>vault</code> conda env using: 
```bash
conda env create -f environment.yml
``` 
and activate it with
```bash
conda activate vault
```

The envs/ folder contains related environments for certain pieces. 


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
