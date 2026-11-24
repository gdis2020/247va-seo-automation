
import requests
from bs4 import BeautifulSoup
import csv

SITE_URL = "https://247virtualassistants.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; SEOChecker/1.0)"
}

try:
    response = requests.get(
        SITE_URL,
        headers=headers,
        timeout=20
    )

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract page title
    title = soup.title.get_text(strip=True) if soup.title else ""

    # Extract meta description
    description_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )
    description = (
        description_tag.get("content", "")
        if description_tag else ""
    )

    # Extract H1
    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(" ", strip=True) if h1_tag else ""

    # Extract canonical URL
    canonical_tag = soup.find(
        "link",
        rel="canonical"
    )
    canonical = (
        canonical_tag.get("href", "")
        if canonical_tag else ""
    )

    # Check noindex
    robots_tag = soup.find(
        "meta",
        attrs={"name": "robots"}
    )
    robots = (
        robots_tag.get("content", "")
        if robots_tag else ""
    )

    noindex = "yes" if "noindex" in robots.lower() else "no"

    # Save results to CSV
    with open("seo_report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "URL",
            "Status Code",
            "Title",
            "Meta Description",
            "H1",
            "Canonical",
            "Noindex"
        ])

        writer.writerow([
            SITE_URL,
            response.status_code,
            title,
            description,
            h1,
            canonical,
            noindex
        ])

    print("SEO check completed!")
    print("HTTP Status:", response.status_code)
    print("Title:", title)
    print("Meta Description:", description)
    print("H1:", h1)
    print("Canonical:", canonical)
    print("Noindex:", noindex)
    print("Report saved as seo_report.csv")

except requests.RequestException as error:
    print("Website request failed:", error)

