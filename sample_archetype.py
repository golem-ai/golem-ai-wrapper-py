#!/usr/bin/python3
#coding=utf-8

"""
This page is a sample to use the package golem_ai.
This specific page show how to deal with Archetype.
More info in the Readme.md & in the official documentation: https://golem.ai/v3/doc/
"""

from golem_ai.objects.archetype import Archetype
from golem_ai.exceptions import GRequestException
import golem_ai

# Only the "php_session_id" is madatory in this case
config = {
    "php_session_id": YOUR_GOLEM_CONSOLE_PHPSESSID # The PHP SESSION ID (Look into your Cookie after login on https://golem.ai/login)
}

# Init the golem.ai api service without check the server status (so no need token)
golem_api = golem_ai.setup(config, ping=False)

# Call Golem.ai Console API to get all archetypes on your account (php_session_id)
golem_response = golem_api.get_archetypes()

# Add an archetype
my_archetype = Archetype({
	"name":"team_member",
	"dict_first_is_id": False,
	"dict_invariable": False,
	"regex_first_is_id": False,
	"langs":["en","fr"],    
	"dict": {
        "en":"Raphael\nBenjamin\nDamien\nCélia\nUlysse\nAmin\nThomas\nTiphaine\nGuillaume\nJocelyn\nSahra\nKillian\nCatherine",
        "fr":"Raphael\nBenjamin\nDamien\nCélia\nUlysse\nAmin\nThomas\nTiphaine\nGuillaume\nJocelyn\nSahra\nKillian\nCatherine"
    },
	"regex":{
        "en":"",
        "fr":""
    }
})
# Add the archetype
golem_api.add_archetype(my_archetype)

try:
    # Atempt to add the same archetype a second time (must fail)
    golem_api.add_archetype(my_archetype)
    print("ERROR: No failure detected")
except GRequestException:
    print("SUCCESS: The archetype cannot be added")

# Duplicate it
my_archetype2 = my_archetype.duplicate()
my_archetype2.name = "my_name_archetype2"

# Add the archetype 2
golem_api.add_archetype(my_archetype2)
