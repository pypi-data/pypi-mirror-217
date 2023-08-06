"""Solana commands.

This file contains multiple CLI commands showcasing how to use the
KilnConnect SDK to interact with the Solana blockchain.

Code here is voluntarily kept simple: it could be refactored with some
levels of abstraction to avoid repetitions, but would imply readers to
understand things unrelated to what their primary goal is: use the
SDK. So let's keep it stupid simple so the integration work is
simpler.
"""
import logging
from enum import Enum

import re
import click
import typer

from rich.console import Console
from rich.table import Table
from typing import Tuple

import kiln_connect
from kiln_connect.utils import lamport_to_sol, sol_to_lamport

sol_cli = typer.Typer(
    name='sol', help='Staking utilities for Solana', no_args_is_help=True)

console = Console()
error_console = Console(stderr=True)


class RewardsFormat(str, Enum):
    daily = "daily"
    epoch = "epoch"


class AccountFormat(str, Enum):
    wallet = "wallet"
    stake_account = "stake-account"


def pretty_lamport_to_sol(lamport: str) -> str:
    """Quick helper to pretty print LAMPORT to SOL.
    """
    if not lamport:
        return 'n/a'
    sol = str(round(lamport_to_sol(int(lamport)), 3))
    return f"{sol} SOL"


def sort_identifiers(identifiers: list[str], account_format: AccountFormat) -> Tuple[list[str], list[str]]:
    """Sorts SOL filtering identifiers in corresponding buckets.

    The Kiln SOL API supports filtering by:

    - Solana wallet address
    - Kiln Account ID (UUID)

    This functions returns the identifiers sorted in their corresponding bucket.
    """

    accounts = []
    wallets = []
    stake_accounts = []

    for identifier in identifiers:
        # Kiln Account UUIDs
        if re.match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$', identifier):
            accounts.append(identifier)
            continue

        # Wallet addresses or Stake accounts
        if re.match('^[1-9A-HJ-NP-Za-km-z]{32,44}$', identifier):
            if account_format == AccountFormat.stake_account:
                stake_accounts.append(identifier)
            else:
                wallets.append(identifier)
            continue

        raise click.UsageError(
            "Unknown identifier (should be a SOL stake account address, a SOL wallet address or a Kiln account UUID)")

    # This is a current limit of the Kiln API, we only support one
    # filter type at a time. This removes confusion when a staked is
    # matched by multiple filters.
    if accounts and (wallets or stake_accounts):
        raise click.UsageError(
            "Identifiers should be of the same type"
        )

    return accounts or None, wallets or None, stake_accounts or None


@sol_cli.command("network-stats")
def sol_network_stats():
    """Show the Solana network stats.
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        stats = kc.sol.get_sol_network_stats()

        table = Table('Network Gross APY %', 'Nb validators',
                      'Supply Percentage Stake')
        table.add_row(
            str(round(stats.data.network_gross_apy, 3)),
            str(stats.data.nb_validators),
            str(round(stats.data.supply_staked_percent, 3)),
        )

        console.print(table)


@sol_cli.command("stakes")
def sol_stakes(
        identifiers: list[str],
        account_format: AccountFormat = typer.Option(AccountFormat.wallet, '--account-format')):
    """Show the stakes for the specified Solana addresses or Kiln Account IDs.
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        accounts, wallets, stake_accounts = sort_identifiers(
            identifiers, account_format)

        stakes = kc.sol.get_sol_stakes(
            wallets=wallets, accounts=accounts, stake_accounts=stake_accounts)

        table = Table('Stake(s)', 'Status', 'Balance', 'Rewards')
        for stake in stakes.data:
            table.add_row(
                stake.stake_account,
                stake.state,
                str(pretty_lamport_to_sol(stake.balance)),
                str(pretty_lamport_to_sol(stake.rewards)),
            )

        console.print(table)


