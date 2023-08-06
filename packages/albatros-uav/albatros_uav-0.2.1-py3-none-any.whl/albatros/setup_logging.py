import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s [%(filename)s:%(lineno)d] %(message)s",
    )
