import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from .models import Order,OrderItem
from EmailTemplate.SendEmailAllTypesFuction import payment_success_and_order_confirm_email,payment_failure_and_order_saved_email

class BkashPaymentService:
    def __init__(self):
        self.username = settings.BKASH_USERNAME
        self.password = settings.BKASH_PASSWORD
        self.app_key = settings.BKASH_APP_KEY
        self.app_secret = settings.BKASH_APP_SECRET
        self.base_url = settings.BKASH_BASE_URL
        self.token = None

    def get_token(self):
        url = f"{self.base_url}/tokenized/checkout/token/grant"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": self.username,
            "password": self.password,
        }
        data = {
            "app_key": self.app_key,
            "app_secret": self.app_secret,
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        self.token = response_data.get('id_token')
        return self.token

    def create_payment(self, amount):
        if not self.token:
            self.get_token()
        amount_str = f"{float(amount):.2f}"
        url = f"{self.base_url}/tokenized/checkout/create"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.token,
            "X-APP-Key": self.app_key,
        }
        data = {
            "mode": "0011",
            "payerReference": " ",
            "callbackURL": "http://127.0.0.1:8000/api/bkash/payment/callback/",
            "amount": amount_str,
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": 'Inv-1234'
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            return {"paymentID": None, "bkashURL": None}

        response_data = response.json()
        return {
            "paymentID": response_data.get("paymentID"),
            "bkashURL": response_data.get("bkashURL"),
        }

    def execute_payment(self, payment_id):
        if not self.token:
            self.get_token()
        url = f"{self.base_url}/tokenized/checkout/execute"
        headers = {
            "Accept": "application/json",
            "Authorization": self.token,
            "X-APP-Key": self.app_key,
        }
        data = {
            "paymentID": payment_id
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def call_back(self, status, payment_id):
        try:
            # Fetch the order associated with the payment_id
            order = Order.objects.get(payment_id=payment_id)
        except Order.DoesNotExist:
            # If the order doesn't exist, redirect to failure page
            return HttpResponseRedirect('http://localhost:3000/failure')

        if status in ['cancel', 'failure']:
            # Update the order status to 'Unpaid' if payment failed or was canceled
            order.payment_status = 'Unpaid'
            order.save()
            
            # Prepare data for redirection or other purposes
            data = {
                'paymentID': payment_id,
                'status': status,
            }
            order_items = OrderItem.objects.filter(order=order)
            order_item_names = ', '.join([item.product.name for item in order_items])
            
            total_order_amount = order.total_price
            payment_status = status
            order_status = order.payment_status
            user = order.user
            user_email = user.email
            username = user.username
            user_data = {
                'username':username,
                'order_items':order_item_names,
                'order_total':total_order_amount,
                'payment_status':payment_status,
                'order_status':order_status
            }
            payment_failure_and_order_saved_email(user_email,user_data)

            # Redirect to the failure page with the data as query parameters
            query_params = urlencode(data)
            failure_url = f"http://localhost:3000/failure?{query_params}"
            return HttpResponseRedirect(failure_url)

        elif status == 'success':
            # Execute payment and get payment details
            data = self.execute_payment(payment_id)
            print('Success data:', data)

            if data.get('statusCode') == '0000':
                # Update order payment status to 'Paid' if successful
                order.payment_status = 'Paid'
                order.paid_amount = data.get('amount')
                order.save()

                # Fetch related order items
                order_items = OrderItem.objects.filter(order=order)
                order_item_names = ', '.join([item.product.name for item in order_items])

                # Prepare user data for the email
                total_order_amount = order.total_price
                paid_amount = order.paid_amount
                payment_method = order.payment_method
                delivery_date = order.delivery_date
                user = order.user
                user_email = user.email
                username = user.username

                # Create a dictionary to pass user and order data to the email function
                user_data = {
                    'username': username,
                    'order_items': order_item_names,
                    'order_total': total_order_amount,
                    'paid_amount': paid_amount,
                    'payment_method': payment_method,
                    'delivery_date': delivery_date
                }

                # Send payment success and order confirmation email
                payment_success_and_order_confirm_email(user_email, user_data)

                # Redirect to the success page with payment details as query parameters
                query_params = urlencode(data)
                success_url = f"http://localhost:3000/success?{query_params}"
                return HttpResponseRedirect(success_url)
            else:
                # In case payment execution fails, redirect to failure page
                return HttpResponseRedirect('http://localhost:3000/failure')

