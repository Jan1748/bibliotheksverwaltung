import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from LibraryManagement.models import Book, Material, Device, Container, TempLoan
from itertools import chain
from django.contrib.auth import authenticate


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('User', username, 'Logged in')
            # TODO Create Session
        else:
            print('Authentication failed for User:', username)
    return render(request, 'login.html', {})


@login_required
def borrow(request):
    id = request.GET.get('id')
    type = request.GET.get('type')  # Types: book, material, device, container
    loan = TempLoan(date_of_issue=datetime.timezone.now(), borrower=request.user)
    item = None
    if type == 'book':
        item = Book.objects.get(pk=id)
    elif type == 'material':
        item = Material.objects.get(pk=id)
    elif type == 'device':
        item = Device.objects.get(pk=id)
    elif type == 'container':
        item = Container.objects.get(pk=id)

    if item is not None:
        item.loan_object.add(loan)
        loan.save()
    return redirect('/overview/')


def overview(request):
    name_filter = {}
    name = request.GET.get('name_field')
    if name:
        name_filter['name'] = name

    book_filter = {}
    subject = request.GET.get('book_subject')
    if subject:
        book_filter['subject'] = subject

    device_filter = {}
    device_type = request.GET.get('type_of_device')
    if device_type:
        device_filter['device_type'] = device_type

    books = Book.objects.filter(**name_filter, **book_filter)
    materials = Material.objects.filter(**name_filter)
    devices = Device.objects.filter(**name_filter, **device_filter)
    containers = Container.objects.filter(**name_filter)

    context = {
        "books": books,
        "materials": materials,
        "devices": devices,
        "containers": containers
    }

    return render(request, 'overview.html', context)


def profile(request):
    return render(request, 'profile.html', {})