@sol_cli.command("rewards")
def sol_rewards(
        identifiers: list[str],
        account_format: AccountFormat = typer.Option(
            AccountFormat.wallet, '--account-format'),
        response_format: RewardsFormat = typer.Option(RewardsFormat.daily, '--format')):
    """Show the rewards for the specified Solana addresses or Kiln Account IDs.
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        accounts, wallets, stake_accounts = sort_identifiers(
            identifiers, account_format)

        rewards = kc.sol.get_sol_rewards(
            wallets=wallets, accounts=accounts, stake_accounts=stake_accounts, format=response_format.value)

        if response_format == RewardsFormat.daily:
            table = Table('Date', 'Active Balance', 'Rewards', 'Gross APY')
            for reward in rewards.data:
                table.add_row(
                    str(reward.actual_instance.var_date),
                    pretty_lamport_to_sol(
                        reward.actual_instance.active_balance),
                    pretty_lamport_to_sol(reward.actual_instance.rewards),
                    str(round(reward.actual_instance.net_apy, 3))
                )
            console.print(table)
        elif response_format == RewardsFormat.epoch:
            table = Table('Epoch', 'Active Balance', 'Rewards', 'Gross APY')
            for reward in rewards.data:
                table.add_row(
                    str(reward.actual_instance.epoch),
                    pretty_lamport_to_sol(
                        reward.actual_instance.active_balance),
                    pretty_lamport_to_sol(reward.actual_instance.rewards),
                    str(round(reward.actual_instance.net_apy, 3)))
                console.print(table)


@sol_cli.command("operations")
def sol_operations(
        identifiers: list[str],
        account_format: AccountFormat = typer.Option(
            AccountFormat.wallet, '--account-format')):
    """Show the operations for the specified Solana addresses or Kiln Account IDs.
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        accounts, wallets, stake_accounts = sort_identifiers(
            identifiers, account_format)

        operations = kc.sol.get_sol_operations(
            wallets=wallets, accounts=accounts, stake_accounts=stake_accounts)

        table = Table('Stake', 'Time', 'Type')
        for op in operations.data:
            op = op.actual_instance
            table.add_row(
                op.stake_account,
                str(op.time),
                op.type)

        console.print(table)


@sol_cli.command("stake")
def sol_stake_via_fireblocks(account_id: str, wallet: str, vote_account: str, amount: float):
    """
    Stake SOL via Fireblocks
    :param account_id:
    :param wallet:
    :param vote_account:
    :param amount:
    :return:
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        with console.status("[bold green]Staking in progress...") as status:
            data = kc.sol.stake("fireblocks", account_id, wallet, vote_account, sol_to_lamport(amount))
            console.print("==============")
            console.print("[bold]Successfully staked[/bold]")
            console.print(f"[bold]TX Hash[/bold]: {data.tx_hash}")
            status.stop()


@sol_cli.command("deactivate-stake")
def sol_deactivate_stake_via_fireblocks(stake_account: str, wallet: str):
    """
    Deactivate stake SOL via Fireblocks
    :param stake_account:
    :param wallet:
    :return:
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        with console.status("[bold green]Deactivation in progress...") as status:
            data = kc.sol.deactivate_stake("fireblocks", stake_account, wallet)
            console.print("==============")
            console.print("[bold]Successfully staked[/bold]")
            console.print(f"[bold]TX Hash[/bold]: {data.tx_hash}")
            status.stop()


@sol_cli.command("withdraw-stake")
def sol_withdraw_stake_via_fireblocks(stake_account: str, wallet: str, amount: float = None):
    """
    Withdraw stake SOL via Fireblocks
    :param stake_account:
    :param wallet:
    :param amount: (Optional)
    :return:
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        with console.status("[bold green]Withdraw in progress...") as status:
            amount_lamports = None
            if amount:
                amount_lamports = sol_to_lamport(amount)

            data = kc.sol.withdraw_stake("fireblocks", stake_account, wallet, amount_lamports)
            console.print("==============")
            console.print("[bold]Successfully staked[/bold]")
            console.print(f"[bold]TX Hash[/bold]: {data.tx_hash}")
            status.stop()


@sol_cli.command("merge-stakes")
def sol_merge_stakes_via_fireblocks(stake_account_source: str, stake_account_destination: str, wallet: str):
    """
    Merge stakes SOL via Fireblocks
    :param stake_account_source:
    :param stake_account_destination:
    :param wallet:
    :return:
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        with console.status("[bold green]Merge in progress...") as status:
            data = kc.sol.merge_stakes("fireblocks", stake_account_source, stake_account_destination, wallet)
            console.print("==============")
            console.print("[bold]Successfully staked[/bold]")
            console.print(f"[bold]TX Hash[/bold]: {data.tx_hash}")
            status.stop()


@sol_cli.command("split-stake")
def sol_split_stake_via_fireblocks(account_id: str, stake_account: str, wallet: str, amount: float):
    """
    Split stake SOL via Fireblocks
    :param account_id:
    :param stake_account:
    :param wallet:
    :param amount:
    :return:
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        with console.status("[bold green]Split in progress...") as status:
            data = kc.sol.split_stake("fireblocks", account_id, stake_account, wallet, sol_to_lamport(amount))
            console.print("==============")
            console.print("[bold]Successfully staked[/bold]")
            console.print(f"[bold]TX Hash[/bold]: {data.tx_hash}")
            status.stop()

@sol_cli.command("test")
def sol_test():
    kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env())
    logging.debug("test")
