from golem_ai.main import GolemAI
from .log import setup as setup_logging

def setup(config, ping=True):
    """
    Setup a GolemAI instance, in order to exchange with Golem.ai API

    :param Config token: The server config, must include at least the token
    :param bool connect: To try if the server is online and valid
    :raise GolemAIInvalidConfig: If the configuration is invalid
    :raise GolemAIServerConnection: If the server cannot be reach, mainly because the token
    :raise GolemAIMaintenance: If the service is in maintenance
    :rtype: GolemAI
    :return: The API wrapper instance
    """
    setup_logging()
    default_config = {
        "language": "fr",
        "labelling": True,
        "parameters_detail": False,
        "disable_verbose": False,
        "multiple_interaction_search": False,
        "conversation_mode": False
    }
    default_config.update(config)
    api = GolemAI(default_config)
    if ping:
        api.ping()
    return api
