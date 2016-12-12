from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def profile(request):
    return render(request, 'biz_content/profile.html', {})


def dashboard(request):
    return render(request, 'biz_content/dashboard.html', {})
