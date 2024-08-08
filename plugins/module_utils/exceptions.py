import os
import sys
from requests.exceptions import HTTPError

# class VcfAPIException(HTTPError):
#     pass

class VcfAPIException(HTTPError):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code