"""
Daily Publishing Report - Workflow Automation

Queries the middleware API and generates a summary of document
publishing status. In production, this would run on a schedule
and send notifications to stakeholders.

Demonstrates the "workflow automation"
"""
import httpx
import asyncio
from datetime import datetime


MIDDLEWARE_URL = "http://127.0.0.1:8001/api/v1"
API_KEY = "dev-api-key-change-in-production"
HEADERS = {"X-API-Key": API_KEY}

async def generate_report():
    async with httpx.AsyncClient() as client:
        # Get stats
        stats_resp = await client.get(f"{MIDDLEWARE_URL}", HEADERS=HEADERS)
        stats = stats_resp.json()

        # Get documents under review (potential bottlenecks)
        review_resp = await client.get(
            f"{MIDDLEWARE_URL}/documents/?status=review", headers=HEADERS
        )
        in_review = review_resp.json()

        # Generate report
        print(f"\n{'='*60}")
        print(f"    DAILY PUBLISHING REPORT")
        print(f"    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'n'*60}")

        print(f"\n  SUMMARY")
        print(f"  Total documents: {stats['total_documents']}")
        print(f"  Categories: {stats['categories']}")
        print(f"  Authors/Agencies: {stats['authors']}")

        print(f"\n  STATUS BREAKDOWN")
        for status, count in stats["by_status"].items():
            bar = "#" * count
            print(f"    {status:12s}: {count:3d} {bar}")

            if in_review:
                print(f"\n  DOCUMENTS PENDING REVIEW ({len(in_review)})")
                for doc in in_review:
                    print(f"    - {doc['document_number']}: {doc['title'][:50]}")

            print(f"\n{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(generate_report())