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

from pydantic import Field, StrictStr, conlist

from typing import Optional, Union

from kiln_connect.openapi_client.models.atom_broadcast_tx_payload import ATOMBroadcastTxPayload
from kiln_connect.openapi_client.models.atom_craft_stake_tx_payload import ATOMCraftStakeTxPayload
from kiln_connect.openapi_client.models.atom_craft_unstake_tx_payload import ATOMCraftUnstakeTxPayload
from kiln_connect.openapi_client.models.atom_craft_withdraw_rewards_tx_payload import ATOMCraftWithdrawRewardsTxPayload
from kiln_connect.openapi_client.models.atom_prepare_tx_payload import ATOMPrepareTxPayload
from kiln_connect.openapi_client.models.get_atom_network_stats200_response import GetAtomNetworkStats200Response
from kiln_connect.openapi_client.models.get_atom_rewards200_response import GetAtomRewards200Response
from kiln_connect.openapi_client.models.get_atom_stakes200_response import GetAtomStakes200Response
from kiln_connect.openapi_client.models.get_atom_tx_status200_response import GetAtomTxStatus200Response
from kiln_connect.openapi_client.models.post_atom_stakes_payload import PostATOMStakesPayload
from kiln_connect.openapi_client.models.post_atom_broadcast_tx201_response import PostAtomBroadcastTx201Response
from kiln_connect.openapi_client.models.post_atom_prepare_tx201_response import PostAtomPrepareTx201Response
from kiln_connect.openapi_client.models.post_atom_stake_tx201_response import PostAtomStakeTx201Response
from kiln_connect.openapi_client.models.post_eth_stakes201_response import PostEthStakes201Response

