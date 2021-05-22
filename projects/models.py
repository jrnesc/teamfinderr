from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class CompletedProjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(end_date__lt=timezone.now())


class Project(models.Model):  # a project that a user will create
    name = models.CharField(max_length=200)  # charfield limited to 255 characters
    description = models.TextField(max_length=500)  # Textfield >255 characters
    owner = models.ForeignKey(User, related_name="projects_owned", on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through="ProjectMembership")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()  # default manager
    completed_objects = CompletedProjectsManager()  # custom completed projects manager

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.members.exists():  # only run when project is created
            member, created = ProjectMembership.objects.get_or_create(user=self.owner, project=self, role="owner")
            member.save()
            self.members.add(self.owner)
        return self

    def __str__(self):
        return f"{self.name}"


class ProjectMembership(models.Model):
    user = models.ForeignKey(User, related_name="project_memberships", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="project_memberships", on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    message = models.TextField(max_length=64, null=True)

    def __str__(self):
        return f"{self.user}{self.project}"


class ProjectMembershipRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="requests", on_delete=models.CASCADE)
    to_project = models.ForeignKey(Project, related_name="requests", on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    status = models.CharField(
        max_length=8,
        choices=(
            ("accepted", "Accepted"),
            ("pending", "Pending"),
            ("declined", "Declined"),
        ),
        default="pending",
    )
    responded = models.BooleanField(blank=True, null=True, default=False)

    def save(self, *args, **kwargs):
        # Once the request has been responded to be a project member -> set self.responded to true
        if (self.status) in ["accepted", "declined"]:
            if (self.status == "accepted"):
                member, created = ProjectMembership.objects.get_or_create(user=self.from_user, project=self.to_project, role=self.role)
                member.save()
                self.to_project.members.add(self.from_user)
                self.to_project.roles.add(self.role)
            self.responded = True
        super().save(*args, **kwargs)
        return self

    class Meta:
        unique_together = ("from_user", "to_project")

    def __str__(self):
        return f"{self.from_user} to {self.to_project}"
