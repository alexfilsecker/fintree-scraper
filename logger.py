import logging

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s %(module)10s, line: %(lineno)d] %(message)s"
)
logger = logging.getLogger()
