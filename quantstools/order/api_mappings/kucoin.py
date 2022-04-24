KUCOIN_API_PARAMS_MAPPING = {
    'cancel_all_orders': {
        'response': {
            'orders_ids': 'cancelledOrderIds',
        },
        'request': {

        }
    },
    'cancel_order_by_id': {
        'response': {
            'order_id': 'cancelledOrderIds',
        },
        'request': {
            'order_id': 'order_id',
        }
    },
    'get_order_by_id': {
        'response': {
            'id_': 'id',
            'symbol': 'symbol',
            'type_': 'type',
            'side': 'side',
            'price': 'price',
            'amount': 'size',
            'is_active': 'isActive',
            'is_cancelled': 'cancelExist',
            'mili_unixtime': 'createdAt',
        },
        'request': {
        }
    },
    'send_limit_order': {
        'response': {
            'order_id': 'orderId',
        },
        'request': {
            'symbol': 'symbol',
            'amount': 'size',
            'side': 'side',
            'price': 'price',
        }
    },
}