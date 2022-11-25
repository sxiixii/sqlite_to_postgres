import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s %(levelname)s %(asctime)s %(message)s',
    datefmt='%I:%M:%S'
)
handler = logging.FileHandler('database_loader.log')
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s:%(name)s     %(message)s', datefmt='%I:%M:%S'))
log = logging.getLogger()
log.addHandler(handler)
