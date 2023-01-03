from django.shortcuts import render
from django.contrib.auth.decorators import *


# Create your views here.
@login_required(login_url='login')
@permission_required('transaction.view_transaction')
def transaction_view(request):
    page_title = 'Transaction'
    context = {'title': page_title}
    return render(request, 'transaction.html', context)
