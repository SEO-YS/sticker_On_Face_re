from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests

@login_required(login_url='common:login')
def bat(requests):
    return render(requests,'stickers/sticker_edit_bat.html')

