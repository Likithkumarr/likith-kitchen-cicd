from django.shortcuts import render, redirect
from .models import Order, OrderItem
from restaurant.models import Product

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('/menu/')

    total = 0
    discount_val = request.session.get('discount', 0)

    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid)
            total += p.price * qty
        except Product.DoesNotExist:
            continue
            
    discount_amount = total * (discount_val / 100) if discount_val else 0
    final_total = total - discount_amount

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            total_amount=final_total
        )
        
        for pid, qty in cart.items():
            try:
                p = Product.objects.get(id=pid)
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    price=p.price,
                    quantity=qty
                )
            except Product.DoesNotExist:
                continue
                
        request.session['cart'] = {}
        request.session['cart_count'] = 0
        request.session['discount'] = 0
        request.session['msg'] = "Order placed successfully!"
        return redirect('/success/')

    return render(request, 'checkout.html', {'total': final_total})

def success(request):
    return render(request, 'success.html')

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = []
    return render(request, 'orders.html', {'orders': orders})
