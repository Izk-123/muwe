from django.urls import path
from . import views

urlpatterns = [
    # Class-based views
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Additional class-based views (optional)
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('skills/', views.SkillListView.as_view(), name='skill_list'),
    
    # Legacy function-based view (for backward compatibility)
    # path('contact/legacy/', views.contact_legacy, name='contact_legacy'),
]