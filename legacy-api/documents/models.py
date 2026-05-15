from django.db import models

class Category(models.Model):
    """Document categories (e.g., Congressional Record, Federal Register)."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]  # Default sort: alphabetical by name in all queries

    def __str__(self):
        return self.name
    
class Author(models.Model):
    """Government authors/agencies that submit documents."""
    name = models.CharField(max_length=200)
    agency = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return f"{self.name} ({self.agency})"

class Document(models.Model):
    """Federal document being tracked through the publishing lifecycle."""
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "Under Review"),
        ("approved", "Approved"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=500)
    document_number = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="documents")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="documents")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    content_summary = models.TextField(blank=True)
    page_count = models.IntegerField(default=0)
    submitted_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_date"]
    
    def __str__(self):
	    return f"{self.document_number}: {self.title}"
    
class StatusHistory(models.Model):
    """Audit trail for document status changes."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="status_history")
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.CharField(max_length=100, default="system")
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "status histories"
        ordering = ["-changed_at"]
    
    def __str__(self):
        return f"{self.document.document_number}: {self.old_status} -> {self.new_status}"