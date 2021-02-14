from decimal import Decimal
from web3.datastructures import AttributeDict
from multicall import Call, Multicall
from web3 import Web3
from yearn import uniswap
from packaging import version
MIN_VERSION = version.parse("0.3.0")

from functools import reduce

def get_nested_default(d, path):
    return reduce(lambda d, k: d.setdefault(k, {}), path, d)

def set_nested(d, path, value):
    get_nested_default(d, path[:-1])[path[-1]] = value

def unflatten(d, separator='.'):
    output = {}
    for k, v in d.items():
        path = k.split(separator)
        set_nested(output, path, v)
    return output

def from_dec(value):
    return Decimal(value)

def add_call(contract, method, calls, transform):
    calls.append(Call(contract, [method + '()(uint256)'], [[contract + '.' + method, transform]]))

def add_call_with_type(contract, method, type, calls, transform):
    calls.append(Call(contract, [method + '()(' + type + ')'], [[contract + '.' + method, transform]]))

def scale_values(vault_data):
    scale = 10 ** vault_data['decimals']
    for prop in vault_values_to_scale:
        value = vault_data[prop]
        vault_data[prop] = value / scale

relevant_vault_methods = ['decimals', 'totalAssets', 'maxAvailableShares', 'pricePerShare', 'debtOutstanding',
                          'creditAvailable', 'expectedReturn', 'totalSupply', 'emergencyShutdown', 'depositLimit',
                          'debtRatio', 'totalDebt', 'lastReport', 'managementFee', 'performanceFee']

vault_values_to_scale = ['totalAssets', 'maxAvailableShares', 'pricePerShare', 'debtOutstanding',
                          'creditAvailable', 'expectedReturn', 'totalSupply', 'depositLimit',
                          'totalDebt']

def get_compatible_vaults(vaults):
    calls = []

    for vault in vaults:
        add_call_with_type(vault, 'token', 'address', calls, None)
        add_call_with_type(vault, 'apiVersion', 'string', calls, None)
        add_call_with_type(vault, 'name', 'string', calls, None)

    multi = Multicall(calls)

    data = multi()

    data = unflatten(data)

    #print('versions', data)

    compatible_vaults = []

    for key, value in data.items():
        print(key, ' -> ', value['apiVersion'])
        if MIN_VERSION <= version.parse(value['apiVersion']):
            compatible_vaults.append(key)

    return compatible_vaults

def fetch_data(vaults):

    calls = []

    for vault in vaults:
        for method in relevant_vault_methods:
            add_call(vault, method, calls, from_dec)
        add_call_with_type(vault, 'token', 'address', calls, None)
        add_call_with_type(vault, 'apiVersion', 'string', calls, None)
        add_call_with_type(vault, 'name', 'string', calls, None)

    multi = Multicall(calls)

    data = multi()

    data = unflatten(data)

    for vault in data.values():
        scale_values(vault)
        token = vault['token']
        try:
            vault["token price"] = Decimal(uniswap.token_price_cached(token))
        except ValueError:
            vault["token price"] = Decimal(0)

        #print('price for token', token, vault["token price"])

        if "totalAssets" in vault:
            vault["tvl"] = vault["token price"] * vault["totalAssets"]

    return data


def main():
    vaults = {
        "DAI 0.3.0": "0x19D3364A399d251E894aC732651be8B0E4e85001",
        "USDC 0.3.0": "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9",
        "HEGIC 0.3.0": "0xe11ba472F74869176652C35D30dB89854b5ae84D",
        "stETH 0.3.0": "0xdCD90C7f6324cfa40d7169ef80b12031770B4325",
        "WBTC 0.3.0": "0xcB550A6D4C8e3517A939BC79d0c7093eb7cF56B5",
    }

    data = fetch_data(vaults.values())
    print('data', data)


if __name__ == "__main__":
    main()
