from datetime import datetime

import pymongo

from models.Database import Database
from models.Order import Order


class Service:
    # #################################################################################################
    # 1. TABLE NAMES IN DATABASE                                                                      #
    # #################################################################################################
    #
    #
    #
    login_table = 'login'
    user_table = 'user'
    order_seq_table = 'seq_order_id'
    locality_seq_table = 'seq_locality_id'
    locality = 'locality'
    order = 'order'
    order_log = 'order_log'
    status_enum = {
        1: 'Order Received by Vip Khana',
        2: 'Order assigned to delivery guy',
        3: 'Tiffin received to customer and payment received to us',
        4: 'Tiffin received to customer and payment not received to us',
        5: 'Perfectly completed order',
        6: 'Faulty tiffin received by Vip Khana',
        7: 'Order cancelled by user',
        8: 'Order cancelled by Vip Khana'
    }
    #
    #
    #
    #
    #
    # #################################################################################################
    # 2. DATABASE CONNECTION                                                                          #
    # #################################################################################################
    #
    #

    def startup(self):
        Database.__initialize__()
    #
    #
    #
    #
    #
    # #################################################################################################
    # 3. LOGIN MODULE                                                                                  #
    # #################################################################################################
    #

    # return      1- no user found, 2- successful login, 3- password mismatch
    def logging_in(self, username, password):
        result = Database.find_one(collection=self.login_table, query={"_id": username})
        if result is None:
            return 1
        elif result['password'] == password:
            return 2
        else:
            return 3

    def get_first_name(self, username):
        return Database.find_one(collection=self.user_table, query={"_id": username})['first_name']
    #
    #
    #
    #
    #
    # #################################################################################################
    # 3. ORDER MODULE                                                                                  #
    # #################################################################################################
    #

    def seq_order_id(self):
        order_id = int(Database.find_one(collection=self.order_seq_table, query={})['num'])
        return order_id

    def seq_locality_id(self):
        locality_id = int(Database.find_one(collection=self.locality_seq_table, query={})['num'])
        return locality_id

    def get_locality_list(self):
        locality_list = []
        for locality in Database.find(self.locality, query={}):
            locality_list.append(locality)
        return locality_list

    def add_new_locality(self, locality_name):
        locality_id = self.seq_locality_id()
        result = Database.insert(collection=self.locality,
                                 query={"_id": locality_id+1, "name": locality_name})
        if result is None:
            return -1
        else:
            result1 = Database.update(collection=self.locality_seq_table, query={},
                                      new_data={"_id": "seq", "num": locality_id+1})
        return locality_id+1 if result1 is not None else -1

    def add_new_order(self, order):
        result = Database.insert(collection=self.order, query=order)
        if result is None:
            return False
        else:
            order_seq = self.seq_order_id()
            result1 = Database.update(collection=self.order_seq_table, query={},
                                      new_data={"_id": "seq", "num": order_seq + 1})
            if result1 is None:
                return False
            else:
                result3 = self.update_order_log(order_seq, 1)
                return True if result3 is not None else False

    def list_orders_by_locality(self, stat):
        result = [i for i in Database.find(collection=self.order, query={"status": stat})]
        return sorted(result, key=lambda i: int(i['locality_id']))

    def update_order_log(self, order_id, new_status):
        result = Database.insert(collection=self.order_log,
                                 query={
                                     "order_id": order_id,
                                     "order_current_stat": new_status,
                                     "_id": datetime.now()
                                 })
        return False if result is None else True

    def get_order_logs(self, order_id):
        return [i for i in Database.find(
            collection=self.order_log,
            query={"order_id": order_id}
        )]
