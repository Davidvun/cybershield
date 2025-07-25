from django.db import models
from django.contrib.auth.models import User

class IncidentType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Incident(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='Low')
    type = models.ForeignKey(IncidentType, on_delete=models.CASCADE)
    affected_systems = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_incidents')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.type.name})"

class IncidentStep(models.Model):
    STEP_CHOICES = [
        ('triage', 'Initial Triage & Validation'),
        ('containment', 'Containment'),
        ('investigation', 'Investigation'),
        ('eradication', 'Eradication'),
        ('recovery', 'Recovery'),
        ('closure', 'Documentation & Closure'),
    ]

    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='steps')
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    step = models.CharField(max_length=20, choices=STEP_CHOICES)
    notes = models.TextField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('incident', 'step')

    def __str__(self):
        return f"{self.get_step_display()} - {self.incident.title}"
