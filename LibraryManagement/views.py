from django.shortcuts import render


def login(request):
    return render(request, 'login.html', {})


def overview(request):
    return render(request, 'overview.html', {})


def profile(request):
    return render(request, 'profile.html', {})
