class Order:
    order_id = None
    phone_number = None
    no_of_tiffin = None
    street = None
    locality_id = None
    cust_name = None
    order_remarks = None
    address_remarks = None
    order_date = None
    status = None

    def __init__(self, order_id, phone_number, no_of_tiffin, street, locality_id,
                 cust_name, order_remarks, address_remarks, order_date, status):
        self.order_id = order_id
        self.phone_number = phone_number
        self.no_of_tiffin = no_of_tiffin
        self.street = street
        self.locality_id = locality_id
        self.cust_name = cust_name
        self.order_remarks = order_remarks
        self.address_remarks = address_remarks
        self.order_date = order_date
        self.status = status

    def json(self):
        return{
            '_id': self.order_id,
            'phone_number': self.phone_number,
            'no_of_tiffin': self.no_of_tiffin,
            'street': self.street,
            'locality_id': self.locality_id,
            'cust_name': self.cust_name,
            'order_remarks': self.order_remarks,
            'address_remarks': self.address_remarks,
            'order_date': self.order_date,
            "status" : self.status
        }
