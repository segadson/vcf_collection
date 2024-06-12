import os
import sys
from requests.exceptions import HTTPError

class VcfAPIException(HTTPError):
    pass