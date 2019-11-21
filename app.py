from models.Order import Order
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
            return render_template('home.html', first_name=service.get_first_name(session['username']))
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
                return render_template('home.html', first_name=session['first_name'])
        else:
            username = request.form['username']
            password = request.form['password']
            login_flag = service.logging_in(username=username, password=password)
            if login_flag == 1:
                return render_template('index.html')
            elif login_flag == 3:
                return render_template('index.html')
            elif login_flag == 2:
                session['username'] = username
                session['first_name'] = service.get_first_name(session['username'])
                return render_template('home.html', first_name=session['first_name'])
            else:
                return render_template('index.html')
#
#
#
# B. Logout Method
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('first_name', None)
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
    return render_template('add_order.html',
                           order_id=service.seq_order_id(),
                           locality_list=service.get_locality_list()
                           )


@app.route('/adding_order', methods=['GET', 'POST'])
def adding_order():
    if request.form['loc_id'] == '1.0' or request.form['loc_id'] == '1':
        locality_id = service.add_new_locality(request.form['locality'])
        if locality_id == -1:
            flash("not Added")
            return render_template("home.html", first_name=session['first_name'])
    else:
        locality_id = request.form['loc_id']

    order = Order(
        order_id=request.form['order_id'],
        cust_name=request.form['cust_name'],
        phone_number=request.form['phone_number'],
        no_of_tiffin=request.form['no_of_tiffin'],
        street=request.form['street'],
        locality_id=locality_id,
        address_remarks=request.form['address_remarks'],
        order_remarks=request.form['order_remarks'],
        order_date=datetime.now(),
        status=1
    )
    if service.add_new_order(order.json()):
        flash("Successfully Added")
        return render_template("home.html", first_name=session['first_name'])
    else:
        flash("not Added")
        return render_template("home.html", first_name=session['first_name'])

# List Orders active
@app.route('/list_order_stat1', methods=['GET', 'POST'])
def list_order_stat1():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(1),
        header='List of all Active Orders'
    )

# List Orders Cancelled
@app.route('/list_order_stat2', methods=['GET', 'POST'])
def list_order_stat2():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(2),
        header='List of all orders with delivery guy'
    )

# List Orders Cancelled
@app.route('/list_order_stat3', methods=['GET', 'POST'])
def list_order_stat3():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(3),
        header='Tiffin received to customer and payment received to us'
    )

# List Orders Cancelled
@app.route('/list_order_stat4', methods=['GET', 'POST'])
def list_order_stat4():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(4),
        header='Tiffin received to customer and payment not received to us'
    )

# List Orders Cancelled
@app.route('/list_order_stat5', methods=['GET', 'POST'])
def list_order_stat5():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(5),
        header='Perfectly completed order'
    )

# List Orders Cancelled
@app.route('/list_order_stat6', methods=['GET', 'POST'])
def list_order_stat6():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(6),
        header='Faulty tiffin received by Vip Khana'
    )

# List Orders Cancelled
@app.route('/list_order_stat7', methods=['GET', 'POST'])
def list_order_stat7():
    return render_template(
        'list_order.html',
        first_name=session['first_name'],
        orders=service.list_orders_by_locality(7),
        header='Order cancelled by user'
    )


@app.route('/order_details', methods=['GET', 'POST'])
def list_order():
    order_id = int(request.form['order_id'])
    result = service.get_order_logs(order_id)
    print(*result)
    if result is None:
        flash("No such Order")
    else:
        return render_template(
            'order_details.html',
            first_name=session['first_name'],
            order_log=result,
            status_enum=status_enum
        )


if __name__ == '__main__':
    app.run(debug=True)
