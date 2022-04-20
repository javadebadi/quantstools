from quantstools.order import Order
from quantstools.price import Price
from quantstools.order_collection import OrderCollection

oc = OrderCollection('BTC-USDT')
o1 = Order('BTC-USDT', 'BUY', Price(40000,8,2), '1.0')
o2 = Order('BTC-USDT', 'BUY', Price(20000,8,2), '1.0')
oc.add_order(o2)
oc.add_order(o1)

print(oc.get_orders_list_of_dict())
print(o1.to_dict())