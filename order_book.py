from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order

engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def process_order(order_dict):
    order = Order(sender_pk=order_dict['sender_pk'], receiver_pk=order_dict['receiver_pk'],
                  buy_currency=order_dict['buy_currency'], sell_currency=order_dict['sell_currency'],
                  buy_amount=order_dict['buy_amount'], sell_amount=order_dict['sell_amount'],
                  creator_id=order_dict.get('creator_id', None))
    session.add(order)
    session.commit()
    orders = session.query(Order).filter(Order.filled == "").all()
    for existing_order in orders:
        if match_found(order, existing_order):
            order.filled = datetime.now()
            existing_order.filled = datetime.now()
            order.counterparty_id = existing_order.id
            existing_order.counterparty_id = order.id

            if order.buy_amount > existing_order.sell_amount:
                new_order = {}
                new_order['creator_id'] = order.id
                new_order['sender_pk'] = order.sender_pk
                new_order['receiver_pk'] = order.receiver_pk
                new_order['buy_currency'] = order.buy_currency
                new_order['sell_currency'] = order.sell_currency
                new_buy_amount = order.buy_amount - existing_order.sell_amount
                new_order['buy_amount'] =  new_buy_amount
                new_order['sell_amount'] = 1.1*(new_buy_amount * order.sell_amount / order.buy_amount)
                new_order = Order(creator_id=new_order['creator_id'], sender_pk=new_order['sender_pk'],
                                  receiver_pk=new_order['receiver_pk'], buy_currency=new_order['buy_currency'],
                                  sell_currency=new_order['sell_currency'], buy_amount=new_order['buy_amount'],
                                  sell_amount=new_order['sell_amount'])
                process_order(new_order)

            elif order.buy_amount < existing_order.sell_amount:
                new_order = {}
                new_order['creator_id'] = order.id
                new_order['sender_pk'] = existing_order.sender_pk
                new_order['receiver_pk'] = existing_order.receiver_pk
                new_order['buy_currency'] = existing_order.buy_currency
                new_order['sell_currency'] = existing_order.sell_currency
                new_sell_amount = existing_order.sell_amount - order.buy_amount
                new_order['buy_amount'] =  new_sell_amount
                new_order['sell_amount'] = 1.1*(new_sell_amount * existing_order.buy_amount / existing_order.sell_amount)
                new_order = Order(creator_id=new_order['creator_id'], sender_pk=new_order['sender_pk'],
                                  receiver_pk=new_order['receiver_pk'], buy_currency=new_order['buy_currency'],
                                  sell_currency=new_order['sell_currency'], buy_amount=new_order['buy_amount'],
                                  sell_amount=new_order['sell_amount'])

                process_order(new_order)

def match_found(order, existing_order):
    if existing_order.filled == None:
        if existing_order.buy_currency == order.sell_currency:
            if existing_order.sell_currency == order.buy_currency:
                if existing_order.sell_amount / existing_order.buy_amount >= order.buy_amount / order.sell_amount:
                    return True
    return False
