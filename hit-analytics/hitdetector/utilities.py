from argparse import ArgumentParser


def cli_arguments():
    parser = ArgumentParser()

    parser.add_argument(
        "--ais-table",
        dest="AIS_TABLE",
    )

    parser.add_argument(
        "--tle-table",
        dest="TLE_TABLE",
    )    

    args = parser.parse_args()

    return args
