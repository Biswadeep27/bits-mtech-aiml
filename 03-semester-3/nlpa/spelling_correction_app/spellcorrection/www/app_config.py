import json
import datetime

from spellcorrection import conf

BASE_URL = conf.get('webserver', 'base_url')
APP_NAME = conf.get(section="webserver", key="instance_name", fallback="SpellCorrection")