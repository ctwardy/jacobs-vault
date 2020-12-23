from argparse import ArgumentParser


def cli_arguments():
    parser = ArgumentParser()

    parser.add_argument(
        "--ais-input-table",
        dest="AIS_INPUT_TABLE",
    )

    parser.add_argument(
        "--velocities-output-table",
        dest="VELOCITIES_OUTPUT_TABLE",
    )

    args = parser.parse_args()

    return args
