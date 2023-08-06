# coding: utf-8

"""
    Kiln API

    This API provides reporting staking data on various protocols as well as network wide data, staking transaction crafting features and so on.  ### ACCESS  In order to use the Kiln API, you must first get an API token from your <a href=\"https://dashboard.kiln.fi/\">Kiln dashboard</a> (applications section). If you don't have access to our dashboard, please get in touch at hello@kiln.fi.  Once you have your API token, you can set it as a bearer token in your HTTP request headers, and target the Kiln API endpoint with the current MAJOR version of the API as a prefix to routes:  <blockquote> curl \"https://api.kiln.fi/v1/...\" -H \"Authorization: Bearer $KILN_API_TOKEN\" </blockquote>  <i> If you need a development environment, please reach out to hello@kiln.fi to have a specific access to our testnet environment and dedicated API endpoint. </i>  ### CHANGELOG  <details> <summary>Preview (experimental & candidate changes for Kiln API 1.2.0) <a href=\"/preview.html\">[link]</a></summary> <ul>   <li>ETH: Add new route GET <b>/v1/eth/exit-messages</b> to get GPG encrypted exit messages</li>   <li>ATOM: Add new route GET <b>/v1/atom/reports</b> to generate an Excel report of stakes and rewards</li>   <li>ATOM: Add new route GET <b>/v1/atom/stakes</b> to to list stakes</li>   <li>ATOM: Add new route GET <b>/v1/atom/rewards</b> to list rewards</li>   <li>ATOM: Add new method POST <b>/v1/atom/stakes</b> to link a stake to a Atom account</li>   <li>ATOM: Add new route GET <b>/v1/atom/network-stats</b> to view network statistics of Atom</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/stake</b> to generate a delegation transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/withdraw-rewards</b> to generate a withdraw-rewards transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/unstake</b> to generate an undelegate transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ATOM: Add new route GET <b>/v1/atom/transaction/status</b> to view the status of a broadcasted transaction</li>   <li>ADA: Add new route GET <b>/v1/ada/reports</b> to generate an Excel report of stakes and rewards</li> </ul> </details>  <details> <summary>Version 1.1.0 (2023-06-19) <a href=\"/v1.1.0.html\">[link]</a></summary> <ul>   <li>ACCOUNTS: Add the ability to list Kiln account via GET <b>/v1/accounts</b></li>   <li>ACCOUNTS: Add the ability to create Kiln account via POST <b>/v1/accounts</b></li>   <li>ACCOUNTS: Add the ability to describe a Kiln account via GET <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to update a Kiln account via PUT <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to delete a Kiln account via DEL <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to get an account portfolio via GET <b>/v1/accounts/{id}/portfolio</b></li>    <li>ORGANIZATIONS: Add the ability to get an organization portfolio via GET <b>/v1/organizatrions/{id}/portfolio</b></li>    <li>ETH: Add the ability to query <b>/v1/eth/stakes</b>, <b>/v1/eth/rewards</b>, <b>/v1/eth/operations</b> by <b>proxies</b> and <b>validator_indexes</b></li>   <li>ETH: Add <b>validator_index</b> in the responses of <b>/v1/eth/stakes</b>, <b>/v1/eth/rewards</b> and <b>/v1/eth/operations</b></li>   <li>ETH: Add <b>delegated_at</b> field to <b>/v1/eth/stakes</b></li>   <li>ETH: Add <b>is_kiln</b> field to <b>/v1/eth/stakes</b></li>   <li>ETH: Add <b>eth_price_usd</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_entry_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_exit_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_withdrawal_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add POST method to <b>/v1/eth/stakes</b> to link a stake to a Kiln account</li>   <li>ETH: Add new route GET <b>/v1/eth/operations</b> to list on-chain operations on a stake</li>   <li>ETH: Add new route GET <b>/v1/eth/kiln-stats</b> to expose Kiln operational statistics</li>   <li>ETH: Add new route POST <b>/v1/eth/keys</b> to generate ready-to-stake deposit data payloads</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/stake</b> to generate an EIP-1559 staking transaction ready to be signed</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/prepare</b> to craft a transaction ready to be broadcast from a payload and a signature</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ETH: Add new route GET <b>/v1/eth/transaction/status</b> to get the status of a broadcasted transaction</li>   <li>ETH: Add new route GET <b>/v1/eth/reports</b> to generate an Excel report of stakes and rewards</li>    <li>XTZ: Add new route GET <b>/v1/xtz/stakes</b> to to list stakes</li>   <li>XTZ: Add new route GET <b>/v1/xtz/rewards</b> to list rewards</li>   <li>XTZ: Add new route GET <b>/v1/xtz/operations</b> to list on-chain operations of a stake</li>   <li>XTZ: Add new route GET <b>/v1/xtz/network-stats</b> to view network statistics of Tezos</li>   <li>XTZ: Add new route GET <b>/v1/xtz/reports</b> to generate an Excel report</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/stake</b> to generate a delegation transaction</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/unstake</b> to generate an undelegation transaction</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>XTZ: Add new route GET <b>/v1/xtz/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>SOL: Add new route GET <b>/v1/sol/stakes</b> to to list stakes</li>   <li>SOL: Add new method POST <b>/v1/sol/stakes</b> to link a stake to a Solana account</li>   <li>SOL: Add new route GET <b>/v1/sol/rewards</b> to list rewards</li>   <li>SOL: Add new route GET <b>/v1/sol/operations</b> to list on-chain operations of a stake</li>   <li>SOL: Add new route GET <b>/v1/sol/network-stats</b> to view network statistics of Solana</li>   <li>SOL: Add new route GET <b>/v1/sol/reports</b> to generate an Excel report</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/stake</b> to generate a delegation transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/deactivate-stake</b> to generate a deactivate transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/withdraw-stake</b> to prepare a withdraw stake transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/merge-stakes</b> to prepare a merge stakes transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/split-stake</b> to prepare a split stake transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/prepare</b> to prepare any transaction from a payload and signature</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>SOL: Add new route GET <b>/v1/sol/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>ADA: Add new route POST <b>/v1/ada/transaction/stake</b> to generate a delegation transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/withdraw-rewards</b> to generate a withdraw-rewards transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/unstake</b> to generate an undelegate transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ADA: Add new route GET <b>/v1/ada/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>MATIC: Add new route POST <b>/v1/matic/transaction/approve</b> to generate a transaction to allow a smart-contract to spend MATIC tokens on behalf of the user</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/buy-voucher</b> to generate a transaction to buy shares from a validator</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/sell-voucher</b> to generate a transaction to sell shares from a validator</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/unstake-claim-tokens</b> to generate a transaction to withdraw unbounded tokens</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/withdraw-rewards</b> to generate a transaction to withdraw rewards</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/restake-rewards</b> to generate a transaction to restake rewards</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/prepare</b> to prepare a signed transaction for broadcasting</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/broadcast</b> to broadcast a prepared transaction</li>   <li>MATIC: Add new route GET <b>/v1/matic/transaction/status</b> to view the status of a broadcasted transaction</li>  </ul> </details>  <details> <summary>Version 1.0.0 (2023-01-01) <a href=\"/v1.0.0.html\">[link]</a></summary>  <ul>   <li>ETH: Initial support of GET <b>/v1/eth/stakes</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/rewards</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/network-stats</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/keys</b> endpoint</li> </ul>  </details>  ### VERSIONING  Versions of the Kiln API use <b>MAJOR.MINOR.PATCH</b> where:  - <b>MAJOR</b> version is increased when there is major   incompatible API changes, major versions will be communicated in   advance to all customers with a smooth transition path that   spans over a minimum period of 3 MINOR versions or ~3   months. <i>Intended frequency: 1 year</i>. - <b>MINOR</b> version is increased for backward compatible API   changes without notice, or communicated breaking changes with a   1 minor version notice and a smooth migration path. Minor   versions will be communicated regularly to customers with the   changelog. <i>Intended frequency: 1 month</i>. - <b>PATCH</b> version is increased for backward compatible   hot-fixes, patch versions will be communicated to affected   customers.  <i> Due to the nature of blockchains (protocol disappearing, breaking protocol upgrades), Kiln may introduce backward-incompatible changes in MINOR versions after following a 1 MINOR version deprecation path (~1 month). These impacting changes will be narrowed as much as possible to the protocol, heavily communicated with clear guidelines and support. Customer not relying on affected protocols will not be affected. </i>  ### BACKWARD COMPATIBILITY  Kiln considers the following changes to be backward compatible:  - Adding new API routes. - Adding new optional request parameters to existing API methods. - Adding new properties to existing API responses. - Changing the order of properties in existing API responses. - Adding new event types in existing enums.  Non-breaking changes may be introduced in our API and subject to modification before being officialy communicated and documented here. Your application should not depend on them until part of this specification. The preview Kiln API specifications with upcoming and experimental new features can be found [here](/preview.html).  # noqa: E501

    The version of the OpenAPI document: Preview
    Contact: contact@kiln.fi
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import re  # noqa: F401
import io
import warnings

from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated

from datetime import date

from pydantic import Field, StrictInt, StrictStr, conlist

from typing import Optional, Union

from kiln_connect.openapi_client.models.eth_broadcast_tx_payload import ETHBroadcastTxPayload
from kiln_connect.openapi_client.models.eth_craft_stake_tx_payload import ETHCraftStakeTxPayload
from kiln_connect.openapi_client.models.eth_post_keys_payload import ETHPostKeysPayload
from kiln_connect.openapi_client.models.eth_prepare_tx_payload import ETHPrepareTxPayload
from kiln_connect.openapi_client.models.get_eth_kiln_stats200_response import GetEthKilnStats200Response
from kiln_connect.openapi_client.models.get_eth_network_stats200_response import GetEthNetworkStats200Response
from kiln_connect.openapi_client.models.get_eth_operations200_response import GetEthOperations200Response
from kiln_connect.openapi_client.models.get_eth_rewards200_response import GetEthRewards200Response
from kiln_connect.openapi_client.models.get_eth_stakes200_response import GetEthStakes200Response
from kiln_connect.openapi_client.models.get_eth_tx_status200_response import GetEthTxStatus200Response
from kiln_connect.openapi_client.models.get_exit_message200_response import GetExitMessage200Response
from kiln_connect.openapi_client.models.post_eth_stakes_payload import PostETHStakesPayload
from kiln_connect.openapi_client.models.post_eth_broadcast_tx201_response import PostEthBroadcastTx201Response
from kiln_connect.openapi_client.models.post_eth_keys201_response import PostEthKeys201Response
from kiln_connect.openapi_client.models.post_eth_prepare_tx201_response import PostEthPrepareTx201Response
from kiln_connect.openapi_client.models.post_eth_stake_tx201_response import PostEthStakeTx201Response
from kiln_connect.openapi_client.models.post_eth_stakes201_response import PostEthStakes201Response

from kiln_connect.openapi_client.api_client import ApiClient
from kiln_connect.openapi_client.api_response import ApiResponse
from kiln_connect.openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class EthApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def get_eth_kiln_stats(self, **kwargs) -> GetEthKilnStats200Response:  # noqa: E501
        """Kiln Stats  # noqa: E501

        Get some Kiln statistics on Ethereum staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_kiln_stats(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetEthKilnStats200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_kiln_stats_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_kiln_stats_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_kiln_stats_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Kiln Stats  # noqa: E501

        Get some Kiln statistics on Ethereum staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_kiln_stats_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetEthKilnStats200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_kiln_stats" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetEthKilnStats200Response",
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/kiln-stats', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_eth_network_stats(self, **kwargs) -> GetEthNetworkStats200Response:  # noqa: E501
        """Network Stats  # noqa: E501

        Get some network statistics on Ethereum staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_network_stats(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetEthNetworkStats200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_network_stats_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_network_stats_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_network_stats_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Network Stats  # noqa: E501

        Get some network statistics on Ethereum staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_network_stats_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetEthNetworkStats200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_network_stats" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetEthNetworkStats200Response",
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/network-stats', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_eth_operations(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, proxies : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of proxy-contract addresses")] = None, validator_indexes : Annotated[Optional[conlist(StrictInt)], Field(description="Comma-separated list of validators' consensus layer indexes")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> GetEthOperations200Response:  # noqa: E501
        """Operations  # noqa: E501

        Get the operations of Ethereum stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_operations(validators, wallets, proxies, validator_indexes, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param proxies: Comma-separated list of proxy-contract addresses
        :type proxies: List[str]
        :param validator_indexes: Comma-separated list of validators' consensus layer indexes
        :type validator_indexes: List[int]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetEthOperations200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_operations_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_operations_with_http_info(validators, wallets, proxies, validator_indexes, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_operations_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, proxies : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of proxy-contract addresses")] = None, validator_indexes : Annotated[Optional[conlist(StrictInt)], Field(description="Comma-separated list of validators' consensus layer indexes")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Operations  # noqa: E501

        Get the operations of Ethereum stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_operations_with_http_info(validators, wallets, proxies, validator_indexes, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param proxies: Comma-separated list of proxy-contract addresses
        :type proxies: List[str]
        :param validator_indexes: Comma-separated list of validators' consensus layer indexes
        :type validator_indexes: List[int]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetEthOperations200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators',
            'wallets',
            'proxies',
            'validator_indexes',
            'accounts'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_operations" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('validators') is not None:  # noqa: E501
            _query_params.append(('validators', _params['validators']))
            _collection_formats['validators'] = 'csv'

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))
            _collection_formats['wallets'] = 'csv'

        if _params.get('proxies') is not None:  # noqa: E501
            _query_params.append(('proxies', _params['proxies']))
            _collection_formats['proxies'] = 'csv'

        if _params.get('validator_indexes') is not None:  # noqa: E501
            _query_params.append(('validator_indexes', _params['validator_indexes']))
            _collection_formats['validator_indexes'] = 'csv'

        if _params.get('accounts') is not None:  # noqa: E501
            _query_params.append(('accounts', _params['accounts']))
            _collection_formats['accounts'] = 'csv'

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetEthOperations200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/operations', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_eth_reports(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Excel Reports  # noqa: E501

        Generates an Excel report sheet for your stakes and rewards  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_reports(validators, wallets, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: bytearray
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_reports_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_reports_with_http_info(validators, wallets, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_reports_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Excel Reports  # noqa: E501

        Generates an Excel report sheet for your stakes and rewards  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_reports_with_http_info(validators, wallets, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(bytearray, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators',
            'wallets',
            'accounts'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_reports" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('validators') is not None:  # noqa: E501
            _query_params.append(('validators', _params['validators']))
            _collection_formats['validators'] = 'csv'

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))
            _collection_formats['wallets'] = 'csv'

        if _params.get('accounts') is not None:  # noqa: E501
            _query_params.append(('accounts', _params['accounts']))
            _collection_formats['accounts'] = 'csv'

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "bytearray",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/reports', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_eth_rewards(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, proxies : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of proxy-contract addresses")] = None, validator_indexes : Annotated[Optional[conlist(StrictInt)], Field(description="Comma-separated list of validators' consensus layer indexes")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, start_date : Annotated[Optional[date], Field(description="Get rewards from this date (YYYY-MM-DD)")] = None, end_date : Annotated[Optional[date], Field(description="Get rewards to this date (YYYY-MM-DD)")] = None, **kwargs) -> GetEthRewards200Response:  # noqa: E501
        """Rewards  # noqa: E501

        Get historical rewards by day of Ethereum stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_rewards(validators, wallets, proxies, validator_indexes, accounts, start_date, end_date, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param proxies: Comma-separated list of proxy-contract addresses
        :type proxies: List[str]
        :param validator_indexes: Comma-separated list of validators' consensus layer indexes
        :type validator_indexes: List[int]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param start_date: Get rewards from this date (YYYY-MM-DD)
        :type start_date: date
        :param end_date: Get rewards to this date (YYYY-MM-DD)
        :type end_date: date
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetEthRewards200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_rewards_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_rewards_with_http_info(validators, wallets, proxies, validator_indexes, accounts, start_date, end_date, **kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_rewards_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, proxies : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of proxy-contract addresses")] = None, validator_indexes : Annotated[Optional[conlist(StrictInt)], Field(description="Comma-separated list of validators' consensus layer indexes")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, start_date : Annotated[Optional[date], Field(description="Get rewards from this date (YYYY-MM-DD)")] = None, end_date : Annotated[Optional[date], Field(description="Get rewards to this date (YYYY-MM-DD)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Rewards  # noqa: E501

        Get historical rewards by day of Ethereum stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_rewards_with_http_info(validators, wallets, proxies, validator_indexes, accounts, start_date, end_date, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param proxies: Comma-separated list of proxy-contract addresses
        :type proxies: List[str]
        :param validator_indexes: Comma-separated list of validators' consensus layer indexes
        :type validator_indexes: List[int]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param start_date: Get rewards from this date (YYYY-MM-DD)
        :type start_date: date
        :param end_date: Get rewards to this date (YYYY-MM-DD)
        :type end_date: date
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetEthRewards200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators',
            'wallets',
            'proxies',
            'validator_indexes',
            'accounts',
            'start_date',
            'end_date'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_rewards" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('validators') is not None:  # noqa: E501
            _query_params.append(('validators', _params['validators']))
            _collection_formats['validators'] = 'csv'

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))
            _collection_formats['wallets'] = 'csv'

        if _params.get('proxies') is not None:  # noqa: E501
            _query_params.append(('proxies', _params['proxies']))
            _collection_formats['proxies'] = 'csv'

        if _params.get('validator_indexes') is not None:  # noqa: E501
            _query_params.append(('validator_indexes', _params['validator_indexes']))
            _collection_formats['validator_indexes'] = 'csv'

        if _params.get('accounts') is not None:  # noqa: E501
            _query_params.append(('accounts', _params['accounts']))
            _collection_formats['accounts'] = 'csv'

        if _params.get('start_date') is not None:  # noqa: E501
            if isinstance(_params['start_date'], date):
                _query_params.append(('start_date', _params['start_date'].strftime(self.api_client.configuration.date_format)))
            else:
                _query_params.append(('start_date', _params['start_date']))

        if _params.get('end_date') is not None:  # noqa: E501
            if isinstance(_params['end_date'], date):
                _query_params.append(('end_date', _params['end_date'].strftime(self.api_client.configuration.date_format)))
            else:
                _query_params.append(('end_date', _params['end_date']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetEthRewards200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/rewards', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_eth_stakes(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, proxies : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of proxy-contract addresses")] = None, validator_indexes : Annotated[Optional[conlist(StrictInt)], Field(description="Comma-separated list of validators' consensus layer indexes")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> GetEthStakes200Response:  # noqa: E501
        """Stakes  # noqa: E501

        Get the status of Ethereum stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_stakes(validators, wallets, proxies, validator_indexes, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param proxies: Comma-separated list of proxy-contract addresses
        :type proxies: List[str]
        :param validator_indexes: Comma-separated list of validators' consensus layer indexes
        :type validator_indexes: List[int]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetEthStakes200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_stakes_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_stakes_with_http_info(validators, wallets, proxies, validator_indexes, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_stakes_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, proxies : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of proxy-contract addresses")] = None, validator_indexes : Annotated[Optional[conlist(StrictInt)], Field(description="Comma-separated list of validators' consensus layer indexes")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Stakes  # noqa: E501

        Get the status of Ethereum stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_stakes_with_http_info(validators, wallets, proxies, validator_indexes, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param proxies: Comma-separated list of proxy-contract addresses
        :type proxies: List[str]
        :param validator_indexes: Comma-separated list of validators' consensus layer indexes
        :type validator_indexes: List[int]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetEthStakes200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators',
            'wallets',
            'proxies',
            'validator_indexes',
            'accounts'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_stakes" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('validators') is not None:  # noqa: E501
            _query_params.append(('validators', _params['validators']))
            _collection_formats['validators'] = 'csv'

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))
            _collection_formats['wallets'] = 'csv'

        if _params.get('proxies') is not None:  # noqa: E501
            _query_params.append(('proxies', _params['proxies']))
            _collection_formats['proxies'] = 'csv'

        if _params.get('validator_indexes') is not None:  # noqa: E501
            _query_params.append(('validator_indexes', _params['validator_indexes']))
            _collection_formats['validator_indexes'] = 'csv'

        if _params.get('accounts') is not None:  # noqa: E501
            _query_params.append(('accounts', _params['accounts']))
            _collection_formats['accounts'] = 'csv'

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetEthStakes200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/stakes', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_eth_tx_status(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> GetEthTxStatus200Response:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of an Ethereum transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_tx_status(tx_hash, async_req=True)
        >>> result = thread.get()

        :param tx_hash: Hash of the transaction (required)
        :type tx_hash: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetEthTxStatus200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_eth_tx_status_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_eth_tx_status_with_http_info(tx_hash, **kwargs)  # noqa: E501

    @validate_arguments
    def get_eth_tx_status_with_http_info(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> ApiResponse:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of an Ethereum transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_eth_tx_status_with_http_info(tx_hash, async_req=True)
        >>> result = thread.get()

        :param tx_hash: Hash of the transaction (required)
        :type tx_hash: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetEthTxStatus200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'tx_hash'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_eth_tx_status" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('tx_hash') is not None:  # noqa: E501
            _query_params.append(('tx_hash', _params['tx_hash']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetEthTxStatus200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/transaction/status', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def get_exit_message(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, **kwargs) -> GetExitMessage200Response:  # noqa: E501
        """Exit Messages  # noqa: E501

        Get encrypted exit message for a validator  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_exit_message(validators, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetExitMessage200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_exit_message_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_exit_message_with_http_info(validators, **kwargs)  # noqa: E501

    @validate_arguments
    def get_exit_message_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Exit Messages  # noqa: E501

        Get encrypted exit message for a validator  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_exit_message_with_http_info(validators, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses
        :type validators: List[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GetExitMessage200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_exit_message" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('validators') is not None:  # noqa: E501
            _query_params.append(('validators', _params['validators']))
            _collection_formats['validators'] = 'csv'

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetExitMessage200Response",
            '400': None,
            '404': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/exit-messages', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def post_eth_broadcast_tx(self, eth_broadcast_tx_payload : Annotated[ETHBroadcastTxPayload, Field(..., description="Transaction to broadcast")], **kwargs) -> PostEthBroadcastTx201Response:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcasts a signed Ethereum transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_broadcast_tx(eth_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param eth_broadcast_tx_payload: Transaction to broadcast (required)
        :type eth_broadcast_tx_payload: ETHBroadcastTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostEthBroadcastTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_eth_broadcast_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_eth_broadcast_tx_with_http_info(eth_broadcast_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_eth_broadcast_tx_with_http_info(self, eth_broadcast_tx_payload : Annotated[ETHBroadcastTxPayload, Field(..., description="Transaction to broadcast")], **kwargs) -> ApiResponse:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcasts a signed Ethereum transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_broadcast_tx_with_http_info(eth_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param eth_broadcast_tx_payload: Transaction to broadcast (required)
        :type eth_broadcast_tx_payload: ETHBroadcastTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PostEthBroadcastTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'eth_broadcast_tx_payload'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_eth_broadcast_tx" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['eth_broadcast_tx_payload'] is not None:
            _body_params = _params['eth_broadcast_tx_payload']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json; charset=utf-8']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '201': "PostEthBroadcastTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/transaction/broadcast', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def post_eth_keys(self, eth_post_keys_payload : Annotated[ETHPostKeysPayload, Field(..., description="Ethereum keys to generate")], **kwargs) -> PostEthKeys201Response:  # noqa: E501
        """Validation Keys  # noqa: E501

        Create Ethereum validation keys on Kiln's infrastructure.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_keys(eth_post_keys_payload, async_req=True)
        >>> result = thread.get()

        :param eth_post_keys_payload: Ethereum keys to generate (required)
        :type eth_post_keys_payload: ETHPostKeysPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostEthKeys201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_eth_keys_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_eth_keys_with_http_info(eth_post_keys_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_eth_keys_with_http_info(self, eth_post_keys_payload : Annotated[ETHPostKeysPayload, Field(..., description="Ethereum keys to generate")], **kwargs) -> ApiResponse:  # noqa: E501
        """Validation Keys  # noqa: E501

        Create Ethereum validation keys on Kiln's infrastructure.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_keys_with_http_info(eth_post_keys_payload, async_req=True)
        >>> result = thread.get()

        :param eth_post_keys_payload: Ethereum keys to generate (required)
        :type eth_post_keys_payload: ETHPostKeysPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PostEthKeys201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'eth_post_keys_payload'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_eth_keys" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['eth_post_keys_payload'] is not None:
            _body_params = _params['eth_post_keys_payload']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json; charset=utf-8']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '201': "PostEthKeys201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/keys', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def post_eth_prepare_tx(self, eth_prepare_tx_payload : Annotated[ETHPrepareTxPayload, Field(..., description="Transaction to prepare")], **kwargs) -> PostEthPrepareTx201Response:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an Ethereum transaction for broadcasting. It takes a serialized transaction and its signatures and returns a serialized signed transaction that can be broadcasted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_prepare_tx(eth_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param eth_prepare_tx_payload: Transaction to prepare (required)
        :type eth_prepare_tx_payload: ETHPrepareTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostEthPrepareTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_eth_prepare_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_eth_prepare_tx_with_http_info(eth_prepare_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_eth_prepare_tx_with_http_info(self, eth_prepare_tx_payload : Annotated[ETHPrepareTxPayload, Field(..., description="Transaction to prepare")], **kwargs) -> ApiResponse:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an Ethereum transaction for broadcasting. It takes a serialized transaction and its signatures and returns a serialized signed transaction that can be broadcasted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_prepare_tx_with_http_info(eth_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param eth_prepare_tx_payload: Transaction to prepare (required)
        :type eth_prepare_tx_payload: ETHPrepareTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PostEthPrepareTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'eth_prepare_tx_payload'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_eth_prepare_tx" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['eth_prepare_tx_payload'] is not None:
            _body_params = _params['eth_prepare_tx_payload']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json; charset=utf-8']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '201': "PostEthPrepareTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/transaction/prepare', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def post_eth_stake_tx(self, eth_craft_stake_tx_payload : Annotated[ETHCraftStakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostEthStakeTx201Response:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Generates an Ethereum EIP 1559 stake transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_stake_tx(eth_craft_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param eth_craft_stake_tx_payload: Transaction to craft (required)
        :type eth_craft_stake_tx_payload: ETHCraftStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostEthStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_eth_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_eth_stake_tx_with_http_info(eth_craft_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_eth_stake_tx_with_http_info(self, eth_craft_stake_tx_payload : Annotated[ETHCraftStakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Generates an Ethereum EIP 1559 stake transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_stake_tx_with_http_info(eth_craft_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param eth_craft_stake_tx_payload: Transaction to craft (required)
        :type eth_craft_stake_tx_payload: ETHCraftStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PostEthStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'eth_craft_stake_tx_payload'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_eth_stake_tx" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['eth_craft_stake_tx_payload'] is not None:
            _body_params = _params['eth_craft_stake_tx_payload']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json; charset=utf-8']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '201': "PostEthStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/transaction/stake', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def post_eth_stakes(self, post_eth_stakes_payload : Annotated[PostETHStakesPayload, Field(..., description="Stakes to create")], **kwargs) -> PostEthStakes201Response:  # noqa: E501
        """Create stakes  # noqa: E501

        Link ETH stakes to a Kiln account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_stakes(post_eth_stakes_payload, async_req=True)
        >>> result = thread.get()

        :param post_eth_stakes_payload: Stakes to create (required)
        :type post_eth_stakes_payload: PostETHStakesPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostEthStakes201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_eth_stakes_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_eth_stakes_with_http_info(post_eth_stakes_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_eth_stakes_with_http_info(self, post_eth_stakes_payload : Annotated[PostETHStakesPayload, Field(..., description="Stakes to create")], **kwargs) -> ApiResponse:  # noqa: E501
        """Create stakes  # noqa: E501

        Link ETH stakes to a Kiln account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_eth_stakes_with_http_info(post_eth_stakes_payload, async_req=True)
        >>> result = thread.get()

        :param post_eth_stakes_payload: Stakes to create (required)
        :type post_eth_stakes_payload: PostETHStakesPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the 
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PostEthStakes201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'post_eth_stakes_payload'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_eth_stakes" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['post_eth_stakes_payload'] is not None:
            _body_params = _params['post_eth_stakes_payload']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json; charset=utf-8'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json; charset=utf-8']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '201': "PostEthStakes201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/eth/stakes', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
