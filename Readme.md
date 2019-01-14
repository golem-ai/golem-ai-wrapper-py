# Wrapper Python Golem.ai API

This package is simplifying the usage a the Golem.ai API (Public + Console)

## General

* Version Package: 0.0.1
* Maintainer: Damien Delbos (Golem.ai)

## Installation

* Copy the golem_ai folder in your project and add `import golem_ai`

## Usage

Several sample file are available in this repository, in order to show how to use the Wrapper.

### Basic

```
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

# Init the golem.ai api service (do a ping by default)
golem_api = golem_ai.setup(config)

# Call Golem.ai with a text to analyse according the config set previously
call_analysis = golem_api.call("Can you turn on the light in kitchen and make me a coffee?")

print(call_analysis)
```

### Archetype

```
from golem_ai.objects.archetype import Archetype
import golem_ai

# Only the "php_session_id" is madatory in this case
config = {
    "php_session_id": YOUR_GOLEM_CONSOLE_PHPSESSID # The PHP SESSION ID (Look into your Cookie after login on https://golem.ai/login)
}

# Init the golem.ai api service without check the server status (so no need token)
golem_api = golem_ai.setup(config, ping=False)

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

```

## Features

### Config

* `setup(config, ping=True)`: Get a API instance according a specific config. You can also disable the server ping test.

### Public

* `call(msg)`: A basic call to the API to get the analysis. Need Token
* `ping()`: Ping a server and raise an **GPingException** if the server is not available. Need Token

### Archetypes

* `get_archetypes()`: Get all archetypes on the account. Need PHPSESSID (php-session-id)
* `add_archetype(archetype)`: Add an archetype on the account. Need PHPSESSID (php-session-id)

## Custom Config

### Log

To enable the log, use the environnement variable GOLEM_LOG. If the folder doesn't exist it will be created (if possible) otherwith a **GConfigException** will be raised. The following files will be created and filled according the level:
`golem_ai-error.log`, `golem_ai-full.log`, `golem_ai-info.log`.

ex:
```
echo $GOLEM_LOG
/tmp
```

### Golem Server

To set a custom golem server address, use environnement variable GOLEM_SERVER.

ex: 
```
echo $GOLEM_SERVER
https://golem.ai:3005
```

### Golem Server Console

To set a custom golem console server, use environnement variable GOLEM_SERVER_CONSOLE.

ex: 
```
echo $GOLEM_SERVER_CONSOLE
https://golem.ai
```

## In the Future

* Add feature for archetypes (`delete_archetype`, `edit_archetype`) _(Soon)_
* Add features to the Archetype object (`build_from_list(archetypes)`, `add_archetype_dict(lang, row)`) _(Soon)_
* Start/Stop a server (`start_server()`, `stop_server()`) _(Soon)_
* Remove the php-session-id _(Once the console API will be reworked)_
* Support the **Conversation Mode** _(Not yet available in Production)_
* Create objects Context/Interaction object and Add feature for Context (`enable_interaction(Interaction)`) _(Once the console API will be reworked)_
