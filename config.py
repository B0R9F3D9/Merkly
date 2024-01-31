import json

with open('abi/merkly_refuel_abi.json', 'r') as f:
    MERKLY_REFUEL_ABI = json.load(f)

with open('abi/erc20_abi.json', 'r') as file:
    ERC20_ABI = json.load(file)


CHAINS = {
    'Polygon': {
        'rpc': ['https://rpc.ankr.com/polygon'],
        'scan': 'https://polygonscan.com/tx/',
        'token': 'MATIC',
        'chain_id': 137,
        'l0_chain_id': 109,
        'contract': '0x0E1f20075C90Ab31FC2Dd91E536e6990262CF76d'
    },
    'Celo': {
        'rpc': ['https://rpc.ankr.com/celo'],
        'scan': 'https://celoscan.io/tx/',
        'token': 'CELO',
        'chain_id': 42220,
        'l0_chain_id': 125,
        'contract': '0xC20A842e1Fc2681920C1A190552A2f13C46e7fCF'
    },
    'Gnosis': {
        'rpc': ['https://rpc.ankr.com/gnosis'],
        'scan': 'https://gnosisscan.io/tx/',
        'token': 'xDAI',
        'chain_id': 100,
        'l0_chain_id': 145,
        'contract': '0x556F119C7433b2232294FB3De267747745A1dAb4'
    },
    'Core': {
        'rpc': ['https://rpc.ankr.com/core'],
        'scan': 'https://scan.coredao.org/tx/',
        'token': 'CORE',
        'chain_id': 1116,
        'l0_chain_id': 153,
        'contract': '0xa513F61Bc23F0eB1FC0aC4d9dab376d79bC7F3cB'
    },
    'Harmony': {
        'rpc': ['https://rpc.ankr.com/harmony'],
        'scan': 'https://explorer.harmony.one/tx/',
        'token': 'ONE',
        'chain_id': 1666600000,
        'l0_chain_id': 116,
        'contract': '0x671861008497782F7108D908D4dF18eBf9598b82'
    },
    'Klaytn': {
        'rpc': ['https://1rpc.io/klay'],
        'scan': 'https://klaytnscope.com/tx/',
        'token': 'KLAY',
        'chain_id': 8217,
        'l0_chain_id': 150,
        'contract': '0x79DB0f1A83f8e743550EeB5DD5B0B83334F2F083'
    },
    'Moonbeam': {
        'rpc': ['https://rpc.ankr.com/moonbeam'],
        'scan': 'https://moonscan.io/tx/',
        'token': 'GLMR',
        'chain_id': 1284,
        'l0_chain_id': 126,
        'contract': '0x671861008497782F7108D908D4dF18eBf9598b82'
    },
    'Moonriver': {
        'rpc': ['https://moonriver.public.blastapi.io'],
        'scan': 'https://moonriver.moonscan.io/tx/',
        'token': 'MOVR',
        'chain_id': 1285,
        'l0_chain_id': 167,
        'contract': '0xd379c3D0930d70022B3C6EBA8217e4B990705540'
    },
    'DFK': {
        'rpc': ['https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'],
        'scan': 'https://subnets.avax.network/defi-kingdoms/tx/',
        'token': 'JEWEL',
        'chain_id': 53935,
        'l0_chain_id': 115,
        'contract': '0x457Fd60FFA26576E226252092c98921f12E90FbB'
    },
    'Fuse': {
        'rpc': ['https://fuse-pokt.nodies.app'],
        'scan': 'https://explorer.fuse.io/tx/',
        'token': 'FUSE',
        'chain_id': 122,
        'l0_chain_id': 138,
        'contract': '0xf6b88C4a86965170dd42DBB8b53e790B3490b912'
    }
}

ROUTES = {
    'Polygon': ['Celo', 'Gnosis', 'Core', 'Harmony', 'Klaytn', 'Moonbeam', 'Moonriver', 'DFK', 'Fuse'],
    'Celo': ['Polygon', 'Gnosis', 'Fuse', 'Moonbeam'],
    'Gnosis': ['Polygon', 'Celo', 'Klaytn', 'Moonbeam', 'Fuse'],
    'Core': ['Polygon'],
    'Harmony': ['Polygon', 'Moonbeam', 'DFK'],
    'Klaytn': ['Polygon', 'Celo', 'Gnosis', 'Moonbeam', 'DFK', 'Fuse'],
    'Moonbeam': ['Polygon', 'Celo', 'Gnosis', 'Harmony', 'Klaytn', 'DFK'],
    'Moonriver': ['Polygon'],
    'DFK': ['Polygon', 'Harmony', 'Klaytn', 'Moonbeam'],
    'Fuse': ['Polygon', 'Celo', 'Gnosis', 'Klaytn']
}
