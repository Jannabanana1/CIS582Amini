from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import sys

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()


""" Suggested helper methods """

def match_orders(order, existing):
  
    if order.filled == None and order.sell_currency==existing.buy_currency and order.buy_currency== existing.sell_currency and existing_order.sell_amount / existing_order.buy_amount >= order.buy_amount/order.sell_amount:
      return True 
    return False

def check_sig(payload,sig):
    content = request.get_json(silent=True)
    signature1 = content['sig']
    payload = content['payload']
    sender_pk = payload['sender_pk']
    receiver_pk = payload['receiver_pk']
    buy_currency = payload['buy_currency']
    sell_currency = payload['sell_currency']
    buy_amount = payload['buy_amount']
    sell_amount = payload['sell_amount']
    platform = payload['platform']
    payload_json = json.dumps(payload)  
    
    if platform == 'Ethereum':
        message =  eth_account.messages.encode_defunct(text=payload_json)
        verify= eth_account.Account.recover_message(message, signature=signature1)
        if verify == sender_pk:
          verification=True
        else:
          verification= False
    if platform == 'Algorand':
        verification = algosdk.util.verify_bytes(payload_json.encode('utf-8'), signature1, sender_pk)
        
    if verification==True: 
        order1 = Order(receiver_pk = receiver_pk,sender_pk = sender_pk, buy_currency = buy_currency, sell_currency = sell_currency, buy_amount = buy_amount,sell_amount = sell_amount,signature = signature1)
            
            
        g.session.add(order1)
        g.session.commit()
            
          
    if verification==False:
        log_message(payload)
        return jsonify(False)
    return jsonify(True)

def fill_order(order,txes=[]):
  for existing_order in txes:
      if match_orders(order, existing_order):
        order.filled = datetime.now()
        existing_order.filled = datetime.now()
        order.counterparty_id = existing_order.id
        existing_order.counterparty_id = order.id
        if order.buy_amount > existing_order.sell_amount:
                child = {}
                child['sender_pk'] = order.sender_pk
                child['receiver_pk'] = order.receiver_pk
                child['buy_currency'] = order.buy_currency
                child['sell_currency'] = order.sell_currency
                child['buy_amount'] = order.buy_amount - existing_order.sell_amount
                child['sell_amount'] = 1.1*((order.buy_amount - existing_order.sell_amount) * order.buy_amount/order.sell_amount )
                child['creator_id'] = order.id
                child = Order(creator_id=child['creator_id'], sender_pk=child['sender_pk'],receiver_pk=child['receiver_pk'], buy_currency=child['buy_currency'], sell_currency=child['sell_currency'], buy_amount=child['buy_amount'], sell_amount=child['sell_amount'] )

                session.add(child)
                session.commit()
        if existing_order.sell_amount  >order.buy_amount:
                child = {}
                child['sender_pk'] = existing_order.sender_pk
                child['receiver_pk'] = existing_order.receiver_pk
                child['buy_currency'] = existing_order.buy_currency
                child['sell_currency'] = existing_order.sell_currency
                child['sell_amount'] = existing_order.sell_amount - order.buy_amount
                child['buy_amount'] = 0.9*((existing_order.sell_amount - order.buy_amount) * existing_order.buy_amount/existing_order.sell_amount )
                child['creator_id'] = existing_order.id
                child = Order(creator_id=child['creator_id'], sender_pk=child['sender_pk'],receiver_pk=child['receiver_pk'], buy_currency=child['buy_currency'], sell_currency=child['sell_currency'], buy_amount=child['buy_amount'], sell_amount=child['sell_amount'] )

                session.add(child)
                session.commit()

  
def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    # Hint: use json.dumps or str() to get it in a nice string form
    log_session = Log(message=json.dumps(d))
    g.session.add(log_session)
    g.session.commit()

""" End of helper methods """



@app.route('/trade', methods=['POST'])
def trade():
    print("In trade endpoint")
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]

        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
        
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
            
        #Your code here
        #Note that you can access the database session using g.session

        # TODO: Check the signature
        signature2 = content['sig']
        payload2 = content['payload']
        # TODO: Add the order to the database
        if check_sig(payload2, signature2)==True:
            
            sender_pk = content['sender_pk']
            receiver_pk = content['receiver_pk']
            buy_currency = content['buy_currency']
            sell_currency = content['sell_currency']
            buy_amount = content['buy_amount']
            sell_amount = content['sell_amount']
            
            # TODO: Add the order to the database
            order1 = Order(receiver_pk = receiver_pk,sender_pk = sender_pk, buy_currency = buy_currency, sell_currency = sell_currency, buy_amount = buy_amount,sell_amount = sell_amount,signature = signature2)
            g.session.add(order1)
            g.session.commit()
        
        
        
        # TODO: Fill the order
            existing_orders = g.session.query(Order).filter(Order.filled==None).all()
            fill_order(order1, existing_orders)
            return jsonify(True)
        # TODO: Be sure to return jsonify(True) or jsonify(False) depending on if the method was successful
        return jsonify(False)

@app.route('/order_book')
def order_book():
    #Your code here
    #Note that you can access the database session using g.session
    data_dict={}
    data_dict['data']=[]
    orders=g.session.query(Order)
    for n in orders:
        dict = {}
        dict['sender_pk'] = n.sender_pk
        dict['receiver_pk'] = n.receiver_pk
        dict['buy_currency'] = n.buy_currency
        dict['sell_currency'] = n.sell_currency
        dict['buy_amount'] = n.buy_amount
        dict['sell_amount'] = n.sell_amount
        dict['signature'] = n.signature
        data_dict['data'].append(dict)
    return json.dumps(data_dict)

if __name__ == '__main__':
    app.run(port='5002')
