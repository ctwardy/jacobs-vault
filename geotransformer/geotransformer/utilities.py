from argparse import ArgumentParser


def cli_arguments():
    parser = ArgumentParser()

    parser.add_argument(
        "--geo-input-table",
        dest="GEO_INPUT_TABLE",
    )

    parser.add_argument(
        "--geo-output-table",
        dest="GEO_OUTPUT_TABLE",
    )

    args = parser.parse_args()

    return args
