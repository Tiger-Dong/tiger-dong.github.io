from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ProjectStage
from .forms import ProjectForm, ProjectStageForm
from django.core.serializers import serialize


def project_list(request):
    projects = Project.objects.all()
    for project in projects:
        try:
            project.latest_stage = ProjectStage.objects.filter(project=project).latest(
                "Updated_time"
            )
        except ProjectStage.DoesNotExist:
            project.latest_stage = None

    return render(request, "projects/project_list.html", {"projects": projects})


def project_create(request):
    if request.method == "POST":
        form_project = ProjectForm(request.POST)
        if form_project.is_valid():
            project = form_project.save()
            form_stage = ProjectStageForm({'State':request.POST.get('state'),
                                          "project": project})            
            stage = form_stage.save()             
            return redirect("project_list")
    else:
        form_project = ProjectForm()
        form_stage = ProjectStageForm()

    return render(
        request, "projects/project_create.html", 
            {"form_project": form_project, "form_stage": form_stage}
    )


def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project_form = ProjectForm(request.POST, instance=project)
        stage_form = ProjectStageForm({"State": request.POST.get("state"), "project": project})
        if project_form.is_valid() and stage_form.is_valid():
            project = project_form.save()
            stage = stage_form.save()
            # Serialize the project and stage instances to JSON
            project_json = serialize('json', [project])
            stage_json = serialize('json', [stage])
            
            print(project_json)
            print(stage_json)
            
            return redirect(
                "project_list"
            )  # replace with the name of your project list view
    else:
        project_form = ProjectForm(instance=project)
        stage = project.projectstage_set.latest("Updated_time")
        stage_form = ProjectStageForm(instance=stage)
    return render(
        request,
        "projects/edit_project.html",
        {"project_form": project_form, "stage_form": stage_form},
    )
