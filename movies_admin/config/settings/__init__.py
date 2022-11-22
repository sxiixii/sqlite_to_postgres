import os

from dotenv import load_dotenv
from split_settings.tools import include, optional

load_dotenv()

base_settings = [
    'components/base.py',
    'components/database.py',
    'environments/development.py',
    optional('environments/local.py')
]

include(*base_settings)
