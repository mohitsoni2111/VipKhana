class Expense:
    expense_id = None
    quantity = None
    price_of_one = None
    remarks = None

    def __init__(self, expense_id, quantity, price_of_one, remarks):
        self.expense_id = expense_id
        self.quantity = quantity
        self.price_of_one = price_of_one
        self.remarks = remarks

    def json(self):
        return{
            '_id': self.expense_id,
            'quantity': self.quantity,
            'price_of_one': self.price_of_one,
            'remarks': self.remarks,
        }
