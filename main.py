import asyncio, sys, random
from loguru import logger
from datetime import datetime
import questionary

from core import Merkly, Account, Checker, sleep
from config import CHAINS, ROUTES
from settings import *

date_now = datetime.now().strftime("%d-%m-%Y")
format = '<white>{time:HH:mm:ss}</white> | <bold><level>{level: <7}</level></bold> | <level>{message}</level>'
logger.remove()
logger.add(sys.stderr, format=format)
logger.add(f'logs/{date_now}.log', format=format, level='INFO')


def get_accs(accs: list[Account]) -> list:
    if len(accs) == 1:
        return accs
    print(
        'Выберите аккаунты для работы. Формат: \n'
        '1 — для выбора только первого аккаунта\n'
        '1,2,3 — для выбора первого, второго и третьего аккаунта\n'
        '1-3 — для выбора аккаунтов от первого до третьего включительно\n'
        'all — для выбора всех аккаунтов')
    result = input('Введите ваш выбор: ')
    if result == 'all':
        return accs
    else:
        try:
            if ',' in result:
                return [accs[int(i) - 1] for i in result.split(',')]
            elif '-' in result:
                return accs[int(result.split('-')[0]) - 1:int(result.split('-')[1])]
            elif '-' not in result and ',' not in result:
                return [accs[int(result) - 1]]
        except ValueError:
            print('Некорректный выбор аккаунтов')
            exit()


def get_module() -> str:
    return questionary.select(
        message="Выберите модуль",
        instruction="(используйте стрелочки для выбора)",
        choices=[
            questionary.Choice("1) Меркли рефуел", 'merkly'),
            questionary.Choice("2) Чекер балансов", 'checker'), 
            questionary.Choice("❌ Выход", 'exit'),
        ],
        qmark="\n❓ ",
        pointer="👉 "
    ).ask()


def get_source_chain() -> str:
    return questionary.select(
        message="Выберите source сеть",
        instruction="(используйте стрелочки для выбора)",
        choices=[chain for chain in CHAINS],
        qmark="\n❓ ",
        pointer="👉 "
    ).ask()

def get_dest_chain(source_chain_name: str) -> str:
    return questionary.select(
        message="Выберите dest сеть",
        instruction="(используйте стрелочки для выбора)",
        choices=[chain for chain in ROUTES[source_chain_name]],
        qmark="\n❓ ",
        pointer="👉 "
    ).ask()

async def get_min_max_amount(token_name: str) -> tuple[float, float]:
    min_amount = await questionary.text(
        message=f"Укажите минимальную сумму ${token_name} для получения:",
        qmark="\n❓ ",
    ).ask_async()
    max_amount = await questionary.text(
        message=f"Укажите максимальную сумму ${token_name} для получения:",
        qmark="\n❓ ",
    ).ask_async()
    return float(min_amount), float(max_amount)

async def get_min_max_tx_count() -> tuple[int, int]:
    min_amount = await questionary.text(
        message=f"Укажите минимальное количество транзакций:",
        qmark="\n❓ ",
    ).ask_async()
    max_amount = await questionary.text(
        message=f"Укажите максимальное количество транзакций:",
        qmark="\n❓ ",
    ).ask_async()
    return int(min_amount), int(max_amount)

async def merkly_refuel(accs: list[Account], source_chain_name: str, dest_chain_name: str) -> None:
    min_tx_count, max_tx_count = await get_min_max_tx_count() if not USE_PRESET else (PRESET[4], PRESET[5])
    min_amount, max_amount = await get_min_max_amount(CHAINS[dest_chain_name]['token']) if not USE_PRESET else (PRESET[2], PRESET[3])
    for acc in accs:
        merkly = Merkly(acc, source_chain_name)
        tx_count = random.randint(min_tx_count, max_tx_count)
        for i in range(tx_count):
            amount = random.uniform(min_amount, max_amount)
            await merkly.refuel(dest_chain_name, amount)
            if i != tx_count - 1:
                await sleep(*SLEEP_BETWEEN_TXS)
        if acc != accs[-1]:
            await sleep(*SLEEP_BETWEEN_ACCS)

async def run_checker(accs: list[Account]) -> None:
    checker = Checker(accs)
    await checker.check()


if __name__ == '__main__':
    with open('data/accounts.txt', 'r') as file:
        ACCOUNTS = [x.strip() for x in file.readlines()]
    
    accs = [Account(_id, acc) for _id, acc in enumerate(ACCOUNTS, 1)]
    logger.info(f'Найдено кошелеков: {len(accs)}')

    if SHUFFLE_WALLET:
        logger.warning('Список аккаунтов перемешан!')
        random.shuffle(accs)

    if USE_PRESET:
        logger.warning('Используется пресет!')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_checker(accs))
    accs = get_accs(accs)

    while True:
        try:
            module = get_module()
            if module == 'merkly':
                if USE_PRESET:
                    source_chain = PRESET[0]
                    dest_chain = PRESET[1]
                    if dest_chain not in ROUTES[source_chain]: exit()
                else:
                    source_chain = get_source_chain()
                    dest_chain = get_dest_chain(source_chain)
                loop.run_until_complete(merkly_refuel(accs, source_chain, dest_chain))
            elif module == 'checker':
                loop.run_until_complete(run_checker(accs))
            elif module == 'exit':
                break
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.critical(e)
            break
            
    loop.close()
    print('\n👋👋👋')
