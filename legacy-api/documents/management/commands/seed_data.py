from django.core.management.base import BaseCommand
from documents.models import Category, Author, Document, StatusHistory
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Seed the dataase with sample federal documents"

    def handle(self, *args, **options):
        # Categories  (real GPO **Government Publishing Office** document types)
        categories = [
            ("Congresssional Record", "CR", "Daily proceedings of Congress"),
             ("Federal Register", "FR", "Daily journal of the federal government"),
            ("Code of Federal Regulations", "CFR", "Codification of federal rules"),
            ("Public Law", "PL", "Enacted legislation"),
            ("Executive Order", "EO", "Presidential directives")
        ]
    
        cat_objects = {}
        for name, code, description in categories:
            cat, _ = Category.objects.get_or_create(
                code=code, defaults={"name":name, "description":description}
                )
            cat_objects[code] = cat
        
        # Authors (goverment agencies)
        authors = [
            ("Office of the Federal Register", "National Archives", "ofr@nara.gov"),
            ("Government Publishing Office", "GPO", "publications@gpo.gov"),
            ("Congressional Record Office", "U.S. Congress", "cro@congress.gov"),
            ("Office of Management and Budget", "Executive Office", "omb@whitehouse.gov"),
            ("Department of Justice", "DOJ", "publications@doj.gov")
        ]

        author_objects = {}
        for name, agency, email in authors:
            author, _ = Author.objects.get_or_create(
                email=email, defaults={"name": name, "agency": agency}
            )
            author_objects[email] = author

        # Documents in various statuses
        now = timezone.now()
        documents = [
            {
                "title": "Daily Congressional Proceedings Vol. 172 No. 89",
                "document_number": "CR-2026-0089",
                "category": cat_objects["CR"],
                "author": author_objects["cro@congress.gov"],
                "status": "published",
                "content_summary": "Complete record of House and Senate proceedings for May 12, 2026",
                "page_count": 142,
                "published_date": now - timedelta(days=1),
            },
            {
                "title": "Federal Register Vol. 91 No. 94",
                "document_number": "FR-2026-0094",
                "category": cat_objects["FR"],
                "author": author_objects["ofr@nara.gov"],
                "status": "review",
                "content_summary": "Proposed rules, notices, and presidential documents for federal publication",
                "page_count": 256,
            },
            {
                "title": "Executive Order on Federal Cybersecurity Standards",
                "document_number": "EO-2026-14157",
                "category": cat_objects["EO"],
                "author": author_objects["omb@whitehouse.gov"],
                "status": "approved",
                "content_summary": "Establishes minimum cybersecurity standards for all federal agencies",
                "page_count": 18,
            },
            {
                "title": "Public Law 119-42: Federal IT Modernization Act",
                "document_number": "PL-119-42",
                "category": cat_objects["PL"],
                "author": author_objects["cro@congress.gov"],
                "status": "published",
                "content_summary": "Authorizes funding for legacy system modernization across federal agencies",
                "page_count": 34,
                "published_date": now - timedelta(days=30),
            },
            {
                "title": "CFR Title 44 Revision: Public Printing and Documents",
                "document_number": "CFR-44-2026-R1",
                "category": cat_objects["CFR"],
                "author": author_objects["publications@gpo.gov"],
                "status": "draft",
                "content_summary": "Annual revision of regulations governing government publishing operations",
                "page_count": 89,
            },
            {
                "title": "Federal Register Notice: API Modernization Standards",
                "document_number": "FR-2026-N-0051",
                "category": cat_objects["FR"],
                "author": author_objects["publications@gpo.gov"],
                "status": "draft",
                "content_summary": "Proposed standards for federal agency API development and documentation",
                "page_count": 12,
            },
            {
                "title": "Congressional Record: Debate on Infrastructure Spending",
                "document_number": "CR-2026-0085",
                "category": cat_objects["CR"],
                "author": author_objects["cro@congress.gov"],
                "status": "published",
                "content_summary": "Senate floor debate on FY2027 infrastructure appropriations",
                "page_count": 78,
                "published_date": now - timedelta(days=5),
            },
            {
                "title": "Executive Order on Government Data Transparency",
                "document_number": "EO-2026-14158",
                "category": cat_objects["EO"],
                "author": author_objects["omb@whitehouse.gov"],
                "status": "review",
                "content_summary": "Directs agencies to publish machine-readable data inventories",
                "page_count": 15,
            },
            {
                "title": "DOJ Guidance on Digital Records Retention",
                "document_number": "DOJ-2026-G-003",
                "category": cat_objects["FR"],
                "author": author_objects["publications@doj.gov"],
                "status": "approved",
                "content_summary": "Updated guidance for federal digital records retention and disposition",
                "page_count": 42,
            },
            {
                "title": "Public Law 119-45: Open Government Data Act Amendments",
                "document_number": "PL-119-45",
                "category": cat_objects["PL"],
                "author": author_objects["cro@congress.gov"],
                "status": "archived",
                "content_summary": "Amendments requiring all federal data to be published in open formats",
                "page_count": 22,
                "published_date": now - timedelta(days=120),
            },
        ]
        documents_objects = {}
        for doc_data in documents:
            doc, created = Document.objects.get_or_create(
                document_number=doc_data["document_number"],
                defaults=doc_data
            )
            if created:
                # Add initial status history
                StatusHistory.objects.create(
                    document=doc,
                    old_status="",
                    new_status="draft",
                    changed_by="system",
                    notes="Document created"
                )
                # Add transitions for non-draft documents
                if doc.status != "draft":
                    transitions = {
                        "review": ["review"],
                        "approved": ["review", "approved"],
                        "published": ["review", "approved", "published"],
                        "archived": ["review", "approved", "published", "archived"]
                    }
                    prev = "draft"
                    for s in transitions.get(doc.status,[]):
                        StatusHistory.objects.create(
                            document=doc,
                            old_status=prev,
                            new_status=s,
                            changed_by="system",
                           notes=f"Transitioned to {s}"
                        )
                        prev = s

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {Category.objects.count()} categories, "
            f"{Author.objects.count()} authors, "
            f"{Document.objects.count()} documents"
        ))
        
