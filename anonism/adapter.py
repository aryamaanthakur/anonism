from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render, redirect
class MyAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        if "iitism.ac.in" not in u.email.split('@')[1]:
            raise ImmediateHttpResponse(redirect('index'))