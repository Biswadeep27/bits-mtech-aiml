class SpellCorrectionException(Exception):
    """
    Base class for all SpellCorrection's errors.
    Each custom exception should be derived from this class.
    """

    status_code = 500