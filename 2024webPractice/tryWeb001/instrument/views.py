from django.shortcuts import render, redirect
from .forms import InstrumentForm

def submit_instrument(request):
    if request.method == 'POST':
        form = InstrumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_view')  # 重定向到成功页面
    else:
        form = InstrumentForm()
    return render(request, 'instrument/submit_instrument.html', {'form': form})