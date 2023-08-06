import logging
import os

from dataclasses import dataclass

from kiln_connect.openapi_client import ApiClient, Configuration

from .atom import ATOM
from .eth import ETH
from .matic import MATIC
from .sol import SOL
from .xtz import XTZ
from .accounts import Accounts
from .errors import (
    KilnInvalidEnvError,
    KilnError  # noqa: F401
)
from .integrations import IntegrationConfig, Integrations, Asset


@dataclass
class KilnConfig:
    """Configuration of the Kiln Connect SDK.
    """
    kiln_base_url: str
    kiln_api_token: str
    integrations: list[IntegrationConfig]

    @staticmethod
    def from_env():
        """Init the Config looking at what we find in the env.
        """
        integration_configs = []

        env = os.getenv("KILN_ENV")
        if env not in ["devnet", "testnet", "mainnet"]:
            raise KilnInvalidEnvError

        # Fireblocks integration
        fireblocks_api_token = os.getenv("FIREBLOCKS_API_KEY")
        if fireblocks_api_token:
            assets = {}

            if env in ("devnet", "testnet"): 
                    assets = {
                        Asset.eth: "ETH_TEST3",
                        Asset.xtz: "XTZ_TEST",
                        Asset.sol: "SOL_TEST",
                        Asset.matic: "MATIC_POLYGON_MUMBAI"
                    }
            elif env == "mainnet":
                    assets = {
                        Asset.eth: "ETH",
                        Asset.xtz: "XTZ",
                        Asset.sol: "SOL",
                        Asset.matic: "MATIC"
                    }

            fireblocks_raw_key_path = os.getenv("FIREBLOCKS_RAW_KEY_PATH")
            fireblocks_vault_account_id = os.getenv(
                "FIREBLOCKS_VAULT_ACCOUNT_ID")
            integration_configs.append(IntegrationConfig(
                name="fireblocks",
                provider="fireblocks",
                parameters={
                    "api_token": fireblocks_api_token,
                    "raw_key_path": fireblocks_raw_key_path,
                    "vault_account_id": fireblocks_vault_account_id,
                    "assets": assets,
                },
            ))

        log_dir = os.getenv("KILN_DEBUG_LOG_DIR")

        # Set a predefined format
        format = "[%(levelname)s] %(asctime)s - %(message)s"
        if log_dir is not None:
            os.makedirs(os.path.dirname(log_dir), exist_ok=True)
            logging.basicConfig(
                format=format,
                filename=log_dir,
                level=logging.DEBUG,
                encoding="utf-8")
        else:
            logging.basicConfig(
                format=format, level=logging.DEBUG, encoding="utf-8")

        return KilnConfig(
            kiln_base_url=os.getenv("KILN_API_URL"),
            kiln_api_token=os.getenv("KILN_API_TOKEN"),
            integrations=integration_configs,
        )


class KilnConnect:
    """Main class for Kiln connect.
    """

    def __init__(self, config: KilnConfig):
        self.config = config

        openapi_cfg = Configuration(host=config.kiln_base_url)
        openapi_cfg.access_token = config.kiln_api_token

        self._api = ApiClient(
            configuration=openapi_cfg,
        )

        self._integrations = Integrations(config.integrations)

        self.xtz = XTZ(self._api, self._integrations)
        self.eth = ETH(self._api, self._integrations)
        self.sol = SOL(self._api, self._integrations)
        self.atom = ATOM(self._api, self._integrations)
        self.matic = MATIC(self._api, self._integrations)
        self.accounts = Accounts(self._api, self._integrations)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._api:
            self._api.close()
