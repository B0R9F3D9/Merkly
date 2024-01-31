from tabulate import tabulate
import asyncio

from web3 import AsyncWeb3

from .account import Account
from config import CHAINS

RPC_SERVERS = {}
for chain_name, chain in CHAINS.items():
    RPC_SERVERS[chain_name] = chain['rpc'][0]


class Checker:
    def __init__(self, accs: list[Account]) -> None:
        self.accs: list[Account] = accs

    async def get_balance(self, w3: AsyncWeb3, address: str) -> str:
        balance = await w3.eth.get_balance(address)
        ether_balance = w3.from_wei(balance, 'ether')
        return f'{ether_balance:.3f}'

    async def check_balances_for_chain(self, chain_name: str, w3: AsyncWeb3):
        balances = {}
        for acc in self.accs:
            balance = await self.get_balance(w3, acc.address)
            balances[acc.address] = balance
        return chain_name, balances

    async def check(self):
        results = {acc.address: {'№': i + 1, 'Адрес': f'{acc.address[:5]}...{acc.address[-5:]}'}
                   for i, acc in enumerate(self.accs)}
                
        tasks = []
        for chain_name, rpc_url in RPC_SERVERS.items():
            w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc_url))
            tasks.append(self.check_balances_for_chain(chain_name, w3))
        
        for chain_name, balances in await asyncio.gather(*tasks):
            for address, balance in balances.items():
                results[address][chain_name] = balance
        
        print(tabulate([result for address, result in results.items()], headers='keys', tablefmt='rounded_grid'))
