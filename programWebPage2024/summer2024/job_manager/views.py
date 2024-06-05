from django.shortcuts import render, redirect
from .models import Job, Chemical_A
from .forms import JobForm, Chemical_AForm, Chemical_AFormSet
import json
from pathlib import Path
import subprocess

def job_list(request):
    jobs = Job.objects.all()
    return render(request, "job_list.html", {"jobs": jobs})

def find_job_id():
    in_text = "information from the list "
    start_index = in_text.find("Python ") + len("Python ")
    end_index = start_index + len("0.0.00")
    job_id = in_text[start_index:end_index]
    return job_id


def calcualte_N(job: Job, chemical_A: Chemical_A, total_shares_A) -> float:
    return (
        float(job.chemial_A_mass)
        * (chemical_A.shares / total_shares_A)
        / chemical_A.molecular_mass
    )


def calculate_parameter(job: Job, chemical_As: list):
    total_shares_A = sum([chemical_A.shares for chemical_A in chemical_As])
    total_hydroxyl_A = float(sum(
        [chemical_A.hydroxyl * chemical_A.shares for chemical_A in chemical_As]
    ))
    job.theory_shares_ratio = (
        4202.0 / (float(job.chemical_B_NCO) * total_shares_A) * total_hydroxyl_A / 56100
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
    
    job.N0 = parameters["N0"]
    job.N1 = parameters["N1"]
    job.N2 = parameters["N2"]
    job.N3 = parameters["N3"]
    job.N4 = parameters["N4"]
    job.N5 = parameters["N5"]
    job.save()
        
    # dump the parameters to a json file
    tool_path = Path.cwd().parent / "tools"
    assert tool_path.exists(), f"{tool_path} does not exist, the test.sh, *.molg and py should be in this folder"
    parameter_file = tool_path / f"{job.id}.json"
    print(f"parameter file: {parameter_file}")

    # write parameter to parameter file
    with parameter_file.open("w") as f:
        json.dump(parameters, f)

    # read shell template file
    with (tool_path / "test.sh.template").open("r") as f:
        shell_template = f.read()
    test_sh = tool_path / "test.sh"
    with test_sh.open("w") as f:
        f.write(shell_template.replace("{{job_id}}", str(job.id)))
            
    completed_process = subprocess.run(
        [
            "sbatch",
            test_sh.as_posix(),            
        ],
        text=True,
        capture_output=True,
    )
    print(f"Return code: {completed_process.returncode}")
    print(f"Output: {completed_process.stdout}")

    # Search job_id
    sbatch_id 
    sbatch_id = print(f"Output: {completed_process.stdout}")
    start_index = job.sbatch_job_id.find("job_output_") + len("job_output_")
    end_index = start_index + len("00000")
    job.sbatch_job_id = sbatch_id [start_index:end_index]


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
            "chemical_A_dict": Chemical_A.chemicalData_A,
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
