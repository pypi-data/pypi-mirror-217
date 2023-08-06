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

from pydantic import Field, StrictStr, conlist

from typing import Optional, Union

from kiln_connect.openapi_client.models.ada_broadcast_tx_payload import ADABroadcastTxPayload
from kiln_connect.openapi_client.models.ada_craft_stake_tx_payload import ADACraftStakeTxPayload
from kiln_connect.openapi_client.models.ada_craft_unstake_tx_payload import ADACraftUnstakeTxPayload
from kiln_connect.openapi_client.models.ada_craft_withdraw_rewards_tx_payload import ADACraftWithdrawRewardsTxPayload
from kiln_connect.openapi_client.models.ada_prepare_tx_payload import ADAPrepareTxPayload
from kiln_connect.openapi_client.models.get_ada_tx_status200_response import GetAdaTxStatus200Response
from kiln_connect.openapi_client.models.post_ada_broadcast_tx201_response import PostAdaBroadcastTx201Response
from kiln_connect.openapi_client.models.post_ada_prepare_tx201_response import PostAdaPrepareTx201Response
from kiln_connect.openapi_client.models.post_ada_stake_tx201_response import PostAdaStakeTx201Response

from kiln_connect.openapi_client.api_client import ApiClient
from kiln_connect.openapi_client.api_response import ApiResponse
from kiln_connect.openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class AdaApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def get_ada_reports(self, stake_addresses : Optional[StrictStr] = None, wallets : Optional[StrictStr] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, format : Annotated[Optional[StrictStr], Field(description="The format of the response. Defaults to daily")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Reports  # noqa: E501

        Get reports on Cardano staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_ada_reports(stake_addresses, wallets, accounts, format, async_req=True)
        >>> result = thread.get()

        :param stake_addresses:
        :type stake_addresses: str
        :param wallets:
        :type wallets: str
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
            raise ValueError("Error! Please call the get_ada_reports_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_ada_reports_with_http_info(stake_addresses, wallets, accounts, format, **kwargs)  # noqa: E501

    @validate_arguments
    def get_ada_reports_with_http_info(self, stake_addresses : Optional[StrictStr] = None, wallets : Optional[StrictStr] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, format : Annotated[Optional[StrictStr], Field(description="The format of the response. Defaults to daily")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Reports  # noqa: E501

        Get reports on Cardano staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_ada_reports_with_http_info(stake_addresses, wallets, accounts, format, async_req=True)
        >>> result = thread.get()

        :param stake_addresses:
        :type stake_addresses: str
        :param wallets:
        :type wallets: str
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
            'stake_addresses',
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
                    " to method get_ada_reports" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('stake_addresses') is not None:  # noqa: E501
            _query_params.append(('stake_addresses', _params['stake_addresses']))

        if _params.get('wallets') is not None:  # noqa: E501
            _query_params.append(('wallets', _params['wallets']))

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
            '/v1/ada/reports', 'GET',
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
    def get_ada_tx_status(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> GetAdaTxStatus200Response:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_ada_tx_status(tx_hash, async_req=True)
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
        :rtype: GetAdaTxStatus200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_ada_tx_status_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_ada_tx_status_with_http_info(tx_hash, **kwargs)  # noqa: E501

    @validate_arguments
    def get_ada_tx_status_with_http_info(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> ApiResponse:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_ada_tx_status_with_http_info(tx_hash, async_req=True)
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
        :rtype: tuple(GetAdaTxStatus200Response, status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_ada_tx_status" % _key
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
            '200': "GetAdaTxStatus200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/ada/transaction/status', 'GET',
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
    def post_ada_broadcast_tx(self, ada_broadcast_tx_payload : Annotated[ADABroadcastTxPayload, Field(..., description="Transaction to broadcast")], **kwargs) -> PostAdaBroadcastTx201Response:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcast a signed transaction to the Cardano network  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_broadcast_tx(ada_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_broadcast_tx_payload: Transaction to broadcast (required)
        :type ada_broadcast_tx_payload: ADABroadcastTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAdaBroadcastTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_ada_broadcast_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_ada_broadcast_tx_with_http_info(ada_broadcast_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_ada_broadcast_tx_with_http_info(self, ada_broadcast_tx_payload : Annotated[ADABroadcastTxPayload, Field(..., description="Transaction to broadcast")], **kwargs) -> ApiResponse:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcast a signed transaction to the Cardano network  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_broadcast_tx_with_http_info(ada_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_broadcast_tx_payload: Transaction to broadcast (required)
        :type ada_broadcast_tx_payload: ADABroadcastTxPayload
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
        :rtype: tuple(PostAdaBroadcastTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'ada_broadcast_tx_payload'
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
                    " to method post_ada_broadcast_tx" % _key
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
        if _params['ada_broadcast_tx_payload'] is not None:
            _body_params = _params['ada_broadcast_tx_payload']

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
            '201': "PostAdaBroadcastTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/ada/transaction/broadcast', 'POST',
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
    def post_ada_prepare_tx(self, ada_prepare_tx_payload : Annotated[ADAPrepareTxPayload, Field(..., description="Transaction to prepare")], **kwargs) -> PostAdaPrepareTx201Response:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an unsigned transaction for broadcast by adding signatures to it  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_prepare_tx(ada_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_prepare_tx_payload: Transaction to prepare (required)
        :type ada_prepare_tx_payload: ADAPrepareTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAdaPrepareTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_ada_prepare_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_ada_prepare_tx_with_http_info(ada_prepare_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_ada_prepare_tx_with_http_info(self, ada_prepare_tx_payload : Annotated[ADAPrepareTxPayload, Field(..., description="Transaction to prepare")], **kwargs) -> ApiResponse:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an unsigned transaction for broadcast by adding signatures to it  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_prepare_tx_with_http_info(ada_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_prepare_tx_payload: Transaction to prepare (required)
        :type ada_prepare_tx_payload: ADAPrepareTxPayload
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
        :rtype: tuple(PostAdaPrepareTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'ada_prepare_tx_payload'
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
                    " to method post_ada_prepare_tx" % _key
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
        if _params['ada_prepare_tx_payload'] is not None:
            _body_params = _params['ada_prepare_tx_payload']

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
            '201': "PostAdaPrepareTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/ada/transaction/prepare', 'POST',
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
    def post_ada_stake_tx(self, ada_craft_stake_tx_payload : Annotated[ADACraftStakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostAdaStakeTx201Response:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Generates a delegate transaction on Cardano  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_stake_tx(ada_craft_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_craft_stake_tx_payload: Transaction to craft (required)
        :type ada_craft_stake_tx_payload: ADACraftStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAdaStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_ada_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_ada_stake_tx_with_http_info(ada_craft_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_ada_stake_tx_with_http_info(self, ada_craft_stake_tx_payload : Annotated[ADACraftStakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Generates a delegate transaction on Cardano  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_stake_tx_with_http_info(ada_craft_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_craft_stake_tx_payload: Transaction to craft (required)
        :type ada_craft_stake_tx_payload: ADACraftStakeTxPayload
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
        :rtype: tuple(PostAdaStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'ada_craft_stake_tx_payload'
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
                    " to method post_ada_stake_tx" % _key
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
        if _params['ada_craft_stake_tx_payload'] is not None:
            _body_params = _params['ada_craft_stake_tx_payload']

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
            '201': "PostAdaStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/ada/transaction/stake', 'POST',
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
    def post_ada_unstake_tx(self, ada_craft_unstake_tx_payload : Annotated[ADACraftUnstakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostAdaStakeTx201Response:  # noqa: E501
        """Unstake Transaction  # noqa: E501

        Generates an undelegate transaction on Cardano  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_unstake_tx(ada_craft_unstake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_craft_unstake_tx_payload: Transaction to craft (required)
        :type ada_craft_unstake_tx_payload: ADACraftUnstakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAdaStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_ada_unstake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_ada_unstake_tx_with_http_info(ada_craft_unstake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_ada_unstake_tx_with_http_info(self, ada_craft_unstake_tx_payload : Annotated[ADACraftUnstakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Unstake Transaction  # noqa: E501

        Generates an undelegate transaction on Cardano  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_unstake_tx_with_http_info(ada_craft_unstake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_craft_unstake_tx_payload: Transaction to craft (required)
        :type ada_craft_unstake_tx_payload: ADACraftUnstakeTxPayload
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
        :rtype: tuple(PostAdaStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'ada_craft_unstake_tx_payload'
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
                    " to method post_ada_unstake_tx" % _key
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
        if _params['ada_craft_unstake_tx_payload'] is not None:
            _body_params = _params['ada_craft_unstake_tx_payload']

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
            '201': "PostAdaStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/ada/transaction/unstake', 'POST',
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
    def post_ada_withdraw_rewards_tx(self, ada_craft_withdraw_rewards_tx_payload : Annotated[ADACraftWithdrawRewardsTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostAdaStakeTx201Response:  # noqa: E501
        """Withdraw Rewards Transaction  # noqa: E501

        Generates a withdraw rewards transaction on Cardano  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_withdraw_rewards_tx(ada_craft_withdraw_rewards_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_craft_withdraw_rewards_tx_payload: Transaction to craft (required)
        :type ada_craft_withdraw_rewards_tx_payload: ADACraftWithdrawRewardsTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAdaStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_ada_withdraw_rewards_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_ada_withdraw_rewards_tx_with_http_info(ada_craft_withdraw_rewards_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_ada_withdraw_rewards_tx_with_http_info(self, ada_craft_withdraw_rewards_tx_payload : Annotated[ADACraftWithdrawRewardsTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Withdraw Rewards Transaction  # noqa: E501

        Generates a withdraw rewards transaction on Cardano  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_ada_withdraw_rewards_tx_with_http_info(ada_craft_withdraw_rewards_tx_payload, async_req=True)
        >>> result = thread.get()

        :param ada_craft_withdraw_rewards_tx_payload: Transaction to craft (required)
        :type ada_craft_withdraw_rewards_tx_payload: ADACraftWithdrawRewardsTxPayload
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
        :rtype: tuple(PostAdaStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'ada_craft_withdraw_rewards_tx_payload'
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
                    " to method post_ada_withdraw_rewards_tx" % _key
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
        if _params['ada_craft_withdraw_rewards_tx_payload'] is not None:
            _body_params = _params['ada_craft_withdraw_rewards_tx_payload']

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
            '201': "PostAdaStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/ada/transaction/withdraw-rewards', 'POST',
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