from kiln_connect.openapi_client.api_client import ApiClient
from kiln_connect.openapi_client.api_response import ApiResponse
from kiln_connect.openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class AtomApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def get_atom_network_stats(self, **kwargs) -> GetAtomNetworkStats200Response:  # noqa: E501
        """Network Stats  # noqa: E501

        Get some network statistics on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_network_stats(async_req=True)
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
        :rtype: GetAtomNetworkStats200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_atom_network_stats_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_atom_network_stats_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def get_atom_network_stats_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Network Stats  # noqa: E501

        Get some network statistics on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_network_stats_with_http_info(async_req=True)
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
        :rtype: tuple(GetAtomNetworkStats200Response, status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_atom_network_stats" % _key
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
            '200': "GetAtomNetworkStats200Response",
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/network-stats', 'GET',
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
    def get_atom_reports(self, delegators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> bytearray:  # noqa: E501
        """Reports  # noqa: E501

        Get reports on Cosmos staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_reports(delegators, validators, accounts, async_req=True)
        >>> result = thread.get()

        :param delegators: Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type delegators: List[str]
        :param validators: Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type validators: List[str]
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
            raise ValueError("Error! Please call the get_atom_reports_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_atom_reports_with_http_info(delegators, validators, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_atom_reports_with_http_info(self, delegators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Reports  # noqa: E501

        Get reports on Cosmos staking  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_reports_with_http_info(delegators, validators, accounts, async_req=True)
        >>> result = thread.get()

        :param delegators: Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type delegators: List[str]
        :param validators: Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type validators: List[str]
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
            'delegators',
            'validators',
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
                    " to method get_atom_reports" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('delegators') is not None:  # noqa: E501
            _query_params.append(('delegators', _params['delegators']))
            _collection_formats['delegators'] = 'csv'

        if _params.get('validators') is not None:  # noqa: E501
            _query_params.append(('validators', _params['validators']))
            _collection_formats['validators'] = 'csv'

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
            '/v1/atom/reports', 'GET',
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
    def get_atom_rewards(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, delegators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, start_date : Annotated[Optional[date], Field(description="Get rewards from this date (YYYY-MM-DD)")] = None, end_date : Annotated[Optional[date], Field(description="Get rewards to this date (YYYY-MM-DD)")] = None, **kwargs) -> GetAtomRewards200Response:  # noqa: E501
        """Rewards  # noqa: E501

        Get historical rewards by day of ATOM stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_rewards(validators, delegators, accounts, start_date, end_date, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type validators: List[str]
        :param delegators: Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type delegators: List[str]
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
        :rtype: GetAtomRewards200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_atom_rewards_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_atom_rewards_with_http_info(validators, delegators, accounts, start_date, end_date, **kwargs)  # noqa: E501

    @validate_arguments
    def get_atom_rewards_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, delegators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, start_date : Annotated[Optional[date], Field(description="Get rewards from this date (YYYY-MM-DD)")] = None, end_date : Annotated[Optional[date], Field(description="Get rewards to this date (YYYY-MM-DD)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Rewards  # noqa: E501

        Get historical rewards by day of ATOM stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_rewards_with_http_info(validators, delegators, accounts, start_date, end_date, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type validators: List[str]
        :param delegators: Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type delegators: List[str]
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
        :rtype: tuple(GetAtomRewards200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators',
            'delegators',
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
                    " to method get_atom_rewards" % _key
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

        if _params.get('delegators') is not None:  # noqa: E501
            _query_params.append(('delegators', _params['delegators']))
            _collection_formats['delegators'] = 'csv'

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
            '200': "GetAtomRewards200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/rewards', 'GET',
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
    def get_atom_stakes(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, delegators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> GetAtomStakes200Response:  # noqa: E501
        """Stakes  # noqa: E501

        Get the status of ATOM stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_stakes(validators, delegators, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type validators: List[str]
        :param delegators: Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type delegators: List[str]
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
        :rtype: GetAtomStakes200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_atom_stakes_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_atom_stakes_with_http_info(validators, delegators, accounts, **kwargs)  # noqa: E501

    @validate_arguments
    def get_atom_stakes_with_http_info(self, validators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, delegators : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. ")] = None, accounts : Annotated[Optional[conlist(StrictStr)], Field(description="Comma-separated list of Kiln accounts identifiers")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Stakes  # noqa: E501

        Get the status of ATOM stakes  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_stakes_with_http_info(validators, delegators, accounts, async_req=True)
        >>> result = thread.get()

        :param validators: Comma-separated list of validators addresses, these addresses are matched with the corresponding delegator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type validators: List[str]
        :param delegators: Comma-separated list of delegator addresses, these addresses are matched with the corresponding validator addresses. To fetch a specific stake, pass your wallet address and the validator address as parameters. 
        :type delegators: List[str]
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
        :rtype: tuple(GetAtomStakes200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'validators',
            'delegators',
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
                    " to method get_atom_stakes" % _key
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

        if _params.get('delegators') is not None:  # noqa: E501
            _query_params.append(('delegators', _params['delegators']))
            _collection_formats['delegators'] = 'csv'

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
            '200': "GetAtomStakes200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/stakes', 'GET',
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
    def get_atom_tx_status(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> GetAtomTxStatus200Response:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_tx_status(tx_hash, async_req=True)
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
        :rtype: GetAtomTxStatus200Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the get_atom_tx_status_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.get_atom_tx_status_with_http_info(tx_hash, **kwargs)  # noqa: E501

    @validate_arguments
    def get_atom_tx_status_with_http_info(self, tx_hash : Annotated[StrictStr, Field(..., description="Hash of the transaction")], **kwargs) -> ApiResponse:  # noqa: E501
        """Transaction Status  # noqa: E501

        Get the status of a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_atom_tx_status_with_http_info(tx_hash, async_req=True)
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
        :rtype: tuple(GetAtomTxStatus200Response, status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_atom_tx_status" % _key
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
            '200': "GetAtomTxStatus200Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/transaction/status', 'GET',
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
    def post_atom_broadcast_tx(self, atom_broadcast_tx_payload : Annotated[ATOMBroadcastTxPayload, Field(..., description="Transaction to broadcast")], **kwargs) -> PostAtomBroadcastTx201Response:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcast a signed transaction to the Cosmos network  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_broadcast_tx(atom_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_broadcast_tx_payload: Transaction to broadcast (required)
        :type atom_broadcast_tx_payload: ATOMBroadcastTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAtomBroadcastTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_atom_broadcast_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_atom_broadcast_tx_with_http_info(atom_broadcast_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_atom_broadcast_tx_with_http_info(self, atom_broadcast_tx_payload : Annotated[ATOMBroadcastTxPayload, Field(..., description="Transaction to broadcast")], **kwargs) -> ApiResponse:  # noqa: E501
        """Broadcast Transaction  # noqa: E501

        Broadcast a signed transaction to the Cosmos network  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_broadcast_tx_with_http_info(atom_broadcast_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_broadcast_tx_payload: Transaction to broadcast (required)
        :type atom_broadcast_tx_payload: ATOMBroadcastTxPayload
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
        :rtype: tuple(PostAtomBroadcastTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'atom_broadcast_tx_payload'
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
                    " to method post_atom_broadcast_tx" % _key
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
        if _params['atom_broadcast_tx_payload'] is not None:
            _body_params = _params['atom_broadcast_tx_payload']

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
            '201': "PostAtomBroadcastTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/transaction/broadcast', 'POST',
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
    def post_atom_prepare_tx(self, atom_prepare_tx_payload : Annotated[ATOMPrepareTxPayload, Field(..., description="Transaction to prepare")], **kwargs) -> PostAtomPrepareTx201Response:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an unsigned transaction for broadcast by adding signatures to it  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_prepare_tx(atom_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_prepare_tx_payload: Transaction to prepare (required)
        :type atom_prepare_tx_payload: ATOMPrepareTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAtomPrepareTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_atom_prepare_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_atom_prepare_tx_with_http_info(atom_prepare_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_atom_prepare_tx_with_http_info(self, atom_prepare_tx_payload : Annotated[ATOMPrepareTxPayload, Field(..., description="Transaction to prepare")], **kwargs) -> ApiResponse:  # noqa: E501
        """Prepare Transaction  # noqa: E501

        Prepare an unsigned transaction for broadcast by adding signatures to it  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_prepare_tx_with_http_info(atom_prepare_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_prepare_tx_payload: Transaction to prepare (required)
        :type atom_prepare_tx_payload: ATOMPrepareTxPayload
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
        :rtype: tuple(PostAtomPrepareTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'atom_prepare_tx_payload'
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
                    " to method post_atom_prepare_tx" % _key
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
        if _params['atom_prepare_tx_payload'] is not None:
            _body_params = _params['atom_prepare_tx_payload']

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
            '201': "PostAtomPrepareTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/transaction/prepare', 'POST',
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
    def post_atom_stake_tx(self, atom_craft_stake_tx_payload : Annotated[ATOMCraftStakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostAtomStakeTx201Response:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Generates a delegate transaction on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_stake_tx(atom_craft_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_craft_stake_tx_payload: Transaction to craft (required)
        :type atom_craft_stake_tx_payload: ATOMCraftStakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAtomStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_atom_stake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_atom_stake_tx_with_http_info(atom_craft_stake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_atom_stake_tx_with_http_info(self, atom_craft_stake_tx_payload : Annotated[ATOMCraftStakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Stake Transaction  # noqa: E501

        Generates a delegate transaction on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_stake_tx_with_http_info(atom_craft_stake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_craft_stake_tx_payload: Transaction to craft (required)
        :type atom_craft_stake_tx_payload: ATOMCraftStakeTxPayload
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
        :rtype: tuple(PostAtomStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'atom_craft_stake_tx_payload'
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
                    " to method post_atom_stake_tx" % _key
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
        if _params['atom_craft_stake_tx_payload'] is not None:
            _body_params = _params['atom_craft_stake_tx_payload']

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
            '201': "PostAtomStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/transaction/stake', 'POST',
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
    def post_atom_stakes(self, post_atom_stakes_payload : Annotated[PostATOMStakesPayload, Field(..., description="Stakes to create")], **kwargs) -> PostEthStakes201Response:  # noqa: E501
        """Create stakes  # noqa: E501

        Link an ATOM stake to a Kiln account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_stakes(post_atom_stakes_payload, async_req=True)
        >>> result = thread.get()

        :param post_atom_stakes_payload: Stakes to create (required)
        :type post_atom_stakes_payload: PostATOMStakesPayload
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
            raise ValueError("Error! Please call the post_atom_stakes_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_atom_stakes_with_http_info(post_atom_stakes_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_atom_stakes_with_http_info(self, post_atom_stakes_payload : Annotated[PostATOMStakesPayload, Field(..., description="Stakes to create")], **kwargs) -> ApiResponse:  # noqa: E501
        """Create stakes  # noqa: E501

        Link an ATOM stake to a Kiln account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_stakes_with_http_info(post_atom_stakes_payload, async_req=True)
        >>> result = thread.get()

        :param post_atom_stakes_payload: Stakes to create (required)
        :type post_atom_stakes_payload: PostATOMStakesPayload
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
            'post_atom_stakes_payload'
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
                    " to method post_atom_stakes" % _key
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
        if _params['post_atom_stakes_payload'] is not None:
            _body_params = _params['post_atom_stakes_payload']

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
            '/v1/atom/stakes', 'POST',
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
    def post_atom_unstake_tx(self, atom_craft_unstake_tx_payload : Annotated[ATOMCraftUnstakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostAtomStakeTx201Response:  # noqa: E501
        """Unstake Transaction  # noqa: E501

        Generates an undelegate transaction on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_unstake_tx(atom_craft_unstake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_craft_unstake_tx_payload: Transaction to craft (required)
        :type atom_craft_unstake_tx_payload: ATOMCraftUnstakeTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAtomStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_atom_unstake_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_atom_unstake_tx_with_http_info(atom_craft_unstake_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_atom_unstake_tx_with_http_info(self, atom_craft_unstake_tx_payload : Annotated[ATOMCraftUnstakeTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Unstake Transaction  # noqa: E501

        Generates an undelegate transaction on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_unstake_tx_with_http_info(atom_craft_unstake_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_craft_unstake_tx_payload: Transaction to craft (required)
        :type atom_craft_unstake_tx_payload: ATOMCraftUnstakeTxPayload
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
        :rtype: tuple(PostAtomStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'atom_craft_unstake_tx_payload'
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
                    " to method post_atom_unstake_tx" % _key
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
        if _params['atom_craft_unstake_tx_payload'] is not None:
            _body_params = _params['atom_craft_unstake_tx_payload']

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
            '201': "PostAtomStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/transaction/unstake', 'POST',
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
    def post_atom_withdraw_rewards_tx(self, atom_craft_withdraw_rewards_tx_payload : Annotated[ATOMCraftWithdrawRewardsTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> PostAtomStakeTx201Response:  # noqa: E501
        """Withdraw Rewards Transaction  # noqa: E501

        Generates a withdraw rewards transaction on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_withdraw_rewards_tx(atom_craft_withdraw_rewards_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_craft_withdraw_rewards_tx_payload: Transaction to craft (required)
        :type atom_craft_withdraw_rewards_tx_payload: ATOMCraftWithdrawRewardsTxPayload
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostAtomStakeTx201Response
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            raise ValueError("Error! Please call the post_atom_withdraw_rewards_tx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data")
        return self.post_atom_withdraw_rewards_tx_with_http_info(atom_craft_withdraw_rewards_tx_payload, **kwargs)  # noqa: E501

    @validate_arguments
    def post_atom_withdraw_rewards_tx_with_http_info(self, atom_craft_withdraw_rewards_tx_payload : Annotated[ATOMCraftWithdrawRewardsTxPayload, Field(..., description="Transaction to craft")], **kwargs) -> ApiResponse:  # noqa: E501
        """Withdraw Rewards Transaction  # noqa: E501

        Generates a withdraw rewards transaction on Cosmos  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.post_atom_withdraw_rewards_tx_with_http_info(atom_craft_withdraw_rewards_tx_payload, async_req=True)
        >>> result = thread.get()

        :param atom_craft_withdraw_rewards_tx_payload: Transaction to craft (required)
        :type atom_craft_withdraw_rewards_tx_payload: ATOMCraftWithdrawRewardsTxPayload
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
        :rtype: tuple(PostAtomStakeTx201Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'atom_craft_withdraw_rewards_tx_payload'
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
                    " to method post_atom_withdraw_rewards_tx" % _key
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
        if _params['atom_craft_withdraw_rewards_tx_payload'] is not None:
            _body_params = _params['atom_craft_withdraw_rewards_tx_payload']

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
            '201': "PostAtomStakeTx201Response",
            '400': None,
            '401': None,
            '500': None,
        }

        return self.api_client.call_api(
            '/v1/atom/transaction/withdraw-rewards', 'POST',
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
