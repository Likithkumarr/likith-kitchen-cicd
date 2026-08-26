from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Product

def menu(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, "menu.html", {"products": products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session['cart_count'] = sum(cart.values())
    request.session['msg'] = "Item added to cart!"
    return redirect('/menu/')

def cart_view(request):
    cart = request.session.get('cart', {})
    items, total = [], 0

    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=pid)
            p.qty = qty
            p.subtotal = p.price * qty
            total += p.subtotal
            items.append(p)
        except Product.DoesNotExist:
            continue

    request.session['cart_total'] = float(total)
    
    # Calculate discount
    discount_val = request.session.get('discount', 0)
    discount_amount = total * (discount_val / 100) if discount_val else 0
    final_total = total - discount_amount

    context = {
        'items': items, 
        'total': total,
        'discount_amount': discount_amount,
        'final_total': final_total
    }
    return render(request, 'cart.html', context)

def apply_coupon(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon', '').strip().upper()
        if coupon == "SAVE10":
            request.session['discount'] = 10
            request.session['msg'] = "Coupon SAVE10 applied! 10% off."
        else:
            request.session['discount'] = 0
            request.session['msg'] = "Invalid coupon code."
    return redirect('/cart/')

def toggle_theme(request):
    request.session['theme'] = 'dark' if request.session.get('theme') == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', '/menu/'))
