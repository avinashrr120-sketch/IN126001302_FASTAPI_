from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class OrderRequest(BaseModel):
    customer_name:str = Field(..., min_length=2, max_length=100)
    product_id:int = Field(..., gt=0)
    quantity:int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

products = [
    {'id':1,'name':'Wireless Mouse','price':499,'category':'Electronics','in_stock':True},
    {'id':2,'name':'Notebook','price': 99,'category':'Stationery', 'in_stock':True},
    {'id':3,'name':'USB Hub','price':799,'category':'Electronics','in_stock':False},
    {'id':4,'name':'Pen Set','price': 49,'category':'Stationery', 'in_stock':True},
]
orders = []
order_counter = 1
# ══ HELPER FUNCTIONS ═══════════════════════════════════════
def find_product(product_id: int):
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_total(product: dict, quantity: int) -> int:
    return product['price'] * quantity

def filter_products_logic(category=None, min_price=None,
                          max_price=None, in_stock=None):
    result = products
    if category  is not None: result = [p for p in result if p['category']==category]
    if min_price is not None: result = [p for p in result if p['price']>=min_price]
    if max_price is not None: result = [p for p in result if p['price']<=max_price]
    if in_stock  is not None: result = [p for p in result if p['in_stock']==in_stock]
    return result

# ══ ENDPOINTS ════════════════════════════════════════════

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# NOTE: /filter, /compare, /summary must come BEFORE /{product_id}
@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description="Product category"),
    min_price: int = Query(None, description="Minimum price filter"),
    max_price: int = Query(None, description="Maximum price filter"),
    in_stock: bool = Query(None, description="Stock availability")
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {
        "filtered_products": result,
        "count": len(result)
    }

@app.get('/products/filter')
def filter_products(category:str=Query(None), min_price:int=Query(None),
                    max_price:int=Query(None), in_stock:bool=Query(None)):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}



@app.get('/products/compare')
def compare_products(product_id_1:int=Query(...), product_id_2:int=Query(...)):
    p1 = find_product(product_id_1)
    p2 = find_product(product_id_2)
    if not p1: return {'error': f'Product {product_id_1} not found'}
    if not p2: return {'error': f'Product {product_id_2} not found'}
    cheaper = p1 if p1['price'] < p2['price'] else p2
    return {'product_1':p1,'product_2':p2,
'better_value':cheaper['name'],
'price_diff':abs(p1['price']-p2['price'])}

@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {'error': 'Product not found'}
    return {'product': product}


@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter
    product = find_product(order_data.product_id)
    if not product:
        return {'error': 'Product not found'}
    if not product['in_stock']:
        return {'error': f"{product['name']} is out of stock"}
    total = calculate_total(product, order_data.quantity)
    order = {'order_id':order_counter,'customer_name':order_data.customer_name,
'product':product['name'],'quantity':order_data.quantity,
'delivery_address':order_data.delivery_address,
'total_price':total,'status':'confirmed'}
    orders.append(order)
    order_counter += 1

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
app = FastAPI()

# ══ PYDANTIC MODEL ════════════════════════════════════════════════

class OrderRequest(BaseModel):
    customer_name:str = Field(..., min_length=2, max_length=100)
    product_id:int = Field(..., gt=0)
    quantity:int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

 

# ══ DATA ══════════════════════════════════════════════════════════

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook','price':  99, 'category': 'Stationery',  'in_stock': True},
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True},

]

orders        = []
order_counter = 1

# ══ HELPER FUNCTIONS ══════════════════════════════════════════════

def find_product(product_id: int):
    """Search products list by ID. Returns product dict or None."""
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_total(product: dict, quantity: int) -> int:
    """Multiply price by quantity and return total."""
    return product['price'] * quantity

 

def filter_products_logic(category=None, min_price=None,
                          max_price=None, in_stock=None):
    """Apply filters and return matching products."""
    result = products
    if category  is not None:
        result = [p for p in result if p['category'] == category]
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock  is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return result


# ══ ENDPOINTS ═════════════════════════════════════════════════════

# ROUTE ORDER RULE:

#   Fixed routes  (/filter, /compare)  must come BEFORE

#   Variable route (/products/{product_id})

# ═════════════════════════════════════════════════════════════════

 

# ── Day 1 ─────────────────────────────────────────────────────────

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── Day 2: Query Parameters ────────────────────────────────────────

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    min_price: int  = Query(None, description='Minimum price'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only'),
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}

# ── Day 3: Compare (fixed route — must stay BEFORE /{product_id}) ─

@app.get('/products/compare')
def compare_products(
    product_id_1: int = Query(..., description='First product ID'),
    product_id_2: int = Query(..., description='Second product ID'),
):
    p1 = find_product(product_id_1)
    p2 = find_product(product_id_2)
    if not p1:
        return {'error': f'Product {product_id_1} not found'}
    if not p2:
        return {'error': f'Product {product_id_2} not found'}
    cheaper = p1 if p1['price'] < p2['price'] else p2
    return {
        'product_1':    p1,
        'product_2':    p2,
        'better_value': cheaper['name'],
        'price_diff':   abs(p1['price'] - p2['price']),
    }

# ── Day 1: Path Parameter (variable — always AFTER all fixed routes)

@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {'error': 'Product not found'}
    return {'product': product}

