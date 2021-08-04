from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from pprint import pprint
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        tx = rpc_connection.getrawtransaction(tx_hash, True)
        tx_hash = tx.get('hash')
        vout = tx.get('vout')[n]
        amount = vout.get('value')
        owner = vout.get('scriptPubKey').get('addresses')
        time= datetime.fromtimestamp(tx.get('time'))
        return cls(tx_hash, n, amount, owner, time)

    def get_inputs(self,d=1):
        tx = rpc_connection.getrawtransaction(self.tx_hash, True)
        vins = tx.get('vin')
        for vin in vins:
            txid = vin.get('txid')
            self.inputs.append(TXO.from_tx_hash(txid))



# Transaction ID is an identification number for a bitcoin transaction.
# First ever Bitcoin transaction to Hal Finney in 2010
txid_first = 'f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16'
# #  Pizza transaction for 10,000 BTC in 2010.
# txid_pizza= 'a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d'
# tx_first = rpc_connection.getrawtransaction(txid_first, True)
# tx_pizza = rpc_connection.getrawtransaction(txid_pizza, True)
# print(tx_pizza['time'])
# print("Pizza transation in 2010: {}".format(datetime.fromtimestamp(tx_pizza['time'])))
# print("Frist transation in 2009: {}".format(datetime.fromtimestamp(tx_first['time'])))
# pprint(list(tx_pizza.keys()))
# vins = tx_pizza.get('vin')
# print("vin: ")
# for vin in vins:
#     pprint(vin)
# print("vout: ")
# pprint(tx_pizza.get('vout'))

# pprint(tx_pizza.get('hash'))

# {'scriptSig': {'asm': '304402206d404ac1dbd95cf899652a2ed6cc74eeaf003b46c00d0fa20097a4e901279f4402203ecb94993307fa940c071094d3efb2adfbc282eb8d53c14aade3c9e7b6703956[ALL] '
#                       '0434417dd8d89deaf0f6481c2c160d6de0921624ef7b956f38eef9ed4a64e36877be84b77cdee5a8d92b7d93694f89c3011bf1cbdf4fd7d8ca13b58a7bb4ab0804',
#                'hex': '47304402206d404ac1dbd95cf899652a2ed6cc74eeaf003b46c00d0fa20097a4e901279f4402203ecb94993307fa940c071094d3efb2adfbc282eb8d53c14aade3c9e7b670395601410434417dd8d89deaf0f6481c2c160d6de0921624ef7b956f38eef9ed4a64e36877be84b77cdee5a8d92b7d93694f89c3011bf1cbdf4fd7d8ca13b58a7bb4ab0804'},
#  'sequence': 4294967295,
#  'txid': '85c325b5a4b25f750a05e7f0eb12a10fd234c704564c09d8c8a0c8df4063871c',
#  'vout': 0}
