from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import markdown
from .models import *

def home(request):
    context = {
        'site_settings': SiteSettings.objects.first(),
        'about': About.objects.first(),
        'skills': Skill.objects.all(),
        'featured_projects': Project.objects.filter(featured=True).order_by('order')[:3],
        'all_projects': Project.objects.all().order_by('-featured', 'order'),
        'education': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'extracurriculars': Extracurricular.objects.all(),
        'recent_posts': Post.objects.filter(is_published=True).order_by('-published_date')[:3],
    }
    return render(request, 'core/home.html', context)

def blog_list(request):
    posts_list = Post.objects.filter(is_published=True).order_by('-published_date')
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'site_settings': SiteSettings.objects.first(),
        'featured_posts': Post.objects.filter(is_published=True, is_featured=True)[:3],
    }
    return render(request, 'core/blog_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post_content_html = md.convert(post.markdown_content)
    
    context = {
        'post': post,
        'post_content': post_content_html,
        'site_settings': SiteSettings.objects.first(),
        'toc': md.toc if hasattr(md, 'toc') else '',
    }
    return render(request, 'core/post_detail.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        'project': project,
        'site_settings': SiteSettings.objects.first(),
    }
    return render(request, 'core/project_detail.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
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
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return redirect('home')
    
    return redirect('home')