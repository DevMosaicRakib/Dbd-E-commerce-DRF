from django.urls import path
from .views import AllOrdersView,PlaceOrderView,AddCouponToCheckout,checkoutView,bkash_payment_callback
urlpatterns = [
    path('checkout/',checkoutView.as_view()),
    path('add-coupon-checkout/',AddCouponToCheckout.as_view()),
    path('allorders/',AllOrdersView.as_view()),
    path('place-order/',PlaceOrderView.as_view()),
    # path('bkash/payment/create/', bkash_payment_create, name='bkash_payment_create'),
    path('bkash/payment/callback/', bkash_payment_callback, name='bkash_payment_callback'),
]