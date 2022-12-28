from django.shortcuts import render

# Create your views here.

def transaction_view(request):
    return render(request, 'transaction.html')