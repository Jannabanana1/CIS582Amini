#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

#Connect to Algorand node maintained by PureStake
#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

mnemonic_secret = 'front lizard garbage attack proof casual lion pluck clutch agree tongue swing try celery awful shiver spring blind doll arctic vehicle ripple dutch absent honey'
sk = mnemonic.to_private_key(mnemonic_secret)
pk = mnemonic.to_public_key(mnemonic_secret)


acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen = params.gen
    gh = params.gh
    first_valid_round = params.first
    fee = params.min_fee
    last_valid_round = params.last
    #Your code here
    tx = transaction.PaymentTxn(pk, fee, first_valid_round, last_valid_round, gh, receiver_pk, tx_amount, flat_fee=True)
    signed_tx = tx.sign(sk)
    txid = signed_tx.transaction.get_txid()
    try:
        tx_confirm = acl.send_transaction(signed_tx)
        print('Transaction sent with ID', txid)
        wait_for_confirmation(acl, txid=txid)
    except Exception as e:
        print(e)
    return pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo


# send_tokens('AEC4WDHXCDF4B5LBNXXRTB3IJTVJSWUZ4VJ4THPU2QGRJGTA3MIDFN3CQA', 7 )
