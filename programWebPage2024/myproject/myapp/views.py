from django.shortcuts import render, redirect
from .forms import MaterialForm

def index(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            print("now it is valid")
            material = form.save(commit=False)
            # 在这里可以添加计算理论投料比的逻辑
            theoretical_ratio = calculate_theoretical_ratio(material.functionality, material.hydroxyl_value)
            # 假设我们直接将理论投料比保存到数据库
            material.theoretical_ratio = theoretical_ratio
            material.save()
    
            create_json_file(n, M, N1, N2)
            call_mu0529_mlog(json_file)
    
            return redirect('success')  # 假设你有一个成功页面
    else:
        form = MaterialForm()
    return render(request, 'myapp/create_job.html', {'form_abc': form})

def calculate_theoretical_ratio(functionality, hydroxyl_value):

    # 这里应该是你的特定公式
    # 例如：理论投料比 = functionality * hydroxyl_value
    return functionality * hydroxyl_value

def success(request):
    # 处理成功页面的逻辑
    return render(request, 'myapp/success.html')