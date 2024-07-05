# 为了更好的管理代码，我们将视图函数放在这个文件中， 并定义/赋值/计算了一些辅助函数

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Job, Chemical_A
from .forms import JobForm, Chemical_AForm, Chemical_AFormSet
import json
from pathlib import Path
import subprocess
import os
from .models import Job
from django.http import HttpResponse
from loguru import logger
import markdown

# 四种运行状态
status_dict = {
    "R": "正在运行",
    "PD": "正在排队",
    "CG": "即将完成",
    "CD": "已完成",
}

# 此处影响 任务列表 ｜ 为任务列表添加了 搜索，翻页 功能
def job_list(request):
    search_query = request.GET.get("search", "")  # Capture the search query
    if search_query:
        # Filter jobs based on the search query
        jobs_list = Job.objects.filter(
            name__icontains=search_query
        )  # Adjust the filter based on your needs
    else:
        jobs_list = Job.objects.all()  # 获取所有 jobs

    paginator = Paginator(jobs_list, 10)  # 每页10个 jobs

    page_number = request.GET.get("page")  # 从请求中获取页码
    page_obj = paginator.get_page(page_number)  # 获取当前页码的 jobs

    # Include the search query in the context so it can be reused in the template
    return render(
        request, "job_list.html", {"page_obj": page_obj, "search_query": search_query}
    )


# 删除任务
def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, pk=job_id)
        # Optional: Check if the current user is allowed to delete this job
        # if request.user != job.owner:
        #     return HttpResponseForbidden('You are not allowed to delete this job.')
        job.delete()
        # Redirect to the job list page with a success message
        return redirect('job_list')
    else:
        # If the request method is not POST, return an error (405 Method Not Allowed)
        return HttpResponseNotAllowed(['POST'])


# 计算 
def calcualte_N(job: Job, chemical_A: Chemical_A, total_shares_A) -> int:
    return round(float(job.chemial_A_mass)
        * (chemical_A.shares / total_shares_A)
        / chemical_A.molecular_mass)

# 计算
def calculate_parameter(job: Job, chemical_As: list):
    total_shares_A = sum([chemical_A.shares for chemical_A in chemical_As])
    total_hydroxyl_A = float(
        sum([chemical_A.hydroxyl * chemical_A.shares for chemical_A in chemical_As])
    )
    # 计算 理论投料比(B/A）
    job.theory_shares_ratio = (
        4202.0 / (float(job.chemical_B_NCO) * total_shares_A) * total_hydroxyl_A / 56100
    )
    job.save()

    parameters = {"job_id": job.id, "job_name": job.name}
    parameters["Temperature"] = job.temperature
    parameters["N0"] = round(job.chemical_B_mass / job.chemical_B_molecular_mass)
    parameter_mapping = {
        "PTMG1000": "N1",
        "PTMG2000": "N2",
        "330N": "N3",
        "BDO": "N4",
        "water": "N5",
    }
    for chemical_A in chemical_As:
        for key, value in parameter_mapping.items():
            if key in chemical_A.name:
                parameters[value] = calcualte_N(job, chemical_A, total_shares_A)
    # 为N0-N5赋值, 若没有则为0，然后保存
    job.N0 = parameters.get("N0", 0) 
    job.N1 = parameters.get("N1", 0)
    job.N2 = parameters.get("N2", 0)
    job.N3 = parameters.get("N3", 0)
    job.N4 = parameters.get("N4", 0)
    job.N5 = parameters.get("N5", 0)
    job.save()

    # dump the parameters to a json file
    tool_path = Path.cwd()/ "tools"
    assert (
        tool_path.exists()
    ), f"{tool_path} does not exist, the test.sh, *.molg and py should be in this folder"
    parameter_file = tool_path / "config.json"
    print(f"parameter file: {parameter_file}")

    # write parameter to parameter file
    with parameter_file.open("w") as f:
        json.dump(parameters, f)

    # 如果不是本地运行，则提交任务
    if os.environ.get("LOCAL_RUN", "False") == "True":
        output = "Submitted batch job 34880"
    else:        
        completed_process = subprocess.run(
            [
                "sbatch",
                tool_path.joinpath("test.sh").as_posix(),
            ],
            cwd=tool_path.as_posix(),
            text=True,
            capture_output=True,
        )        
        output = completed_process.stdout
        print(f"Return code: {completed_process.returncode}")
        print(f"Output: {output}")

    # Search job_id
    job.sbatch_job_id = find_sbatch_job_id(output)
    job.status = status_dict.get("R", "正在运行")
    job.save()

