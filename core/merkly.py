from loguru import logger
import random

from web3 import AsyncWeb3
from web3.contract.async_contract import AsyncContract
from web3.middleware import async_geth_poa_middleware
from eth_abi.packed import encode_packed

from config import CHAINS, MERKLY_REFUEL_ABI
from settings import GAS_MULTIPLIER
from .account import Account
from .helpers import retry


class Merkly:
    def __init__(self, acc: Account, chain_source_name: str) -> None:
        self.source_chain = CHAINS[chain_source_name]
        self.source_chain_name = chain_source_name
        self.acc = acc
        self.address = self.acc.address
        self.info = self.acc.info
        self.acc.w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(random.choice(self.source_chain['rpc'])),
            middlewares=[async_geth_poa_middleware]
        )
        self.acc.explorer = self.source_chain['scan']
        self.w3 = self.acc.w3
        
    async def get_bridge_fee_params(self, dst_chain_id: int, value_wei: int, contract: AsyncContract) -> tuple[str, int]:
        data = AsyncWeb3.to_hex(encode_packed(["uint16", "uint", "uint", "address"], [2, 250000, value_wei, self.address]))
        fee = await contract.functions.estimateSendFee(dst_chain_id, '0x', data).call()
        return data, int(fee[0] * 1.10)

    @retry
    async def refuel(self, chain_dest_name: str, value: float) -> None:
        value_wei = int(value * 10**18)
        dest_chain = CHAINS[chain_dest_name]
        dest_l0_chain_id = CHAINS[chain_dest_name]['l0_chain_id']
        contract: AsyncContract = self.w3.eth.contract(address=self.source_chain['contract'], abi=MERKLY_REFUEL_ABI)
        adapter_params, value_send_wei = await self.get_bridge_fee_params(dest_l0_chain_id, value_wei, contract)
        
        value_send = value_send_wei / 10**18
        logger.info(
            f"{self.info} Рефуел {self.source_chain_name} -> {chain_dest_name} | " + 
            f"{value_send:.4f} {self.source_chain['token']} -> {value:.4f} {dest_chain['token']}...")
        
        txn_data = await contract.functions.bridgeGas(
            dest_l0_chain_id,
            self.address,
            adapter_params
        ).build_transaction(
            {
                "from": self.address,
                "value": value_send_wei,
                "nonce": await self.w3.eth.get_transaction_count(self.address),
                'gasPrice': int(await self.w3.eth.gas_price),
                'gas': 0
            }
        )
        
        if self.source_chain_name == 'Moonbeam':
            txn_data['gas'] = 500000
        else:
            txn_data['gas'] = int(await self.w3.eth.estimate_gas(txn_data) * GAS_MULTIPLIER)

        txn_hash = await self.acc.send_txn(txn_data)
        await self.acc.wait_until_tx_finished(txn_hash)
