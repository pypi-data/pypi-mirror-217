# coding: utf-8

"""
    Kiln API

    This API provides reporting staking data on various protocols as well as network wide data, staking transaction crafting features and so on.  ### ACCESS  In order to use the Kiln API, you must first get an API token from your <a href=\"https://dashboard.kiln.fi/\">Kiln dashboard</a> (applications section). If you don't have access to our dashboard, please get in touch at hello@kiln.fi.  Once you have your API token, you can set it as a bearer token in your HTTP request headers, and target the Kiln API endpoint with the current MAJOR version of the API as a prefix to routes:  <blockquote> curl \"https://api.kiln.fi/v1/...\" -H \"Authorization: Bearer $KILN_API_TOKEN\" </blockquote>  <i> If you need a development environment, please reach out to hello@kiln.fi to have a specific access to our testnet environment and dedicated API endpoint. </i>  ### CHANGELOG  <details> <summary>Preview (experimental & candidate changes for Kiln API 1.2.0) <a href=\"/preview.html\">[link]</a></summary> <ul>   <li>ETH: Add new route GET <b>/v1/eth/exit-messages</b> to get GPG encrypted exit messages</li>   <li>ATOM: Add new route GET <b>/v1/atom/reports</b> to generate an Excel report of stakes and rewards</li>   <li>ATOM: Add new route GET <b>/v1/atom/stakes</b> to to list stakes</li>   <li>ATOM: Add new route GET <b>/v1/atom/rewards</b> to list rewards</li>   <li>ATOM: Add new method POST <b>/v1/atom/stakes</b> to link a stake to a Atom account</li>   <li>ATOM: Add new route GET <b>/v1/atom/network-stats</b> to view network statistics of Atom</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/stake</b> to generate a delegation transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/withdraw-rewards</b> to generate a withdraw-rewards transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/unstake</b> to generate an undelegate transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ATOM: Add new route GET <b>/v1/atom/transaction/status</b> to view the status of a broadcasted transaction</li>   <li>ADA: Add new route GET <b>/v1/ada/reports</b> to generate an Excel report of stakes and rewards</li> </ul> </details>  <details> <summary>Version 1.1.0 (2023-06-19) <a href=\"/v1.1.0.html\">[link]</a></summary> <ul>   <li>ACCOUNTS: Add the ability to list Kiln account via GET <b>/v1/accounts</b></li>   <li>ACCOUNTS: Add the ability to create Kiln account via POST <b>/v1/accounts</b></li>   <li>ACCOUNTS: Add the ability to describe a Kiln account via GET <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to update a Kiln account via PUT <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to delete a Kiln account via DEL <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to get an account portfolio via GET <b>/v1/accounts/{id}/portfolio</b></li>    <li>ORGANIZATIONS: Add the ability to get an organization portfolio via GET <b>/v1/organizatrions/{id}/portfolio</b></li>    <li>ETH: Add the ability to query <b>/v1/eth/stakes</b>, <b>/v1/eth/rewards</b>, <b>/v1/eth/operations</b> by <b>proxies</b> and <b>validator_indexes</b></li>   <li>ETH: Add <b>validator_index</b> in the responses of <b>/v1/eth/stakes</b>, <b>/v1/eth/rewards</b> and <b>/v1/eth/operations</b></li>   <li>ETH: Add <b>delegated_at</b> field to <b>/v1/eth/stakes</b></li>   <li>ETH: Add <b>is_kiln</b> field to <b>/v1/eth/stakes</b></li>   <li>ETH: Add <b>eth_price_usd</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_entry_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_exit_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_withdrawal_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add POST method to <b>/v1/eth/stakes</b> to link a stake to a Kiln account</li>   <li>ETH: Add new route GET <b>/v1/eth/operations</b> to list on-chain operations on a stake</li>   <li>ETH: Add new route GET <b>/v1/eth/kiln-stats</b> to expose Kiln operational statistics</li>   <li>ETH: Add new route POST <b>/v1/eth/keys</b> to generate ready-to-stake deposit data payloads</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/stake</b> to generate an EIP-1559 staking transaction ready to be signed</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/prepare</b> to craft a transaction ready to be broadcast from a payload and a signature</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ETH: Add new route GET <b>/v1/eth/transaction/status</b> to get the status of a broadcasted transaction</li>   <li>ETH: Add new route GET <b>/v1/eth/reports</b> to generate an Excel report of stakes and rewards</li>    <li>XTZ: Add new route GET <b>/v1/xtz/stakes</b> to to list stakes</li>   <li>XTZ: Add new route GET <b>/v1/xtz/rewards</b> to list rewards</li>   <li>XTZ: Add new route GET <b>/v1/xtz/operations</b> to list on-chain operations of a stake</li>   <li>XTZ: Add new route GET <b>/v1/xtz/network-stats</b> to view network statistics of Tezos</li>   <li>XTZ: Add new route GET <b>/v1/xtz/reports</b> to generate an Excel report</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/stake</b> to generate a delegation transaction</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/unstake</b> to generate an undelegation transaction</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>XTZ: Add new route GET <b>/v1/xtz/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>SOL: Add new route GET <b>/v1/sol/stakes</b> to to list stakes</li>   <li>SOL: Add new method POST <b>/v1/sol/stakes</b> to link a stake to a Solana account</li>   <li>SOL: Add new route GET <b>/v1/sol/rewards</b> to list rewards</li>   <li>SOL: Add new route GET <b>/v1/sol/operations</b> to list on-chain operations of a stake</li>   <li>SOL: Add new route GET <b>/v1/sol/network-stats</b> to view network statistics of Solana</li>   <li>SOL: Add new route GET <b>/v1/sol/reports</b> to generate an Excel report</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/stake</b> to generate a delegation transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/deactivate-stake</b> to generate a deactivate transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/withdraw-stake</b> to prepare a withdraw stake transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/merge-stakes</b> to prepare a merge stakes transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/split-stake</b> to prepare a split stake transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/prepare</b> to prepare any transaction from a payload and signature</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>SOL: Add new route GET <b>/v1/sol/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>ADA: Add new route POST <b>/v1/ada/transaction/stake</b> to generate a delegation transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/withdraw-rewards</b> to generate a withdraw-rewards transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/unstake</b> to generate an undelegate transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ADA: Add new route GET <b>/v1/ada/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>MATIC: Add new route POST <b>/v1/matic/transaction/approve</b> to generate a transaction to allow a smart-contract to spend MATIC tokens on behalf of the user</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/buy-voucher</b> to generate a transaction to buy shares from a validator</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/sell-voucher</b> to generate a transaction to sell shares from a validator</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/unstake-claim-tokens</b> to generate a transaction to withdraw unbounded tokens</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/withdraw-rewards</b> to generate a transaction to withdraw rewards</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/restake-rewards</b> to generate a transaction to restake rewards</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/prepare</b> to prepare a signed transaction for broadcasting</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/broadcast</b> to broadcast a prepared transaction</li>   <li>MATIC: Add new route GET <b>/v1/matic/transaction/status</b> to view the status of a broadcasted transaction</li>  </ul> </details>  <details> <summary>Version 1.0.0 (2023-01-01) <a href=\"/v1.0.0.html\">[link]</a></summary>  <ul>   <li>ETH: Initial support of GET <b>/v1/eth/stakes</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/rewards</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/network-stats</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/keys</b> endpoint</li> </ul>  </details>  ### VERSIONING  Versions of the Kiln API use <b>MAJOR.MINOR.PATCH</b> where:  - <b>MAJOR</b> version is increased when there is major   incompatible API changes, major versions will be communicated in   advance to all customers with a smooth transition path that   spans over a minimum period of 3 MINOR versions or ~3   months. <i>Intended frequency: 1 year</i>. - <b>MINOR</b> version is increased for backward compatible API   changes without notice, or communicated breaking changes with a   1 minor version notice and a smooth migration path. Minor   versions will be communicated regularly to customers with the   changelog. <i>Intended frequency: 1 month</i>. - <b>PATCH</b> version is increased for backward compatible   hot-fixes, patch versions will be communicated to affected   customers.  <i> Due to the nature of blockchains (protocol disappearing, breaking protocol upgrades), Kiln may introduce backward-incompatible changes in MINOR versions after following a 1 MINOR version deprecation path (~1 month). These impacting changes will be narrowed as much as possible to the protocol, heavily communicated with clear guidelines and support. Customer not relying on affected protocols will not be affected. </i>  ### BACKWARD COMPATIBILITY  Kiln considers the following changes to be backward compatible:  - Adding new API routes. - Adding new optional request parameters to existing API methods. - Adding new properties to existing API responses. - Changing the order of properties in existing API responses. - Adding new event types in existing enums.  Non-breaking changes may be introduced in our API and subject to modification before being officialy communicated and documented here. Your application should not depend on them until part of this specification. The preview Kiln API specifications with upcoming and experimental new features can be found [here](/preview.html).  # noqa: E501

    The version of the OpenAPI document: Preview
    Contact: contact@kiln.fi
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import copy
import logging
import multiprocessing
import sys
import urllib3

import http.client as httplib
from kiln_connect.openapi_client.exceptions import ApiValueError

JSON_SCHEMA_VALIDATION_KEYWORDS = {
    'multipleOf', 'maximum', 'exclusiveMaximum',
    'minimum', 'exclusiveMinimum', 'maxLength',
    'minLength', 'pattern', 'maxItems', 'minItems'
}

class Configuration(object):
    """This class contains various settings of the API client.

    :param host: Base url.
    :param api_key: Dict to store API key(s).
      Each entry in the dict specifies an API key.
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is the API key secret.
    :param api_key_prefix: Dict to store API prefix (e.g. Bearer).
      The dict key is the name of the security scheme in the OAS specification.
      The dict value is an API key prefix when generating the auth data.
    :param username: Username for HTTP basic authentication.
    :param password: Password for HTTP basic authentication.
    :param access_token: Access token.
    :param server_index: Index to servers configuration.
    :param server_variables: Mapping with string values to replace variables in
      templated server configuration. The validation of enums is performed for
      variables with defined enum values before.
    :param server_operation_index: Mapping from operation ID to an index to server
      configuration.
    :param server_operation_variables: Mapping from operation ID to a mapping with
      string values to replace variables in templated server configuration.
      The validation of enums is performed for variables with defined enum values before.
    :param ssl_ca_cert: str - the path to a file of concatenated CA certificates
      in PEM format.

    :Example:
    """

    _default = None

    def __init__(self, host=None,
                 api_key=None, api_key_prefix=None,
                 username=None, password=None,
                 access_token=None,
                 server_index=None, server_variables=None,
                 server_operation_index=None, server_operation_variables=None,
                 ssl_ca_cert=None,
                 ):
        """Constructor
        """
        self._base_path = "https://api.devnet.kiln.fi" if host is None else host
        """Default Base url
        """
        self.server_index = 0 if server_index is None and host is None else server_index
        self.server_operation_index = server_operation_index or {}
        """Default server index
        """
        self.server_variables = server_variables or {}
        self.server_operation_variables = server_operation_variables or {}
        """Default server variables
        """
        self.temp_folder_path = None
        """Temp file folder for downloading files
        """
        # Authentication Settings
        self.api_key = {}
        if api_key:
            self.api_key = api_key
        """dict to store API key(s)
        """
        self.api_key_prefix = {}
        if api_key_prefix:
            self.api_key_prefix = api_key_prefix
        """dict to store API prefix (e.g. Bearer)
        """
        self.refresh_api_key_hook = None
        """function hook to refresh API key if expired
        """
        self.username = username
        """Username for HTTP basic authentication
        """
        self.password = password
        """Password for HTTP basic authentication
        """
        self.access_token = access_token
        """Access token
        """
        self.logger = {}
        """Logging Settings
        """
        self.logger["package_logger"] = logging.getLogger("kiln_connect.openapi_client")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        self.logger_format = '%(asctime)s %(levelname)s %(message)s'
        """Log format
        """
        self.logger_stream_handler = None
        """Log stream handler
        """
        self.logger_file_handler = None
        """Log file handler
        """
        self.logger_file = None
        """Debug file location
        """
        self.debug = False
        """Debug switch
        """

        self.verify_ssl = True
        """SSL/TLS verification
           Set this to false to skip verifying SSL certificate when calling API
           from https server.
        """
        self.ssl_ca_cert = ssl_ca_cert
        """Set this to customize the certificate file to verify the peer.
        """
        self.cert_file = None
        """client certificate file
        """
        self.key_file = None
        """client key file
        """
        self.assert_hostname = None
        """Set this to True/False to enable/disable SSL hostname verification.
        """
        self.tls_server_name = None
        """SSL/TLS Server Name Indication (SNI)
           Set this to the SNI value expected by the server.
        """

        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5
        """urllib3 connection pool's maximum number of connections saved
           per pool. urllib3 uses 1 connection as default value, but this is
           not the best value when you are making a lot of possibly parallel
           requests to the same host, which is often the case here.
           cpu_count * 5 is used as default value to increase performance.
        """

        self.proxy = None
        """Proxy URL
        """
        self.proxy_headers = None
        """Proxy headers
        """
        self.safe_chars_for_path_param = ''
        """Safe chars for path_param
        """
        self.retries = None
        """Adding retries to override urllib3 default value 3
        """
        # Enable client side validation
        self.client_side_validation = True

        self.socket_options = None
        """Options to pass down to the underlying urllib3 socket
        """

        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        """datetime format
        """

        self.date_format = "%Y-%m-%d"
        """date format
        """

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k not in ('logger', 'logger_file_handler'):
                setattr(result, k, copy.deepcopy(v, memo))
        # shallow copy of loggers
        result.logger = copy.copy(self.logger)
        # use setters to configure loggers
        result.logger_file = self.logger_file
        result.debug = self.debug
        return result

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    @classmethod
    def set_default(cls, default):
        """Set default instance of configuration.

        It stores default configuration, which can be
        returned by get_default_copy method.

        :param default: object of Configuration
        """
        cls._default = default

    @classmethod
    def get_default_copy(cls):
        """Deprecated. Please use `get_default` instead.

        Deprecated. Please use `get_default` instead.

        :return: The configuration object.
        """
        return cls.get_default()

    @classmethod
    def get_default(cls):
        """Return the default configuration.

        This method returns newly created, based on default constructor,
        object of Configuration class or returns a copy of default
        configuration.

        :return: The configuration object.
        """
        if cls._default is None:
            cls._default = Configuration()
        return cls._default

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        return self.__logger_file

    @logger_file.setter
    def logger_file(self, value):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        self.__logger_file = value
        if self.__logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in self.logger.items():
                logger.addHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self.__debug = value
        if self.__debug:
            # if debug status is True, turn on debug logging
            for _, logger in self.logger.items():
                logger.setLevel(logging.DEBUG)
            # turn on httplib debug
            httplib.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in self.logger.items():
                logger.setLevel(logging.WARNING)
            # turn off httplib debug
            httplib.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(self, identifier, alias=None):
        """Gets API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :param alias: The alternative identifier of apiKey.
        :return: The token for api key authentication.
        """
        if self.refresh_api_key_hook is not None:
            self.refresh_api_key_hook(self)
        key = self.api_key.get(identifier, self.api_key.get(alias) if alias is not None else None)
        if key:
            prefix = self.api_key_prefix.get(identifier)
            if prefix:
                return "%s %s" % (prefix, key)
            else:
                return key

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        username = ""
        if self.username is not None:
            username = self.username
        password = ""
        if self.password is not None:
            password = self.password
        return urllib3.util.make_headers(
            basic_auth=username + ':' + password
        ).get('authorization')

    def auth_settings(self):
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        auth = {}
        if self.access_token is not None:
            auth['bearerAuth'] = {
                'type': 'bearer',
                'in': 'header',
                'key': 'Authorization',
                'value': 'Bearer ' + self.access_token
            }
        return auth

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: Preview\n"\
               "SDK Package Version: 1.0.0".\
               format(env=sys.platform, pyversion=sys.version)

    def get_host_settings(self):
        """Gets an array of host settings

        :return: An array of host settings
        """
        return [
            {
                'url': "https://api.devnet.kiln.fi",
                'description': "No description provided",
            },
            {
                'url': "https://api.testnet.kiln.fi",
                'description': "No description provided",
            },
            {
                'url': "https://api.mainnet.kiln.fi",
                'description': "No description provided",
            }
        ]

    def get_host_from_settings(self, index, variables=None, servers=None):
        """Gets host URL based on the index and variables
        :param index: array index of the host settings
        :param variables: hash of variable and the corresponding value
        :param servers: an array of host settings or None
        :return: URL based on host settings
        """
        if index is None:
            return self._base_path

        variables = {} if variables is None else variables
        servers = self.get_host_settings() if servers is None else servers

        try:
            server = servers[index]
        except IndexError:
            raise ValueError(
                "Invalid index {0} when selecting the host settings. "
                "Must be less than {1}".format(index, len(servers)))

        url = server['url']

        # go through variables and replace placeholders
        for variable_name, variable in server.get('variables', {}).items():
            used_value = variables.get(
                variable_name, variable['default_value'])

            if 'enum_values' in variable \
                    and used_value not in variable['enum_values']:
                raise ValueError(
                    "The variable `{0}` in the host URL has invalid value "
                    "{1}. Must be {2}.".format(
                        variable_name, variables[variable_name],
                        variable['enum_values']))

            url = url.replace("{" + variable_name + "}", used_value)

        return url

    @property
    def host(self):
        """Return generated host."""
        return self.get_host_from_settings(self.server_index, variables=self.server_variables)

    @host.setter
    def host(self, value):
        """Fix base path."""
        self._base_path = value
        self.server_index = None
