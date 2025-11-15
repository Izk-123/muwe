from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=64, default="Muwemi's Portfolio")
    hero_title = models.CharField(max_length=128, default="Mechanical Engineering Innovator")
    hero_subtitle = models.TextField(default="Specializing in hydraulic systems, automation, and sustainable energy solutions")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return 'Site Settings'

class About(models.Model):
    content = models.TextField(default="I am a goal-oriented mechanical engineering student with a passion for problem-solving and innovation...")
    
    def __str__(self):
        return 'About Section'

class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('ENG', 'Engineering'),
        ('PROG', 'Programming'),
        ('DESIGN', 'Design'),
        ('SOFT', 'Soft Skills'),
    ]
    
    name = models.CharField(max_length=64)
    level = models.PositiveSmallIntegerField(help_text="0-100")
    category = models.CharField(max_length=10, choices=SKILL_CATEGORIES, default='ENG')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['category', '-level', 'name']

class Project(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    long_description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    technologies = models.CharField(max_length=200, help_text="Comma-separated list of technologies")
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    completion_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return f"Image for {self.project.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=140, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"

class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    current = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return self.degree

class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True)
    in_progress = models.BooleanField(default=False)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return self.title

class Extracurricular(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True)
    period = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    current = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=80, default="Muwemi Ndovie")
    markdown_content = models.TextField(help_text="Write your post using Markdown syntax")
    excerpt = models.TextField(blank=True, help_text="Brief summary of the post")
    header_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True, related_name='blog_posts')
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.markdown_content:
            plain_text = self.markdown_content[:150]
            self.excerpt = plain_text + '...' if len(plain_text) == 150 else plain_text
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})