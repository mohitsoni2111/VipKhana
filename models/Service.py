from datetime import datetime, timedelta

from django import db

from models.Database import Database
from models.Order import Order


class Service:
    # #################################################################################################
    # TABLE NAMES AND VARIABLES IN DATABASE                                                           #
    # #################################################################################################
    #
    # Table Names with flag values
    # flag= 1
    order = 'order'
    # flag= 2
    locality = 'locality'
    # flag= 3
    address = 'address'
    # flag= 4
    customer = 'customer'
    # flag= 5
    login_table = 'login'
    # flag= 6
    user_table = 'user'
    # flag= 7
    order_log = 'order_log'
    # flag= 8
    delivery_boy = 'delivery_boy'
    # flag= 9
    delivery = 'delivery'
    # flag= 10
    payment = 'payment'
    # flag= 11
    order_history = 'order_history'
    # flag=12
    db_variables = 'variables'
    #
    #
    # Sequences Names with flag value
    # flag= 31
    order_seq_table = 'seq_orderid'
    # flag= 32
    locality_seq_table = 'seq_localityid'
    # flag= 33
    address_seq_table = 'seq_addressid'
    # flag= 34
    customer_seq_table = 'seq_customerid'
    # flag= 35
    delivery_seq_table = 'seq_deliveryid'
    # flag= 36
    payment_seq_table = 'seq_paymentid'
    # flag = 37
    expense_seq_table = 'seq_expenseid'
    #
    #
    # Variables
    #
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
    # Database connection initialization:
    def startup(self):
        Database.__initialize__()

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # #################################################################################################
    # A. Login Table                                                                                  #
    # #################################################################################################
    #
    # return      1- no user found, 2- successful login, 3- password mismatch
    def logging_in(self, username, password):
        result = self.get_element_by_id('password', username, 5)
        if result is None:
            return 1
        elif str(result) == password:
            return 2
        else:
            return 3

    #
    #
    #
    #
    #
    # #################################################################################################
    # B. User Table                                                                                  #
    # #################################################################################################
    #
    def get_first_name(self, username):
        result = self.get_element_by_id('first_name', username, 6)
        return None if result is None else str(result)

    #
    #
    #
    #
    #
    # #################################################################################################
    # C. Locality Table                                                                                  #
    # #################################################################################################
    #

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

    def get_locality_name(self, locality_id):
        loc_name = self.get_element_by_id('name', locality_id, 2)
        if loc_name is not None:
            return str(loc_name)
        else:
            return '-1'

    #
    #
    #
    #
    #
    # #################################################################################################
    # D. Address Table                                                                                  #
    # #################################################################################################
    #
    def get_address(self, address_id):
        line1 = self.get_element_by_id('line1', address_id, 3)
        line2 = self.get_element_by_id('line2', address_id, 3)
        line3 = self.get_element_by_id('line3', address_id, 3)
        if line1 is not None and line2 is not None and line3 is not None:
            return str(line1) + ', ' + str(line2) + ', ' + str(line3)
        else:
            return ' '

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

    #
    #
    #
    #
    #
    # #################################################################################################
    # E. Order Table                                                                                  #
    # #################################################################################################
    #
    def get_order(self, order_id):
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
                        'phone_number': self.get_customer_phone(order['customer_id']),
                        'customer_name': self.get_customer_name(order['customer_id']),
                        'locality_name': self.get_locality_name(order['locality_id']),
                        'order_date': order['order_date'],
                        'quantity': order['quantity'],
                        'status': order['status']
                    }
                )
        return final_list

    def list_orders_by_delivery_guy(self, delivery_boy_id):
        order_id_list = [
            int(i['order_id']) for i in Database.find(
                collection=self.delivery,
                query={"delivery_boy_id": delivery_boy_id})
            if i is not None and i['delivery_boy_id'] is not None]

        final_list = []
        for i in order_id_list:
            order = Database.find_one(collection=self.order, query={"_id": i})
            if order is not None:
                final_list.append(
                    {
                        'order_id': order['_id'],
                        'phone_number': self.get_customer_phone(order['customer_id']),
                        'customer_name': self.get_customer_name(order['customer_id']),
                        'locality_name': self.get_locality_name(order['locality_id']),
                        'order_date': order['order_date'],
                        'quantity': order['quantity'],
                        'status': order['status']
                    }
                )
        return final_list

    def change_order_status(self, order_id, new_status):
        order = self.get_order(order_id)
        order.status = new_status
        order.lu_date = datetime.now()
        result = Database.update(collection=self.order, query={'_id': order_id}, new_data=order.json())
        if result['updatedExisting'] is False:
            return False
        else:
            return True if self.update_order_log(order_id, new_status) else False

    #
    #
    #
    #
    #
    # #################################################################################################
    # F. Customer Table                                                                                  #
    # #################################################################################################
    #
    def get_customer_phone(self, customer_id):
        phone_number = self.get_element_by_id('phone_number', customer_id, 4)
        if phone_number is not None:
            return str(phone_number)
        else:
            return '-1'

    def get_customer_name(self, customer_id):
        first_name = self.get_element_by_id('first_name', customer_id, 4)
        last_name = self.get_element_by_id('last_name', customer_id, 4)
        if first_name is not None and last_name is not None:
            return str(first_name) + ' ' + str(last_name)
        else:
            return '-1'

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

    #
    #
    #
    #
    #
    # #################################################################################################
    # G. Delivery Boy Table                                                                                  #
    # #################################################################################################
    #
    def get_delivery_boy_list(self):
        boy_list = []
        result = Database.find(collection=self.delivery_boy, query={})
        # print(*result)
        if result is not None:
            for boy in result:
                if boy is not None and boy['first_name'] is not None:
                    # may use dictionary
                    boy_list.append(
                        {
                            'username': int(boy['_id']),
                            'name': str(boy['first_name'])
                        }
                    )
        print(boy_list)
        return boy_list

    def get_delivery_boy_name(self, order_id):
        result = Database.find_one(collection=self.delivery, query={'order_id': order_id})
        if result is not None:
            delivery_boy_id = result['delivery_boy_id']
            if delivery_boy_id is not None:
                delivery_boy_name = self.get_element_by_id('first_name', delivery_boy_id, 8)
                if delivery_boy_name is not None:
                    return str(delivery_boy_name)
        else:
            return 'Delivery boy not assign'
        return 'Delivery boy not assign'

    #
    #
    #
    #
    #
    # #################################################################################################
    # H. Order Log Table                                                                                  #
    # #################################################################################################
    #
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

    #
    #
    #
    #
    #
    # #################################################################################################
    # H. Delivery Table                                                                                  #
    # #################################################################################################
    #
    def add_delivery(self, order_id, delivery_boy_id):
        delivery_id = self.get_sequence_value(5)
        if delivery_id != -1:
            result = Database.insert(collection=self.delivery,
                                     query={
                                         '_id': delivery_id,
                                         'order_id': order_id,
                                         'delivery_boy_id': delivery_boy_id,
                                         'delivery_date': datetime.now(),
                                         'delivery_status': 1
                                     }
                                     )
            if result is not None:
                self.set_sequence_value(5)
                if self.change_order_status(order_id, 2):
                    return True
                else:
                    Database.delete(collection=self.delivery, query={'_id': delivery_id})
                    self.rev_sequence_value(5)
                    return False
            else:
                return False
        else:
            return False

    #
    #
    #
    #
    #
    # #################################################################################################
    # I. Payment Table                                                                                  #
    # #################################################################################################
    #
    def add_payment_order(self, order_id):
        amount = 0
        payment_id = self.get_sequence_value(6)
        quantity = self.get_element_by_id('quantity', order_id, 1)
        rate = self.get_db_variable('tiffin_rate')
        if quantity is not None and rate is not None:
            amount = int(rate) * int(quantity)
        result = Database.insert(
            collection=self.payment,
            query={
                '_id': payment_id,
                'payment_type': 11,
                'order_id': order_id,
                'payment_date': datetime.now(),
                'amount': amount
            }
        )
        if result is not None:
            if self.change_order_status(order_id, 3):
                self.set_sequence_value(6)
            else:
                Database.delete(collection=self.payment, query={'_id': payment_id})
                self.rev_sequence_value(6)
        return amount

    #
    #
    #
    #
    #
    # #################################################################################################
    # J. Sequences Table                                                                                  #
    # #################################################################################################
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
        elif flag == 4:
            table = self.customer_seq_table
        elif flag == 5:
            table = self.delivery_seq_table
        elif flag == 6:
            table = self.db_variables
        else:
            table = self.payment_seq_table
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
        elif flag == 4:
            table = self.customer_seq_table
        elif flag == 5:
            table = self.delivery_seq_table
        elif flag == 6:
            table = self.expense_seq_table
        else:
            table = self.payment_seq_table
        Database.update(collection=table, query={}, new_data={'$inc': {'num': 1}})

    # This will decrement the value of sequence
    def rev_sequence_value(self, flag):
        if flag == 1:
            table = self.order_seq_table
        elif flag == 2:
            table = self.locality_seq_table
        elif flag == 3:
            table = self.address_seq_table
        elif flag == 4:
            table = self.customer_seq_table
        elif flag == 5:
            table = self.delivery_seq_table
        elif flag == 6:
            table = self.expense_seq_table
        else:
            table = self.payment_seq_table
        Database.update(collection=table, query={}, new_data={'$inc': {'num': -1}})

    #
    #
    #
    #
    #
    # #################################################################################################
    # K. Generic Methods                                                                                  #
    # #################################################################################################
    #
    def getlist(self, flag):
        if flag == 2:
            table = self.locality
        elif flag == 3:
            table = self.address
        elif flag == 4 or 5 or 6:
            table = self.db_variables
        else:
            table = self.customer
        result_list = []
        list2 = []
        # if flag == 4:
        #     # Easy query also available but need to find
        #     query2 = {$and:[{'_id' : {$not : /:0:/}}, {$and : [{'_id' : /^2/}, {'_id' : /0$/}]}]}
        #     result = Database.find(collection=table, query=query2)
        # else:
        result = Database.find(collection=table, query={})
        if result is not None:
            for element in result:
                if element is not None:
                    result_list.append(element)
        if flag == 4:
            for element in result_list:
                for key, value in element.items():
                    if key == '_id':
                        a = value.split(':')
                        if a[0] == '2' and a[1] != '0' and a[2] == '0':
                            list2.append(element)
            result_list = list2

        if flag == 5:
            for element in result_list:
                for key, value in element.items():
                    if key == '_id':
                        a = value.split(':')
                        if a[0] == '2' and a[1] == '10' and a[2] != '0':
                            list2.append(element)
            result_list = list2

        if flag == 6:
            for element in result_list:
                for key, value in element.items():
                    if key == '_id':
                        a = value.split(':')
                        if a[0] == '2' and a[1] == '11' and a[2] != '0':
                            list2.append(element)
            result_list = list2
        return result_list

    def find_expense_seq_no(self, flag):
        result_list = []
        result = Database.find(collection=self.db_variables, query={})
        if result is not None:
            for element in result:
                if element is not None:
                    result_list.append(element)

        for element in result_list:
            for key, value in element.items():
                if key == '_id':
                    a = value.split(':')
                    if flag == 1 and a[1] and a[2] == '0':
                            return a[0]
                    elif flag == 2 and a[0] == '2' and a[1] != '0' and a[2] == '0':
                            return max(a[1])

        if flag == 2:
            for element in result_list:
                for key, value in element.items():
                    if key == '_id':
                        a = value.split(':')
                        if a[0] == '2' and a[1] == '10' and a[2] != '0':
                            list2.append(element)
            result_list = list2

        if flag == 3:
            for element in result_list:
                for key, value in element.items():
                    if key == '_id':
                        a = value.split(':')
                        if a[0] == '2' and a[1] == '11' and a[2] != '0':
                            list2.append(element)
            result_list = list2
        return result_list


    def get_element_by_id(self, element, id_value, flag):
        if flag == 1:
            table = self.order
        elif flag == 2:
            table = self.locality
        elif flag == 3:
            table = self.address
        elif flag == 4:
            table = self.customer
        elif flag == 5:
            table = self.login_table
        elif flag == 6:
            table = self.user_table
        elif flag == 7:
            table = self.order_log
        elif flag == 8:
            table = self.delivery_boy
        elif flag == 9:
            table = self.delivery
        elif flag == 10:
            table = self.payment
        elif flag == 11:
            table = self.order_history
        elif flag == 12:
            table = self.db_variables
        elif flag == 31:
            table = self.order_seq_table
        elif flag == 32:
            table = self.locality_seq_table
        elif flag == 33:
            table = self.address_seq_table
        elif flag == 34:
            table = self.customer_seq_table
        elif flag == 35:
            table = self.delivery_seq_table
        elif flag == 36:
            table = self.payment_seq_table
        elif flag == 37:
            table = self.expense_seq_table
        else:
            table = self.payment_seq_table
        result = Database.find_one(collection=table, query={'_id': id_value})
        if result is not None:
            return result[element] if result[element] is not None else None
            # To be tested by mohit
        else:
            return None

    def get_db_variable(self, variable_name):
        result = Database.find_one(collection='variables', query={'_id': variable_name})
        return result['var_value'] if result is not None else None

    def map_order_to_tiffin(self, order_id, tiffin_number):
        Database.update(
            collection='order_tiffin_map',
            query={'_id': tiffin_number},
            new_data={'order_id': order_id, '_id': tiffin_number}
        )
        return True

    def add_order_history(self, order):
        Database.insert(collection='order_history', query=order)
        Database.delete(collection='order', query={'_id': order['_id']})

    def list_order_history(self):
        final_list = []
        result = [i for i in Database.find(collection='order_history', query={}) if i is not None]
        if len(result) != 0:
            for order in sorted(result, key=lambda i: int(i['locality_id'])):
                final_list.append(
                    {
                        'order_id': order['_id'],
                        'phone_number': self.get_customer_phone(order['customer_id']),
                        'customer_name': self.get_customer_name(order['customer_id']),
                        'locality_name': self.get_locality_name(order['locality_id']),
                        'order_date': order['order_date'],
                        'quantity': order['quantity'],
                        'status': order['status']
                    }
                )
        return final_list

    def get_order_from_history(self, order_id):
        result = Database.find_one(collection='order_history', query={'_id': order_id})
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

    # type= 20 for income, 30 for expense, 			payment_type= int
    def get_tot_inc_exp_by_month(self, payment_type, month):
        current_date = datetime.now()
        if payment_type == 20:
            start_type = 0
            end_type = 20
        else:
            start_type = 21
            end_type = 30
        if month == 0:
            start_date = datetime.now() - timedelta(days=365)
            end_date = datetime.now()
        else:
            start_date = datetime(current_date.year, int(month), 1)
            if int(month) == 12:
                end_date = datetime(int(current_date.year) + 1, 1, 1)
            else:
                end_date = datetime(current_date.year, int(month) + 1, 1)

        result_list = [
            int(i['amount']) for i in Database.find(
                collection=self.payment,
                query={
                    "$and": [
                        {'payment_type': {"$gte": start_type, "$lte": end_type}},
                        {'payment_date': {"$gte": start_date, "$lte": end_date}}
                    ]
                }
            ) if i is not None and i['amount'] is not None
        ]
        return sum(result_list)

    def check_phone_number(self, phone_number):
        result = Database.find_one(collection=self.customer, query={'phone_number': phone_number})
        if result is not None:
            final_list = []
            customer_id = result['_id']
            result2 = [int(i['_id']) for i in Database.find(collection=self.order,
                                                            query={"customer_id": customer_id}) if i is not None]
            # print(result2)
            result4 = [i for i in Database.find(collection=self.order,
                                                query={"customer_id": customer_id}) if i is not None]
            # if len(result4) != 0:
            #     for payment in sorted(result4, key=lambda i: int(i['_id'])):
            #         final_list.append(
            #             {
            #                 'order_date': payment['order_date'],
            #                 'quantity': payment['quantity'],
            #             })
            # print(result4)
            query2 = {'order_id': {'$in': result2}}
            result3 = [i for i in Database.find(collection=self.payment, query=query2) if i is not None]
            if len(result3) != 0:
                for payment in sorted(result3, key=lambda i: int(i['_id'])):
                    if len(result4) != 0:
                        for element in sorted(result4, key=lambda i: int(i['_id'])):
                            if element['quantity']*400 == payment['amount']:
                                final_list.append(
                                    {
                                        'payment_date': payment['payment_date'],
                                        'amount': payment['amount'],
                                        'order_id': payment['order_id'],
                                        'order_date': element['order_date'],
                                        'quantity': element['quantity'],
                                    })
            print('FINAL LISTTTTT' , final_list)
            return final_list
        else:
            return None

    def get_first_name_of_customer(self, phone_number):
        result = Database.find_one(collection=self.customer, query={'phone_number': phone_number})
        if result is not None:
            customer_name = result['first_name']
        else:
            return None
        return customer_name

    # def add_expense_class(self, expense_class):
    #     if Database.find_one(collection=self.db_variables, query={"var_value": expense_class}) is None:
    #         expense_class_id = self.get_sequence_value(6)
    #         if expense_class_id != -1:
    #             result = Database.insert(collection=self.db_variables,
    #                                      query={"_id": locality_id, "var_value": expense_class}
    #                                      )
    #             if result is not None:
    #                 self.set_sequence_value(2)
    #                 return locality_id
    #             else:
    #                 return -1
    #         else:
    #             return -1
    #     else:
    #         return int(Database.find_one(collection=self.locality, query={"name": locality_name})['_id'])
    #
    # def find_expense_class
