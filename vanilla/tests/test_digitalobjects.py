# -*- coding: utf-8 -*-

"""
Test dataobjects endpoints

Run single test:
nose2 test.custom.test_dataobjects.TestDataObjects.test_07_delete_dataobjects
"""

from __future__ import absolute_import

import io
# from restapi.jsonify import json
from .. import RestTestsAuthenticatedBase
from commons.logs import get_logger

__author__ = 'Roberto Mucci (r.mucci@cineca.it)'

logger = get_logger(__name__, True)


class TestDigitalObjects(RestTestsAuthenticatedBase):

    _main_endpoint = '/namespace'
    _irods_path = '/tempZone/home/guest/test'
    _invalid_irods_path = '/tempZone/home/x/guest/test'
    _test_filename = 'test.pdf'

    def test_01_post_create_test_directory(self):
        """ Test directory creation: POST """

        logger.info('*** Testing POST')
        # Create a directory
        endpoint = self._api_uri + self._main_endpoint
        r = self.app.post(endpoint, data=dict(path=self._irods_path),
                          headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Overwrite a directory
        r = self.app.post(endpoint, data=dict(path=self._irods_path,
                          force='True'), headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Overwrite a directory w/o force flag
        r = self.app.post(endpoint, data=dict(path=self._irods_path),
                          headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

        # Create a directory in a non existing path
        r = self.app.post(endpoint, data=dict(path=self._invalid_irods_path),
                          headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

        # Create a directory w/o passing a path
        r = self.app.post(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(
            r.status_code, self._hcodes.HTTP_BAD_METHOD_NOT_ALLOWED)

    def test_02_put_upload_entity(self):
        """ Test file upload: PUT """

        logger.info('*** Testing PUT')
        # Upload entity in test folder
        endpoint = self._api_uri + self._main_endpoint + self._irods_path
        r = self.app.put(endpoint, data=dict(
                         file=(io.BytesIO(b"this is a test"),
                               self._test_filename)),
                         headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Overwrite entity in test folder
        r = self.app.put(endpoint, data=dict(
                         file=(io.BytesIO(b"this is a test"),
                               self._test_filename), force='True'),
                         headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Overwrite entity in test folder w/o force flag
        r = self.app.put(endpoint, data=dict(
                         file=(io.BytesIO(b"this is a test"),
                               self._test_filename)),
                         headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

        # Upload entity w/o passing a file
        r = self.app.put(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(
            r.status_code, self._hcodes.HTTP_BAD_METHOD_NOT_ALLOWED)

        # Upload entity in a non existing path
        endpoint = self._api_uri + \
            self._main_endpoint + self._invalid_irods_path
        r = self.app.put(endpoint, data=dict(
                         file=(io.BytesIO(b"this is a test"),
                               self._test_filename)),
                         headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

    def test_03_get_entities(self):
        """ Test the entity listingend retrieval: GET """

        logger.info('*** Testing GET')
        # GET non existing entity
        endpoint = (self._api_uri + self._main_endpoint +
                    self._irods_path + '/' + self._test_filename)
        r = self.app.get(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_NOTFOUND)

        ###################################################
        # I need to upload some data to test the DELETE..
        # Create a directory
        endpoint = self._api_uri + self._main_endpoint
        r = self.app.post(endpoint, data=dict(path=self._irods_path),
                          headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Upload entity in test folder
        endpoint = self._api_uri + self._main_endpoint + self._irods_path
        r = self.app.put(endpoint, data=dict(
                         file=(io.BytesIO(b"this is a test"),
                               self._test_filename)),
                         headers=self.__class__.auth_header)
        ###################################################

        # Obtain entity metadata
        endpoint = (self._api_uri + self._main_endpoint +
                    self._irods_path + '/' + self._test_filename)
        r = self.app.get(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Get list of entities in a directory
        endpoint = self._api_uri + self._main_endpoint + self._irods_path
        r = self.app.get(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Download an entity
        endpoint = (self._api_uri + self._main_endpoint +
                    self._irods_path + '/' + self._test_filename)
        r = self.app.get(endpoint, data=dict(download='True'),
                         headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
        self.assertEqual(r.data, b'this is a test')

    def test_04_delete_entities(self):
        """ Test the entity delete: DELETE """

        ###################################################
        # I need to upload some data to test the DELETE..
        # Create a directory
        endpoint = self._api_uri + self._main_endpoint
        r = self.app.post(endpoint, data=dict(path=self._irods_path),
                          headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Upload entity in test folder
        endpoint = self._api_uri + self._main_endpoint + self._irods_path
        r = self.app.put(endpoint, data=dict(
                         file=(io.BytesIO(b"this is a test"),
                               self._test_filename)),
                         headers=self.__class__.auth_header)
        ###################################################

        logger.info('*** Testing DELETE')
        # Delete non empty directory
        endpoint = self._api_uri + self._main_endpoint + self._irods_path
        r = self.app.delete(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

        # Delete entity
        endpoint = (self._api_uri + self._main_endpoint + self._irods_path +
                    '/' + self._test_filename)
        r = self.app.delete(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Delete directory
        endpoint = self._api_uri + self._main_endpoint + self._irods_path
        r = self.app.delete(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

        # Delete non existing entity
        endpoint = (self._api_uri + self._main_endpoint + self._irods_path +
                    '/' + self._test_filename + 'x')
        r = self.app.delete(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_NOTFOUND)
        # HTTP_BAD_NOTFOUND is more appropriate

        # Delete non existing directory
        endpoint = self._api_uri \
            + self._main_endpoint + self._invalid_irods_path
        r = self.app.delete(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_NOTFOUND)

        # Delete w/o passing a path
        endpoint = self._api_uri + self._main_endpoint
        r = self.app.delete(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

        ##############################
        ## OLD NOTES:

        # create directory

        # upload a file

        # upload a file force

        # upload a big file

        # list content

        # download a file

        # remove previous files

        # remove empty directory
        ##############################

#     def test_05_get_dataobjects(self):
#         """ Test file download: GET """

#         objURI = os.path.join(self._api_uri, 'dataobjects', self.__class__.small)
#         r = self.app.get(objURI, headers=self.auth_header)
#         self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
#         # Verify file content
#         self.assertEqual(r.data, b'a test again')

#     def test_06_get_large_dataobjects(self):
#         """ Test file download: GET """
#         objURI = os.path.join(self._api_uri, 'dataobjects', self.__class__.large)
#         r = self.app.get(objURI, headers=self.auth_header)
#         self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

#     def test_07_post_already_existing_dataobjects(self):
#         """ Test file upload with already existsing object: POST """
#         r = self.app.post(
#             self._api_uri + '/dataobjects',
#             headers=self.auth_header,
#             data=dict(file=(io.BytesIO(b"this is a test"), 'test.pdf')))
#         # content = json.loads(r.data.decode('utf-8'))
#         # error_message = content['Response']['errors']
#         # logger.debug(error_message)
#         self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)  # or 409?

# ## // TO FIX:
# # If tests fails before the next method,
# # you will find your self with data already existing on irods
# # which will lead to errors also when tests are good

# # Maybe we could add a method which finds data and removes it
# # at 'init time' of the class.

#     def test_08_delete_dataobjects(self):
#         """ Test file delete: DELETE """

#         URI = os.path.join(self._api_uri, 'dataobjects')

#         # Obtain the list of objects end delete
#         r = self.app.get(URI, headers=self.auth_header)
#         self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
#         content = json.loads(r.data.decode('utf-8'))

#         # Find the path
#         data = content['Response']['data']['content']
#         for obj in data:
#             deleteURI = os.path.join(URI, obj['id'])
#             r = self.app.delete(deleteURI, headers=self.auth_header)
#             self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

#     def test_09_delete_nonexisting_dataobjects(self):
#         """ Test fake file delete: DELETE """

#         URI = os.path.join(self._api_uri, 'dataobjects', 'NonExistingUUID')
#         r = self.app.get(URI, headers=self.auth_header)
#         self.assertEqual(r.status_code, self._hcodes.HTTP_SERVER_ERROR)

#     def test_10_post_dataobjects_in_non_existing_collection(self):
#         """ Test file upload in a non existing collection: POST """

#         URI = os.path.join(self._api_uri, 'dataobjects')
#         r = self.app.post(
#             URI, headers=self.auth_header,
#             data=dict(collection=('/home/wrong/path'),
#                       file=(io.BytesIO(b"this is a test"), 'test.pdf')))
#         self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)  # or 409?
#         content = json.loads(r.data.decode('utf-8'))
#         error_message = content['Response']['errors'][0]['iRODS']
#         self.assertIn('collection does not exist', error_message)

#     def test_11_get_non_exising_dataobjects(self):
#         """ Test file download of a non existing object: GET """

#         filename = 'test.pdf'
#         URI = os.path.join(self._api_uri, 'dataobjects', filename)

#         r = self.app.get(
#             URI, headers=self.auth_header,
#             data=dict(collection=('/home/guest')))
#         self.assertEqual(r.status_code, self._hcodes.HTTP_SERVER_ERROR)  # or 404?

#         content = json.loads(r.data.decode('utf-8'))
#         error_messages = content['Response']['errors'].pop()
#         self.assertIn('Not found.', error_messages[filename])
