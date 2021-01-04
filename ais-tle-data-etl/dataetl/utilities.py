from argparse import ArgumentParser


def cli_arguments():
    parser = ArgumentParser()

    parser.add_argument(
        "--input-ais-dir",
        dest="INPUT_AIS_DIR",
    )

    parser.add_argument(
        "--input-tle-dir",
        dest="INPUT_TLE_DIR",
    )

    parser.add_argument(
        "--input-gdb-dir",
        dest="INPUT_GDB_DIR",
    )

    parser.add_argument(
        "--hdfs-dir",
        dest="HDFS_DIR",
    )

    parser.add_argument(
        "--output-local-gdb-dir",
        dest="OUTPUT_LOCAL_GDB_DIR",
    )

    parser.add_argument(
        "--output-ais-table",
        dest="OUTPUT_AIS_TABLE",
    )

    parser.add_argument(
        "--output-tle-table",
        dest="OUTPUT_TLE_TABLE",
    )

    parser.add_argument(
        "--output-gdb-table",
        dest="OUTPUT_GDB_TABLE",
    )

    args = parser.parse_args()

    return args
