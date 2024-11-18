from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic
from .models import *

# Home Page
class HomeView(generic.TemplateView):
    template_name = 'home.html'
    
# Users Page
class DetailUserView(generic.DetailView):
    model = User
    template_name = "user/detail_user.html" 

#Clients Page
class ClientListView(generic.ListView):
    model = Client
    context_object_name = "clients"
    template_name = "client/client_list.html"

class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'client/client_detail.html'
    context_object_name = 'client'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = Loan.objects.filter(client=self.object)
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = Loan.objects.filter(client=self.object)
        context['transactions'] = Transaction.objects.filter(client=self.object).order_by('-transaction_date')
        return context

class UpdateClientView(generic.UpdateView):
    model = Client
    fields = "__all__"
    template_name = "client/client_form.html"
    success_url = reverse_lazy('Base-Page')


class DeleteClientView(generic.DeleteView):
    model = Client
    template_name = 'client/conf_del_client.html'
    success_url = reverse_lazy('Client-List')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.get_object()
        return context


class CreateClientView(generic.CreateView):
    model = Client
    fields = "__all__"
    template_name = "client/client_form.html"
    success_url = reverse_lazy('Base-Page')
  
# Loans 

# class LoanCreateView(generic.CreateView):
#     model = Loan 
#     fields = "__all__"  
#     template_name = "loan/loan_form.html"
#     success_url = reverse_lazy("Base-Page")  

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)  
#         context['loans'] = Loan.objects.all() 
#         context['clients'] = Client.objects.all()  
#         return context

#     def form_valid(self, form):
#         if client.balance + loan.amount > 100000: 
#             form.add_error('amount', 'Сумма займа превышает допустимый лимит.')
#             return self.form_invalid(form)
#         loan = form.save(commit=False)
#         client = loan.client
#         client.balance += loan.amount
#         client.save()
#         loan.save()
#         return super().form_valid(form)


# Transaction 

class CreateTransactionView(generic.CreateView):
    model = Transaction
    fields = ["transaction_type", "amount"] 
    template_name = "transaction/transaction_form.html"
    success_url = reverse_lazy('Client-List')  

    def form_valid(self, form):
        transaction = form.save(commit=False)
        client_id = self.kwargs.get('client_id')
        transaction.client = Client.objects.get(id=client_id)

        client = transaction.client
        if transaction.transaction_type == Transaction.LOAN_TYPE:
            client.balance += transaction.amount
            transaction_type_text = "Loan received"
        elif transaction.transaction_type == Transaction.REPAYMENT_TYPE:
            if client.balance >= transaction.amount:
                client.balance -= transaction.amount
                transaction_type_text = "Repayment made"
            else:
                form.add_error(None, "Insufficient balance for repayment.")
                return self.form_invalid(form)

        client.save()
        transaction.save()

        subject = 'Transaction Notification'
        message = (
            f"Hello {client.first_name},\n\n"
            f"{transaction_type_text}: {transaction.amount}.\n"
            f"Your new balance is: {client.balance}.\n\n"
            "Thank you for using our services!"
            "Application made by Khusainov Abubakr!"
        )
        recipient_list = [client.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(id=self.kwargs.get('client_id'))
        return context



    
       