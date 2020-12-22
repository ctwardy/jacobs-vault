from argparse import ArgumentParser


def cli_arguments():
    parser = ArgumentParser()

    parser.add_argument(
        "--test-argument",
        dest="TEST_ARGUMENT",
    )

    args = parser.parse_args()

    return args
