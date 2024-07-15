# Let users know if they're missing any of our hard dependencies
hard_dependencies = [
    'flask',
    'spellchecker',
    'language_tool_python',
    'jsonschema',
    'pandas',
    'setuptools',
    'gunicorn'
]

missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

from typing import (
    Callable,
    TypeVar,
    Any
)

# used in decorators to preserve the signature of the function it decorates
# see https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)

from spellcorrection.version import version
from spellcorrection.configuration import conf
from spellcorrection.model import SpellingCorrector
from spellcorrection.exception import SpellCorrectionException

__version__ = version

__all__ = [
    'conf',
    'SpellingCorrector',
    'SpellCorrectionException',
    '__version__'
]

__doc__ = """
spellcorrection - A NLP application app for checking and correcting the spelling of input text.
Built by BITS Pilani WILP AIML 2023-25 Batch, 3rd Sem, Group 44.
"""