#!/usr/bin/python3
#coding=utf-8

"""
This module is included in the package golem_ai.
It is composed by a list of method use to manage the network communication
with the Golem.ai API / Golem.ai Console API
"""

from .log import debug, warning, info
from .exceptions import GConfigException
from .config import VERSION, DEFAULT_GOLEM_SERVER, DEFAULT_GOLEM_SERVER_CONSOLE
import requests
import random
import string
import json
import os

GOLEM_SERVER = DEFAULT_GOLEM_SERVER if not "GOLEM_SERVER" in os.environ else str(os.environ["GOLEM_SERVER"])
GOLEM_SERVER_CONSOLE = DEFAULT_GOLEM_SERVER_CONSOLE if not "GOLEM_SERVER_CONSOLE" in os.environ else str(os.environ["GOLEM_SERVER_CONSOLE"])

def _parse_response(url, response):
    """
    Parse the golem API request response, in order to detect error and extract the reason if any
    
    :param str url: The sub url to call
    :param requests.Response response: The response to parse
    :rtype: (bool, str|{})
    :return: A simple request result (True/False), The message return or the obj if json.
    """
    try:
        json_data = json.loads(response.text)
    except:
        warning("Request failure ({}), because :{}".format(url, response.text))
        return False, str(response.text)
    try:
        # Check status code or "status" in API response
        if int(response.status_code / 100) != 2 or ("status" in json_data and json_data["status"] != "ok"):
            warning("Request failure ({}), because :{}".format(url, json_data))
            return False, json_data
        # Check "error_message" in API response
        if "error_message" in json_data:
            warning("Request failure ({}), because :{}".format(url, json_data["error_message"]))
            return False, json_data["error_message"]
        # No error detected
        debug("Request success, {}".format(json_data))
        return True, json_data
    except Exception as err:
        # Exception
        warning("Request failure ({}), because :{}".format(url, err))
        return False, str(err)

def _get_header():
    """
    Get the header to use in a request
    
    :rtype: {}
    :return: The header for the request
    """
    return {
        'user-agent': 'golem-ai-wrapper-py/{}'.format(VERSION),
        'content-type': 'application/json'
    }

def _prepare_data_for_form(data, headers):
    """
    Format a form to send informations
    
    :param {} data: The data to format and add into the form
    :param {} headers: The headers partially completed
    :rtype: ({}, str)
    :return: The headers ready for the request, the payload (formatted data)
    """
    boundary = "----WebKitFormBoundary" + ''.join(random.choice(string.digits) for _ in range(15))
    payload = "--" + boundary + "\nContent-Disposition: form-data; name=\"json\"\n\n"
    payload += json.dumps(data) + "\n"
    payload += "--" + boundary + "--"
    headers["content-type"] = "multipart/form-data; boundary={}".format(boundary)
    return headers, payload

def post(url, json_data=None, form=None, extra_info=None):
    """
    Execute a POST request to the Golem.ai server.
    To change de server address, see var env GOLEM_SERVER.
    
    :param str url: The sub url to call
    :param {} json_data: The json data to send on the request
    :rtype: (bool, str|{})
    :return: A simple request result (True/False), The message return or the obj if json. See _parse_response()
    """
    debug("Post Request to '{}{}' with data: {}".format(GOLEM_SERVER, url, str(json_data)))
    try:
        # Setup Headers
        headers = _get_header()
        server = GOLEM_SERVER
        if url.find("console/api") != -1:
            # Use console api so need phpsessionid in extra_info
            if not extra_info or not "php_session_id" in extra_info:
                # Exception
                raise GConfigException("Cannot perform request to API Console ({}) because, 'php_session_id' field is missing".format(url))
            # Add Cookies + Reset Port
            headers["Cookie"] = "PHPSESSID={}".format(extra_info["php_session_id"])
            server = GOLEM_SERVER_CONSOLE
        if form:
            headers, form = _prepare_data_for_form(form, headers)
        # Execute the Request
        response = requests.post("{}{}".format(server, url), json=json_data, data=form, headers=headers)
        return _parse_response(url, response)
    except Exception as err:
        # Exception
        warning("Request failure ({}), because :{}".format(url, err))
        return False, str(err)

def get(url, json_data=None, extra_info=None):
    """
    Execute a GET request to the Golem.ai server.
    To change de server address, see var env GOLEM_SERVER.
    
    :param str url: The sub url to call
    :param {} json_data: The json data to send on the request
    :param {} extra_info: Some info like the php_session_id to use the API Console
    :raise GConfigException: If php_session_id or mandatory info is missing
    :rtype: (bool, str|{})
    :return: A simple request result (True/False), The message return or the obj if json. See _parse_response()
    """
    debug("Post Request to '{}{}' with data: {} / extra info: {}".format(GOLEM_SERVER, url, str(json_data), extra_info))
    try:
        # Setup Headers
        headers = _get_header()
        server = GOLEM_SERVER
        if url.find("console/api") != -1:
            # Use console api so need phpsessionid in extra_info
            if not extra_info or not "php_session_id" in extra_info:
                # Exception
                raise GConfigException("Cannot perform request to API Console ({}) because, 'php_session_id' field is missing".format(url))
            # Add Cookies + Change the server
            headers["Cookie"] = "PHPSESSID={}".format(extra_info["php_session_id"])
            server = GOLEM_SERVER_CONSOLE
        # Execute the Request
        response = requests.get("{}{}".format(server, url), json=json_data, headers=headers)
        return _parse_response(url, response)
    except Exception as err:
        # Exception
        warning("Request failure ({}), because :{}".format(url, err))
        return False, str(err)