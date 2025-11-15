from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
import markdown
from .models import *

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site_settings': SiteSettings.objects.first(),
            'about': About.objects.first(),
            'skills': Skill.objects.all(),
            'featured_projects': Project.objects.filter(featured=True).order_by('order')[:3],
            'all_projects': Project.objects.all().order_by('-featured', 'order'),
            'education': Education.objects.all(),
            'certifications': Certification.objects.all(),
            'extracurriculars': Extracurricular.objects.all(),
            'recent_posts': Post.objects.filter(is_published=True).order_by('-published_date')[:3],
        })
        return context

class BlogListView(ListView):
    model = Post
    template_name = 'core/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-published_date']
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site_settings': SiteSettings.objects.first(),
            'featured_posts': Post.objects.filter(is_published=True, is_featured=True)[:3],
        })
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post_content_html = md.convert(post.markdown_content)
        
        context.update({
            'post_content': post_content_html,
            'site_settings': SiteSettings.objects.first(),
            'toc': md.toc if hasattr(md, 'toc') else '',
        })
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.objects.first()
        return context

class ContactView(CreateView):
    model = ContactMessage
    template_name = 'core/home.html'  # Redirects to home where contact form is located
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Send email notification
        contact_message = self.object
        send_mail(
            f'Portfolio Contact: {contact_message.subject}',
            f'From: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        
        messages.success(self.request, 'Thank you for your message! I will get back to you soon.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your submission. Please check the form and try again.')
        return super().form_invalid(form)

# Alternative approach for contact using FormView if you want more control
class ContactFormView(FormView):
    template_name = 'core/home.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification
        send_mail(
            f'Portfolio Contact: {subject}',
            f'From: {name} ({email})\n\n{message}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        
        messages.success(self.request, 'Thank you for your message! I will get back to you soon.')
        return super().form_valid(form)

# Project List View (if you want a dedicated projects page)
class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    ordering = ['-featured', 'order']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.objects.first()
        return context

# Skills View (if you want a dedicated skills page)
class SkillListView(ListView):
    model = Skill
    template_name = 'core/skill_list.html'
    context_object_name = 'skills'
    ordering = ['category', '-level', 'name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.objects.first()
        
        # Group skills by category
        skills_by_category = {}
        for skill in context['skills']:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        
        context['skills_by_category'] = skills_by_category
        return context

# Function-based view for backward compatibility (optional)
def contact_legacy(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        send_mail(
            f'Portfolio Contact: {subject}',
            f'From: {name} ({email})\n\n{message}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return redirect('home')
    
    return redirect('home')