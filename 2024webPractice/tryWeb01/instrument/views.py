from django.shortcuts import render, redirect
from .forms import InstrumentForm

def add_instrument(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # 重定向到首页或其他页面
    else:
        form = InstrumentForm()
    return render(request, 'instrument/add_instrument.html', {'form': form})