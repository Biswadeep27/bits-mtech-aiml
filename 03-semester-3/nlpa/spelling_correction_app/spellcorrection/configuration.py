import os
import sys
import json
import shlex
import pathlib
import functools

from typing import Any, Dict, List, Optional, Tuple, Union
from configparser import _UNSET, ConfigParser, NoOptionError, NoSectionError

from spellcorrection.exception import SpellCorrectionException

def expand_env_var(env_var):
    """
    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


def get_spellcorrection_home():
    """Get path to SpellCorrection Home"""
    return expand_env_var(os.environ.get('SPELLCORRECTION_HOME', '~/spellcorrection'))


def get_spellcorrection_config(spellcorrection_home):
    """Get Path to spellcorrection.cfg path"""
    if 'SPELLCORRECTION_CONFIG' not in os.environ:
        return os.path.join(spellcorrection_home, 'spellcorrection.cfg')
    return expand_env_var(os.environ['SPELLCORRECTION_CONFIG'])


def _default_config_file_path(file_name: str):
    templates_dir = os.path.join(os.path.dirname(__file__), 'config')
    return os.path.join(templates_dir, file_name)


class SpellCorrectionConfigParser(ConfigParser):
    """Custom SpellCorrection Configparser supporting defaults options"""

    def optionxform(self, optionstr: str) -> str:
        return optionstr

    def __init__(self, default_config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.spellcorrection_defaults = ConfigParser(*args, **kwargs)
        if default_config is not None:
            self.spellcorrection_defaults.read_string(default_config)

        else:
            raise SpellCorrectionException('Default Config template not found.')

        self.is_validated = False

    def validate_config(self):
        if any(self.get('core','config_path')):
            if any(self.get('core','config_path')):
                self.is_validated = True
            else:
                raise SpellCorrectionException('rabbit MQ port details not provided.')
        else:
            raise SpellCorrectionException('rabbit MQ host details not provided.')
        
    def has_option(self, section, option):
        try:
            # Using self.get() to avoid reimplementing the priority order
            # of config variables (env, config, cmd, defaults)
            # UNSET to avoid logging a warning about missing values
            self.get(section, option, fallback=_UNSET)
            return True
        except (NoOptionError, NoSectionError):
            return False
        
    
    def _get_option_from_config_file(self, key, kwargs, section):
        # ...then the config file
        if super().has_option(section, key):
            # Use the parent's methods to get the actual config here to be able to
            # separate the config from default config.
            return expand_env_var(super().get(section, key, **kwargs))
        return None


    def _get_option_from_default_config(self, section, key, **kwargs):
        # ...then the default config
        if self.spellcorrection_defaults.has_option(section, key) or 'fallback' in kwargs:
            return expand_env_var(self.spellcorrection_defaults.get(section, key, **kwargs))

        else:
            #log.warning("section/key [%s/%s] not found in config", section, key)

            raise SpellCorrectionException(f"section/key [{section}/{key}] not found in config")
        

    def read(self, filenames, encoding=None):
        super().read(filenames=filenames, encoding=encoding)


    def get(self, section, key, **kwargs):
        section = str(section).lower()
        key = str(key).lower()

        option = self._get_option_from_config_file( key, kwargs, section)
        if option is not None:
            return option
        
        return self._get_option_from_default_config(section, key, **kwargs)
    


def _parameterized_config_from_template(filename) -> str:
    TEMPLATE_START = '# ----------------------- TEMPLATE BEGINS HERE -----------------------\n'

    path = _default_config_file_path(filename)
    with open(path) as fh:
        for line in fh:
            if line != TEMPLATE_START:
                continue
            return parameterized_config(fh.read().strip())
    raise RuntimeError(f"Template marker not found in {path!r}")


def parameterized_config(template):
    """
    Generates a configuration from the provided template + variables defined in
    current scope
    :param template: a config content templated with {{variables}}
    """
    all_vars = {k: v for d in [globals(), locals()] for k, v in d.items()}
    return template.format(**all_vars)

def initialize_config():
    """
    Load the Sparkway config files.
    Called for you automatically as part of the Sparkway boot process.
    """
    global SPELLCORRECTION_HOME

    default_config = _parameterized_config_from_template('default_spellcorrection.cfg')

    conf = SpellCorrectionConfigParser(default_config=default_config)

    if not os.path.isfile(SPELLCORRECTION_CONFIG):
        pathlib.Path(SPELLCORRECTION_HOME).mkdir(parents=True, exist_ok=True)

        with open(SPELLCORRECTION_CONFIG, 'w') as file:
            file.write(default_config)


    conf.read(SPELLCORRECTION_CONFIG)

    return conf


@functools.lru_cache(maxsize=None)
def _DEFAULT_CONFIG():
    path = _default_config_file_path('default_sparkway.cfg')
    with open(path) as fh:
        return fh.read()
    

# Setting SPARKWAY_HOME and SPARKWAY_CONFIG from environment variables, using
# "~/sparkway" and "$SPARKWAY_HOME/sparkway.cfg" respectively as defaults.

SPELLCORRECTION_HOME = get_spellcorrection_home()
SPELLCORRECTION_CONFIG = get_spellcorrection_config(SPELLCORRECTION_HOME)

conf = initialize_config()

try:
    conf.validate_config()
except Exception as e:
    pass


    