@app.get('/products/{product_id}/price')
def get_product_price(product_id: int):
    product = find_product(product_id)
    if not product:
        return {'error': 'Product not found'}
    
    return {
        'name': product['name'],
        'price': product['price']
    }
# ── Day 2: POST + Pydantic ─────────────────────────────────────────


@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter
    product = find_product(order_data.product_id)
    if not product:
        return {'error': 'Product not found'}
    if not product['in_stock']:
        return {'error': f"{product['name']} is out of stock"}
    total = calculate_total(product, order_data.quantity)
    order = {
        'order_id':         order_counter,
        'customer_name':    order_data.customer_name,
        'product':          product['name'],
        'quantity':         order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price':      total,
        'status':           'confirmed',
    }
    orders.append(order)
    order_counter = order_counter + 1
    return {'message': 'Order placed successfully', 'order': order}

@app.get('/orders')
def get_all_orders():
    return {'orders': orders, 'total_orders': len(orders)}
    return {'message':'Order placed successfully','order':order}

@app.get('/orders')
def get_all_orders():
    return {'orders': orders, 'total_orders': len(orders)}

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# ══ PYDANTIC MODELS ═══════════════════════════════════════════════

class OrderRequest(BaseModel):
    customer_name:str = Field(..., min_length=2, max_length=100)
    product_id:int = Field(..., gt=0)
    quantity:int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

# ══ DATA ══════════════════════════════════════════════════════════

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook','price':  99, 'category': 'Stationery',  'in_stock': True},
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True},
]

orders        = []
order_counter = 1
feedback      = []

# ══ HELPER FUNCTIONS ══════════════════════════════════════════════

def find_product(product_id: int):
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_total(product: dict, quantity: int) -> int:
    return product['price'] * quantity

def filter_products_logic(category=None, min_price=None, max_price=None, in_stock=None):
    result = products
    if category  is not None:
        result = [p for p in result if p['category'] == category]
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock  is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return result

# ══ ENDPOINTS ═════════════════════════════════════════════════════

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    min_price: int  = Query(None, description='Minimum price'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only'),
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}

@app.get('/products/compare')
def compare_products(
    product_id_1: int = Query(..., description='First product ID'),
    product_id_2: int = Query(..., description='Second product ID'),
):
    p1 = find_product(product_id_1)
    p2 = find_product(product_id_2)
    if not p1: return {'error': f'Product {product_id_1} not found'}
    if not p2: return {'error': f'Product {product_id_2} not found'}
    cheaper = p1 if p1['price'] < p2['price'] else p2
    return {
        'product_1':    p1,
        'product_2':    p2,
        'better_value': cheaper['name'],
        'price_diff':   abs(p1['price'] - p2['price']),
    }

@app.get('/products/summary')
def get_product_summary():
    in_stock_count = sum(1 for p in products if p['in_stock'])
    out_of_stock_count = len(products) - in_stock_count
    cheapest_prod = min(products, key=lambda p: p['price'])
    expensive_prod = max(products, key=lambda p: p['price'])
    unique_categories = list(set(p['category'] for p in products))
    return {
        "total_products": len(products),
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {"name": expensive_prod['name'], "price": expensive_prod['price']},
        "cheapest": {"name": cheapest_prod['name'], "price": cheapest_prod['price']},
        "categories": unique_categories
    }

@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    if not product: return {'error': 'Product not found'}
    return {'product': product}

@app.get('/products/{product_id}/price')
def get_product_price(product_id: int):
    product = find_product(product_id)
    if not product: return {'error': 'Product not found'}
    return {'name': product['name'], 'price': product['price']}

@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter
    product = find_product(order_data.product_id)
    if not product: return {'error': 'Product not found'}
    if not product['in_stock']: return {'error': f"{product['name']} is out of stock"}
    
    total = calculate_total(product, order_data.quantity)
    order = {
        'order_id':         order_counter,
        'customer_name':    order_data.customer_name,
        'product':          product['name'],
        'quantity':         order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price':      total,
        'status':           'confirmed',
    }
    orders.append(order)
    order_counter += 1
    return {'message': 'Order placed successfully', 'order': order}
def find_order(order_id: int):
    """Search the orders list by order_id."""
    for o in orders:
        if o['order_id'] == order_id:
            return o
    return None
@app.get('/orders')
def get_all_orders():
    return {'orders': orders, 'total_orders': len(orders)}

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)
class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_length=1) 

@app.post('/orders/bulk')
def place_bulk_order(bulk_data: BulkOrder):
    confirmed_items = []
    failed_items = []
    total_bill = 0
    for item in bulk_data.items:
        product = find_product(item.product_id)
        if not product:
            failed_items.append({
                "product_id": item.product_id, 
                "reason": "Product not found"
            })
            continue  
        if not product['in_stock']:
            failed_items.append({
                "product_id": item.product_id, 
                "reason": f"{product['name']} is out of stock"
            })
            continue 
        subtotal = calculate_total(product, item.quantity)
        total_bill += subtotal
        confirmed_items.append({
            "product": product['name'],
            "qty": item.quantity,
            "subtotal": subtotal
        })
    return {
        "company": bulk_data.company_name,
        "confirmed": confirmed_items,
        "failed": failed_items,
        "total_bill": total_bill
    }

@app.post('/feedback')
def submit_feedback(feedback_data: CustomerFeedback):
    feedback.append(feedback_data.model_dump()) 
    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback_data,
        "total_feedback": len(feedback)
    }