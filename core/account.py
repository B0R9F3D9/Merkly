import asyncio
import time
from loguru import logger

from web3 import AsyncWeb3
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound


class Account:
    def __init__(self, _id: int, private_key: str) -> None:
        self.private_key: str = private_key
        self.w3: AsyncWeb3 = None
        self.explorer: str = None
        self.account = EthereumAccount.from_key(private_key)
        self.address = AsyncWeb3.to_checksum_address(self.account.address)
        self.info = f"[#{_id} - {self.address[:5]}...{self.address[-5:]}]"

    async def send_txn(self, txn: dict) -> str:
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
        raw_txn = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return raw_txn.hex()
    
    async def wait_until_tx_finished(self, hash: str, max_wait_time=90) -> bool:
        start_time = time.time()
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"{self.info} Транзакция успешна! {self.explorer+hash}")
                    return True
                elif status is None:
                    await asyncio.sleep(0.3)
                else:
                    logger.error(f"{self.info} Транзакция не удалась! {self.explorer+hash}")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    logger.error(f"{self.info} Транзакция не найдена! {self.explorer+hash}")
                    return False
                await asyncio.sleep(1)