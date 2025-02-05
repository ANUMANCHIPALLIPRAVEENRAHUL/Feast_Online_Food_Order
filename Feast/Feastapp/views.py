from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Customer, FoodItem, DeliveryBoy, Order, Address
from django.utils import timezone

def home(request):
    food_items = FoodItem.objects.all()
    return render(request, 'home.html', {'food_items': food_items})

def customer(request):
    return render(request, 'customer.html')

def customer_signup(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('customer_email')
        password = request.POST.get('customer_password')
        number = request.POST.get('customer_number')
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
        else:
            customer = Customer(name=name, email=email, number=number)
            customer.set_password(password)
            customer.save()
            messages.success(request, 'Registration Successful!')
        return redirect('customer_signup')
    return render(request, 'customer.html')

def customer_signin(request):
    if request.method == 'POST':
        email = request.POST.get('customer_email')
        password = request.POST.get('customer_password')
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.name
                return redirect('customer_page')
            else:
                messages.error(request, 'Invalid email or password.')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please sign up first.')
        return redirect('customer_signin')
    return render(request, 'customer.html')

def customer_page(request):
    customer_name = request.session.get('customer_name', 'Guest')
    if not request.session.get('customer_id'):
        messages.error(request, 'Please login to order food.')
        return redirect('customer_signin')
    food_items = FoodItem.objects.all()
    customer_id = request.session.get('customer_id')
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer, delivery_boy__isnull=False)
    return render(request, 'customer_page.html', {'food_items': food_items, 'customer_name': customer_name, 'orders': orders})

def place_order(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'status': 'error', 'message': 'Please login to place an order.'})
        try:
            customer = get_object_or_404(Customer, id=customer_id)
            food_item_id = request.POST.get('food_item_id')
            door_no = request.POST.get('door_no')
            street = request.POST.get('street')
            area = request.POST.get('area')
            pincode = request.POST.get('pincode')
            address = Address.objects.create(
                customer=customer,
                door_no=door_no,
                street=street,
                area=area,
                pincode=pincode
            )
            food_item = get_object_or_404(FoodItem, id=food_item_id)
            order = Order.objects.create(
                customer=customer,
                food_item=food_item,
                address=address,
                status='Pending'
            )
            return JsonResponse({'status': 'success', 'message': 'Order confirmed!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def my_orders(request):
    if not request.session.get('customer_id'):
        messages.error(request, 'Please login to view your orders.')
        return redirect('customer_signin')
    customer_id = request.session.get('customer_id')
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer, delivery_boy__isnull=False)
    return render(request, 'customer_page.html', {'orders': orders})

def delivery(request):
    return render(request, 'delivery.html')

def delivery_boy_application(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        number = request.POST.get('number')
        if DeliveryBoy.objects.filter(user_id=user_id).exists():
            messages.error(request, 'User ID already exists!')
        else:
            delivery_boy = DeliveryBoy(full_name=full_name, user_id=user_id, number=number)
            delivery_boy.set_password(password)
            delivery_boy.save()
            messages.success(request, 'Application sent successfully!')
        return redirect('delivery')
    return render(request, 'delivery.html')

def delivery_boy_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        try:
            delivery_boy = DeliveryBoy.objects.get(user_id=user_id)
            if delivery_boy.status == 'accepted' and delivery_boy.check_password(password):
                request.session['delivery_boy_id'] = delivery_boy.id
                request.session['delivery_boy_name'] = delivery_boy.full_name
                return redirect('delivery_boy_page')
            else:
                messages.error(request, 'Invalid credentials or application not accepted.')
        except DeliveryBoy.DoesNotExist:
            messages.error(request, 'Invalid credentials or application not accepted.')
        return redirect('delivery_boy_login')
    return render(request, 'delivery.html')

def delivery_boy_page(request):
    if not request.session.get('delivery_boy_id'):
        messages.error(request, 'Please login as Delivery Boy.')
        return redirect('delivery_boy_login')
    delivery_boy_id = request.session.get('delivery_boy_id')
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    orders = Order.objects.filter(status='Pending')
    delivered_orders = Order.objects.filter(delivery_boy=delivery_boy, status='Delivered')
    return render(request, 'delivery_boy_page.html', {
        'orders': orders,
        'delivered_orders': delivered_orders,
        'delivery_boy_name': delivery_boy.full_name
    })

def accept_order(request, order_id):
    if not request.session.get('delivery_boy_id'):
        messages.error(request, 'Please login as Delivery Boy.')
        return redirect('delivery_boy_login')
    try:
        order = Order.objects.get(id=order_id)
        delivery_boy = DeliveryBoy.objects.get(id=request.session.get('delivery_boy_id'))
        order.delivery_boy = delivery_boy
        order.status = 'Delivered'
        order.accepted_time = timezone.now()
        order.save()
        messages.success(request, 'Order accepted successfully.')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
    except DeliveryBoy.DoesNotExist:
        messages.error(request, 'Delivery boy not found.')
    return redirect('delivery_boy_page')

def my_orders_delivered(request):
    if not request.session.get('delivery_boy_id'):
        messages.error(request, 'Please login as Delivery Boy.')
        return redirect('delivery_boy_login')
    delivery_boy_id = request.session.get('delivery_boy_id')
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    delivered_orders = Order.objects.filter(delivery_boy=delivery_boy, status='Delivered')
    return render(request, 'delivery_boy_page.html', {
        'delivered_orders': delivered_orders,
        'delivery_boy_name': delivery_boy.full_name
    })

def feast_page(request):
    if not request.session.get('feast_admin'):
        messages.error(request, 'Please login as Feast admin.')
        return redirect('feast_admin_login')
    
    # Fetch pending delivery requests
    delivery_boys = DeliveryBoy.objects.filter(status='not_accepted')
    
    # Fetch accepted delivery boys
    accepted_delivery_boys = DeliveryBoy.objects.filter(status='accepted')
    
    # Fetch all orders
    orders = Order.objects.all().order_by('-order_date')
    
    return render(request, 'feast_page.html', {
        'delivery_boys': delivery_boys,
        'accepted_delivery_boys': accepted_delivery_boys,
        'orders': orders,
    })

def feast_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'feastgod' and password == 'feast@123':
            request.session['feast_admin'] = True
            return redirect('feast_page')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'feast.html')

def accept_delivery_boy(request, delivery_boy_id):
    if not request.session.get('feast_admin'):
        messages.error(request, 'Please login as Feast admin.')
        return redirect('feast_admin_login')
    
    try:
        # Fetch the delivery boy
        delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
        
        # Update the delivery boy's status to 'accepted'
        delivery_boy.status = 'accepted'
        delivery_boy.save()
        
        # Display a success message
        messages.success(request, 'Delivery Boy Accepted Successfully.')
    except DeliveryBoy.DoesNotExist:
        messages.error(request, 'Delivery boy not found.')
    
    # Redirect back to the feast page
    return redirect('feast_page')

def about_us(request):
    return render(request, 'about_us.html')

def logout(request):
    request.session.flush()
    return redirect('home')

def customer_success(request):
    if not request.session.get('customer_id'):
        messages.error(request, 'Please login to view your orders.')
        return redirect('customer_signin')
    return redirect('customer_page')
    