#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Christian Fender"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Christian Fender"
__email__ = "info@fenderdev.com"

import logging

import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


class Secvest(object):

    DEFAULT_PORT = 4433
    HEADERS = {'Authorization': 'Basic Tk80MDE6Tk80MDE='}

    FORM_FIELD_USER = 'usr'
    FORM_FIELD_PASS = 'pwd'

    PATH_INDEX = '/index.html'
    PATH_LOGIN = '/sec_login.cgi'
    PATH_SYSTEM = '/system/'
    PATH_PARTITIONS = '/system/partitions/'
    PATH_PARTITION = '/system/partition-%i'

    SSID = 'ssid'
    NO_SSID = '0'

    STATE_UNSET = 'unset'
    STATE_SET = 'set'
    STATE_PARTSET = 'partset'

    def __init__(self, hostname=None, username=None, password=None, port=DEFAULT_PORT):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.cookies = dict()
        self.__authenticate__()

    def __authenticate__(self):
        response = requests.post(self.__build_uri_for_path__(Secvest.PATH_LOGIN),
                                 headers=Secvest.HEADERS,
                                 data={Secvest.FORM_FIELD_USER: self.username,
                                       Secvest.FORM_FIELD_PASS: self.password},
                                 verify=False,
                                 cookies=self.cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.cookies[Secvest.SSID] = soup.find_all('input', attrs={'id': Secvest.SSID})[0]['value']
        if self.cookies[Secvest.SSID] == Secvest.NO_SSID:
            raise SecvestException('Login on Secvest Failed! Either the user is logged, or your credentials are wrong.')
        else:
            logging.debug('Logged in with SSID %s' % self.cookies[Secvest.SSID])

    def __logout__(self):
        logging.debug('Logging out from Secvest')
        requests.post(self.__build_uri_for_path__(Secvest.PATH_INDEX),
                      headers=Secvest.HEADERS,
                      data={'logout': 'logout', Secvest.SSID: ''},
                      cookies=self.cookies,
                      verify=False)

    def __build_base_uri__(self):
        return 'https://%s:%i' % (self.hostname, self.port)

    def __build_uri_for_path__(self, path):
        return self.__build_base_uri__() + path

    def get_system(self):
        """
        Method returns the name and the partitions of the secvest.
        Example:
        {
            "name": "My Secvest",
            "partitions": [
                "1",
                "2",
                "3",
                "4"
            ]
        }
        :return: The system info
        :rtype: dict
        """
        response = requests.get(self.__build_uri_for_path__(Secvest.PATH_PARTITIONS),
                                headers=Secvest.HEADERS,
                                cookies=self.cookies,
                                verify=False)
        return response.json()

    def get_partition(self, partition=1):
        """
        Gets information about a certain state.
        Example:
        {
            "id": "1",
            "name": "Living Room",
            "state": "set",
            "zones": [
                "202",
                "203"
            ]
        }
        :param partition:
        :return: A partition
        :rtype: dict
        """
        if partition < 1 or partition > 4:
            raise SecvestException('Only partitions 1-4 available')
        response = requests.get(self.__build_uri_for_path__(Secvest.PATH_PARTITION % partition),
                                headers=Secvest.HEADERS,
                                cookies=self.cookies,
                                verify=False)
        return response.json()

    def get_partitions(self):
        """
        Method gets a list of partitions, with their name, state and the assigned zones.
        Example:
        [
            {
                "id": 1,
                "name": "Living Room",
                "state": "unset",
                "zones": [
                    "201",
                    "202"]
            },
            ...
        ]
        :return: A list of partitions
        :rtype: list
        """
        response = requests.get(self.__build_uri_for_path__(Secvest.PATH_PARTITIONS),
                                headers=Secvest.HEADERS,
                                cookies=self.cookies,
                                verify=False)
        return response.json()

    def logout(self):
        """
        Logs out from the current session.
        :return: void
        :rtype: None
        """
        self.__logout__()


class SecvestException(Exception):
    pass