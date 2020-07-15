from werkzeug.utils import redirect

from models.Expense import Expense
from models.Order import Order
from models.Address import Address
from models.Customer import Customer
from models.Service import Service
from datetime import timedelta, datetime
from flask import Flask, render_template, flash, request, session, url_for

app = Flask(__name__)
service = Service()
service.startup()
app.secret_key = 'XhuhuADeiofioe2347298'
app.permanent_session_lifetime = timedelta(minutes=70)
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


# #################################################################################################
# 1. LOGIN & LOGOUT MODULE                                                                        #
# #################################################################################################
#
# 1. Home Rendering Page
@app.route('/home')
def home():
    if 'username' not in session:
        flash('Please sign in first')
        return render_template('index.html')
    else:
        if session['username'] == 'admin':
            return render_template(
                'home_admin.html',
                inc_curr_mon=service.get_tot_inc_exp_by_month(20, 11),
                exp_curr_mon=service.get_tot_inc_exp_by_month(30, 11),
            )
        else:
            return render_template(
                'home.html',
                first_name=service.get_first_name(session['username']),
                delivery_boy_list=service.get_delivery_boy_list()
            )


#
#
# A. Main Method
@app.route('/')
def start():
    if 'username' not in session:
        return render_template('index.html')
    else:
        return redirect(url_for('home'))


#
# B. Login Method
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        username = str(request.form['username'])
        password = str(request.form['password'])
        login_flag = service.logging_in(username=username, password=password)
        if login_flag == 1:
            flash('Username is incorrect, Please try again')
            return render_template('index.html')
        elif login_flag == 3:
            flash('Password is incorrect, Please try again')
            return render_template('index.html')
        elif login_flag == 2:
            session['username'] = username
            if username == 'admin':
                return render_template('home_admin.html', first_name='Admin')
            first_name = service.get_first_name(session['username'])
            if first_name is None:
                flash('User details not found, please contact administrator')
            return render_template(
                'home.html',
                first_name=first_name,
                delivery_boy_list=service.get_delivery_boy_list()
            )


#
#
#
# B. Logout Method
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        session.pop('username', None)
        flash('Successfully logged out')
        return render_template('index.html')


#
# #################################################################################################
# 2. ORDER MODULE                                                                                 #
# #################################################################################################
#
#
# Add Order
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        return render_template(
            'add_order.html',
            order_id=service.get_sequence_value(1),
            locality_list=service.getlist(2),
            address_list=service.getlist(3),
            customer_list=service.getlist(5),
            flag='order',
            first_name=service.get_first_name(session['username'])
        )


@app.route('/adding_order', methods=['GET', 'POST'])
def adding_order():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        # Getting Locality
        ram = request.form['loc_id']
        if str(request.form['loc_id']) == '1.0' or int(request.form['loc_id']) == 1:
            locality_id = service.add_locality(str(request.form['locality']).lower())
            if locality_id == -1:
                flash("Error in adding a new locality, contact admin for this.")
                return render_template(
                    "home.html",
                    first_name=service.get_first_name(session['username']),
                    delivery_boy_list=service.get_delivery_boy_list()
                )
        else:
            locality_id = int(str(request.form['loc_id']))

        # Getting Address
        if str(request.form['adr_id']) == '1.0' or int(request.form['adr_id']) == 1:
            address = Address(
                address_id=service.get_sequence_value(3),
                locality_id=locality_id,
                line1=str(request.form['line1']),
                line2=str(request.form['line2']),
                line3=str(request.form['line3']),
                remarks=str(request.form['address_remarks'])
            )
            address_id = service.add_address(address.json())
            if address_id == -1:
                flash('Error in adding a new address, contact admin for this.')
                return render_template(
                    'home.html',
                    first_name=service.get_first_name(session['username']),
                    delivery_boy_list=service.get_delivery_boy_list()
                )
        else:
            address_id = int(request.form['adr_id'])

        # Getting Customer Details
        if str(request.form['cust_id']) == '1.0' or int(request.form['cust_id']) == 1:
            customer = Customer(
                customer_id=service.get_sequence_value(4),
                first_name=str(request.form['first_name']),
                last_name=str(request.form['last_name']),
                gender=str(request.form['gender']),
                phone_number=str(request.form['phone_number']),
                remarks=str(request.form['customer_remarks'])
            )
            customer_id = service.add_customer(customer.json())
            if customer_id == -1:
                flash('Error in adding a new customer, contact admin for this.')
                return render_template(
                    'home.html',
                    first_name=service.get_first_name(session['username']),
                    delivery_boy_list=service.get_delivery_boy_list()
                )
        else:
            customer_id = int(request.form['cust_id'])

        order = Order(
            order_id=int(request.form['order_id']),
            customer_id=customer_id,
            address_id=address_id,
            locality_id=locality_id,
            created_by=str(session['username']),
            quantity=int(request.form['quantity']),
            order_date=datetime.now(),
            lu_date=datetime.now(),
            remarks=str(request.form['order_remarks']),
            status=1
        )
        if service.add_order(order.json()):
            flash("Successfully Added")
        else:
            flash("not Added")
        return redirect(url_for('home'))


