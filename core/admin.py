from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import *

# Custom admin form for Post with larger textarea
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'markdown_content': forms.Textarea(attrs={'rows': 25, 'style': 'width: 90%; font-family: monospace;'}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'author', 'published_date', 'is_published', 'is_featured', 'view_count']
    list_editable = ['is_published', 'is_featured']
    list_filter = ['is_published', 'is_featured', 'published_date', 'tags']
    search_fields = ['title', 'markdown_content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['published_date', 'updated_date', 'preview_link']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'excerpt', 'tags')
        }),
        ('Content', {
            'fields': ('markdown_content', 'header_image')
        }),
        ('Publication', {
            'fields': ('is_published', 'is_featured', 'published_date', 'updated_date')
        }),
        ('Preview', {
            'fields': ('preview_link',),
            'classes': ('collapse',)
        }),
    )
    
    def preview_link(self, obj):
        if obj.id:
            return format_html(
                '<a href="{}" target="_blank" class="button">View Post on Site</a>',
                obj.get_absolute_url()
            )
        return "Save post first to preview"
    preview_link.short_description = "Post Preview"

# Enhanced Project Admin with better image management
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    classes = ['collapse']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'completion_date', 'order', 'technology_count']
    list_editable = ['featured', 'order']
    list_filter = ['featured', 'completion_date']
    search_fields = ['title', 'short_description', 'technologies']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'long_description')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'github_url', 'demo_url', 'completion_date')
        }),
        ('Display Options', {
            'fields': ('featured', 'order')
        }),
    )
    
    def technology_count(self, obj):
        return len(obj.get_technologies_list())
    technology_count.short_description = 'Tech Count'

# Enhanced Skill Admin with bulk actions
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'order', 'skill_bar']
    list_editable = ['level', 'order', 'category']
    list_filter = ['category']
    search_fields = ['name']
    actions = ['reset_skill_levels']
    
    def skill_bar(self, obj):
        return format_html(
            '<div style="width: 100px; background: #e0e0e0; border-radius: 3px;">'
            '<div style="width: {}%; background: #4CAF50; height: 20px; border-radius: 3px; text-align: center; color: white; font-size: 12px; line-height: 20px;">{}%</div>'
            '</div>',
            obj.level, obj.level
        )
    skill_bar.short_description = 'Level'
    
    def reset_skill_levels(self, request, queryset):
        updated = queryset.update(level=50)
        self.message_user(request, f'Successfully reset {updated} skills to level 50.')
    reset_skill_levels.short_description = "Reset selected skills to level 50"

# Enhanced Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject_preview', 'created_at', 'read', 'reply_action']
    list_editable = ['read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at', 'reply_link']
    list_filter = ['read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    actions = ['mark_as_read', 'mark_as_unread']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at', 'read')
        }),
        ('Quick Actions', {
            'fields': ('reply_link',),
            'classes': ('collapse',)
        }),
    )
    
    def subject_preview(self, obj):
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = 'Subject'
    
    def reply_action(self, obj):
        return format_html(
            '<a href="mailto:{}?subject=Re: {}" class="button">Reply</a>',
            obj.email, obj.subject
        )
    reply_action.short_description = 'Action'
    
    def reply_link(self, obj):
        return format_html(
            '<a href="mailto:{}?subject=Re: {}&body=Hello {}, " class="button" style="background: #4CAF50; color: white; padding: 10px; text-decoration: none; border-radius: 4px;">Compose Reply Email</a>',
            obj.email, obj.subject, obj.name
        )
    reply_link.short_description = ''
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(read=True)
        self.message_user(request, f'Marked {updated} messages as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(read=False)
        self.message_user(request, f'Marked {updated} messages as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'period', 'current']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'in_progress']

@admin.register(Extracurricular)
class ExtracurricularAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'role', 'period', 'current']

admin.site.register(About)

# Custom Admin Site Title
admin.site.site_header = "Muwemi's Portfolio Admin"
admin.site.site_title = "Portfolio Admin"

admin.site.index_title = "Welcome to Portfolio Administration"
