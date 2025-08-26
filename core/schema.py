import graphene
from graphene_django import DjangoObjectType
from .models import Organization, Project, Task, TaskComment

# -------------------------------
# GraphQL Object Types
# -------------------------------
class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ("id", "name", "slug", "contact_email", "created_at", "projects")

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "status", "due_date", "created_at", "organization", "tasks")

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "assignee_email", "due_date", "created_at", "project", "comments")

class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = ("id", "content", "author_email", "timestamp", "task")


# -------------------------------
# Queries
# -------------------------------
class Query(graphene.ObjectType):
    all_organizations = graphene.List(OrganizationType)
    organization_by_slug = graphene.Field(OrganizationType, slug=graphene.String(required=True))
    projects_by_org = graphene.List(ProjectType, org_id=graphene.Int(required=True))

    def resolve_all_organizations(root, info):
        return Organization.objects.all()

    def resolve_organization_by_slug(root, info, slug):
        return Organization.objects.get(slug=slug)

    def resolve_projects_by_org(root, info, org_id):
        return Project.objects.filter(organization_id=org_id)


# -------------------------------
# Mutations
# -------------------------------
class CreateOrganization(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=True)
        contact_email = graphene.String(required=True)

    organization = graphene.Field(OrganizationType)

    def mutate(self, info, name, slug, contact_email):
        org = Organization.objects.create(name=name, slug=slug, contact_email=contact_email)
        return CreateOrganization(organization=org)


class CreateProject(graphene.Mutation):
    class Arguments:
        org_id = graphene.Int(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String(required=True)
        due_date = graphene.types.datetime.Date()

    project = graphene.Field(ProjectType)

    def mutate(self, info, org_id, name, status, description="", due_date=None):
        org = Organization.objects.get(id=org_id)
        project = Project.objects.create(
            organization=org, name=name, description=description, status=status, due_date=due_date
        )
        return CreateProject(project=project)


class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String(required=True)
        assignee_email = graphene.String()

    task = graphene.Field(TaskType)

    def mutate(self, info, project_id, title, status, description="", assignee_email=""):
        project = Project.objects.get(id=project_id)
        task = Task.objects.create(
            project=project, title=title, description=description, status=status, assignee_email=assignee_email
        )
        return CreateTask(task=task)


class CreateTaskComment(graphene.Mutation):
    class Arguments:
        task_id = graphene.Int(required=True)
        content = graphene.String(required=True)
        author_email = graphene.String(required=True)

    comment = graphene.Field(TaskCommentType)

    def mutate(self, info, task_id, content, author_email):
        task = Task.objects.get(id=task_id)
        comment = TaskComment.objects.create(task=task, content=content, author_email=author_email)
        return CreateTaskComment(comment=comment)


# -------------------------------
# Hook Queries + Mutations into Schema
# -------------------------------
class Mutation(graphene.ObjectType):
    create_organization = CreateOrganization.Field()
    create_project = CreateProject.Field()
    create_task = CreateTask.Field()
    create_task_comment = CreateTaskComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
