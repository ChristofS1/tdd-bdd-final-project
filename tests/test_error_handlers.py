######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
"""
Product API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestProductService
"""
import unittest
from flask import json
from service.common import error_handlers
from service import app
from service.common import status
from service.models import DataValidationError


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestErrorHandlers(unittest.TestCase):
    """Testet die Error-Handler in service.common.error_handlers"""

    def setUp(self):
        self.app = app
        self.app.testing = True

    def test_request_validation_error_handler(self):
        """Testet die Error-Handler in service.common.error_handlers"""
        error = DataValidationError("Test validation error")
        response, status_code = error_handlers.request_validation_error(error)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "Bad Request")
        self.assertIn("Test validation error", data["message"])

    def test_bad_request_handler(self):
        """Testet den Handler für 400 Bad Request"""
        error = Exception("Bad request error")
        response, status_code = error_handlers.bad_request(error)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["status"], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["error"], "Bad Request")
        self.assertIn("Bad request error", data["message"])

    def test_not_found_handler(self):
        """Testet den Handler für 404 Not Found"""
        error = Exception("Resource not found")
        response, status_code = error_handlers.not_found(error)
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["status"], status.HTTP_404_NOT_FOUND)
        self.assertEqual(data["error"], "Not Found")
        self.assertIn("Resource not found", data["message"])

    def test_method_not_supported_handler(self):
        """Testet den Handler für 405 Method Not Allowed"""
        error = Exception("Method not allowed")
        response, status_code = error_handlers.method_not_supported(error)
        self.assertEqual(status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["status"], status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(data["error"], "Method not Allowed")
        self.assertIn("Method not allowed", data["message"])

    def test_mediatype_not_supported_handler(self):
        """Testet den Handler für 415 Unsupported Media Type"""
        error = Exception("Unsupported media type")
        response, status_code = error_handlers.mediatype_not_supported(error)
        self.assertEqual(status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["status"], status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(data["error"], "Unsupported media type")
        self.assertIn("Unsupported media type", data["message"])

    def test_internal_server_error_handler(self):
        """Testet den Handler für 500 Internal Server Error"""
        error = Exception("Internal server error")
        response, status_code = error_handlers.internal_server_error(error)
        self.assertEqual(status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["status"], status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(data["error"], "Internal Server Error")
        self.assertIn("Internal server error", data["message"])


if __name__ == '__main__':
    unittest.main()