# 寻找 sbatch job id
def find_sbatch_job_id(input_str: str):
    text_before_id = "Submitted batch job "
    start_index = input_str.find(text_before_id) + len(text_before_id)
    sbatch_id = input_str[start_index:].strip()
    return sbatch_id

# 为job_view 准备数据
def job_view(request, pk):
    job = Job.objects.get(pk=pk)
    if request.method == "POST":
        job.description = request.POST.get("description")
        job.save()
        return HttpResponse("Success", content_type="text/plain", status=200)

    # 图片路径/传递给前端
    wip_path = "wip.jpg"
    img1_path = f"{job.id}/all_variables.png"
    img2_path = f"{job.id}/rcluster.png"
    markdown_path = Path.cwd().joinpath(f"tools/{job.id}/clusters_info.md")
    markdown_content = ""
    if Path.cwd().joinpath(f"tools/{img1_path}").exists():
        if job.status != status_dict.get("CD", "已完成"):
            job.status = status_dict.get("CD", "已完成")
            job.save
        snd_img_path = img2_path if Path.cwd().joinpath(f"tools/{img2_path}").exists() else wip_path
        logger.info(f"snd_img_path:{snd_img_path}, image_path:{img2_path}")

        if markdown_path.exists():
            with markdown_path.open() as f:
                markdown_content = markdown.markdown(f.read(),extensions=['tables'])
                    
        return render(request, "job_view.html", {"job": job, 
                                                 "img1_name": img1_path, 
                                                 "img2_name": snd_img_path,
                                                 "markdown_content": markdown_content})

    #    $ squeue  --job 34880
    output = """JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
                34880  gpu-4080     test yuerongx  CG       0:12      1 MW06"""
    return_code = 0

    if os.environ.get("LOCAL_RUN", "False") == "False":
        completed_process = subprocess.run(
            [
                "squeue",
                "--job",
                str(job.sbatch_job_id),
            ],
            text=True,
            capture_output=True,
        )
        output = completed_process.stdout
        return_code = completed_process.returncode
        print(f"Return code: {completed_process.returncode}")
    print(f"Output: {output}")

    # $ squeue  --job 35671
    # slurm_load_jobs error: Invalid job id specified
    if return_code != 0:  # job is finished
        job.status = status_dict.get("CD", "已完成")
    else:
        line = output.split("\n")[1] 
        logger.info(f"job_id is:{job.sbatch_job_id} , line is {line}")
        if str(job.sbatch_job_id) in line:
            job.status = status_dict.get(line.split()[4], "未知状态")
            job.save()
        else:
            logger.error(f"job id {job.sbatch_job_id} is not in the output: {output}")

    
    return render(request, "job_view.html", {"job": job, 
                                             "img1_name": wip_path, 
                                             "img2_name": wip_path,
                                             "markdown_content": markdown_content})

# 影响 任务创造 界面
def job_create(request):
    prefix = "chemicals"
    if request.method == "POST":
        job_form = JobForm(request.POST)

        if job_form.is_valid():
            job = job_form.save()
            chemical_A_formset = Chemical_AFormSet(
                request.POST, instance=job, prefix=prefix
            )
            chemical_As = []
            for chemical_AForm in chemical_A_formset:
                if chemical_AForm.is_valid() and chemical_AForm.has_changed():
                    cA = chemical_AForm.save()
                    chemical_As.append(cA)
            calculate_parameter(job, chemical_As)

            return redirect("job_view", pk=job.id)
        else:
            # todo add error message
            pass
    else:
        job_form = JobForm()
        chemical_A_formset = Chemical_AFormSet(prefix=prefix)
    return render(
        request,
        "job_create.html",
        {
            "job_form": job_form,
            "chemical_A_formset": chemical_A_formset,
            "prefix": prefix,
            "chemical_A_dict": Chemical_A.chemicalData_A,
        },
    )
