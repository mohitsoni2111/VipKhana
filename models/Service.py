from datetime import datetime

from models.Address import Address
from models.Customer import Customer
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
    order_seq_table = 'seq_orderid'
    locality_seq_table = 'seq_localityid'
    address_seq_table = 'seq_addressid'
    customer_seq_table = 'seq_customerid'
    locality = 'locality'
    order = 'order'
    customer = 'customer'
    address = 'address'
    order_log = 'order_log'
    delivery_boy = 'delivery_boy'
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
    # 3. DATABASE SEQUENCES                                                                          #
    # #################################################################################################
    #
    #
    # Sequences must set to get and use mentality. Use the current value and then update.

    # 1- Order Id, 2- locality ID,
    def get_sequence_value(self, flag):
        if flag == 1:
            table = self.order_seq_table
        elif flag == 2:
            table = self.locality_seq_table
        elif flag == 3:
            table = self.address_seq_table
        else:
            table = self.customer_seq_table
        result = Database.find_one(collection=table, query={})
        if result is not None and result['num'] is not None:
            return int(result['num'])
        else:
            return -1

    # This will increment the value of sequence
    def set_sequence_value(self, flag):
        if flag == 1:
            table = self.order_seq_table
        elif flag == 2:
            table = self.locality_seq_table
        elif flag == 3:
            table = self.address_seq_table
        else:
            table = self.customer_seq_table
        Database.update(collection=table, query={}, new_data={'$inc': {'num': 1}})
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
        result = Database.find_one(collection=self.user_table, query={"_id": username})
        return '' if result is None else result['first_name']
    #
    #
    #
    #
    #
    # #################################################################################################
    # 3. ORDER MODULE                                                                                  #
    # #################################################################################################
    #

    def getlist(self, flag):
        if flag == 2:
            table = self.locality
        elif flag == 3:
            table = self.address
        else:
            table = self.customer
        result_list = []
        result = Database.find(collection=table, query={})
        if result is not None:
            for element in result:
                if element is not None:
                    result_list.append(element)
        return result_list

    def add_locality(self, locality_name):
        if Database.find_one(collection=self.locality, query={"name": locality_name}) is None:
            locality_id = self.get_sequence_value(2)
            if locality_id != -1:
                result = Database.insert(collection=self.locality,
                                         query={"_id": locality_id, "name": locality_name}
                                         )
                if result is not None:
                    self.set_sequence_value(2)
                    return locality_id
                else:
                    return -1
            else:
                return -1
        else:
            return int(Database.find_one(collection=self.locality, query={"name": locality_name})['_id'])

    def add_address(self, address):
        address_id = self.get_sequence_value(3)
        if address_id != -1:
            result = Database.insert(collection=self.address, query=address)
            if result is not None:
                self.set_sequence_value(3)
                return address_id
            else:
                return -1
        else:
            return -1

    def add_customer(self, customer):
        customer_id = self.get_sequence_value(4)
        if customer_id != -1:
            result = Database.insert(collection=self.customer, query=customer)
            if result is not None:
                self.set_sequence_value(4)
                return customer_id
            else:
                return -1
        else:
            return -1

    def add_order(self, order):
        result = Database.insert(collection=self.order, query=order)
        if result is not None:
            self.set_sequence_value(1)
            result2 = self.update_order_log(order['_id'], order['status'])
            return True if result2 is not None else False
        else:
            return False

    def list_orders_by_locality(self, stat):
        final_list = []
        result = [i for i in Database.find(collection=self.order, query={"status": stat}) if i is not None]
        if len(result) != 0:
            for order in sorted(result, key=lambda i: int(i['locality_id'])):
                final_list.append(
                    {
                        'order_id': order['_id'],
                        'phone_number': self.get_pnum_by_cust_id(order['customer_id']),
                        'customer_name': self.get_name_by_cust_id(order['customer_id']),
                        'locality_name': self.get_loc_name_by_loc_id(order['locality_id']),
                        'order_date': order['order_date'],
                        'quantity': order['quantity']
                    }
                )
        return final_list

    def get_pnum_by_cust_id(self, customer_id):
        result = Database.find_one(collection=self.customer, query={'_id': customer_id})
        if result is not None and result['phone_number'] is not None:
            return str(result['phone_number'])
        else:
            return '-1'

    def get_loc_name_by_loc_id(self, locality_id):
        result = Database.find_one(collection=self.locality, query={'_id': locality_id})
        if result is not None and result['name'] is not None:
            return str(result['name'])
        else:
            return '-1'

    def get_name_by_cust_id(self, customer_id):
        result = Database.find_one(collection=self.customer, query={'_id': customer_id})
        if result is not None:
            if result['first_name'] is not None and result['last_name'] is not None:
                return str(result['first_name']) + ' ' + str(result['last_name'])
            else:
                return '-1'
        else:
            return '-1'

    def update_order_log(self, order_id, new_status):
        result = Database.insert(collection=self.order_log,
                                 query={
                                     "order_id": order_id,
                                     "order_current_stat": new_status,
                                     "_id": datetime.now()
                                 })
        return False if result is None else True

    def get_order_logs(self, order_id):
        return [i for i in Database.find(collection=self.order_log, query={"order_id": order_id}) if i is not None]

    def get_delivery_boy_list(self):
        boy_list = []
        result = Database.find(collection=self.delivery_boy, query={})
        if result is not None:
            for boy in result:
                if boy is not None and boy['_id'] is not None and boy['first_name'] is not None:
                    boy_list.append(
                        {
                            'username': boy['_id'],
                            'name': boy['first_name']
                        }
                    )
        return boy_list

    def get_order_by_id(self, order_id):
        result = Database.find_one(collection=self.order, query={'_id': order_id})
        if result is not None:
            return Order(
                order_id=result['_id'],
                order_date=result['order_date'],
                address_id=result['address_id'],
                locality_id=result['locality_id'],
                created_by=result['created_by'],
                customer_id=result['customer_id'],
                quantity=result['quantity'],
                lu_date=result['lu_date'],
                remarks=result['remarks'],
                status=result['status'],
            )
        else:
            return None

    def get_address_by_id(self, address_id):
        result = Database.find_one(collection=self.address, query={'_id': address_id})
        if result is not None:
            return result['line1']+', '+result['line2']+', '+result['line3']
        else:
            return ''
