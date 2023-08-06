# coding: utf-8

# flake8: noqa
"""
    Kiln API

    This API provides reporting staking data on various protocols as well as network wide data, staking transaction crafting features and so on.  ### ACCESS  In order to use the Kiln API, you must first get an API token from your <a href=\"https://dashboard.kiln.fi/\">Kiln dashboard</a> (applications section). If you don't have access to our dashboard, please get in touch at hello@kiln.fi.  Once you have your API token, you can set it as a bearer token in your HTTP request headers, and target the Kiln API endpoint with the current MAJOR version of the API as a prefix to routes:  <blockquote> curl \"https://api.kiln.fi/v1/...\" -H \"Authorization: Bearer $KILN_API_TOKEN\" </blockquote>  <i> If you need a development environment, please reach out to hello@kiln.fi to have a specific access to our testnet environment and dedicated API endpoint. </i>  ### CHANGELOG  <details> <summary>Preview (experimental & candidate changes for Kiln API 1.2.0) <a href=\"/preview.html\">[link]</a></summary> <ul>   <li>ETH: Add new route GET <b>/v1/eth/exit-messages</b> to get GPG encrypted exit messages</li>   <li>ATOM: Add new route GET <b>/v1/atom/reports</b> to generate an Excel report of stakes and rewards</li>   <li>ATOM: Add new route GET <b>/v1/atom/stakes</b> to to list stakes</li>   <li>ATOM: Add new route GET <b>/v1/atom/rewards</b> to list rewards</li>   <li>ATOM: Add new method POST <b>/v1/atom/stakes</b> to link a stake to a Atom account</li>   <li>ATOM: Add new route GET <b>/v1/atom/network-stats</b> to view network statistics of Atom</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/stake</b> to generate a delegation transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/withdraw-rewards</b> to generate a withdraw-rewards transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/unstake</b> to generate an undelegate transaction</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>ATOM: Add new route POST <b>/v1/atom/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ATOM: Add new route GET <b>/v1/atom/transaction/status</b> to view the status of a broadcasted transaction</li>   <li>ADA: Add new route GET <b>/v1/ada/reports</b> to generate an Excel report of stakes and rewards</li> </ul> </details>  <details> <summary>Version 1.1.0 (2023-06-19) <a href=\"/v1.1.0.html\">[link]</a></summary> <ul>   <li>ACCOUNTS: Add the ability to list Kiln account via GET <b>/v1/accounts</b></li>   <li>ACCOUNTS: Add the ability to create Kiln account via POST <b>/v1/accounts</b></li>   <li>ACCOUNTS: Add the ability to describe a Kiln account via GET <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to update a Kiln account via PUT <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to delete a Kiln account via DEL <b>/v1/account</b></li>   <li>ACCOUNTS: Add the ability to get an account portfolio via GET <b>/v1/accounts/{id}/portfolio</b></li>    <li>ORGANIZATIONS: Add the ability to get an organization portfolio via GET <b>/v1/organizatrions/{id}/portfolio</b></li>    <li>ETH: Add the ability to query <b>/v1/eth/stakes</b>, <b>/v1/eth/rewards</b>, <b>/v1/eth/operations</b> by <b>proxies</b> and <b>validator_indexes</b></li>   <li>ETH: Add <b>validator_index</b> in the responses of <b>/v1/eth/stakes</b>, <b>/v1/eth/rewards</b> and <b>/v1/eth/operations</b></li>   <li>ETH: Add <b>delegated_at</b> field to <b>/v1/eth/stakes</b></li>   <li>ETH: Add <b>is_kiln</b> field to <b>/v1/eth/stakes</b></li>   <li>ETH: Add <b>eth_price_usd</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_entry_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_exit_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add <b>estimated_withdrawal_time_seconds</b> to <b>/v1/eth/netwok-stats</b></li>   <li>ETH: Add POST method to <b>/v1/eth/stakes</b> to link a stake to a Kiln account</li>   <li>ETH: Add new route GET <b>/v1/eth/operations</b> to list on-chain operations on a stake</li>   <li>ETH: Add new route GET <b>/v1/eth/kiln-stats</b> to expose Kiln operational statistics</li>   <li>ETH: Add new route POST <b>/v1/eth/keys</b> to generate ready-to-stake deposit data payloads</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/stake</b> to generate an EIP-1559 staking transaction ready to be signed</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/prepare</b> to craft a transaction ready to be broadcast from a payload and a signature</li>   <li>ETH: Add new route POST <b>/v1/eth/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ETH: Add new route GET <b>/v1/eth/transaction/status</b> to get the status of a broadcasted transaction</li>   <li>ETH: Add new route GET <b>/v1/eth/reports</b> to generate an Excel report of stakes and rewards</li>    <li>XTZ: Add new route GET <b>/v1/xtz/stakes</b> to to list stakes</li>   <li>XTZ: Add new route GET <b>/v1/xtz/rewards</b> to list rewards</li>   <li>XTZ: Add new route GET <b>/v1/xtz/operations</b> to list on-chain operations of a stake</li>   <li>XTZ: Add new route GET <b>/v1/xtz/network-stats</b> to view network statistics of Tezos</li>   <li>XTZ: Add new route GET <b>/v1/xtz/reports</b> to generate an Excel report</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/stake</b> to generate a delegation transaction</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/unstake</b> to generate an undelegation transaction</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>XTZ: Add new route POST <b>/v1/xtz/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>XTZ: Add new route GET <b>/v1/xtz/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>SOL: Add new route GET <b>/v1/sol/stakes</b> to to list stakes</li>   <li>SOL: Add new method POST <b>/v1/sol/stakes</b> to link a stake to a Solana account</li>   <li>SOL: Add new route GET <b>/v1/sol/rewards</b> to list rewards</li>   <li>SOL: Add new route GET <b>/v1/sol/operations</b> to list on-chain operations of a stake</li>   <li>SOL: Add new route GET <b>/v1/sol/network-stats</b> to view network statistics of Solana</li>   <li>SOL: Add new route GET <b>/v1/sol/reports</b> to generate an Excel report</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/stake</b> to generate a delegation transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/deactivate-stake</b> to generate a deactivate transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/withdraw-stake</b> to prepare a withdraw stake transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/merge-stakes</b> to prepare a merge stakes transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/split-stake</b> to prepare a split stake transaction</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/prepare</b> to prepare any transaction from a payload and signature</li>   <li>SOL: Add new route POST <b>/v1/sol/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>SOL: Add new route GET <b>/v1/sol/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>ADA: Add new route POST <b>/v1/ada/transaction/stake</b> to generate a delegation transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/withdraw-rewards</b> to generate a withdraw-rewards transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/unstake</b> to generate an undelegate transaction</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/prepare</b> to prepare a transaction for broadcasting from a payload and a signature</li>   <li>ADA: Add new route POST <b>/v1/ada/transaction/broadcast</b> to broadcast a signed transaction</li>   <li>ADA: Add new route GET <b>/v1/ada/transaction/status</b> to view the status of a broadcasted transaction</li>    <li>MATIC: Add new route POST <b>/v1/matic/transaction/approve</b> to generate a transaction to allow a smart-contract to spend MATIC tokens on behalf of the user</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/buy-voucher</b> to generate a transaction to buy shares from a validator</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/sell-voucher</b> to generate a transaction to sell shares from a validator</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/unstake-claim-tokens</b> to generate a transaction to withdraw unbounded tokens</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/withdraw-rewards</b> to generate a transaction to withdraw rewards</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/restake-rewards</b> to generate a transaction to restake rewards</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/prepare</b> to prepare a signed transaction for broadcasting</li>   <li>MATIC: Add new route POST <b>/v1/matic/transaction/broadcast</b> to broadcast a prepared transaction</li>   <li>MATIC: Add new route GET <b>/v1/matic/transaction/status</b> to view the status of a broadcasted transaction</li>  </ul> </details>  <details> <summary>Version 1.0.0 (2023-01-01) <a href=\"/v1.0.0.html\">[link]</a></summary>  <ul>   <li>ETH: Initial support of GET <b>/v1/eth/stakes</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/rewards</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/network-stats</b> endpoint</li>   <li>ETH: Initial support of GET <b>/v1/eth/keys</b> endpoint</li> </ul>  </details>  ### VERSIONING  Versions of the Kiln API use <b>MAJOR.MINOR.PATCH</b> where:  - <b>MAJOR</b> version is increased when there is major   incompatible API changes, major versions will be communicated in   advance to all customers with a smooth transition path that   spans over a minimum period of 3 MINOR versions or ~3   months. <i>Intended frequency: 1 year</i>. - <b>MINOR</b> version is increased for backward compatible API   changes without notice, or communicated breaking changes with a   1 minor version notice and a smooth migration path. Minor   versions will be communicated regularly to customers with the   changelog. <i>Intended frequency: 1 month</i>. - <b>PATCH</b> version is increased for backward compatible   hot-fixes, patch versions will be communicated to affected   customers.  <i> Due to the nature of blockchains (protocol disappearing, breaking protocol upgrades), Kiln may introduce backward-incompatible changes in MINOR versions after following a 1 MINOR version deprecation path (~1 month). These impacting changes will be narrowed as much as possible to the protocol, heavily communicated with clear guidelines and support. Customer not relying on affected protocols will not be affected. </i>  ### BACKWARD COMPATIBILITY  Kiln considers the following changes to be backward compatible:  - Adding new API routes. - Adding new optional request parameters to existing API methods. - Adding new properties to existing API responses. - Changing the order of properties in existing API responses. - Adding new event types in existing enums.  Non-breaking changes may be introduced in our API and subject to modification before being officialy communicated and documented here. Your application should not depend on them until part of this specification. The preview Kiln API specifications with upcoming and experimental new features can be found [here](/preview.html).  # noqa: E501

    The version of the OpenAPI document: Preview
    Contact: contact@kiln.fi
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


# import models into model package
from kiln_connect.openapi_client.models.ada_broadcast_tx_payload import ADABroadcastTxPayload
from kiln_connect.openapi_client.models.ada_craft_stake_tx_payload import ADACraftStakeTxPayload
from kiln_connect.openapi_client.models.ada_craft_unstake_tx_payload import ADACraftUnstakeTxPayload
from kiln_connect.openapi_client.models.ada_craft_withdraw_rewards_tx_payload import ADACraftWithdrawRewardsTxPayload
from kiln_connect.openapi_client.models.ada_prepare_tx_payload import ADAPrepareTxPayload
from kiln_connect.openapi_client.models.ada_prepare_tx_payload_signed_messages_inner import ADAPrepareTxPayloadSignedMessagesInner
from kiln_connect.openapi_client.models.ada_signed_tx import ADASignedTx
from kiln_connect.openapi_client.models.adatx_hash import ADATxHash
from kiln_connect.openapi_client.models.adatx_status import ADATxStatus
from kiln_connect.openapi_client.models.ada_unsigned_tx import ADAUnsignedTx
from kiln_connect.openapi_client.models.atom_broadcast_tx_payload import ATOMBroadcastTxPayload
from kiln_connect.openapi_client.models.atom_craft_stake_tx_payload import ATOMCraftStakeTxPayload
from kiln_connect.openapi_client.models.atom_craft_unstake_tx_payload import ATOMCraftUnstakeTxPayload
from kiln_connect.openapi_client.models.atom_craft_withdraw_rewards_tx_payload import ATOMCraftWithdrawRewardsTxPayload
from kiln_connect.openapi_client.models.atom_network_stats import ATOMNetworkStats
from kiln_connect.openapi_client.models.atom_prepare_tx_payload import ATOMPrepareTxPayload
from kiln_connect.openapi_client.models.atom_reward import ATOMReward
from kiln_connect.openapi_client.models.atom_signed_tx import ATOMSignedTx
from kiln_connect.openapi_client.models.atom_stake import ATOMStake
from kiln_connect.openapi_client.models.atomtx_hash import ATOMTxHash
from kiln_connect.openapi_client.models.atomtx_status import ATOMTxStatus
from kiln_connect.openapi_client.models.atom_unsigned_tx import ATOMUnsignedTx
from kiln_connect.openapi_client.models.account import Account
from kiln_connect.openapi_client.models.account_payload import AccountPayload
from kiln_connect.openapi_client.models.core_stake import CoreStake
from kiln_connect.openapi_client.models.eth_broadcast_tx_payload import ETHBroadcastTxPayload
from kiln_connect.openapi_client.models.eth_broadcasted_tx import ETHBroadcastedTx
from kiln_connect.openapi_client.models.eth_craft_stake_tx_payload import ETHCraftStakeTxPayload
from kiln_connect.openapi_client.models.eth_exit_message import ETHExitMessage
from kiln_connect.openapi_client.models.eth_kiln_stats import ETHKilnStats
from kiln_connect.openapi_client.models.eth_kiln_stats_gross_apy import ETHKilnStatsGrossApy
from kiln_connect.openapi_client.models.eth_network_stats import ETHNetworkStats
from kiln_connect.openapi_client.models.eth_operation_consensus_withdrawal import ETHOperationConsensusWithdrawal
from kiln_connect.openapi_client.models.eth_operation_deposit import ETHOperationDeposit
from kiln_connect.openapi_client.models.eth_operation_execution_reward import ETHOperationExecutionReward
from kiln_connect.openapi_client.models.eth_post_keys_batch_response import ETHPostKeysBatchResponse
from kiln_connect.openapi_client.models.eth_post_keys_cli_response_inner import ETHPostKeysCliResponseInner
from kiln_connect.openapi_client.models.eth_post_keys_payload import ETHPostKeysPayload
from kiln_connect.openapi_client.models.eth_prepare_tx_payload import ETHPrepareTxPayload
from kiln_connect.openapi_client.models.eth_reward import ETHReward
from kiln_connect.openapi_client.models.eth_signed_tx import ETHSignedTx
from kiln_connect.openapi_client.models.eth_stake import ETHStake
from kiln_connect.openapi_client.models.ethtx_status import ETHTxStatus
from kiln_connect.openapi_client.models.eth_unsigned_tx import ETHUnsignedTx
from kiln_connect.openapi_client.models.get_account_portfolio200_response import GetAccountPortfolio200Response
from kiln_connect.openapi_client.models.get_accounts200_response import GetAccounts200Response
from kiln_connect.openapi_client.models.get_ada_tx_status200_response import GetAdaTxStatus200Response
from kiln_connect.openapi_client.models.get_atom_network_stats200_response import GetAtomNetworkStats200Response
from kiln_connect.openapi_client.models.get_atom_rewards200_response import GetAtomRewards200Response
from kiln_connect.openapi_client.models.get_atom_stakes200_response import GetAtomStakes200Response
from kiln_connect.openapi_client.models.get_atom_tx_status200_response import GetAtomTxStatus200Response
from kiln_connect.openapi_client.models.get_eth_kiln_stats200_response import GetEthKilnStats200Response
from kiln_connect.openapi_client.models.get_eth_network_stats200_response import GetEthNetworkStats200Response
from kiln_connect.openapi_client.models.get_eth_operations200_response import GetEthOperations200Response
from kiln_connect.openapi_client.models.get_eth_operations200_response_data_inner import GetEthOperations200ResponseDataInner
from kiln_connect.openapi_client.models.get_eth_rewards200_response import GetEthRewards200Response
from kiln_connect.openapi_client.models.get_eth_stakes200_response import GetEthStakes200Response
from kiln_connect.openapi_client.models.get_eth_tx_status200_response import GetEthTxStatus200Response
from kiln_connect.openapi_client.models.get_exit_message200_response import GetExitMessage200Response
from kiln_connect.openapi_client.models.get_matic_tx_status200_response import GetMaticTxStatus200Response
from kiln_connect.openapi_client.models.get_sol_network_stats200_response import GetSolNetworkStats200Response
from kiln_connect.openapi_client.models.get_sol_operations200_response import GetSolOperations200Response
from kiln_connect.openapi_client.models.get_sol_operations200_response_data_inner import GetSolOperations200ResponseDataInner
from kiln_connect.openapi_client.models.get_sol_rewards200_response import GetSolRewards200Response
from kiln_connect.openapi_client.models.get_sol_rewards200_response_data_inner import GetSolRewards200ResponseDataInner
from kiln_connect.openapi_client.models.get_sol_stakes200_response import GetSolStakes200Response
from kiln_connect.openapi_client.models.get_sol_tx_status200_response import GetSolTxStatus200Response
from kiln_connect.openapi_client.models.get_xtz_network_stats200_response import GetXtzNetworkStats200Response
from kiln_connect.openapi_client.models.get_xtz_operations200_response import GetXtzOperations200Response
from kiln_connect.openapi_client.models.get_xtz_operations200_response_data_inner import GetXtzOperations200ResponseDataInner
from kiln_connect.openapi_client.models.get_xtz_rewards200_response import GetXtzRewards200Response
from kiln_connect.openapi_client.models.get_xtz_rewards200_response_data_inner import GetXtzRewards200ResponseDataInner
from kiln_connect.openapi_client.models.get_xtz_stakes200_response import GetXtzStakes200Response
from kiln_connect.openapi_client.models.get_xtz_tx_status200_response import GetXtzTxStatus200Response
from kiln_connect.openapi_client.models.matic_broadcast_tx_payload import MATICBroadcastTxPayload
from kiln_connect.openapi_client.models.matic_broadcasted_tx import MATICBroadcastedTx
from kiln_connect.openapi_client.models.matic_craft_approve_tx_payload import MATICCraftApproveTxPayload
from kiln_connect.openapi_client.models.matic_craft_buy_voucher_tx_payload import MATICCraftBuyVoucherTxPayload
from kiln_connect.openapi_client.models.matic_craft_restake_rewards_tx_payload import MATICCraftRestakeRewardsTxPayload
from kiln_connect.openapi_client.models.matic_craft_sell_voucher_tx_payload import MATICCraftSellVoucherTxPayload
from kiln_connect.openapi_client.models.matic_craft_unstake_claim_tokens_tx_payload import MATICCraftUnstakeClaimTokensTxPayload
from kiln_connect.openapi_client.models.matic_craft_withdraw_rewards_tx_payload import MATICCraftWithdrawRewardsTxPayload
from kiln_connect.openapi_client.models.matic_prepare_tx_payload import MATICPrepareTxPayload
from kiln_connect.openapi_client.models.matic_signed_tx import MATICSignedTx
from kiln_connect.openapi_client.models.matictx_status import MATICTxStatus
from kiln_connect.openapi_client.models.matic_unsigned_tx import MATICUnsignedTx
from kiln_connect.openapi_client.models.portfolio import Portfolio
from kiln_connect.openapi_client.models.portfolio_protocols_inner import PortfolioProtocolsInner
from kiln_connect.openapi_client.models.portfolio_protocols_inner_total_balance import PortfolioProtocolsInnerTotalBalance
from kiln_connect.openapi_client.models.portfolio_protocols_inner_total_rewards import PortfolioProtocolsInnerTotalRewards
from kiln_connect.openapi_client.models.post_atom_stakes_payload import PostATOMStakesPayload
from kiln_connect.openapi_client.models.post_atom_stakes_payload_stakes_inner import PostATOMStakesPayloadStakesInner
from kiln_connect.openapi_client.models.post_account201_response import PostAccount201Response
from kiln_connect.openapi_client.models.post_ada_broadcast_tx201_response import PostAdaBroadcastTx201Response
from kiln_connect.openapi_client.models.post_ada_prepare_tx201_response import PostAdaPrepareTx201Response
from kiln_connect.openapi_client.models.post_ada_stake_tx201_response import PostAdaStakeTx201Response
from kiln_connect.openapi_client.models.post_atom_broadcast_tx201_response import PostAtomBroadcastTx201Response
from kiln_connect.openapi_client.models.post_atom_prepare_tx201_response import PostAtomPrepareTx201Response
from kiln_connect.openapi_client.models.post_atom_stake_tx201_response import PostAtomStakeTx201Response
from kiln_connect.openapi_client.models.post_eth_stakes_payload import PostETHStakesPayload
from kiln_connect.openapi_client.models.post_eth_stakes_payload_stakes_inner import PostETHStakesPayloadStakesInner
from kiln_connect.openapi_client.models.post_eth_broadcast_tx201_response import PostEthBroadcastTx201Response
from kiln_connect.openapi_client.models.post_eth_keys201_response import PostEthKeys201Response
from kiln_connect.openapi_client.models.post_eth_keys201_response_data import PostEthKeys201ResponseData
from kiln_connect.openapi_client.models.post_eth_prepare_tx201_response import PostEthPrepareTx201Response
from kiln_connect.openapi_client.models.post_eth_stake_tx201_response import PostEthStakeTx201Response
from kiln_connect.openapi_client.models.post_eth_stakes201_response import PostEthStakes201Response
from kiln_connect.openapi_client.models.post_matic_approve_tx201_response import PostMaticApproveTx201Response
from kiln_connect.openapi_client.models.post_matic_broadcast_tx201_response import PostMaticBroadcastTx201Response
from kiln_connect.openapi_client.models.post_matic_prepare_tx201_response import PostMaticPrepareTx201Response
from kiln_connect.openapi_client.models.post_sol_broadcast_tx201_response import PostSolBroadcastTx201Response
from kiln_connect.openapi_client.models.post_sol_prepare_tx201_response import PostSolPrepareTx201Response
from kiln_connect.openapi_client.models.post_sol_stake_tx201_response import PostSolStakeTx201Response
from kiln_connect.openapi_client.models.post_xtz_broadcast_tx201_response import PostXtzBroadcastTx201Response
from kiln_connect.openapi_client.models.post_xtz_prepare_tx201_response import PostXtzPrepareTx201Response
from kiln_connect.openapi_client.models.post_xtz_stake_tx201_response import PostXtzStakeTx201Response
from kiln_connect.openapi_client.models.sol_broadcast_tx import SOLBroadcastTx
from kiln_connect.openapi_client.models.sol_broadcast_tx_payload import SOLBroadcastTxPayload
from kiln_connect.openapi_client.models.sol_deactivate_stake_tx_payload import SOLDeactivateStakeTxPayload
from kiln_connect.openapi_client.models.sol_merge_stakes_tx_payload import SOLMergeStakesTxPayload
from kiln_connect.openapi_client.models.sol_network_stats import SOLNetworkStats
from kiln_connect.openapi_client.models.sol_operation_create_account import SOLOperationCreateAccount
from kiln_connect.openapi_client.models.sol_operation_create_account_with_seed import SOLOperationCreateAccountWithSeed
from kiln_connect.openapi_client.models.sol_operation_deactivate import SOLOperationDeactivate
from kiln_connect.openapi_client.models.sol_operation_delegate import SOLOperationDelegate
from kiln_connect.openapi_client.models.sol_operation_merge import SOLOperationMerge
from kiln_connect.openapi_client.models.sol_operation_redelegate import SOLOperationRedelegate
from kiln_connect.openapi_client.models.sol_operation_split import SOLOperationSplit
from kiln_connect.openapi_client.models.sol_operation_withdraw import SOLOperationWithdraw
from kiln_connect.openapi_client.models.sol_post_stakes_payload import SOLPostStakesPayload
from kiln_connect.openapi_client.models.sol_post_stakes_payload_stakes_inner import SOLPostStakesPayloadStakesInner
from kiln_connect.openapi_client.models.sol_prepare_tx_payload import SOLPrepareTxPayload
from kiln_connect.openapi_client.models.sol_prepared_tx import SOLPreparedTx
from kiln_connect.openapi_client.models.sol_reward_by_day import SOLRewardByDay
from kiln_connect.openapi_client.models.sol_reward_by_epoch import SOLRewardByEpoch
from kiln_connect.openapi_client.models.sol_split_stake_tx_payload import SOLSplitStakeTxPayload
from kiln_connect.openapi_client.models.sol_stake import SOLStake
from kiln_connect.openapi_client.models.sol_stake_tx import SOLStakeTx
from kiln_connect.openapi_client.models.sol_stake_tx_payload import SOLStakeTxPayload
from kiln_connect.openapi_client.models.soltx_status import SOLTxStatus
from kiln_connect.openapi_client.models.sol_withdraw_stake_tx_payload import SOLWithdrawStakeTxPayload
from kiln_connect.openapi_client.models.xtz_broadcast_tx_payload import XTZBroadcastTxPayload
from kiln_connect.openapi_client.models.xtz_broadcasted_tx import XTZBroadcastedTx
from kiln_connect.openapi_client.models.xtz_craft_stake_tx_payload import XTZCraftStakeTxPayload
from kiln_connect.openapi_client.models.xtz_craft_un_stake_tx_payload import XTZCraftUnStakeTxPayload
from kiln_connect.openapi_client.models.xtz_cycle_reward import XTZCycleReward
from kiln_connect.openapi_client.models.xtz_daily_reward import XTZDailyReward
from kiln_connect.openapi_client.models.xtz_network_stats import XTZNetworkStats
from kiln_connect.openapi_client.models.xtz_operation_activation import XTZOperationActivation
from kiln_connect.openapi_client.models.xtz_operation_delegate import XTZOperationDelegate
from kiln_connect.openapi_client.models.xtz_operation_payment import XTZOperationPayment
from kiln_connect.openapi_client.models.xtz_operation_undelegate import XTZOperationUndelegate
from kiln_connect.openapi_client.models.xtz_prepare_tx_payload import XTZPrepareTxPayload
from kiln_connect.openapi_client.models.xtz_signed_tx import XTZSignedTx
from kiln_connect.openapi_client.models.xtz_stake import XTZStake
from kiln_connect.openapi_client.models.xtztx_status import XTZTxStatus
from kiln_connect.openapi_client.models.xtz_unsigned_tx import XTZUnsignedTx