# List Orders active
@app.route('/list_order_stat1', methods=['GET', 'POST'])
def list_order_stat1():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        return render_template(
            'list_order.html',
            first_name=service.get_first_name(session['username']),
            flag='delivery',
            orders=service.list_orders_by_locality(1),
            header='List of all Active Orders',
            delivery_boy_list=service.get_delivery_boy_list()
        )


# List Orders with delivery guy
@app.route('/list_order_stat2', methods=['GET', 'POST'])
def list_order_stat2():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        return render_template(
            'list_order.html',
            first_name=service.get_first_name(session['username']),
            flag='payment',
            orders=service.list_orders_by_locality(2),
            header='List of all orders in delivery'
        )


# List Orders with or without payment
@app.route('/list_order_stat34', methods=['GET', 'POST'])
def list_order_stat34():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        return render_template(
            'list_order.html',
            first_name=service.get_first_name(session['username']),
            flag='after payment',
            orders3=service.list_orders_by_locality(3),
            orders4=service.list_orders_by_locality(4),
            header='List of all orders with customer'
        )


# List Orders completed
@app.route('/list_order_history', methods=['GET', 'POST'])
def list_order_history():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        return render_template(
            'list_order.html',
            first_name=service.get_first_name(session['username']),
            flag='completed',
            orders=service.list_order_history(),
            header='List of all completed orders'
        )


@app.route('/detailed_order', methods=['GET', 'POST'])
def detailed_order():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        order_id = int(request.args.get('order_id'))
        flag = int(request.args.get('flag'))
        if flag == 5:
            order = service.get_order_from_history(order_id)
        else:
            order = service.get_order(order_id)

        return render_template(
            'order_details.html',
            first_name=service.get_first_name(session['username']),
            order=order.json(),
            customer_name=service.get_customer_name(order.customer_id),
            customer_phone=service.get_customer_phone(order.customer_id),
            locality_name=service.get_locality_name(order.locality_id),
            address=service.get_address(order.address_id),
            logs=service.get_order_logs(order.order_id),
            status_enum=status_enum,
            delivery_guy_name=service.get_delivery_boy_name(order.order_id)
        )


@app.route('/order_details', methods=['GET', 'POST'])
def list_order():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        order_id = int(request.form['order_id'])
        result = service.get_order_logs(order_id)
        order = service.get_order(order_id)

        if result is None:
            flash("No such Order")
            render_template('home.html', delivery_boy_list=service.get_delivery_boy_list())
        else:
            return render_template(
                'order_details.html',
                first_name=service.get_first_name(session['username']),
                order=order.json(),
                customer_name=service.get_customer_name(order.customer_id),
                customer_phone=service.get_customer_phone(order.customer_id),
                locality_name=service.get_locality_name(order.locality_id),
                address=service.get_address(order.address_id),
                logs=service.get_order_logs(order.order_id),
                status_enum=status_enum,
                delivery_guy_name=service.get_delivery_boy_name(order.order_id)
            )


@app.route('/delivery_details', methods=['GET', 'POST'])
def delivery_details():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        delivery_boy_id = int(request.form['delboy_id'])
        return render_template(
            'list_order.html',
            first_name=service.get_first_name(session['username']),
            flag='delivery boy list',
            orders=service.list_orders_by_delivery_guy(delivery_boy_id),
            header='List of all orders for Delivery man- ',
            delivery_guy_name=service.get_element_by_id('first_name', delivery_boy_id, 8)
        )


@app.route('/order_to_tiffin', methods=['GET', 'POST'])
def order_to_tiffin():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        tiffin_number = int(request.form['tiffin_number'])
        order_id = int(request.form['order_id'])
        if service.map_order_to_tiffin(order_id, tiffin_number):
            flash('Order Mapped')
        else:
            flash('Not Done bro')


