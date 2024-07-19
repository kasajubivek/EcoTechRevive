from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Device, UserProfile, Product, Cart, CartItem, Order, OrderItem, EnquiryModel
from .forms import LoginForm, RegisterForm, UploadFileForm, UserHistoryForm, EditProfileForm, PasswordResetForm, \
    SetNewPasswordForm, ProductForm, ContactForm, EnquiryForm
from django.contrib.auth import update_session_auth_hash


def index(request):
    return render(request, 'main/index.html')


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the file upload
            form.save()
            return redirect('index')
    else:
        form = UploadFileForm()
    page_view(request, 'Upload File')
    return render(request, 'main/upload.html', {'form': form})


class DeviceListView(ListView):
    model = Device
    template_name = 'main/device_list.html'
    context_object_name = 'devices'


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'main/device_detail.html'


# Login functionality for the user
# It uses he User model provided by Django framework
# and makes sure to display an error in case of
# invalid username and/or password.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not username or not password:
                messages.error(request, 'Invalid username or password.')
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    Cart.objects.get_or_create(user=user)
                    login(request, user)

                    fav_color = request.session.get('fav_color', 'red')
                    request.session.modified = True
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'main/user_login.html', {'form': form})


# Processing the logout request
# making sure to clear the session.
@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')  # redirect to login page or any other page you prefer


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Create UserProfile instance
            UserProfile.objects.create(
                user=user,
                security_question_1=form.cleaned_data['security_question_1'],
                security_answer_1=form.cleaned_data['security_answer_1'],
                security_question_2=form.cleaned_data['security_question_2'],
                security_answer_2=form.cleaned_data['security_answer_2'],
                security_question_3=form.cleaned_data['security_question_3'],
                security_answer_3=form.cleaned_data['security_answer_3']
            )

            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form. Please correct the errors.')
    else:
        form = RegisterForm()
    return render(request, 'main/user_register.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'main/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'main/edit_profile.html', {'form': form})


@login_required
# def user_history(request):
#     if request.method == 'POST':
#         form = UserHistoryForm(request.POST)
#         if form.is_valid():
#             # Process the user session data
#             pass
#     else:
#         form = UserHistoryForm()
#     return render(request, 'main/user_history.html', {'form': form})

# def search_results(request):
#     query = request.GET.get('q')
#     # Perform search based on query
#     results = []
#     page_view(request, 'Search')
#     return render(request, 'main/search_results.html', {'results': results})
#

def contact_us(request):
    page_view(request, 'Contact Us')
    return render(request, 'main/contact_us.html')


def about_us(request):
    page_view(request, 'About Us')
    return render(request, 'main/about_us.html')


def team_details(request):
    page_view(request, 'Team Details')
    return render(request, 'main/team_details.html')


def password_reset_security_question(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            security_answer_1 = form.cleaned_data['security_answer_1']
            security_answer_2 = form.cleaned_data['security_answer_2']
            security_answer_3 = form.cleaned_data['security_answer_3']
            try:
                user = User.objects.get(username=username)
                profile = UserProfile.objects.get(user=user)
                if (profile.security_answer_1 == security_answer_1 and
                        profile.security_answer_2 == security_answer_2 and
                        profile.security_answer_3 == security_answer_3):
                    request.session['reset_user_id'] = user.id
                    return redirect('password_reset_new_password')
                else:
                    form.add_error(None, 'Security answers do not match.')
            except User.DoesNotExist:
                form.add_error('username', 'User does not exist.')
            except UserProfile.DoesNotExist:
                form.add_error('username', 'User profile does not exist.')
    else:
        form = PasswordResetForm()

    return render(request, 'main/password_reset_security_question.html', {'form': form})


def set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')
            if user_id:
                user = get_object_or_404(User, id=user_id)
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password reset successfully. Please log in with your new password.')
                return redirect('login')
            else:
                form.add_error(None, 'Session expired. Please start the password reset process again.')
    else:
        form = SetNewPasswordForm()

    return render(request, 'main/set_new_password.html', {'form': form})


def page_view(request, page):
    page_counts = request.session.get('page_counts', {})
    page_counts[page] = page_counts.get(page, 0) + 1
    request.session['page_counts'] = page_counts
    recently_viewed(request, page)


def recently_viewed(request, page):
    if 'recently_viewed' not in request.session:
        request.session['recently_viewed'] = []

    if page in request.session['recently_viewed']:
        request.session['recently_viewed'].remove(page)

    request.session['recently_viewed'].insert(0, page)

    if len(request.session['recently_viewed']) > 3:
        request.session['recently_viewed'].pop()

    request.session.modified = True


def history(request):
    page_counts = request.session.get('page_counts', {})
    page_visits = [{'page_name': page_name, 'visit_count': count} for page_name, count in page_counts.items()]

    page_visits_sorted = sorted(page_visits, key=lambda x: x['visit_count'], reverse=True)
    recently_viewed = request.session.get('recently_viewed', {})

    return render(request, 'main/history.html', {'page_visits': page_visits_sorted, 'recently_viewed': recently_viewed})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your feedback. We will contact you soon.')
            return redirect('index')  # Redirect to the home page
    else:
        form = ContactForm()
    return render(request, 'main/contact_us.html', {'form': form})


def contact_success(request):
    return redirect('index')


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.uploaded_by = request.user
            product.save()
            return redirect('index')
    else:
        form = ProductForm()
    page_view(request, 'Add Product')
    return render(request, 'main/add_product.html', {'form': form})


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form': sub})


def index(request):
    products = Product.objects.all()  # Fetch all products from the database
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Handle form submission (e.g., send email)
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('index')  # Redirect to index or another page
    else:
        form = ContactForm()

    return render(request, 'main/index.html', {'form': form, 'products': products})


# @login_required
# def add_to_cart_view(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     # Logic to add the product to the cart
#     messages.info(request, f'{product.name} added to cart successfully!')
#     return redirect('index')
#
#
# @login_required
# def add_to_cart(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart.products.add(product)
#     messages.success(request, 'Product added to cart successfully!')
#     return redirect('index')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would handle the form data, e.g., send an email
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('index')  # Redirect to index or wherever you prefer
    else:
        form = ContactForm()

    return render(request, 'main/contact_us.html', {'form': form})


def shop(request):
    if request.user.is_authenticated:
        products = Product.objects.exclude(uploaded_by=request.user)

    else:
        products = Product.objects.all()
    title = 'Explore Our Products'
    return render(request, 'main/shop.html', {'products': products, 'title': title})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('shop')


@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    page_view(request, 'View Cart')
    return render(request, 'main/cart_detail.html', {'cart_items': cart_items})


@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')


@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart_detail')


@login_required
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    cart_items.delete()

    return redirect('order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'main/order_detail.html', {'order': order, 'order_items': order_items})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    page_view(request, 'View Orders')
    return render(request, 'main/order_list.html', {'orders': orders})


def EnquiryRequest(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You request has been submitted successfully.')
            return redirect('index')
    else:
        form = EnquiryForm()
    return render(request, 'main/enquiry_request.html', {'form': form})


@login_required
def search_products(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
        title = 'Search Results'
    else:
        products = Product.objects.all()
        title = 'No results found. Explore our Products'
    return render(request, 'main/shop.html', {'products': products, 'title': title})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'main/product_detail.html', {'product': product})
