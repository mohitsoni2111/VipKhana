class Customer:
    customer_id = None
    first_name = None
    last_name = None
    gender = None
    phone_number = None
    remarks = None

    def __init__(self, customer_id, first_name, last_name, gender, phone_number, remarks):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone_number = phone_number
        self.remarks = remarks

    def json(self):
        return{
            '_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'remarks': self.remarks,
        }
