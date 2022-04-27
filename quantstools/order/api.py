"""A module to integrate a trading web API
with order management
"""

import logging
from .api_mappings import find_api_params_mapping


class OrderAPI:

    def __init__(
        self,
        api_client_object,
        cancel_all_orders: str,
        cancel_order_by_id: str,
        get_order_by_id: str,
        send_limit_order: str,
        side_buy: str,
        side_sell: str,
        api_params_mapping: dict,
        ):
        self.api_client = api_client_object
        self._cancel_all_orders = cancel_all_orders
        self._cancel_order_by_id = cancel_order_by_id
        self._get_order_by_id = get_order_by_id
        self._send_limit_order = send_limit_order
        self._side_buy = side_buy
        self._side_sell = side_sell
        if type(api_params_mapping) == dict:
            self._api_params_mapping = api_params_mapping
        elif type(api_params_mapping) == str:
            self._api_params_mapping = find_api_params_mapping(api_params_mapping)

    def cancel_all_orders(self):
        params = self._api_params_mapping["cancel_all_orders"]["response"]
        results = getattr(
            self.api_client,
            self._cancel_all_orders,
            )()
        if params is not None:
            return results[params['orders_ids']]
        else:
            return []

    def cancel_order_by_id(self, order_id: str):
        try:
            result = getattr(
                self.api_client,
                self._cancel_order_by_id,
                )(order_id)
            return order_id
        except Exception as e:
            logging.error(str(e))
            logging.error(f"Could not delete order with id ='{order_id}' ")
            return None

    def get_order_by_id(self, order_id: str):
        data = getattr(
            self.api_client,
            self._get_order_by_id,
            )(order_id)
        params = self._api_params_mapping["get_order_by_id"]["response"]
        order_data = {}
        order_data['id_'] = data[params['id_']]
        order_data['symbol'] = data[params['symbol']]
        order_data['price'] = str(float(data[params['price']]))
        order_data['amount'] = str(float(data[params['amount']]))
        order_data['side'] = data[params['side']].upper()
        order_data['type_'] = data[params['type_']].upper()
        order_data['is_active'] = str(data[params['is_active']])
        order_data['is_cancelled'] = str(data[params['is_cancelled']])
        order_data['mili_unixtime'] = int(data[params['mili_unixtime']])
        # is active
        if order_data['is_active'].lower() == 'true':
            order_data['is_active'] = True
        elif order_data['is_active'].lower() == 'false':
            order_data['is_active'] = False
        else:
            raise ValueError(
                "string for is_active argument could not be converted to bool"
                )
        # is cancelled
        if order_data['is_cancelled'].lower() == 'true':
            order_data['is_cancelled'] = True
        elif order_data['is_cancelled'].lower() == 'false':
            order_data['is_cancelled'] = False
        else:
            raise ValueError(
                "string for is_cancelled argument could not be converted to bool"
                )
        # type_
        assert order_data['type_'] in ["LIMIT"]
        assert order_data['side'].upper() in ["SELL", "BUY"]
        return order_data
        
    def send_limit_order(
        self,
        order_data: dict,
        ) -> str:
        assert type(order_data) == dict
        rq_params = self._api_params_mapping["send_limit_order"]["request"]
        rp_params = self._api_params_mapping["send_limit_order"]["response"]
        d = {}

        if order_data['side'] == 'BUY':
            order_data['side'] = self._side_buy
        elif order_data['side'] == 'SELL':
            order_data['side'] = self._side_sell

        for main_key, value in order_data.items():
            d[rq_params[main_key]] = value
        result = getattr(
            self.api_client,
            self._send_limit_order,
            )(**d)
        return result[rp_params['order_id']]

    def send_limit_orders(
        self,
        orders_data_list,
        ) -> set:
        orders_ids = set()
        if type(orders_data_list) == list:
            for order_data in orders_data_list:
                try:
                    order_id = self.send_limit_order(order_data)
                    orders_ids.add(order_id)
                except Exception as e:
                    logging.error(str(e))
                    logging.error(order_data)
        elif type(orders_data_list) == dict:
                try:
                    order_id = self.send_limit_order(orders_data_list)
                    orders_ids.add(order_id)
                except Exception as e:
                    logging.error(str(e))
                    logging.error(order_data)
        return orders_ids