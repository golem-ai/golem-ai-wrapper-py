#!/usr/bin/python3
#coding=utf-8

"""
This page is a sample to use the package golem_ai.
This specific page show how to connect to a Golem.ai server and send a request.
More info in the Readme.md & in the official documentation: https://golem.ai/v3/doc/
"""

import golem_ai

# The config
# Only the "token" is madatory
config = {
    "token": YOUR_GOLEM_TOKEN, # Server Token (see golem.ai Console -> Menu -> My servers)
    "language": "fr", # "Default: "fr"
    "labelling": True, # Default: True
    "parameters_detail": False, # Default: False
    "disable_verbose": False, # Default: False
    "multiple_interaction_search": False, # Default: False
    "conversation_mode": False # Default: False
}

# Init the golem.ai api service (do a ping by default) (you can try/except golem_ai.exceptions.GConfigException)
golem_api = golem_ai.setup(config)

# Call Golem.ai with a text to analyse according the config set previously
call_analysis = golem_api.call("Can you turn on the light in kitchen and make me a coffee?")

print(call_analysis)