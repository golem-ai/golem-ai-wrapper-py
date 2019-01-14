#!/usr/bin/python3
#coding=utf-8

"""
This page is a sample to use the package golem_ai.
This specific page show how to check the status of the Golem.ai server
More info in the Readme.md & in the official documentation: https://golem.ai/v3/doc/
"""
from golem_ai.exceptions import GPingException
import golem_ai

# Only the "token" is madatory
config = {
    "token": YOUR_GOLEM_TOKEN, # Server Token (see golem.ai Console -> Menu -> My servers)
}

# Init the golem.ai api service (do a ping by default) (you can try/except golem_ai.exceptions.GConfigException)
golem_api = golem_ai.setup(config, ping=False)

# Ping The Golem.ai Server
try:
    golem_api.ping()
    print("The server {} is Ready".format(config["token"]))
except GPingException:
    print("The server {} is NOT Ready".format(config["token"]))
