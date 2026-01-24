import os
from enum import Enum

class PaymentMode(Enum):
    SANDBOX = "sandbox"
    PRODUCTION = "production"

class SandboxConfig:
    @staticmethod
    def is_sandbox() -> bool:
        return os.getenv("PAYMENT_MODE", "sandbox") == "sandbox"
    
    @staticmethod
    def get_mpesa_config():
        if SandboxConfig.is_sandbox():
            return {
                "consumer_key": "sandbox_consumer_key",
                "consumer_secret": "sandbox_consumer_secret",
                "shortcode": "174379",
                "passkey": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
                "base_url": "https://sandbox.safaricom.co.ke"
            }
        return {
            "consumer_key": os.getenv("MPESA_CONSUMER_KEY"),
            "consumer_secret": os.getenv("MPESA_CONSUMER_SECRET"),
            "shortcode": os.getenv("MPESA_SHORTCODE"),
            "passkey": os.getenv("MPESA_PASSKEY"),
            "base_url": "https://api.safaricom.co.ke"
        }
    
    @staticmethod
    def get_tron_config():
        if SandboxConfig.is_sandbox():
            return {
                "network": "nile",
                "master_wallet": "TXYZ...",
                "private_key": "sandbox_key"
            }
        return {
            "network": "mainnet",
            "master_wallet": os.getenv("TRON_MASTER_WALLET"),
            "private_key": os.getenv("TRON_PRIVATE_KEY")
        }
