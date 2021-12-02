# -*- coding: utf-8 -*-
# Generic/Built-in
import requests
import os
import logging
import pprint


# Other Libs


# Owned
from .CapellaAPIAuth import CapellaAPIAuth
from .CapellaExceptions import MissingBaseURLError, MissingAccessKeyError, \
    MissingSecretKeyError, GenericHTTPError, CbcAPIError

# EnvVars.py sets the environmental variables used here
# If EnvVars.py does not exist, then we'll try the OS environment variables instead
try:
    import capellaAPI.EnvVars
except ImportError:
    pass

__author__ = 'Jonathan Giffard'
__copyright__ = 'Copyright 2021, Couchbase'
__credits__ = ['Jonathan Giffard']
__license__ = 'MIT License'
__version__ = '0.3.1'
__maintainer__ = 'Jonathan Giffard'
__email__ = 'jonathan.giffard@couchbase.com'
__status__ = 'Dev'

# Handles talking to the endpoints over http 
# and returns the response.
# Assumes that the caller then deals with whatever
# the response holds.


class CapellaAPIRequests:

    def __init__(self):
        # handles http requests - GET , PUT, POST, DELETE
        # to the Couchbase Cloud APIs
        # Read the values from the environmental variables
        if os.environ.get('CBC_BASE_URL') is None:
            raise MissingBaseURLError('Environmental variable CBC_BASE_URL has not been set')
        else:
            self.API_BASE_URL = os.environ.get('CBC_BASE_URL')

        self._log = logging.getLogger(__name__)

        # We will re-use the first session we setup to avoid
        # the overhead of creating new sessions for each request
        self.network_session = requests.Session()

    def set_logging_level(self, level):
        self._log.setLevel(level)

    # Methods
    def capella_api_get(self, api_endpoint):
        cbc_api_response = None

        self._log.info(api_endpoint)

        try:
            cbc_api_response = self.network_session.get(self.API_BASE_URL + api_endpoint, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError:
            error = pprint.pformat(cbc_api_response.json())
            raise GenericHTTPError(error)

        except MissingAccessKeyError:
            self._log.debug(f"Missing Access Key environment variable")
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            self._log.debug(f"Missing Access Key environment variable")
            print("Missing Access Key environment variable")

        # Grab any other exception and send to our generic exception
        # handler
        except Exception as e:
            raise CbcAPIError(e)


        return (cbc_api_response)


    def capella_api_post(self, api_endpoint, request_body):
        cbc_api_response = None

        self._log.info(api_endpoint)
        self._log.debug("Request body: " + str(request_body))

        try:
            cbc_api_response = self.network_session.post(self.API_BASE_URL + api_endpoint,
                                                         json=request_body, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError:
            error = pprint.pformat(cbc_api_response.json())
            raise GenericHTTPError(error)

        except MissingAccessKeyError:
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            print("Missing Access Key environment variable")

        # Grab any other exception and send to our generic exception
        # handler
        except Exception as e:
            raise CbcAPIError(e)

        return (cbc_api_response)


    def capella_api_put(self, api_endpoint, request_body):
        cbc_api_response = None

        self._log.info(api_endpoint)
        self._log.debug("Request body: " + str(request_body))

        try:
            cbc_api_response = self.network_session.put(self.API_BASE_URL + api_endpoint,
                                                        json=request_body, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError:
            error = pprint.pformat(cbc_api_response.json())
            raise GenericHTTPError(error)

        except MissingAccessKeyError:
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            print("Missing Access Key environment variable")

        return (cbc_api_response)


    def capella_api_del(self, api_endpoint, request_body=None):
        cbc_api_response = None

        self._log.info(api_endpoint)
        self._log.debug("Request body: " + str(request_body))

        try:
            if request_body is None:
                cbc_api_response = self.network_session.delete(self.API_BASE_URL +
                                                               api_endpoint, auth=CapellaAPIAuth())
            else:
                cbc_api_response = self.network_session.delete(self.API_BASE_URL +
                                                               api_endpoint, json=request_body, auth=CapellaAPIAuth())
            self._log.debug(cbc_api_response.content)

        except requests.exceptions.HTTPError:
            error = pprint.pformat(cbc_api_response.json())
            raise GenericHTTPError(error)

        except MissingAccessKeyError:
            print("Missing Access Key environment variable")

        except MissingSecretKeyError:
            print("Missing Access Key environment variable")

        # Grab any other exception and send to our generic exception
        # handler
        except Exception as e:
            raise CbcAPIError(e)

        return (cbc_api_response)

    
