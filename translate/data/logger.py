import logging
import sys

log = logging.getLogger()
log.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
