from rest_framework import serializers
from .models import Category, Author, Document, StatusHistory

class CategorySerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField(source="documents.count", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "code", "description", "document_count"]

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "agency", "email"]

class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusHistory
        fields = ["id", "old_status", "new_status", "changed_by", "changed_at", "notes"]

class DocumentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category_name = serializers.CharField(source="category.name", read_only=True)
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Document
        fields = [
            "id", "title", "document_number", "category", "category_name",
            "author", "author_name", "status", "page_count",
            "submitted_date", "published_date"
        ]

class DocumentDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested data for detail views."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )
    status_history = StatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            "id", "title", "document_number", "category", "category_id",
            "author", "author_id", "status", "content_summary", "page_count",
            "submitted_date", "published_date", "updated_at", "status_history"
        ]