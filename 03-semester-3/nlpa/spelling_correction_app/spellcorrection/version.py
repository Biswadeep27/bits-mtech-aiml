__all__ = [
    'version'
]


try:
    import importlib_metadata as metadata
except ImportError:
    from importlib import metadata

try:
    version = metadata.version('spellcorrection')
except metadata.PackageNotFoundError:
    import logging

    log = logging.getLogger(__name__)
    log.warning("Package metadata could not be found. Overriding it with version found in version.py")
    version = '1.0.0_build'


del metadata