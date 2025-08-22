import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import ProductForm

API_BASE = "http://localhost:8000/api"

# --- Helper for auth headers ---
def get_headers(request):
    token = request.session.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

#-register page---
def register(request):
    if request.method == "POST":
        print(f"Request data: {request.POST}")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match"})

        payload = {
            "username": username,
            "email": email,
            "password": password1, 
            "password2": password2,  # depends on your API field name
        }

        response = requests.post(f"{API_BASE}/register/", json=payload)

        if response.status_code == 201:
            return redirect("login")  # redirect to login page after success
        else:
            return render(request, "register.html", {"error": response.json()})

    return render(request, "register.html")


#---Add product----

def create_product(request):

    try:
        print("Fetching categories from API...")
        cat_response = requests.get(API_BASE + "/categories/",headers=get_headers(request))

        if cat_response.status_code != 200:
            print(f"Failed to fetch categories. Status code: {cat_response.status_code}, Response: {cat_response.text}")
            messages.error(request, "Not authorized")
            categories = []
            category_choices = []
            return render(request, "create_product.html", {"form": None,messages:["Not authorized"]})  
        print(f"Categories API response status: {cat_response.status_code}, response: {cat_response.text}")
        categories = cat_response.json() 
        print(f"Categories fetched: {categories}")
        category_choices = [(c["id"], c["name"]) for c in categories]
    except Exception as e:
        categories = []
        category_choices = []
    
    if request.method == "POST":
        form = ProductForm(request.POST)
        form.fields["category"].choices = category_choices 

        if form.is_valid():
            data = form.cleaned_data
            payload = {
                "name": data["name"],
                "description": data["description"],
                "price": str(data["price"]),  # convert Decimal to string
                "Category": int(data["category"]),
            }
            response = requests.post(
                API_BASE + "/products/",
                json=payload,
                headers=get_headers(request)
            )

            if response.status_code == 201:
                messages.success(request, "Product created successfully!")
                return redirect("create_product")  # reload form page
            else:
                messages.error(request, f" Error: {response.json()}")
    else:
        form = ProductForm()
        form.fields["category"].choices = category_choices

    return render(request, "create_product.html", {"form": form})



# --- Login Page ---
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        response = requests.post(f"{API_BASE}/token/", data={"username": username, "password": password})

        if response.status_code == 200:
            tokens = response.json()
            request.session["access_token"] = tokens["access"]
            request.session["refresh_token"] = tokens["refresh"]
            return redirect("product_list")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")


# --- Product List Page ---
def product_list(request):
    response = requests.get(f"{API_BASE}/products/")
    products = response.json()
    return render(request, "products.html", {"products": products})


# --- Cart Page ---
def remove_from_cart(request):
    if request.method != "POST":
        return redirect("cart")
    else:
        item_id = int(request.POST.get("cart_id"))
        print(type(item_id))
        if not item_id:
            return render(request, "cart.html", {"error": "Item ID is required"})
        print(f"Request data: {request.POST}")
        print(f"Removing item {item_id} from cart")
        response = requests.delete(f"{API_BASE}/cart/item/{item_id}/remove", headers=get_headers(request))
        if response.status_code == 204:
            return redirect("cart")
        else:
            return render(request, "cart.html", {"error": "Failed to remove item from cart"})


def cart_view(request):
    response = requests.get(f"{API_BASE}/cart/", headers=get_headers(request))
    if response.status_code == 200:
        cart = response.json()
    else:
        cart = {"items": [], "total_price": 0}
    return render(request, "cart.html", {"cart": cart})

def add_to_cart(request):
    if request.method=="POST":
        product_id=request.POST.get("product_id")
        quantity=int(request.POST.get("quantity", 1))
        print(request.POST)
        response = requests.post(f"{API_BASE}/cart/add/", data={"product_id": product_id, "quantity": quantity}, headers=get_headers(request))
        print(f"Adding product {product_id} with quantity {quantity} to cart")
        print(response.status_code, response.json())
        if response.status_code in [200, 201]:
            print("Item added to cart successfully")
            return redirect("cart")
        else:
            return render(request, "cart.html", {"error": "Failed to add item to cart"})
        
def update_cart_item(request):
    print(f"Request method: {request.method}")
    if request.method == "POST":
        item_id = int(request.POST.get("cart_id"))
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity", 1))
        print(f"Request data: {request.POST}")
        print(f"Updating item {item_id} with product {product_id} and quantity {quantity}")
        print(f"Item ID: {item_id}, Quantity: {quantity}")
        print(f"Updating item {item_id} with quantity {quantity}")
        response = requests.put(f"{API_BASE}/cart/item/{item_id}/update/", json={"product_id":product_id,"quantity": quantity}, headers=get_headers(request))
        print(f"Response status code: {response.status_code}, Response data: {response.json()}")
        if response.status_code == 200:
            return redirect("cart")
        else:
            return render(request, "cart.html", {"error": "Failed to update cart item"})
        

def make_order(request):
    if request.method == "POST":
        
        response=requests.post(f"{API_BASE}/orders/", headers=get_headers(request))
        print(response.status_code, response.json())
        if response.status_code == 201:
            return redirect("orders")
        else:
            return render(request, "cart.html", {"error": "Failed to create order"})

# --- Orders list Page ---
def orders_view(request):
    response = requests.get(f"{API_BASE}/orders/", headers=get_headers(request))


    if response.status_code != 200:
        return render(request, "order.html", {"error": "Failed to fetch orders"})

    orders = response.json()
    print(orders)
    print(f"Fetching orders for user {request.user.username}")
    print("Response type:", type(orders))
    if orders:
        print(f"First order ID: {orders[0].get('id')}")

    return render(request, "order.html", {"orders": orders})

def make_payment(request):
    if request.method=="POST":
        order_id = request.POST.get("order_id")
        print(f"Making payment for order {order_id}")
        if not order_id:
            return render(request, "orders.html", {"error": "Order ID is required"})        
        print(f"Making payment for order {order_id}")
        print(f"Request data: {request.POST}")
        response=requests.put(f"{API_BASE}/orders/{order_id}/pay/", headers=get_headers(request), data={"status": "PAID"})
        if response.status_code == 200:
            messages.success(request, "Payment successful")
            return redirect("orders")
        else:
            return render(request, "orders.html", {"error": "Failed to update order status"})
    


# --- Logout ---
def logout_view(request):
    request.session.flush()
    return redirect("login")
