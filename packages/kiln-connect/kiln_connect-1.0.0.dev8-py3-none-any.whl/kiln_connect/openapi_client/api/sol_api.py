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

from pydantic import Field, StrictFloat, StrictInt, StrictStr, conlist

from typing import Optional, Union

from kiln_connect.openapi_client.models.get_sol_network_stats200_response import GetSolNetworkStats200Response
from kiln_connect.openapi_client.models.get_sol_operations200_response import GetSolOperations200Response
from kiln_connect.openapi_client.models.get_sol_rewards200_response import GetSolRewards200Response
from kiln_connect.openapi_client.models.get_sol_stakes200_response import GetSolStakes200Response
from kiln_connect.openapi_client.models.get_sol_tx_status200_response import GetSolTxStatus200Response
from kiln_connect.openapi_client.models.post_eth_stakes201_response import PostEthStakes201Response
from kiln_connect.openapi_client.models.post_sol_broadcast_tx201_response import PostSolBroadcastTx201Response
from kiln_connect.openapi_client.models.post_sol_prepare_tx201_response import PostSolPrepareTx201Response
from kiln_connect.openapi_client.models.post_sol_stake_tx201_response import PostSolStakeTx201Response
from kiln_connect.openapi_client.models.sol_broadcast_tx_payload import SOLBroadcastTxPayload
from kiln_connect.openapi_client.models.sol_deactivate_stake_tx_payload import SOLDeactivateStakeTxPayload
from kiln_connect.openapi_client.models.sol_merge_stakes_tx_payload import SOLMergeStakesTxPayload
from kiln_connect.openapi_client.models.sol_post_stakes_payload import SOLPostStakesPayload
from kiln_connect.openapi_client.models.sol_prepare_tx_payload import SOLPrepareTxPayload
from kiln_connect.openapi_client.models.sol_split_stake_tx_payload import SOLSplitStakeTxPayload
from kiln_connect.openapi_client.models.sol_stake_tx_payload import SOLStakeTxPayload
from kiln_connect.openapi_client.models.sol_withdraw_stake_tx_payload import SOLWithdrawStakeTxPayload

