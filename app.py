from models.Database import Database
from models.Order import Order
from models.Address import Address
from models.Customer import Customer
from models.Service import Service
from datetime import timedelta, datetime
from flask import Flask, render_template, flash, request, session


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
#
# A. Main Method
@app.route('/')
def start():
    if 'username' in session:
        if session['username'] == 'admin':
            return render_template('home_admin.html', first_name='admin')
        else:
            first_name = service.get_first_name(session['username'])
            if first_name is None:
                flash('User details not found, please contact administrator')
                return render_template('home.html', first_name='')
            else:
                return render_template('home.html', first_name=first_name)
    else:
        return render_template('index.html')
#
#
# B. Login Method
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' in session:
            if session['username'] == 'admin':
                return render_template('home_admin.html', first_name='admin')
            else:
                first_name = service.get_first_name(session['username'])
                if first_name is None:
                    flash('User details not found, please contact administrator')
                    return render_template('home.html', first_name='')
                else:
                    return render_template('home.html', first_name=first_name)
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
                first_name = service.get_first_name(session['username'])
                if first_name is None:
                    flash('User details not found, please contact administrator')
                    return render_template('home.html', first_name='')
                else:
                    return render_template('home.html', first_name=first_name)
            else:
                flash('Something went wrong, really really wrong!!')
                return render_template('index.html')
#
#
#
# B. Logout Method
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    print(Database.find_one(collection='locality', query={'name': 'Sector 13'}))
    session.pop('username', None)
    flash('Successfully logged out')
    return render_template('index.html')
#
#
#
#
#
# #################################################################################################
# 2. ORDER MODULE                                                                                 #
# #################################################################################################
#
#
# Add Order
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if 'username' in session:
        return render_template('add_order.html',
                               order_id=service.get_sequence_value(1),
                               locality_list=service.getlist(2),
                               address_list=service.getlist(3),
                               customer_list=service.getlist(4),
                               first_name=service.get_first_name(session['username'])
                               )
    else:
        return render_template('index.html')


@app.route('/adding_order', methods=['GET', 'POST'])
def adding_order():
    if 'username' in session:
        # Getting Locality
        ram = request.form['loc_id']
        print(ram)
        if str(request.form['loc_id']) == '1.0' or int(request.form['loc_id']) == 1:
            locality_id = service.add_locality(str(request.form['locality']).lower())
            if locality_id == -1:
                flash("Error in adding a new locality, contact admin for this.")
                return render_template("home.html", first_name=service.get_first_name(session['username']))
        else:
            locality_id = int(request.form['loc_id'])

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
                return render_template('home.html', first_name=service.get_first_name(session['username']))
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
                return render_template('home.html', first_name=service.get_first_name(session['username']))
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
            return render_template("home.html", first_name=service.get_first_name(session['username']))
        else:
            flash("not Added")
            return render_template("home.html", first_name=service.get_first_name(session['username']))
    else:
        return render_template('index.html')

# List Orders active
@app.route('/list_order_stat1', methods=['GET', 'POST'])
def list_order_stat1():
    if 'username' in session:
        return render_template(
            'list_order.html',
            first_name=service.get_first_name(session['username']),
            orders=service.list_orders_by_locality(1),
            header='List of all Active Orders',
            delivery_boy_list=service.get_delivery_boy_list()
        )
    else:
        return render_template('index.html')


@app.route('/detailed_order', methods=['GET', 'POST'])
def detailed_order():
    if 'username' in session:
        order_id = int(request.args.get('order_id'))
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
            status_enum=status_enum
        )
    else:
        return render_template('index.html')


@app.route('/order_details', methods=['GET', 'POST'])
def list_order():
    order_id = int(request.form['order_id'])
    result = service.get_order_logs(order_id)
    order = service.get_order(order_id)

    if result is None:
        flash("No such Order")
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
            status_enum=status_enum
        )


@app.route('/change_order_stat', methods=['GET', 'POST'])
def change_order_stat():
    new_status = int(request.form['new_status'])
    order_id = int(request.form['order_id'])
    if service.change_order_status(order_id, new_status):
        flash('Status successfully changed')
    else:
        flash('Status not changed')
    return render_template("home.html", first_name=service.get_first_name(session['username']))


if __name__ == '__main__':
    app.run(debug=True)
