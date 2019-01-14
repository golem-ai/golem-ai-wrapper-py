#!/usr/bin/python3
#coding=utf-8

from golem_ai.exceptions import GConfigException
from golem_ai.log import debug, info
import random
import string
import json
import copy

class Archetype:
    id = None
    name = None
    dict_first_is_id = None
    dict_invariable = None
    regex_first_is_id = None
    dictionnary = None
    regex = None
    langs = None
    
    def __init__(self, data_json=None):
        """
        Create an archetype instance. Can be totally fill if data_json is passed
        
        :param {} data_json: (optionnal) The data corresponding to an archetype
        """
        if data_json:
            if "id" in data_json:
                self.id = data_json["id"]
            if "name" in data_json:
                self.name = data_json["name"]
            if "dict_first_is_id" in data_json:
                self.dict_first_is_id = data_json["dict_first_is_id"]
            if "dict_invariable" in data_json:
                self.dict_invariable = data_json["dict_invariable"]
            if "regex_first_is_id" in data_json:
                self.regex_first_is_id = data_json["regex_first_is_id"]
            if "dict" in data_json:
                self.dictionnary = data_json["dict"]
            if "regex" in data_json:
                self.regex = data_json["regex"]
            if "langs" in data_json:
                self.langs = data_json["langs"]
            info("Archetype {} loaded".format(self.name))
    
    def _generate_random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def generate_id(self):
        self.id = "{}-{}-{}-{}-{}".format(
            self._generate_random_string(8),
            self._generate_random_string(4),
            self._generate_random_string(4),
            self._generate_random_string(4),
            self._generate_random_string(12))
        debug("Generate an id for archetype: {} -> {}".format(self.name, self.id))

    def __str__(self):
        """
        The str representation
        
        :rtype: str
        """
        if self.name:
            if self.id:
                return "Archetype: {} ({})".format(self.name, self.id)
            return "Archetype: {}".format(self.name)
        if self.id:
            return "Archetype: {}".format(self.id)
        return "Archetype: Empty"

    def to_json(self):
        """
        Convert the object into a json format
        
        :rtype: json
        :return: The object
        """
        # If no id, generate on
        if not self.id or not len(self.id):
            self.generate_id()
        return {
            "id": self.id,
            "name": self.name,
            "dict_first_is_id": self.dict_first_is_id,
            "dict_invariable": self.dict_invariable,
            "regex_first_is_id": self.regex_first_is_id,
            "dict": self.dictionnary,
            "regex": self.regex,
            "langs": self.langs
        }

    def duplicate(self):
        """
        Create a new instance the current archetype but clear the id,
        in order to be able to add it in the Golem.ai server.
        
        :rtype: golem_ai.objects.Archetype
        :return: The new instance
        """
        new_archetype = copy.deepcopy(self)
        new_archetype.id = None
        return new_archetype