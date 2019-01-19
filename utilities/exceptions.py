class InvalidRequestData(Exception):
    """
    The request data was semantically invalid. This exception is usually
    raised from the actions or the models layer. This exception is not
    to be confused with the custom exceptions of Voluptuous which is
    used to validate the schema of the request data rather than the
    actual value of the data being sent.
    """

    def __init__(self, errors=None):
        """
        :param list(dict) errors: Each dict has keys `field` &
            `description`
        """

        self.errors = errors[:] if errors else []


class ResourceNotFound(InvalidRequestData):
    """
    This is a not_found exception. This can be used on any resource.
    """

    def __init__(self, errors=None, resource=None):
        """
        :param list(dict) errors: Each dict has keys `field` &
            `description`
        """

        self.errors = errors[:] if errors else []
        self.resource = resource
