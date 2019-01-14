#!/usr/bin/python3
#coding=utf-8

"""
This module is included in the package golem_ai.
It is composed by a list of specific exception,
used in this package.
"""
import os
from .log import get_log_details

class GDefaultException(RuntimeError):
    """
    Exception for a Golem.ai API error.

    :param string arg: Exception message
    :keywords: exception, default
    """
    classname = None
    msg = None

    def __init__(self, classname, msg):
        super(GDefaultException, self).__init__()
        self.msg = msg
        self.classname = classname

    def __str__(self):
        """
        Format for str()

        :return: The formated excpetion message
        :rtype: string
        """
        log_is_enable, log_path = get_log_details()
        if log_is_enable:
            return "{}: {} (see more in log folder '{}')".format(self.classname, self.msg, log_path)
        return "{}: {}".format(self.classname, self.msg)


class GConfigException(GDefaultException):
    """
    Exception for a config error

    :param string arg: Exception message
    :keywords: exception, config
    """

    def __init__(self, arg):
        super(GConfigException, self).__init__(self.__class__.__name__, arg)


class GPingException(GDefaultException):
    """
    Exception for a server ping error
    :param string arg: Exception message
    :keywords: exception, ping
    """

    def __init__(self, arg):
        super(GPingException, self).__init__(self.__class__.__name__, arg)


class GRequestException(GDefaultException):
    """
    Exception for a server call error
    :param string arg: Exception message
    :keywords: exception, request
    """

    def __init__(self, arg):
        super(GRequestException, self).__init__(self.__class__.__name__, arg)