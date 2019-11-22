class Order:
    order_id = None
    order_date = None
    quantity = None
    customer_id = None
    locality_id = None
    address_id = None
    created_by = None
    remarks = None
    status = None
    lu_date = None

    def __init__(self, order_id, order_date, quantity, customer_id, locality_id,
                 address_id, created_by, remarks, status, lu_date):
        self.order_id = order_id
        self.order_date = order_date
        self.quantity = quantity
        self.customer_id = customer_id
        self.locality_id = locality_id
        self.address_id = address_id
        self.created_by = created_by
        self.remarks = remarks
        self.status = status
        self.lu_date = lu_date

    def json(self):
        return{
            '_id': self.order_id,
            'order_date': self.order_date,
            'quantity': self.quantity,
            'customer_id': self.customer_id,
            'locality_id': self.locality_id,
            'address_id': self.address_id,
            'created_by': self.created_by,
            'remarks': self.remarks,
            'status': self.status,
            "lu_date" : self.lu_date
        }
