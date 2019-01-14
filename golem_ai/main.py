#!/usr/bin/python3
#coding=utf-8

"""
This module is included in the package golem_ai.
It is composed by the definition of the main class GolemAI to use the Golem.ai API
"""

from .exceptions import GConfigException, GPingException, GRequestException
from .network import post, get
from .log import critical, error, info, debug
import json

class GolemAI:
    token = None # Faster than config["token"]
    config = None
    extra_info = {} # Generated in __init__ with config

    def __init__(self, config):
        """
        Constructor for the GolemAI object, one instance is one API config. To change use another instance
        
        :param {} config: The API config. See the documentation for more details
        :rtype: type
        :return: definition
        """
        debug("GolemAI() config: {}".format(config))
        if "php_session_id" in config:
            self.extra_info["php_session_id"] = config["php_session_id"]
            del config["php_session_id"]
        if "token" in config:
            self.token = config["token"]
        self.config = config
        info("GolemAI() successfully setup")

    def call(self, msg):
        """
        Execute a call request to the API
        
        :param str msg: The message to send
        :raise GConfigException: If config is invalid
        :raise GRequestException: When there is an exception on the request
        :rtype: {}
        :return: The analysis of the message. More info on https://golem.ai/v3/doc/
        """
        # Need Token
        if not self.token:
            raise GConfigException("'token' field is missing")
        debug("call() server '{}' msg: '{}'".format(self.token, msg))
        # Setup header
        data_header = self.config.copy()
        data_header["text"] = msg
        data_header["type"] = "request"
        # Send a call request
        res, data_json = post("/http", data_header)
        debug("call() server '{}' header: {} result: {}".format(self.token, data_header,  data_json))
        if not res:
            # Error
            raise GRequestException("call() server '{}'".format(self.token))
        info("call() server '{}' msg: '{}' success".format(self.token, msg))
        return data_json

    def ping(self):
        """
        Ping a Golem.ai server, to get his status.
        Use the token.
        
        :raise GConfigException: If config is invalid
        :raise GPingException: If the server is not available
        """
        # Need Token
        if not self.token:
            raise GConfigException("'token' field is missing")
        debug("ping() server '{}'".format(self.token))
        # Send a ping request
        res, txt = post("/http", {"type": "ping", "token": self.token})
        debug("ping() server '{}' response: {}".format(self.token, txt))
        if not res:
            # Error
            raise GPingException(self.token)
        info("ping() server '{}' ping success".format(self.token))

    def get_archetypes(self):
        """
        Get all archetypes on the account, using the Golem.ai console.
        Use the php-session-id.
        
        :raise GConfigException: If config is invalid
        :raise GRequestException: If the request fail
        """
        debug("get_archetypes()")
        # Need php_session_id
        if not "php_session_id" in self.extra_info:
            raise GConfigException("'php_session_id' field is missing")
        # Send a call request
        res, data_json = get("/v3/console/api/user/archetypes", extra_info=self.extra_info)
        debug("get_archetypes() response: {}".format(data_json))
        if not res:
            # Error
            raise GRequestException("get_archetypes()")
        info("get_archetypes() result: {} archetype(s) found".format(len(data_json["message"])))
        return data_json["message"]

    def add_archetype(self, archetype):
        """
        Add an archetype on the account, using the Golem.ai console.
        Use the php-session-id.
        
        :param golem.Archetype archetype: The archetype to add
        :raise GConfigException: If config is invalid
        :raise GRequestException: If the request fail
        """
        debug("add_archetypes(): {}".format(archetype))
        # Need php_session_id
        if not "php_session_id" in self.extra_info:
            raise GConfigException("'php_session_id' field is missing")
        # Send a post request
        res, txt = post("/v3/console/api/user/archetype", form=archetype.to_json(), extra_info=self.extra_info)
        debug("add_archetypes(): {} response: {}".format(archetype, txt))
        if not res:
            # Error
            raise GRequestException(archetype.to_json())
        info("add_archetypes(): {}".format(archetype))
