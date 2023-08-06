# Get secrets and certificates from Azure Key Vault

from azure.identity import (
    ChainedTokenCredential,
    DeviceCodeCredential,
    InteractiveBrowserCredential,
)
from azure.keyvault.secrets import SecretClient

