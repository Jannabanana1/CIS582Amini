    session.add(order)
    session.commit()
    for existing_order in orders:
        if match_found(order, existing_order):
            order.filled = datetime.now()
            existing_order.filled = datetime.now()
            order.counterparty_id = existing_order.id
            existing_order.counterparty_id = order.id   
            
            if order.buy_amount > existing_order.sell_amount:
                new_order_dict = {}
                new_order_dict['sender_pk'] = order.sender_pk
                new_order_dict['receiver_pk'] = order.receiver_pk
                new_order_dict['buy_currency'] = order.buy_currency
                new_order_dict['sell_currency'] = order.sell_currency
                new_buy_amount = order.buy_amount - existing_order.sell_amount
                new_order_dict['buy_amount'] = new_buy_amount
                new_order_dict['sell_amount'] = 1.01*(new_buy_amount * order.buy_amount / order.sell_amount)
                new_order_dict['creator_id'] = order.id
                process_order(new_order_dict)
            session.commit()
                

def match_found(order, existing_order):
    if existing_order.filled==None:
        if existing_order.buy_currency==order.sell_currency:
            if existing_order.sell_currency==order.buy_currency:
                if existing_order.sell_amount / existing_order.buy_amount >= order.buy_amount / order.sell_amount:
                    return True
    return False
