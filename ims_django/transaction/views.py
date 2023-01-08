from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from django.forms import ValidationError

from employee.models import Employee

from .forms import *


# Create your views here.
@login_required(login_url='login')
@permission_required('transaction.view_transaction_history', raise_exception=True)
def transaction_view(request):
    detail_template_form = Add_Transaction_Detail_Form()
    page_title = 'Transaction'
    transaction_history = Transaction.get_transaction_history()
    if request.method=='GET':
        transaction_form = Add_Transaction_Form()
        transaction_detail_form = Add_Transaction_Detail_Form()
        context = {'title': page_title, 'detail_template_form':detail_template_form,
                'transaction_form':transaction_form, 'transaction_detail_forms':[transaction_detail_form,],
                'transaction_history':transaction_history}
        return render(request, 'transaction.html', context)

    elif request.method=='POST':
        transaction_form = Add_Transaction_Form(request.POST)
        transaction_detail_form = Add_Transaction_Detail_Form()
        transaction_details_data = {field:request.POST.getlist(field) for field in transaction_detail_form.fields}
        print(transaction_details_data)
        
        employee = request.user
        if transaction_form.is_valid():
            try:
                print('transaction valid')
                new_transaction = transaction_form.save(commit=False)
                new_transaction.employee_id = employee
                time_zone = datetime.now().astimezone().tzinfo
                new_transaction.date_time = datetime.now(time_zone)

                new_transaction_details=[]
                detail_form_has_error = False
                transaction_detail_forms = []
                for values in zip(*transaction_details_data.values()):
                    data = {field:value for field, value in zip(transaction_details_data.keys(), values)}
                    print(data)
                    transaction_detail_form = Add_Transaction_Detail_Form(data)
                    transaction_detail_forms.append(transaction_detail_form)
                    new_transaction_detail=transaction_detail_form.save(commit=False)
                    if not transaction_detail_form.is_valid() or new_transaction.type=='OUT' and new_transaction_detail.product_id.stock - new_transaction_detail.quantity < 0:
                        detail_form_has_error = True
                    else:
                        new_transaction_details.append(new_transaction_detail)

                if detail_form_has_error:
                    raise ValidationError('invalid transaction detail')
                new_transaction.save()
                for new_transaction_detail in new_transaction_details:
                    new_transaction_detail.transaction_id = new_transaction
                    product = new_transaction_detail.product_id
                    new_transaction_detail.price_at_transaction = product.price
                    if new_transaction.type == 'OUT':
                        product.stock -= new_transaction_detail.quantity
                    else:
                        product.stock += new_transaction_detail.quantity
                    product.save()
                    new_transaction_detail.save()
            except ValidationError:
                print(transaction_detail_form.errors)
                print(transaction_detail_form.non_field_errors())
                context = {'title': page_title, 'detail_template_form':detail_template_form,
                'transaction_form':transaction_form, 'transaction_detail_forms':transaction_detail_forms,
                'transaction_history':transaction_history}
                return render(request, 'transaction.html', context)
        return redirect('transaction')