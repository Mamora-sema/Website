from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

orders = [
    {"id": 1, "status": "В процессе", "item": "Бургер"},
    {"id": 2, "status": "Готов", "item": "Картофель фри"},
    {"id": 3, "status": "В процессе", "item": "Напиток"}
]

next_order_id = 4

@app.route('/')
def index():
    in_progress_orders = [order for order in orders if order["status"] == "В процессе"]
    ready_orders = [order for order in orders if order["status"] == "Готов"]
    return render_template('index.html', in_progress=in_progress_orders, ready=ready_orders)

@app.route('/update/<int:order_id>')
def update_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = "Готов"
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    global orders
    orders = [order for order in orders if order["id"] != order_id]
    return redirect(url_for('index'))

@app.route('/guest')
def guest_view():
    return render_template('guest.html')

@app.route('/api/orders')
def api_orders():
    in_progress_orders = [order["id"] for order in orders if order["status"] == "В процессе"]
    ready_orders = [order["id"] for order in orders if order["status"] == "Готов"]
    return jsonify({
        'in_progress': in_progress_orders,
        'ready': ready_orders
    })

@app.route('/new-order', methods=['GET', 'POST'])
def new_order():
    global next_order_id
    if request.method == 'POST':
        item = request.form['item']
        new_order = {"id": next_order_id, "status": "В процессе", "item": item}
        orders.append(new_order)
        next_order_id += 1
        return redirect(url_for('index'))
    return render_template('new_order.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
