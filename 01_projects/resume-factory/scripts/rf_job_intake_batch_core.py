import pathlib
import sys
import re
from typing import Optional, Dict

import requests
from bs4 import BeautifulSoup

def die(msg, code=2):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def valid_url(u: str) -> bool:
    return re.match(r"^https?://", u) is not None

def read_urls_file(path: str):
    p = pathlib.Path(path)
    if not p.exists():
        die(f"URLs file not found: {path}")
    urls = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if not valid_url(line):
            die(f"Invalid URL in file: {line}")
        urls.append(line)
    if not urls:
        die("No valid URLs found in file.")
    return urls

def fetch_html(url: str, timeout: int = 30, verify_ssl: bool = True) -> str:
    if not valid_url(url):
        die(f"Invalid URL: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    r = requests.get(url, headers=headers, timeout=timeout, verify=verify_ssl)
    r.raise_for_status()
    # requests will guess encoding; keep forgiving decode
    r.encoding = r.encoding or "utf-8"
    return r.text

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)



def extract_title_from_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return None

def scrape_job_page(url: str, verify_ssl: bool = True) -> Dict[str, Optional[str]]:
    html = fetch_html(url, verify_ssl=verify_ssl)
    page_title = extract_title_from_html(html)
    text = html_to_text(html)
    if not text.strip():
        die("Extracted text is empty (likely JS-rendered page).")

    # v1: no structured parsing yet (company/role extracted later or via AI)
    provisional_company, provisional_role = derive_from_title(page_title)

    return {
        "company": provisional_company,
        "page_title": page_title,
        "role_title": provisional_role,
        "description": text,
        "location": None,
        "source": url,
    }


def slugify_snake(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text

def slugify_kebab(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def derive_from_title(page_title: str | None):
    if not page_title:
        return None, None

    # common patterns: "Role - Company" or "Role | Company"
    parts = re.split(r"\s[-|]\s", page_title)
    if len(parts) >= 2:
        role = parts[0].strip()
        company = parts[1].strip()
        return company, role

    # fallback: unknown
    return None, page_title.strip()
