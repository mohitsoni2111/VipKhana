class Address:
    address_id = None
    line1 = None
    line2 = None
    line3 = None
    locality_id = None
    remarks = None

    def __init__(self, address_id, line1, line2, line3, locality_id, remarks):
        self.address_id = address_id
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.locality_id = locality_id
        self.remarks = remarks

    def json(self):
        return{
            '_id': self.address_id,
            'line1': self.line1,
            'line2': self.line2,
            'line3': self.line3,
            'locality_id': self.locality_id,
            'remarks': self.remarks,
        }
