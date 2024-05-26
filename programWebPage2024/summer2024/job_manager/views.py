from django.shortcuts import render, redirect
from .models import Job, Chemical_A
from .forms import JobForm, Chemical_AForm, Chemical_AFormSet
import json
from pathlib import Path
import subprocess


def job_list(request):
    jobs = Job.objects.all()
    return render(request, "job_list.html", {"jobs": jobs})


def calcualte_N(job: Job, chemical_A: Chemical_A, total_shares_A) -> float:
    return (
        job.chemial_A_mass
        * (chemical_A.shares / total_shares_A)
        / chemical_A.molecular_mass
    )


def calculate_parameter(job: Job, chemical_As: list):
    total_shares_A = sum([chemical_A.shares for chemical_A in chemical_As])
    total_hydroxyl_A = sum(
        [chemical_A.hydroxyl * chemical_A.shares for chemical_A in chemical_As]
    )
    job.theory_shares_ratio = (
        4202.0 / (job.chemical_B_NCO * total_shares_A) * total_hydroxyl_A / 56100
    )
    job.save()
    parameters = {"job_id": job.id, "job_name": job.name}
    parameters["N0"] = job.chemical_B_mass/ job.chemical_B_molecular_mass
    parameter_mapping =  {"PTMG1000":"N1", "PTMG2000":"N2", 
                          "330N":"N3", "BDO":"N4", "water":"N5"}    
    for chemical_A in chemical_As:
        for key, value in parameter_mapping.items():
            if key in chemical_A.name:
                parameters[value] = calcualte_N(job, chemical_A, total_shares_A)
        
    # dump the parameters to a json file
    parameter_path = Path.cwd() / f"parameters"
    parameter_path.mkdir(exist_ok=True)
    parameter_file = parameter_path / f"{job.id}.json"
    print(f"parameter file: {parameter_file}")
    # write parameter to parameter file
    with parameter_file.open("w") as f:
        json.dump(parameters, f)

    completed_process = subprocess.run(
        [
            "python3",
            Path.cwd().joinpath("tools/0519.molg").as_posix(),
            "--config",
            parameter_file.as_posix(),
        ],
        text=True,
        capture_output=True,
    )
    print(f"Return code: {completed_process.returncode}")
    print(f"Output: {completed_process.stdout}")


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
            for chemical_A in chemical_A_formset:
                if chemical_A.cleaned_data:
                    chemical_A.complete()
                    chemical_A.save()
                    chemical_As.append(chemical_A)                    
            # calculate_parameter(job, chemical_As)    
            return redirect("job_list")
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
        },
    )


def edit_job(request, pk):
    job = Job.objects.get(pk=pk)
    if request.method == "POST":
        job.name = request.POST.get("name")
        job.description = request.POST.get("description")
        job.theory_shares_ratio = request.POST.get("theory_shares_ratio")
        job.chemical_B_NCO = request.POST.get("chemical_B_NCO")
        job.chemical_B_functionality = request.POST.get("chemical_B_functionality")
        job.chemical_B_molecular_mass = request.POST.get("chemical_B_molecular_mass")
        job.chemical_B_shares = request.POST.get("chemical_B_shares")
        job.temperature = request.POST.get("temperature")
        job.save()
        chemical_A = Chemical_A.objects.get(job=job)
        chemical_A.name = request.POST.get("chemical_A_name")
        chemical_A.chemical_A_functionality = request.POST.get(
            "chemical_A_functionality"
        )
        chemical_A.chemical_A_hydroxyl = request.POST.get("chemical_A_hydroxyl")
        chemical_A.chemical_A_molecular_mass = request.POST.get(
            "chemical_A_molecular_mass"
        )
        chemical_A.chemical_A_shares = request.POST.get("chemical_A_shares")
        chemical_A.save()
        return render(request, "edit_job.html", {"job": job, "chemical_A": chemical_A})
    return render(request, "edit_job.html", {"job": job})
