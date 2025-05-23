from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resource
from .forms import ResourceForm

@login_required
def upload_resource(request):
    if not request.user.is_staff:
        return render(request, '403.html')  # Optional
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'upload_resource.html', {'form': form})

def resource_list(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'resource_list.html', {'resources': resources})
