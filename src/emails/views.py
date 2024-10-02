from django.shortcuts import render

from . import services


# Create your views here.
def verify_email_token_view(request, token, *args, **kwargs):
    did_verify = services.verify_token(token)
