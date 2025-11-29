from django.db import models
from djongo import models as djongo_models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from accounts.models import CustomUser
from django.core.validators import RegexValidator, MinValueValidator
import os
import random
import string
import time

def job_attachment_path(instance, filename):
    """Generate file path for job attachments"""
    return f'job_attachments/{instance.job.system_id}/{filename}'


# class Job(models.Model):
#     """Main Job model with comprehensive tracking"""
    
#     REFERENCING_STYLE_CHOICES = [
#         ('harvard', 'Harvard'),
#         ('apa', 'APA'),
#         ('mla', 'MLA'),
#         ('ieee', 'IEEE'),
#         ('vancouver', 'Vancouver'),
#         ('chicago', 'Chicago'),
#     ]
    
#     WRITING_STYLE_CHOICES = [
#         ('proposal', 'Proposal'),
#         ('report', 'Report'),
#         ('essay', 'Essay'),
#         ('dissertation', 'Dissertation'),
#         ('business_report', 'Business Report'),
#         ('personal_development', 'Personal Development'),
#         ('reflection_writing', 'Reflection Writing'),
#         ('case_study', 'Case Study'),
#     ]
    
#     STATUS_CHOICES = [
#         ('draft', 'Draft'),
#         ('pending', 'Pending'),
#         ('allocated', 'Allocated'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('hold', 'Hold'),
#         ('query', 'Query'),
#         ('cancelled', 'Cancelled'),
#     ]
    
#     # Primary identifiers
#     system_id = models.CharField(max_length=50, unique=True, db_index=True)
#     job_id = models.CharField(max_length=200, unique=True, db_index=True)
    
#     # Initial Form Fields
#     instruction = models.TextField(help_text="Minimum 50 characters required")
    
#     # AI Generated Summary Fields
#     topic = models.CharField(max_length=500, blank=True, null=True)
#     word_count = models.IntegerField(blank=True, null=True)
#     referencing_style = models.CharField(
#         max_length=20, 
#         choices=REFERENCING_STYLE_CHOICES,
#         blank=True, 
#         null=True
#     )
#     writing_style = models.CharField(
#         max_length=30,
#         choices=WRITING_STYLE_CHOICES,
#         blank=True,
#         null=True
#     )
#     job_summary = models.TextField(blank=True, null=True)
    
#     # AI Summary Metadata
#     ai_summary_version = models.IntegerField(default=0)
#     ai_summary_generated_at = models.JSONField(default=list, blank=True)  # Array of timestamps
#     job_card_degree = models.IntegerField(default=5)  # 0-5 based on missing fields
    
#     # User Relations (using string reference for MongoDB compatibility)
#     created_by = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         related_name='jobs_created'
#     )
#     allocated_to = models.ForeignKey(
#         CustomUser,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='jobs_allocated'
#     )
    
#     # Status
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='draft'
#     )
    
#     # Timestamps - Initial Form
#     created_at = models.DateTimeField(default=timezone.now)
#     initial_form_submitted_at = models.DateTimeField(null=True, blank=True)
#     initial_form_last_saved_at = models.DateTimeField(null=True, blank=True)
#     job_name_validated_at = models.DateTimeField(null=True, blank=True)
    
#     # Timestamps - AI Summary
#     ai_summary_requested_at = models.DateTimeField(null=True, blank=True)
#     ai_summary_accepted_at = models.DateTimeField(null=True, blank=True)
    
#     # General timestamps
#     updated_at = models.DateTimeField(auto_now=True)
#     deadline = models.DateField(null=True, blank=True)
    
#     class Meta:
#         db_table = 'marketing_jobs'
#         ordering = ['-created_at']
#         verbose_name = 'Job'
#         verbose_name_plural = 'Jobs'
#         indexes = [
#             models.Index(fields=['system_id']),
#             models.Index(fields=['job_id']),
#             models.Index(fields=['status']),
#             models.Index(fields=['created_by']),
#         ]
    
#     def __str__(self):
#         return f"{self.system_id} - {self.job_id}"
    
#     @staticmethod
#     def generate_system_id():
#         """Generate unique system ID: CH-timestamp_ms"""
#         timestamp_ms = int(time.time() * 1000)
#         return f"CH-{timestamp_ms}"
    
