from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from core.decorators import group_required
from core.forms import IncidentStepForm
from .models import Incident, IncidentStep, IncidentType

class CustomLoginView(LoginView):
    template_name = 'pages/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse('admin_dashboard')
        elif user.groups.filter(name='Responder').exists():
            return reverse('responder_dashboard')
        return super().get_success_url()

# Custom logout view
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    http_method_names = ['get', 'post']
    template_name = 'registration/logged_out.html' 
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Admin dashboard
@login_required
@group_required('Admin')
def admin_dashboard(request):
    incidents = Incident.objects.all()
    users = User.objects.all()
    categories = IncidentType.objects.all()
    return render(request, 'pages/admin.html', {
        'incidents': incidents,
        'users': users,
        'categories': categories
    })

# Responder dashboard
@login_required
@group_required('Responder')
def responder_dashboard(request):
    incidents = Incident.objects.filter(assigned_to=request.user)
    return render(request, 'pages/responder.html', {'incidents': incidents})

# Create user
@login_required
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_group = request.POST.get('user_group')  

        if username and email and password and user_group:
            try:
                
                user = User.objects.create_user(username=username, password=password, email=email)
                
                
                from django.contrib.auth.models import Group
                group = Group.objects.get(name=user_group)
                user.groups.add(group)
                
                user.save()
                return JsonResponse({'status': 'success', 'message': f'User {username} created successfully as {user_group}'})
            except Group.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid group selected'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Error creating user: {str(e)}'})
        else:
            missing_fields = []
            if not username: missing_fields.append('username')
            if not email: missing_fields.append('email')
            if not password: missing_fields.append('password')
            if not user_group: missing_fields.append('user role')
            
            return JsonResponse({'status': 'error', 'message': f'Missing required fields: {", ".join(missing_fields)}'})
    
    return render(request, 'partials/create_user_form.html')

# Delete user
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('admin_dashboard')

# Create incident
@login_required
def create_incident(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        severity = request.POST.get('severity')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        affected_systems = request.POST.get('affected_systems')
        assigned_to_id = request.POST.get('assigned_to')

        
        if not all([title, severity, category_id, description]):
            return JsonResponse({'status': 'error', 'message': 'Please fill all required fields.'})

        try:
            category = IncidentType.objects.get(pk=category_id)
        except IncidentType.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid category selected.'})

        assigned_to = None
        if assigned_to_id:
            try:
                assigned_to = User.objects.get(pk=assigned_to_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid user assigned.'})

        incident = Incident.objects.create(
            title=title,
            severity=severity,
            type=category,
            description=description,
            affected_systems=affected_systems,
            assigned_to=assigned_to,
            created_by=request.user  
        )
        return JsonResponse({'status': 'success'})

    users = User.objects.all()
    categories = IncidentType.objects.all()
    return render(request, 'partials/create_incident_form.html', {
        'users': users,
        'categories': categories
    })

# Manage incident
@login_required
def manage_incident(request, incident_id):
    incident = get_object_or_404(Incident, pk=incident_id)
    if request.method == 'POST':
        incident.status = request.POST.get('status')
        incident.severity = request.POST.get('severity')
        incident.affected_systems = request.POST.get('affected_systems')
        incident.save()
        return JsonResponse({'status': 'success'})
    return render(request, 'partials/manage_incident_form.html', {'incident': incident})

@login_required
@group_required('Responder')
def responder_incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id, assigned_to=request.user)
    
    if request.method == 'POST':
        step_value = request.POST.get('step')
        completed = request.POST.get('completed') == 'true'
        notes = request.POST.get('notes')
        
        if step_value and notes:
            existing_step = IncidentStep.objects.filter(
                incident=incident, 
                step=step_value
            ).first()
            
            if existing_step:
                existing_step.notes = notes
                existing_step.completed = completed
                existing_step.responder = request.user
                if completed:
                    existing_step.completed_at = timezone.now()
                existing_step.save()
            else:
                IncidentStep.objects.create(
                    incident=incident,
                    responder=request.user,
                    step=step_value,
                    notes=notes,
                    completed=completed,
                    completed_at=timezone.now() if completed else None
                )
            
            return redirect('responder-incident-detail', incident_id=incident.id)
        else:
            # Handle validation error
            messages.error(request, 'Please fill in all required fields.')
    
    # Get existing steps (fix the order issue)
    steps = incident.steps.order_by('step')  # Remove 'order', use 'step'
    
    return render(request, 'pages/incident_detail.html', {
        'incident': incident,
        'steps': steps
    })

@login_required
@group_required('Admin')
def admin_incident_progress(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)
    
    # Handle admin actions
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'resolve':
            incident.status = 'resolved'
            incident.save()
            messages.success(request, f'Incident "{incident.title}" has been marked as resolved.')
            
        elif action == 'close':
            incident.status = 'closed'
            incident.save()
            messages.success(request, f'Incident "{incident.title}" has been closed.')
            
        elif action == 'reopen':
            incident.status = 'in_progress'
            incident.save()
            messages.success(request, f'Incident "{incident.title}" has been reopened.')
        
        return redirect('admin-incident-progress', incident_id=incident.id)
    
    # Get all steps for this incident, ordered properly
    steps = incident.steps.order_by('step')  # Remove 'order', use 'step'
    
    # Calculate progress percentage
    total_steps = steps.count()
    completed_steps = steps.filter(completed=True).count()
    progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    return render(request, 'pages/incident_progress.html', {
        'incident': incident,
        'steps': steps,
        'total_steps': total_steps,
        'completed_steps': completed_steps,
        'progress_percentage': progress_percentage
    })