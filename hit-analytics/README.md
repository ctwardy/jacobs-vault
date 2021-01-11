# hit-analytics

The `hit-analytics` repo is the start of development of a scaled process to do satellite hit detection across all time, all AIS positions for each satellite. Currently, it is not fully implemented. In its current state, it ingests all TLE records from 2015-2017, and a table with each date from the AIS table represented a single time. It then, at scale, finds the closest TLE record for each satellite, for each day. This is then planned to be used as the input for secondary analytics where satellite positions are calculated for each AIS record based on the already discovered closest satellite TLE record from this table. This second step is implemented locally and demonstrated in notebook form, but is not implemented at scale as yet. 

TLE input table required columns:
- `satellite`: The NORAD satellite identification number.
- `valid`: Whether the checksum of the record was valid for both lines.
- `ts`: Unix epoch time based timestamp.
AIS input table format:
- `basedatetime`: AIS timestamp datetime, in format `"yyyy-MM-dd'T'HH:mm:ss"`
The input tables are specified directly in `main.py` at the current development stage.

# Getting started

## Push the project to the cloud

Usually the project will be run on a cloud, where it is assumed Spark is installed across the cluster already and can be called in the usual manner with `spark-submit` (i.e. the Spark binaries are in the `$PATH`). If this is the case, from the directory containing hit-analytics (i.e. if you are inside the `hit-analytics` directory, first `cd ..`) run:

```
rsync -avz --no-perms --exclude-from hit-analytics/rsync_exclude.txt hit-analytics user@remotehost:path/to/where/you/want/it
```
or if using Windows run:
```
scp -r hit-analytics user@remotehost:path/to/where/you/want/it
```

after replace `user`, `host`, and `path/to/where/you/want/it` with appropriate values for your server. Each time you modify the code locally, you will need to push the repo to your remote server with this command before running on the remote server.

## Building the project

In order to run this code in PySpark, you will need to build the environment, using the `environment.yml` in this directory. You will need to build the environment on the target system, i.e. if you are running on a remote server/cloud, you need to run these commands there once you have rsynced the code up. This created environment is then shipped around to the cloud nodes as your Spark application runs. This eliminates the need to synch environments across the cloud. A single build on the staging server where you launch the Spark job is adequate. The first time you build the conda environment, run:

`make build`

Whenever you update a required package in `environment.yml`, run:

`make reinstall`

Whenever you update the package code in hit-analytics/hitdetector, run:

`make update`

If you want to delete the conda environment and start fresh, run:

`make clean`

## Running the project the first time

To run the project once you have run `make build`, from the main directory run:

```
chmod -R +x scripts
chmod +x submit.sh
```

then run:

`scripts/main.sh` (followed by any command line arguments)

The output can be found in the new `logs` directory.

## Running the project as you edit/refine

As you edit the project and re-run things locally, you'll want to then push them up to the cloud. This command will sync your local files to the cloud, excluding all the git stuff (or anything contained in `rsync_exclude.txt`). It should be run one directory up from your main package directory on your local machine. Replace your username, remote host, and path where you want the repo to go on the remote host:

```
rsync -avz --no-perms --exclude-from hit-analytics/rsync_exclude.txt hit-analytics user@remotehost:path/to/where/you/want/it
```

On the cloud, from the main directory, run these commands:
```
make update
scripts/main.sh
```
The output can then be found in the `logs` directory.

To automatically update your package with the new code edits, run the script, and look at the log output, from the main directory, run these commands:
```
make update && scripts/main.sh && sleep 1 && ls -t logs | head -n 1 && tail -f logs/$( ls -t logs | head -n 1 )
```

## Development in ipython shell or Jupyter notebook

For time efficiency, you will often want to prototype code outside of the main usecase(s) (which may be a long-running process). However, you still want to be able to use the classes/functions from your main package, as well as the specific `conda` environment built for this project, as it may contain packages not available in the base `conda` distribution available to `pyspark` across your cluster.

### ipython shell

On your remote server, from the main directory of your repository, run:

```scripts/ipython_shell.sh```

Note that for this to work properly, you must be in the main directory.

### Jupyter notebook

On your remote server, from the main directory of your repository, run:

```scripts/jupyter_notebook.sh```

Note that for this to work properly, you must be in the main directory. You should see output similar to: 

```
[I 17:18:37.451 NotebookApp] Serving notebooks from local directory: /home/cmorris/haccs/tst/tiger-tester
[I 17:18:37.452 NotebookApp] The Jupyter Notebook is running at:
[I 17:18:37.452 NotebookApp] http://localhost:8898/?token=5b5415e0b1f7b466527f1708b4a4ca06795fe3be126e6fff
[I 17:18:37.452 NotebookApp]  or http://127.0.0.1:8898/?token=5b5415e0b1f7b466527f1708b4a4ca06795fe3be126e6fff
[I 17:18:37.452 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 17:18:37.473 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/cmorris/.local/share/jupyter/runtime/nbserver-22525-open.html
    Or copy and paste one of these URLs:
        http://localhost:8898/?token=5b5415e0b1f7b466527f1708b4a4ca06795fe3be126e6fff
     or http://127.0.0.1:8898/?token=5b5415e0b1f7b466527f1708b4a4ca06795fe3be126e6fff
```
     
You now need to set up port forwarding on your local development machine. In the above output, we look at the last line and see that the notebook is running on port `8898` on the remote machine (the number directly after `127.0.0.1:`). This is the default port the notebook will try to serve on. However, if this port is already occupied on the remote server by another user, Jupyter will automatically find another port. If this port is not `8898`, take note of which port is being used, as it will be needed in the next step.

On your local development machine, in a new terminal window, run (replacing `user` and `remotehost` with your remote server information):

```
ssh -N -f -L 127.0.0.1:8898:127.0.0.1:8898 user@remotehost
```

If the port where the server is running you noted in the previous step is not `8898`, replace both instances of `8898` in the above command with the actual port number before running the command.

Finally, in a web browser on your local development machine, copy/paste the Jupyter notebook URL with token, for example in the above output, you would copy/paste

```
http://127.0.0.1:8898/?token=5b5415e0b1f7b466527f1708b4a4ca06795fe3be126e6fff
``` 
into your web browser. We recommened storing all your development notebooks in the `nbs` folder within your repository, but this is up to your personal preference.

## Testing the project

To check if the Conda environment and library are being distributed to
the executors correctly, edit the `modules_to_test` variable on line `40` of `tests/test_env.py` to match the packages in your `environment.yml` file that you wish to test.

Then, from the main directory of your repository run:

`./submit.sh tests/test_env.py`

Prior to running this, edit the variable `modules_to_test` in `tests/test_env.py` to match the packages installed through `environment.yml` that you wish to test.

This will display the contents of the root directory and the Python `sys.path`
on the executor YARN containers. The directory should contain `environment_zip`
and `hitdetector.zip`. Additionally, the path should include `./hitdetector.zip`.

This script will also display a table with the versions of several Python
modules (including the botlife package itself) installed on the driver and the
executor nodes. These versions should be the same in both columns.

## Adding to GitLab
## Development tips

- Library code should be defined in `hitdetector/__init__.py`
- CLI code should be defined in `utilities.py`
- Always create builds on your target environment (e.g. Silverdale)