from kiln_connect.openapi_client.api_client import ApiClient
from kiln_connect.openapi_client.api_response import ApiResponse
from kiln_connect.openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class SolApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def get_sol_network_stats(self, **kwargs) -> GetSolNetworkStats200Response:  # noqa: E501
        """Network Stats  # noqa: E501

        Get some network statistics on Solana staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_network_stats(async_req=True)
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
        :rtype: GetSolNetworkStats200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_sol_network_stats_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_sol_network_stats_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def get_sol_network_stats_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Network Stats  # noqa: E501

        Get some network statistics on Solana staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_network_stats_with_http_info(async_req=True)
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
        :rtype: tuple(GetSolNetworkStats200Response, status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_sol_network_stats" % _key
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
            '200': "GetSolNetworkStats200Response",
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/network-stats', 'GET',
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
    def get_sol_operations(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> GetSolOperations200Response:  # noqa: E501
        """Operations  # noqa: E501

        Get the operations of Solana stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_operations(stake_accounts, wallets, accounts, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
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
        :rtype: GetSolOperations200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_sol_operations_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_sol_operations_with_http_info(stake_accounts, wallets, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_sol_operations_with_http_info(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Operations  # noqa: E501

        Get the operations of Solana stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_operations_with_http_info(stake_accounts, wallets, accounts, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
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
        :rtype: tuple(GetSolOperations200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'stake_accounts',
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
                    " to method get_sol_operations" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('stake_accounts') is not None:  # noqa: E501
            _query_params.append(('stake_accounts', _params['stake_accounts']))
            _collection_formats['stake_accounts'] = 'csv'

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
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetSolOperations200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/operations', 'GET',
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
    def get_sol_reports(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, format : Annotated[Optional[StrictStr], Field(description="The format of the response. Defaults to daily")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Reports  # noqa: E501

        Get reports on Solana staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_reports(stake_accounts, wallets, accounts, format, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param format: The format of the response. Defaults to daily
        :type format: str
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
            raise ValueError("Error! Please call the get_sol_reports_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_sol_reports_with_http_info(stake_accounts, wallets, accounts, format, **kwargs)  # noqa: E501

    @validate_arguments
    def get_sol_reports_with_http_info(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, format : Annotated[Optional[StrictStr], Field(description="The format of the response. Defaults to daily")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Reports  # noqa: E501

        Get reports on Solana staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_reports_with_http_info(stake_accounts, wallets, accounts, format, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param format: The format of the response. Defaults to daily
        :type format: str
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
            'stake_accounts',
            'wallets',
            'accounts',
            'format'
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
                    " to method get_sol_reports" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('stake_accounts') is not None:  # noqa: E501
            _query_params.append(('stake_accounts', _params['stake_accounts']))
            _collection_formats['stake_accounts'] = 'csv'

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))
            _collection_formats['wallets'] = 'csv'

        if _params.get('accounts') is not None:  # noqa: E501
            _query_params.append(('accounts', _params['accounts']))
            _collection_formats['accounts'] = 'csv'

        if _params.get('format') is not None:  # noqa: E501
            _query_params.append(('format', _params['format']))

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
            '/v1/sol/reports', 'GET',
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
    def get_sol_rewards(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, start_date : Annotated[Optional[date], Field(description="Get rewards from this date (YYYY-MM-DD)")] = None, end_date : Annotated[Optional[date], Field(description="Get rewards to this date (YYYY-MM-DD)")] = None, format : Annotated[Optional[StrictStr], Field(description="The format of the response. Defaults to daily")] = None, start_epoch : Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="The epoch from which we want to fetch rewards. Must be used with format=epoch")] = None, end_epoch : Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="The epoch until which we want to fetch rewards. Must be used with format=epoch")] = None, **kwargs) -> GetSolRewards200Response:  # noqa: E501
        """Rewards  # noqa: E501

        Get historical rewards of Solana stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_rewards(stake_accounts, wallets, accounts, start_date, end_date, format, start_epoch, end_epoch, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param start_date: Get rewards from this date (YYYY-MM-DD)
        :type start_date: date
        :param end_date: Get rewards to this date (YYYY-MM-DD)
        :type end_date: date
        :param format: The format of the response. Defaults to daily
        :type format: str
        :param start_epoch: The epoch from which we want to fetch rewards. Must be used with format=epoch
        :type start_epoch: float
        :param end_epoch: The epoch until which we want to fetch rewards. Must be used with format=epoch
        :type end_epoch: float
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GetSolRewards200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_sol_rewards_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_sol_rewards_with_http_info(stake_accounts, wallets, accounts, start_date, end_date, format, start_epoch, end_epoch, **kwargs)  # noqa: E501

    @validate_arguments
    def get_sol_rewards_with_http_info(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, start_date : Annotated[Optional[date], Field(description="Get rewards from this date (YYYY-MM-DD)")] = None, end_date : Annotated[Optional[date], Field(description="Get rewards to this date (YYYY-MM-DD)")] = None, format : Annotated[Optional[StrictStr], Field(description="The format of the response. Defaults to daily")] = None, start_epoch : Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="The epoch from which we want to fetch rewards. Must be used with format=epoch")] = None, end_epoch : Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="The epoch until which we want to fetch rewards. Must be used with format=epoch")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Rewards  # noqa: E501

        Get historical rewards of Solana stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_rewards_with_http_info(stake_accounts, wallets, accounts, start_date, end_date, format, start_epoch, end_epoch, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
        :param wallets: Comma-separated list of wallets addresses
        :type wallets: List[str]
        :param accounts: Comma-separated list of Kiln accounts identifiers
        :type accounts: List[str]
        :param start_date: Get rewards from this date (YYYY-MM-DD)
        :type start_date: date
        :param end_date: Get rewards to this date (YYYY-MM-DD)
        :type end_date: date
        :param format: The format of the response. Defaults to daily
        :type format: str
        :param start_epoch: The epoch from which we want to fetch rewards. Must be used with format=epoch
        :type start_epoch: float
        :param end_epoch: The epoch until which we want to fetch rewards. Must be used with format=epoch
        :type end_epoch: float
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
        :rtype: tuple(GetSolRewards200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'stake_accounts',
            'wallets',
            'accounts',
            'start_date',
            'end_date',
            'format',
            'start_epoch',
            'end_epoch'
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
                    " to method get_sol_rewards" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('stake_accounts') is not None:  # noqa: E501
            _query_params.append(('stake_accounts', _params['stake_accounts']))
            _collection_formats['stake_accounts'] = 'csv'

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))
            _collection_formats['wallets'] = 'csv'

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

        if _params.get('format') is not None:  # noqa: E501
            _query_params.append(('format', _params['format']))

        if _params.get('start_epoch') is not None:  # noqa: E501
            _query_params.append(('start_epoch', _params['start_epoch']))

        if _params.get('end_epoch') is not None:  # noqa: E501
            _query_params.append(('end_epoch', _params['end_epoch']))

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
            '200': "GetSolRewards200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/rewards', 'GET',
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
    def get_sol_stakes(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> GetSolStakes200Response:  # noqa: E501
        """Stakes  # noqa: E501

        Get the status of Solana stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_stakes(stake_accounts, wallets, accounts, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
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
        :rtype: GetSolStakes200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_sol_stakes_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_sol_stakes_with_http_info(stake_accounts, wallets, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_sol_stakes_with_http_info(self, stake_accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of stake addresses")] = None, wallets : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of wallets addresses")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Stakes  # noqa: E501

        Get the status of Solana stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_stakes_with_http_info(stake_accounts, wallets, accounts, async_req=True)
        >>> result = thread.get()

        :param stake_accounts: Comma-separated list of stake addresses
        :type stake_accounts: List[str]
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
        :rtype: tuple(GetSolStakes200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'stake_accounts',
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
                    " to method get_sol_stakes" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('stake_accounts') is not None:  # noqa: E501
            _query_params.append(('stake_accounts', _params['stake_accounts']))
            _collection_formats['stake_accounts'] = 'csv'

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
            ['application/json; charset=utf-8'])  # noqa: E501

        # authentication setting
        _auth_settings = ['bearerAuth']  # noqa: E501

        _response_types_map = {
            '200': "GetSolStakes200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/stakes', 'GET',
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
    def get_sol_tx_status(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> GetSolTxStatus200Response:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_tx_status(tx_hash, async_req=True)
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
        :rtype: GetSolTxStatus200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_sol_tx_status_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_sol_tx_status_with_http_info(tx_hash, **kwargs)  # noqa: E501

    @validate_arguments
    def get_sol_tx_status_with_http_info(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> ApiResponse:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_sol_tx_status_with_http_info(tx_hash, async_req=True)
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
        :rtype: tuple(GetSolTxStatus200Response, status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_sol_tx_status" % _key
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
            '200': "GetSolTxStatus200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/status', 'GET',
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
    def post_sol_broadcast_tx(self, sol_broadcast_tx_payload : Annotated[SOLBroadcastTxPayload, Field(..., description="Signed transaction to broadcast")], **kwargs) -> PostSolBroadcastTx201Response:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcast a serialized signed transaction to the blockchain  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_broadcast_tx(sol_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_broadcast_tx_payload: Signed transaction to broadcast (required)
        :type sol_broadcast_tx_payload: SOLBroadcastTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolBroadcastTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_broadcast_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_broadcast_tx_with_http_info(sol_broadcast_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_broadcast_tx_with_http_info(self, sol_broadcast_tx_payload : Annotated[SOLBroadcastTxPayload, Field(..., description="Signed transaction to broadcast")], **kwargs) -> ApiResponse:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcast a serialized signed transaction to the blockchain  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_broadcast_tx_with_http_info(sol_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_broadcast_tx_payload: Signed transaction to broadcast (required)
        :type sol_broadcast_tx_payload: SOLBroadcastTxPayload
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
        :rtype: tuple(PostSolBroadcastTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_broadcast_tx_payload'
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
                    " to method post_sol_broadcast_tx" % _key
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
        if _params['sol_broadcast_tx_payload'] is not None:
            _body_params = _params['sol_broadcast_tx_payload']

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
            '201': "PostSolBroadcastTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/broadcast', 'POST',
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
    def post_sol_deactivate_stake_tx(self, sol_deactivate_stake_tx_payload : Annotated[SOLDeactivateStakeTxPayload, Field(..., description="Stake to deactivate")], **kwargs) -> PostSolStakeTx201Response:  # noqa: E501
        """Deactivate Stake Transaction  # noqa: E501

        Craft a deactivate stake account transaction.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_deactivate_stake_tx(sol_deactivate_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_deactivate_stake_tx_payload: Stake to deactivate (required)
        :type sol_deactivate_stake_tx_payload: SOLDeactivateStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_deactivate_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_deactivate_stake_tx_with_http_info(sol_deactivate_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_deactivate_stake_tx_with_http_info(self, sol_deactivate_stake_tx_payload : Annotated[SOLDeactivateStakeTxPayload, Field(..., description="Stake to deactivate")], **kwargs) -> ApiResponse:  # noqa: E501
        """Deactivate Stake Transaction  # noqa: E501

        Craft a deactivate stake account transaction.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_deactivate_stake_tx_with_http_info(sol_deactivate_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_deactivate_stake_tx_payload: Stake to deactivate (required)
        :type sol_deactivate_stake_tx_payload: SOLDeactivateStakeTxPayload
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
        :rtype: tuple(PostSolStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_deactivate_stake_tx_payload'
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
                    " to method post_sol_deactivate_stake_tx" % _key
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
        if _params['sol_deactivate_stake_tx_payload'] is not None:
            _body_params = _params['sol_deactivate_stake_tx_payload']

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
            '201': "PostSolStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/deactivate-stake', 'POST',
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
    def post_sol_merge_stakes_tx(self, sol_merge_stakes_tx_payload : Annotated[SOLMergeStakesTxPayload, Field(..., description="Stakes to merge")], **kwargs) -> PostSolStakeTx201Response:  # noqa: E501
        """Merge Stakes Transaction  # noqa: E501

        Craft a merge stakes transaction.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_merge_stakes_tx(sol_merge_stakes_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_merge_stakes_tx_payload: Stakes to merge (required)
        :type sol_merge_stakes_tx_payload: SOLMergeStakesTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_merge_stakes_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_merge_stakes_tx_with_http_info(sol_merge_stakes_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_merge_stakes_tx_with_http_info(self, sol_merge_stakes_tx_payload : Annotated[SOLMergeStakesTxPayload, Field(..., description="Stakes to merge")], **kwargs) -> ApiResponse:  # noqa: E501
        """Merge Stakes Transaction  # noqa: E501

        Craft a merge stakes transaction.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_merge_stakes_tx_with_http_info(sol_merge_stakes_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_merge_stakes_tx_payload: Stakes to merge (required)
        :type sol_merge_stakes_tx_payload: SOLMergeStakesTxPayload
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
        :rtype: tuple(PostSolStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_merge_stakes_tx_payload'
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
                    " to method post_sol_merge_stakes_tx" % _key
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
        if _params['sol_merge_stakes_tx_payload'] is not None:
            _body_params = _params['sol_merge_stakes_tx_payload']

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
            '201': "PostSolStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/merge-stakes', 'POST',
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
    def post_sol_prepare_tx(self, sol_prepare_tx_payload : Annotated[SOLPrepareTxPayload, Field(..., description="Transaction to sign")], **kwargs) -> PostSolPrepareTx201Response:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an unsigned transaction for broadcast by adding signatures to it  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_prepare_tx(sol_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_prepare_tx_payload: Transaction to sign (required)
        :type sol_prepare_tx_payload: SOLPrepareTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolPrepareTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_prepare_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_prepare_tx_with_http_info(sol_prepare_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_prepare_tx_with_http_info(self, sol_prepare_tx_payload : Annotated[SOLPrepareTxPayload, Field(..., description="Transaction to sign")], **kwargs) -> ApiResponse:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an unsigned transaction for broadcast by adding signatures to it  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_prepare_tx_with_http_info(sol_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_prepare_tx_payload: Transaction to sign (required)
        :type sol_prepare_tx_payload: SOLPrepareTxPayload
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
        :rtype: tuple(PostSolPrepareTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_prepare_tx_payload'
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
                    " to method post_sol_prepare_tx" % _key
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
        if _params['sol_prepare_tx_payload'] is not None:
            _body_params = _params['sol_prepare_tx_payload']

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
            '201': "PostSolPrepareTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/prepare', 'POST',
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
    def post_sol_split_stake_tx(self, sol_split_stake_tx_payload : Annotated[SOLSplitStakeTxPayload, Field(..., description="Stake to split")], **kwargs) -> PostSolStakeTx201Response:  # noqa: E501
        """Split Stake Transaction  # noqa: E501

        Craft a solana split stake transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_split_stake_tx(sol_split_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_split_stake_tx_payload: Stake to split (required)
        :type sol_split_stake_tx_payload: SOLSplitStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_split_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_split_stake_tx_with_http_info(sol_split_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_split_stake_tx_with_http_info(self, sol_split_stake_tx_payload : Annotated[SOLSplitStakeTxPayload, Field(..., description="Stake to split")], **kwargs) -> ApiResponse:  # noqa: E501
        """Split Stake Transaction  # noqa: E501

        Craft a solana split stake transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_split_stake_tx_with_http_info(sol_split_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_split_stake_tx_payload: Stake to split (required)
        :type sol_split_stake_tx_payload: SOLSplitStakeTxPayload
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
        :rtype: tuple(PostSolStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_split_stake_tx_payload'
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
                    " to method post_sol_split_stake_tx" % _key
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
        if _params['sol_split_stake_tx_payload'] is not None:
            _body_params = _params['sol_split_stake_tx_payload']

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
            '201': "PostSolStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/split-stake', 'POST',
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
    def post_sol_stake_tx(self, sol_stake_tx_payload : Annotated[SOLStakeTxPayload, Field(..., description="Stake transaction to create")], **kwargs) -> PostSolStakeTx201Response:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Craft a stake transaction. This results in a new stake account created with the amount given.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_stake_tx(sol_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_stake_tx_payload: Stake transaction to create (required)
        :type sol_stake_tx_payload: SOLStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_stake_tx_with_http_info(sol_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_stake_tx_with_http_info(self, sol_stake_tx_payload : Annotated[SOLStakeTxPayload, Field(..., description="Stake transaction to create")], **kwargs) -> ApiResponse:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Craft a stake transaction. This results in a new stake account created with the amount given.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_stake_tx_with_http_info(sol_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_stake_tx_payload: Stake transaction to create (required)
        :type sol_stake_tx_payload: SOLStakeTxPayload
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
        :rtype: tuple(PostSolStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_stake_tx_payload'
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
                    " to method post_sol_stake_tx" % _key
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
        if _params['sol_stake_tx_payload'] is not None:
            _body_params = _params['sol_stake_tx_payload']

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
            '201': "PostSolStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/stake', 'POST',
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
    def post_sol_stakes(self, sol_post_stakes_payload : Annotated[SOLPostStakesPayload, Field(..., description="Stakes to create")], **kwargs) -> PostEthStakes201Response:  # noqa: E501
        """Create stakes  # noqa: E501

        Create Solana stakes and linked them to a Kiln account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_stakes(sol_post_stakes_payload, async_req=True)
        >>> result = thread.get()

        :param sol_post_stakes_payload: Stakes to create (required)
        :type sol_post_stakes_payload: SOLPostStakesPayload
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
            raise ValueError("Error! Please call the post_sol_stakes_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_stakes_with_http_info(sol_post_stakes_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_stakes_with_http_info(self, sol_post_stakes_payload : Annotated[SOLPostStakesPayload, Field(..., description="Stakes to create")], **kwargs) -> ApiResponse:  # noqa: E501
        """Create stakes  # noqa: E501

        Create Solana stakes and linked them to a Kiln account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_stakes_with_http_info(sol_post_stakes_payload, async_req=True)
        >>> result = thread.get()

        :param sol_post_stakes_payload: Stakes to create (required)
        :type sol_post_stakes_payload: SOLPostStakesPayload
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
            'sol_post_stakes_payload'
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
                    " to method post_sol_stakes" % _key
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
        if _params['sol_post_stakes_payload'] is not None:
            _body_params = _params['sol_post_stakes_payload']

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
            '/v1/sol/stakes', 'POST',
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
    def post_sol_withdraw_stake_tx(self, sol_withdraw_stake_tx_payload : Annotated[SOLWithdrawStakeTxPayload, Field(..., description="Stake to withdraw")], **kwargs) -> PostSolStakeTx201Response:  # noqa: E501
        """Withdraw Stake Transaction  # noqa: E501

        Craft a withdraw stake transaction.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_withdraw_stake_tx(sol_withdraw_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_withdraw_stake_tx_payload: Stake to withdraw (required)
        :type sol_withdraw_stake_tx_payload: SOLWithdrawStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostSolStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_sol_withdraw_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_sol_withdraw_stake_tx_with_http_info(sol_withdraw_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_sol_withdraw_stake_tx_with_http_info(self, sol_withdraw_stake_tx_payload : Annotated[SOLWithdrawStakeTxPayload, Field(..., description="Stake to withdraw")], **kwargs) -> ApiResponse:  # noqa: E501
        """Withdraw Stake Transaction  # noqa: E501

        Craft a withdraw stake transaction.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_sol_withdraw_stake_tx_with_http_info(sol_withdraw_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param sol_withdraw_stake_tx_payload: Stake to withdraw (required)
        :type sol_withdraw_stake_tx_payload: SOLWithdrawStakeTxPayload
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
        :rtype: tuple(PostSolStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'sol_withdraw_stake_tx_payload'
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
                    " to method post_sol_withdraw_stake_tx" % _key
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
        if _params['sol_withdraw_stake_tx_payload'] is not None:
            _body_params = _params['sol_withdraw_stake_tx_payload']

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
            '201': "PostSolStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/sol/transaction/withdraw-stake', 'POST',
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