#     def calculate_degree(self):
#         """Calculate job card degree based on missing fields"""
#         required_fields = [
#             self.topic,
#             self.word_count,
#             self.referencing_style,
#             self.writing_style,
#             self.job_summary
#         ]
#         missing_count = sum(1 for field in required_fields if not field)
#         self.job_card_degree = missing_count
#         return missing_count
    
#     def can_regenerate_summary(self):
#         """Check if summary can be regenerated (max 3 versions)"""
#         return self.ai_summary_version < 3
    
#     def should_auto_accept(self):
#         """Determine if summary should be auto-accepted"""
#         return self.job_card_degree == 0 or self.ai_summary_version >= 3



class Job(models.Model):
    """Main Job model with comprehensive tracking"""

    # Use Mongo ObjectId as primary key to match stored documents
    id = djongo_models.ObjectIdField(primary_key=True, db_column='_id')
    CATEGORY_CHOICES = [
        ('IT', 'IT'),
        ('NON-IT', 'Non-IT'),
        ('FINANCE', 'Finance'),
    ]

    REFERENCING_STYLE_CHOICES = [
        ('harvard', 'Harvard'),
        ('apa', 'APA'),
        ('mla', 'MLA'),
        ('ieee', 'IEEE'),
        ('vancouver', 'Vancouver'),
        ('chicago', 'Chicago'),
    ]
    
    WRITING_STYLE_CHOICES = [
        ('proposal', 'Proposal'),
        ('report', 'Report'),
        ('essay', 'Essay'),
        ('dissertation', 'Dissertation'),
        ('business_report', 'Business Report'),
        ('personal_development', 'Personal Development'),
        ('reflection_writing', 'Reflection Writing'),
        ('case_study', 'Case Study'),
    ]
    LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('allocated', 'Allocated'),
        ('in_progress', 'In Progress'),
        ('unallocated', 'Unallocated'),
        ('completed', 'Completed'),
        ('hold', 'Hold'),
        ('query', 'Query'),
        ('cancelled', 'Cancelled'),
        ('Review', 'Review'),
    ]
    
    # Primary identifiers
    system_id = models.CharField(max_length=50, unique=True, db_index=True)
    job_id = models.CharField(max_length=200, unique=True, db_index=True)
    
    # Initial Form Fields
    instruction = models.TextField(help_text="Minimum 50 characters required")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )
    customer_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Customer ID from marketing_customers"
    )
    customer_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Customer name captured at final submission"
    )

    # AI Generated Summary Fields
    topic = models.CharField(max_length=500, blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True)
    referencing_style = models.CharField(
        max_length=20, 
        choices=REFERENCING_STYLE_CHOICES,
        blank=True, 
        null=True
    )
    writing_style = models.CharField(
        max_length=30,
        choices=WRITING_STYLE_CHOICES,
        blank=True,
        null=True
    )
    job_summary = models.TextField(blank=True, null=True)
    
    # AI Summary Metadata
    ai_summary_version = models.IntegerField(default=0)
    ai_summary_generated_at = models.JSONField(default=list, blank=True)  # Array of timestamps
    job_card_degree = models.IntegerField(default=5)  # 0-5 based on missing fields
    final_form_opened_at = models.DateTimeField(null=True, blank=True)
    final_form_submitted_at = models.DateTimeField(null=True, blank=True)
    masking_id_generated_at = models.DateTimeField(null=True, blank=True)
    expected_deadline = models.DateTimeField(null=True, blank=True)
    strict_deadline = models.DateTimeField(null=True, blank=True)
    software = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    system_expected_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True
    )


    # User Relations (using string reference for MongoDB compatibility)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='jobs_created'
    )
    allocated_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs_allocated'
    )
    template = models.ForeignKey(
        'superadminpanel.TemplateMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marketing_jobs'
    )
    project_group = models.ForeignKey(
        'superadminpanel.ProjectGroupMaster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marketing_jobs'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Timestamps - Initial Form
    created_at = models.DateTimeField(default=timezone.now)
    initial_form_submitted_at = models.DateTimeField(null=True, blank=True)
    initial_form_last_saved_at = models.DateTimeField(null=True, blank=True)
    job_name_validated_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps - AI Summary
    ai_summary_requested_at = models.DateTimeField(null=True, blank=True)
    ai_summary_accepted_at = models.DateTimeField(null=True, blank=True)
    
    # General timestamps
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'marketing_jobs'
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        indexes = [
            models.Index(fields=['system_id']),
            models.Index(fields=['job_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return f"{self.system_id} - {self.job_id}"
    
    @staticmethod
    def generate_system_id():
        """
        Generate unique system ID: CH-XXXXXX
        Where XXXXXX is 6 random alphanumeric characters (A-Z, 0-9)
        Example: CH-A3K9M2, CH-7B4XP1
        """
        while True:
            # Generate 6 random alphanumeric characters
            random_part = ''.join(random.choices(
                string.ascii_uppercase + string.digits, 
                k=6
            ))
            system_id = f"CH-{random_part}"
            
            # Check if it already exists
            if not Job.objects.filter(system_id=system_id).exists():
                return system_id
    
    def calculate_degree(self):
        """Calculate job card degree based on missing fields"""
        required_fields = [
            self.topic,
            self.word_count,
            self.referencing_style,
            self.writing_style,
            self.job_summary
        ]
        missing_count = sum(1 for field in required_fields if not field)
        self.job_card_degree = missing_count
        return missing_count
    
    def can_regenerate_summary(self):
        """Check if summary can be regenerated (max 3 versions)"""
        return self.ai_summary_version < 3
    
    def should_auto_accept(self):
        """Determine if summary should be auto-accepted"""
        return self.job_card_degree == 0 or self.ai_summary_version >= 3


class JobAttachment(models.Model):
    """Model for job attachments with validation"""
    
    ALLOWED_EXTENSIONS = ['pdf', 'docx', 'jpg', 'jpeg', 'png']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(
        upload_to=job_attachment_path,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
        ]
    )
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField()  # in bytes
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='uploaded_attachments'
    )
    
    class Meta:
        db_table = 'job_attachments'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"{self.job.system_id} - {self.original_filename}"
    
    def clean(self):
        """Validate file size"""
        from django.core.exceptions import ValidationError
        if self.file.size > self.MAX_FILE_SIZE:
            raise ValidationError(
                f'File size must not exceed 10MB. Current size: {self.file.size / (1024*1024):.2f}MB'
            )
    
    def get_file_extension(self):
        """Get file extension"""
        return os.path.splitext(self.original_filename)[1].lower()


class JobSummaryVersion(models.Model):
    """Store each AI summary generation version"""
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='summary_versions'
    )
    version_number = models.IntegerField()
    
    # Summary fields for this version
    topic = models.CharField(max_length=500, blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True)
    referencing_style = models.CharField(max_length=20, blank=True, null=True)
    writing_style = models.CharField(max_length=30, blank=True, null=True)
    job_summary = models.TextField(blank=True, null=True)
    
    # Metadata
    degree = models.IntegerField()  # 0-5 missing fields
    generated_at = models.DateTimeField(default=timezone.now)
    performed_by = models.CharField(max_length=50, default='system')
    ai_model_used = models.CharField(max_length=50, default='gpt-4o-mini')
    
    class Meta:
        db_table = 'job_summary_versions'
        ordering = ['version_number']
        indexes = [
            models.Index(fields=['job', 'version_number']),
        ]
    
    def __str__(self):
        return f"{self.job.system_id} - V{self.version_number} (Degree: {self.degree})"


class JobActionLog(models.Model):
    """Audit log for all job actions - integrates with your ActivityLog pattern"""
    
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('initial_form_submitted', 'Initial Form Submitted'),
        ('initial_form_saved', 'Initial Form Saved'),
        ('job_name_validated', 'Job Name Validated'),
        ('ai_summary_requested', 'AI Summary Requested'),
        ('ai_summary_generated', 'AI Summary Generated'),
        ('ai_summary_accepted', 'AI Summary Accepted'),
        ('status_changed', 'Status Changed'),
        ('allocated', 'Allocated'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='action_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    performed_by_type = models.CharField(
        max_length=20,
        choices=[('user', 'User'), ('system', 'System')],
        default='user'
    )
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'job_action_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.job.system_id} - {self.action} at {self.timestamp}"


# Utility function to log job actions to ActivityLog
def log_job_activity(job, event_key, category='job_management', performed_by=None, metadata=None):
    """
    Logs job-related activities to the main ActivityLog table
    This integrates with your existing ActivityLog system
    """
    from accounts.models import ActivityLog
    
    if metadata is None:
        metadata = {}
    
    # Add job-specific metadata
    metadata.update({
        'job_system_id': job.system_id,
        'job_id': job.job_id,
        'job_status': job.status,
    })
    
    # Add new category for jobs if not exists
    ActivityLog.objects.create(
        event_key=event_key,
        category=category,
        subject_user=job.created_by,  # The marketing user who created the job
        performed_by=performed_by,
        metadata=metadata,
    )
class Customer(models.Model):
    """Customer model for marketing module"""
    
    # Use Mongo ObjectId as primary key
    id = djongo_models.ObjectIdField(primary_key=True, db_column='_id')
    
    # Primary identifier
    customer_id = models.CharField(
        max_length=50, 
        unique=True, 
        db_index=True,
        editable=False
    )
    
    # Customer details
    customer_name = models.CharField(
        max_length=255,
        help_text="Minimum 3 characters required"
    )
    
    customer_email = models.EmailField(
        unique=True,
        db_index=True
    )
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits"
    )
    customer_phone = models.CharField(
        max_length=10,
        validators=[phone_regex]
    )
    
    targeted_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text="Target amount in INR"
    )
    
    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Current amount accumulated from jobs"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Relations
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customers_created'
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # KPI Cache (updated via signals/methods)
    total_projects = models.IntegerField(default=0)
    completed_projects = models.IntegerField(default=0)
    cancelled_projects = models.IntegerField(default=0)
    projects_with_issues = models.IntegerField(default=0)
    total_order_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    it_projects = models.IntegerField(default=0)
    non_it_projects = models.IntegerField(default=0)
    finance_projects = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'marketing_customers'
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        indexes = [
            models.Index(fields=['customer_id']),
            models.Index(fields=['customer_email']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.customer_id} - {self.customer_name}"
    
    @staticmethod
    def generate_customer_id():
        """Generate unique customer ID: CUST-timestamp_ms"""
        timestamp_ms = int(time.time() * 1000)
        return f"CUST-{timestamp_ms}"
    
    def clean(self):
        """Custom validation"""
        if len(self.customer_name) < 3:
            raise ValidationError({
                'customer_name': 'Customer name must be at least 3 characters long.'
            })
    
    def save(self, *args, **kwargs):
        """Override save to generate customer_id if not exists"""
        if not self.customer_id:
            self.customer_id = self.generate_customer_id()
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    def update_kpis(self):
        """Update customer KPIs from related jobs"""
        from marketing.models import Job
        from decimal import Decimal, InvalidOperation
        
        def _to_decimal(value):
            try:
                return Decimal(str(value))
            except (InvalidOperation, TypeError, ValueError):
                return Decimal('0')
        
        jobs = Job.objects.filter(customer=self)
        
        self.total_projects = jobs.count()
        self.completed_projects = jobs.filter(status='completed').count()
        self.cancelled_projects = jobs.filter(status='cancelled').count()
        self.projects_with_issues = jobs.filter(status__in=['query', 'hold']).count()
        
        # Financial KPIs
        self.total_order_amount = sum(
            _to_decimal(job.amount or 0) for job in jobs if job.amount is not None
        )
        self.total_paid_amount = sum(
            _to_decimal(job.paid_amount or 0) for job in jobs if hasattr(job, 'paid_amount') and job.paid_amount is not None
        )
        self.remaining_amount = self.total_order_amount - self.total_paid_amount
        
        # Category breakdown
        self.it_projects = jobs.filter(category='IT').count()
        self.non_it_projects = jobs.filter(category='NON-IT').count()
        self.finance_projects = jobs.filter(category='FINANCE').count()
        
        # Update current amount
        self.current_amount = self.total_order_amount
        
        self.save(update_fields=[
            'total_projects', 'completed_projects', 'cancelled_projects',
            'projects_with_issues', 'total_order_amount', 'total_paid_amount',
            'remaining_amount', 'it_projects', 'non_it_projects', 'finance_projects',
            'current_amount'
        ])


class CustomerActionLog(models.Model):
    """Audit log for customer actions"""
    
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
        ('kpi_updated', 'KPI Updated'),
    ]
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='action_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'customer_action_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.customer.customer_id} - {self.action} at {self.timestamp}"
