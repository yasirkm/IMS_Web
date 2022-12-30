from django.shortcuts import render

# Create your views here.

def transaction_view(request):
    page_title = 'Transaction'
    context = {'title':page_title}
    return render(request, 'transaction.html', context)