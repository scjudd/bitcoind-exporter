import json
import logging
import requests

class UnauthorizedError(Exception):
    pass

class JsonRpcCallError(Exception):
    pass

class JsonRpcClient:
    def __init__(self, endpoint, username, password):
        self.endpoint = endpoint
        self.username = username
        self.password = password

    def call(self, method, params=[]):
        headers = {'content-type': 'application/json'}

        payload = {
            'jsonrpc': '2.0',
            'id': 0,
            'method': method,
            'params': params,
        }

        logging.debug(
            "calling json-rpc method '{}' with params {}".format(
                method, params))

        response = requests.post(
            self.endpoint,
            auth=(self.username, self.password),
            headers=headers,
            data=json.dumps(payload))

        if response.status_code == 401:
            logging.warn('authorization failed')
            raise UnauthorizedError

        try:
            response = response.json()
        except ValueError:
            logging.error('json-rpc response did not contain valid json')
            raise

        if response.get('error'):
            raise JsonRpcCallError(response['error']['message'])

        return response['result']
