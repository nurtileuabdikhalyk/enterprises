from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, ProductForm, PlatejForm, NotesForm, SignInForm, SignUpForm, OrderForm, CourierForm
from .models import *
from io import BytesIO as IO
import pandas as pd


def index(request):
    feedbacks = Feedback.objects.order_by('-created')
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form = contact_form.save(commit=False)
            contact_form.save()
            return redirect('home')
    contact_form = ContactForm()
    context = {
        "title": "Басты бет",
        'contact_form': contact_form,
        "feedbacks": feedbacks
    }
    return render(request, 'firstapp/index.html', context)


# admin
# imangali
def excel_products(request):
    products = Product.objects.filter(organization=request.user)
    product_name = []
    product_place = []
    product_price = []
    product_count = []
    product_total = []
    total = 0
    total_price = 0
    total_count = 0
    for product in products:
        product_name.append(product.name)
        product_place.append(product.place)
        product_price.append(product.price)
        product_count.append(product.count)
        product_total.append(product.total)
        total_price += product.price
        total_count += product.count
        total += product.total
    product_name.append('Барлығы')
    product_place.append('')
    product_price.append(total_price)
    product_count.append(total_count)
    product_total.append(total)
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_output = pd.DataFrame(
        {'Тауар аты': product_name, 'Орналасқан орны': product_place, 'Бағасы': product_price,
         'Саны': product_count, 'Жалпы құны': product_total})
    df_output.to_excel(xlwriter, 'sheetname')

    xlwriter.close()

    excel_file.seek(0)
    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report_products.xlsx'

    return response


def excel_sales(request):
    total_sum = 0
    total_ndc = 0
    total_profit = 0

    platej = Platej.objects.filter(organization=request.user)
    dogovor = []
    products = []
    oplata = []
    address = []
    sum = []
    ndc = []
    profit = []
    status = []
    for p in platej:
        dogovor.append(p.dogovor)
        products.append(p.product)
        oplata.append(p.oplata)
        address.append(p.address)
        sum.append(p.sum)
        ndc.append(p.ndc)
        profit.append(p.profit)
        status.append(p.status)

        total_sum += p.sum
        total_ndc += p.ndc
        total_profit += p.profit
    excel_file = IO()
    dogovor.append('Барлығы')
    products.append('')
    oplata.append('')
    address.append('')
    sum.append(total_sum)
    ndc.append(total_ndc)
    profit.append(total_profit)
    status.append('')
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_output = pd.DataFrame(
        {'Келісім-шарт': dogovor, 'Тауар': products, 'Төлем түрі': oplata,
         'Мекен-жай': address, 'Сумма': sum, 'НДС': ndc, 'Табыс': profit, 'Статус': status}, )
    df_output.to_excel(xlwriter, 'sheetname')
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedxocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=report_sales.xlsx'
    return response


def products(request):
    products = Product.objects.filter(organization=request.user)
    if request.method == 'POST':
        form = ProductForm(request.user, request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('products')
    form = ProductForm(request.user)
    total = 0
    total_price = 0
    total_count = 0
    for p in products:
        total_price += p.price
        total_count += p.count
        total += p.total
    context = {
        "title": "Тауарлар",
        "products": products,
        "form": form,
        "total_count": total_count,
        "total_price": total_price,
        "total": total,
    }
    return render(request, 'firstapp/products.html', context)


def graphics(request):
    products = Product.objects.filter(organization=request.user)
    platej = Platej.objects.filter(organization=request.user)

    platej_sum = []
    for p in platej:
        platej_sum.append(int(p.sum))
    context = {
        'title': 'Есептер',
        'products': products,
        'platej': platej,
        'platej_sum': platej_sum,
    }
    return render(request, 'firstapp/chart.html', context)


def sales(request):
    error = ''
    platej = Platej.objects.filter(organization=request.user)
    total_sum = 0
    total_ndc = 0
    total_profit = 0

    for p in platej:
        total_sum += p.sum
        total_ndc += p.ndc
        total_profit += p.profit
    if request.method == 'POST':
        form = PlatejForm(request.user, request.POST)
        if form.is_valid():
            p = request.POST['product']
            product = get_object_or_404(Product, id=int(p))
            c = int(request.POST['count'])
            s = int(request.POST['sum'])
            if product.count < c or product.price > s:
                form = PlatejForm(request.user)
                error = 'Қате орын алды!'
                context = {
                    "title": "Сатылымдар",
                    "platej": platej,
                    "form": form,
                    'total_sum': total_sum,
                    'total_ndc': total_ndc,
                    'total_profit': total_profit,
                    'error': error,
                }
                return render(request, 'firstapp/sales.html', context)
            else:
                product.count = product.count - c
            product.save()
            form = form.save(commit=False)
            form.save()
            return redirect('sales')

    form = PlatejForm(request.user)

    context = {
        "title": "Сатылымдар",
        "platej": platej,
        "form": form,
        'total_sum': total_sum,
        'total_ndc': total_ndc,
        'total_profit': total_profit,
        'error': error,
    }
    return render(request, 'firstapp/sales.html', context)


def signin(request):
    messages = ""
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['login']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            try:
                login(request, user)
            except:
                messages = "Логин/пароль қате!"
                context = {
                    'title': 'Кіру',
                    'form': form,

                    "messages": messages
                }
                return render(request, 'account/login.html', context)
            return redirect('home')
        else:
            messages = "Логин/пароль қате!"
    else:
        form = SignInForm()
    context = {
        'title': 'Кіру',
        'form': form,

        "messages": messages
    }
    return render(request, 'account/login.html', context)


def signup(request):
    messages = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
        else:
            messages = "Форма қате толтырылды!"

    else:
        form = SignUpForm()
    context = {
        'title': 'Тіркелу',
        'form': form,
        "messages": messages
    }
    return render(request, 'account/signup.html', context)


def notes(request):
    notes = Notes.objects.filter(organization=request.user).order_by('-created')
    if request.method == 'POST':
        form = NotesForm(request.user, request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('notes')
    form = NotesForm(request.user)
    context = {
        "title": "Ескертпелер",
        "notes": notes,
        "form": form
    }
    return render(request, 'firstapp/notes.html', context)


def orders(request):
    orders = Order.objects.filter(organization=request.user).order_by('-data')
    if request.method == 'POST':
        form = OrderForm(request.user, request.POST)
        if form.is_valid():
            form = form.save(commit=True)
            form.save()
            return redirect('orders')
    form = OrderForm(request.user)

    context = {
        'title': 'Тапсырыстар',
        'orders': orders,
        'form': form,
    }
    return render(request, 'firstapp/orders.html', context)


def delete(request, id):
    question = Product.objects.get(id=id)
    question.delete()
    return redirect('products')


def delete_courier(request, id):
    question = Courier.objects.get(id=id)
    question.delete()
    return redirect('courier')


def courier(request):
    couriers = Courier.objects.filter(organization=request.user)
    if request.method == 'POST':
        form = CourierForm(request.user, request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('courier')
    form = CourierForm(request.user)
    context = {'form': form, 'couriers': couriers}
    return render(request, 'firstapp/couriers.html', context)
