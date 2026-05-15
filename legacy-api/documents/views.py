from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Category, Author, Document, StatusHistory

# Alternative: use backslash \ at end of each line, but parentheses are cleaner
from .serializers import (
    CategorySerializer, AuthorSerializer,
    DocumentListSerializer, DocumentDetailSerializer,
    StatusHistorySerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "code"]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["agency"]
    search_fields = ["name", "agency", "email"]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related("category", "author").all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "category", "author"]
    search_fields = ["title", "document_number", "content_summary"]
    ordering_fields = ["submitted_date", "published_date", "title", "status"]

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentListSerializer
        return DocumentDetailSerializer
    
    @action(detail=True, methods=["post"])
    def transition(self, request, pk=None):
        """Transition a document to a new status with audit logging."""
        document = self.get_object()
        new_status = request.data.get("status")
        notes = request.data.get("notes", "")
        changed_by = request.data.get("changed_by", "system")

        valid_statuses = [choice[0] for choice in Document.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = document.status

        # Create audit record
        StatusHistory.objects.create(
            document=document,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            notes=notes
        )

        # Update document
        document.status = new_status
        if new_status == "published":
            document.published_date = timezone.now()
        document.save()

        serializer = DocumentDetailSerializer(document)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def stats(self, request):
        """Return publishing statistics."""
        total = Document.objects.count()
        by_status = {}
        for choice in Document.STATUS_CHOICES:
            by_status[choice[0]] = Document.objects.filter(status=choice[0]).count()
        
        return Response({
            "total": total,
            "by_status": by_status,
            "categories": Category.objects.count(),
            "authors": Author.objects.count()
        })