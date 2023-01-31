import requests

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth   
from django.contrib.auth.decorators import login_required

from .forms import RegisterationFrom, UserForm, UserProfileForm
from .models import Account

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.conf import settings

import uuid

from cart.views import _cart_id
from cart.models import Cart, CartItem
from orders.models import Order
from .models import UserProfile
from orders.models import OrderProduct

def register(request):
    if request.method == "POST":
        form = RegisterationFrom(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['Phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.Phone_number = phone_number
            # user.is_active = True
            user.save()
            
            
            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            # profile.profile_picture = 'default/default-user.png'
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            subject = 'Please activate your account'
            message = render_to_string('shop/accounts/email_activate/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()
    
            # messages.success(request, 'Check Gmail To Active Your Account')
            return redirect('/account/register/?command=verification&email='+email)

            
            # auth.login(request, user)
            # messages.success(request, 'You Loged in')
            # return redirect('accounts:dashboard')


    else : # request == GET
        form = RegisterationFrom()

    context = {
        'forms': form,
    }

    return render(request, 'shop/accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id 
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)

                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('accounts:dashboard')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Your email or password is wrong!')
            return redirect('accounts:login')
    return render(request, 'shop/accounts/login.html')


@login_required(login_url = 'accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You've successfully logged out . Come back soon!")
    return redirect('accounts:login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated, log in and let's go.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Invalid activation link, Try again!")
        return redirect('accounts:register')

@login_required(login_url = 'accounts:login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    profile = UserProfile.objects.get(user_id=request.user.id)
    
    orders_count = orders.count()
    context = {
        'orders_count':orders_count,
        'profile':profile,
        
    }
    return render(request, 'shop/accounts/dashboard/dashboard.html', context)



@login_required(login_url = 'accounts:login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()
    
    context = {
        'orders':orders,
        'orders_count':orders_count,
    }
    return render(request, 'shop/accounts/dashboard/my_orders.html', context)


@login_required(login_url = 'accounts:login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'shop/accounts/dashboard/edit_profile.html', context)


@login_required(login_url = 'accounts:login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        repeat_new_password = request.POST['repeat_new_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == repeat_new_password:
            success = user.check_password(old_password)
            if success :
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                messages.success(request, 'Password Updated successfully.')
                return redirect('accounts:change_password')
            else:
                messages.error(request, 'Old password is wrong')
                return redirect('accounts:change_password')
        else:
            messages.error(request, 'Password does not match')
            return redirect('accounts:change_password')
    return render(request, 'shop/accounts/dashboard/change_password.html')


@login_required(login_url = 'accounts:login')
def order_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)

    subtotal = 0
    for x in order_detail:
        subtotal += x.product_price * x.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'shop/accounts/dashboard/order_detail.html', context)


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # SEND EMAIL
            current_site = get_current_site(request)
            subject = 'Reset Your Password'
            message = render_to_string('shop/accounts/forget_password/send_resetpassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()

            # essages.success(request, "We sent a verification message to your email, click verify it, and let's start")
            
            
            return redirect('/account/forget_password/?command=resetpassword&email='+email)
        else: 
            messages.error(request, 'This email does not exist!')
            return redirect('accounts:forget_password')

    return render(request, 'shop/accounts/forget_password/forget_password.html') 


def resetpassword_validate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This is link has been expired !')
        return redirect('accounts:forget_password')



def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        repeat_password = request.POST['confirm_password']

        try:
            if password == repeat_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password Reset Successful')
                return redirect('accounts:login')
            else:
                messages.error(request, "Password does not match!")
                return redirect('accounts:reset_password')
        except Account.DoesNotExist:
            messages.error(request, "Please enter your email address here first! ")
            return redirect('accounts:forget_password')

    else:
        return render(request, 'shop/accounts/forget_password/reset_password.html')