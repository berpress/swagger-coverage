#!/usr/bin/env python
import argparse
import logging.config
import sys

from swagger_coverage.coverage import SwaggerCoverage
from swagger_coverage.logging import setup

logger = logging.getLogger()

LOGGER_LEVEL = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def main():
    parser = argparse.ArgumentParser(description="Swagger coverage")
    parser.add_argument("url", type=str)
    parser.add_argument(
        "-s",
        "--status-codes",
        nargs="+",
        help="set status codes to " "create a report",
        type=str,
    )
    parser.add_argument(
        "-l", "--level", help=f"set logging level {LOGGER_LEVEL}", type=str
    )
    args = parser.parse_args()
    url = args.url
    status_codes = args.status_codes
    logging_level = args.level
    if logging_level is None:
        logging_level = "INFO"
    elif logging_level not in LOGGER_LEVEL:
        raise ValueError("Check logger level")
    setup(logging_level)
    logger.setLevel(logging_level)
    swagger = SwaggerCoverage(url=url, status_codes=status_codes)
    swagger.create_coverage_data()


if __name__ == "__main__":
    try:
        main()
    except ValueError:
        sys.exit(2)
