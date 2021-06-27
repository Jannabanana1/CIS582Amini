from web3 import Web3
from hexbytes import HexBytes

IP_ADDR='18.188.235.196'
PORT='8545'

w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))

if w3.isConnected():
#     This line will mess with our autograders, but might be useful when debugging
    print( "Connected to Ethereum node" )
else:
    print( "Failed to connect to Ethereum node!" )

max_tx = HexBytes('0xf7f4905225c0fde293e2fd3476e97a9c878649dd96eb02c86b86be5b92d826b6')

def get_transaction(tx):
    tx = {}   #YOUR CODE HERE
    tx = w3.eth.get_transaction(tx)
    return tx

def get_gas_price(tx):
    """
    Unit in wei.
    1 gwei = 0.000000001 ETH
    10^18 wei = 1 ETH
    1 gwei = 10^9 wei
    """
    gas_price = 1 #YOUR CODE HERE
    tx2 = w3.eth.get_transaction(tx.hex())
    gas_price = tx2.get('gasPrice')
    return gas_price

def get_gas(tx):
    gas = 1 #YOUR CODE HERE
    tx2 = w3.eth.get_transaction_receipt(tx.hex())
    gas = tx2.get('gasUsed')
    return gas

def get_transaction_cost(tx):
    """
    Unit in Wei
    """
    tx_cost = 1 #YOUR CODE HERE
    gas = get_gas(tx)
    gas_price = get_gas_price(tx)
    tx_cost = gas * gas_price
    return tx_cost

def get_block_cost(block_num):
    """
    Unit in Wei
    """
    block_cost = 1  #YOUR CODE HERE
    block = w3.eth.get_block(block_num)
    txs = block.get('transactions')
    block_cost = 0
    for tx in txs:
        block_cost += get_transaction_cost(tx)
    return block_cost

# Return the hash of the most expensive transaction
def get_most_expensive_transaction(block_num):
    max_tx = HexBytes('0xf7f4905225c0fde293e2fd3476e97a9c878649dd96eb02c86b86be5b92d826b6')  #YOUR CODE HERE
    block = w3.eth.get_block(block_num)
    txs = block.get('transactions')
    max_tx_cost = 0
    for tx in txs:
        tx_cost = get_transaction_cost(tx)
        if tx_cost > max_tx_cost:
            max_tx_cost = tx_cost
            max_tx = tx

    return max_tx