@app.route('/change_order_stat', methods=['GET', 'POST'])
def change_order_stat():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        new_status = int(request.form['new_status'])
        order_id = int(request.form['order_id'])
        if service.change_order_status(order_id, new_status):
            flash('Status successfully changed')
        else:
            flash('Status not changed')
        return render_template(
            "home.html",
            first_name=service.get_first_name(session['username']),
            delivery_boy_list=service.get_delivery_boy_list()
        )


@app.route('/order_to_delivery', methods=['GET', 'POST'])
def order_to_delivery():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            delivery_boy_id = int(request.form['delboy_id'])
            order_id = int(request.form['order_id'])
            if service.add_delivery(order_id, delivery_boy_id):
                flash('Delivery assigned')
                return redirect(url_for('list_order_stat1'))
            else:
                flash('Delivery not assigned')
                return redirect(url_for('list_order_stat1'))


@app.route('/order_to_payment', methods=['GET', 'POST'])
def order_to_payment():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        payment_type = int(request.form['payment_type'])
        order_id = int(request.form['order_id'])
        if payment_type == 1:
            amount = service.add_payment_order(order_id)
            if amount != 0:
                message_on_flash = 'Payment recorded of ' + str(amount)
                flash(message_on_flash)
                return redirect(url_for('list_order_stat2'))
            else:
                flash('Action failed')
                return redirect(url_for('list_order_stat2'))
        else:
            if service.change_order_status(order_id, 4):
                flash('Order Updated')
                return redirect(url_for('list_order_stat2'))


@app.route('/order_to_final', methods=['GET', 'POST'])
def order_to_final():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        order_type = int(request.form['order_type'])
        order_id = int(request.form['order_id'])
        if order_type == 2:
            if service.change_order_status(order_id, 6):
                flash('Order Updated')
                return redirect(url_for('list_order_stat34'))
        else:
            if service.change_order_status(order_id, 5):
                order = service.get_order(order_id)
                service.add_order_history(order.json())
                flash('Congratulations Order is completed')
                return redirect(url_for('list_order_stat34'))


@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        phone_number = str(request.form['phone-number'])
        return render_template(
            'payment.html',
            first_name=service.get_first_name(session['username']),
            flag='after payment',
            customer_name=service.get_first_name_of_customer(phone_number),
            final_list1=service.check_phone_number(phone_number)
        )


@app.route('/add_expense', methods=['get', 'post'])
def add_expense():
    if request.method != 'POST':
        return redirect(url_for('home'))
    elif str(request.form['isExpense']):
        # Expense option is selected
        return render_template('add_order.html',
                               expense_id=service.get_sequence_value(6),
                               expense_class_list=service.getlist(4),
                               expense_type_list_10=service.getlist(5),
                               expense_type_list_11=service.getlist(6),
                               flag='expense',
                               first_name=service.get_first_name(session['username'])
                               )
    else:
        # Income option is selected
        # TO DO LATER
        return render_template('add_order.html',
                               income_id=service.get_sequence_value(6),
                               expense_list=service.getlist(4),
                               flag='income',
                               first_name=service.get_first_name(session['username'])
                               )


@app.route('/adding_expense', methods=['GET', 'POST'])
def adding_expense():
    if request.method != 'POST':
        return redirect(url_for('home'))
    else:
        # Getting Expense Class
        if str(request.form['expense_class_id']) == '1.0' or int(request.form['expense_class_id']) == 1:
            expense_class_id = service.add_expense_class(str(request.form['expense_class']).lower())
            if expense_class_id == -1:
                flash("Error in adding a new Expense Class, contact admin for this.")
                return render_template(
                    "home.html",
                    first_name=service.get_first_name(session['username']),
                )
        else:
            expense_class_id = int(str(request.form['expense_class_id']))

        # Getting Expense Details
        if str(request.form['expen_id']) == '1.0' or int(request.form['expen_id']) == 1:
            expense = Expense(
                expense_id=service.get_sequence_value(6),
                quantity=str(request.form['quantity']),
                price_of_one=str(request.form['price_of_one']),
                remarks=str(request.form['customer_remarks'])
            )
            expense_id = service.add_customer(expense.json())
            if expense_id == -1:
                flash('Error in adding a new expense, contact admin for this.')
                return render_template(
                    'home.html',
                    first_name=service.get_first_name(session['username']),
                )
        else:
            expense_id = int(request.form['expen_id'])


if __name__ == '__main__':
    app.run()
