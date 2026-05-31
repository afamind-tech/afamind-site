from flask import Flask, render_template, request, flash, abort, Response
from services.messaging import send_teams_message
import secrets
from dotenv import load_dotenv
import os
import glob as file_glob
import re
from datetime import datetime, timezone
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from markupsafe import Markup
import bleach
import frontmatter as fm
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

BOOKINGS_URL = os.getenv("BOOKINGS_URL", "")
BASE_URL = "https://afamind.com"
ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "articles")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ARTICLE_LEVELS = {
    "decouverte": "Découverte",
    "intermediaire": "Intermédiaire",
    "avance": "Avancé",
}
START_HERE_SLUGS = [
    "microsoft-fabric-c-est-quoi",
    "pourquoi-j-ecris-sur-microsoft-fabric",
    "fonctionnalites-phares-microsoft-fabric",
]

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "a", "ul", "ol", "li",
    "blockquote", "h1", "h2", "h3", "h4", "h5", "h6",
    "code", "pre", "span", "div", "img", "figure", "figcaption",
    "table", "thead", "tbody", "tr", "th", "td", "hr",
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "target", "class", "id"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "span": ["class"],
    "div": ["class"],
    "code": ["class"],
    "pre": ["class"],
    "h1": ["id"], "h2": ["id"], "h3": ["id"],
    "h4": ["id"], "h5": ["id"], "h6": ["id"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]
MONTHS_FR = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


@app.template_filter("date_fr")
def date_fr(value, short=False):
    if not value:
        return ""
    month = MONTHS_FR[value.month - 1]
    if short:
        return f"{value.day:02d} {month[:3]} {value.year}"
    return f"{value.day:02d} {month} {value.year}"


# â”€â”€ Article helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _slug_from(post, filepath):
    slug = post.metadata.get("slug") or os.path.splitext(os.path.basename(filepath))[0]
    return str(slug).strip()


def _validate_slug(slug):
    if not SLUG_RE.fullmatch(slug):
        raise ValueError(f"Invalid article slug: {slug}")
    return slug


def _clean_tags(tags):
    if not isinstance(tags, list):
        return []
    cleaned = []
    for tag in tags:
        tag = str(tag).strip().lower()
        if TAG_RE.fullmatch(tag):
            cleaned.append(tag)
    return cleaned


def _clean_level(level):
    if not level:
        return None
    key = str(level).strip().lower()
    if key not in ARTICLE_LEVELS:
        return None
    return {
        "key": key,
        "label": ARTICLE_LEVELS[key],
    }


def _clean_serie(serie):
    if not serie:
        return ""
    return str(serie).strip()[:120]


def _clean_serie_ordre(serie_ordre):
    if serie_ordre in (None, ""):
        return None
    try:
        return int(serie_ordre)
    except (TypeError, ValueError):
        return None


def _clean_cover(cover):
    if not cover:
        return ""
    cover = str(cover).strip()
    if cover.startswith("/static/"):
        return cover
    parsed = urlparse(cover)
    if parsed.scheme == "https" and parsed.netloc:
        return cover
    return ""


def _cover_url(cover):
    if not cover:
        return ""
    if cover.startswith("https://"):
        return cover
    return f"{BASE_URL}{cover}"


def _parse_date(d):
    if isinstance(d, str):
        return datetime.strptime(d, "%Y-%m-%d").date()
    return d


def _reading_time(content):
    return max(1, round(len(content.split()) / 200))


def _sanitize_html(html):
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def _render_md(content):
    md = markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(linenums=False, guess_lang=False, noclasses=False, css_class="highlight"),
            TableExtension(),
            TocExtension(permalink="#", permalink_class="heading-anchor", permalink_title="Lien permanent"),
            "attr_list",
        ]
    )
    return _sanitize_html(md.convert(content))


def get_all_articles(include_drafts=False):
    articles = []
    if not os.path.isdir(ARTICLES_DIR):
        return articles
    for filepath in file_glob.glob(os.path.join(ARTICLES_DIR, "*.md")):
        post = fm.load(filepath)
        if post.metadata.get("draft", False) and not include_drafts:
            continue
        try:
            slug = _validate_slug(_slug_from(post, filepath))
        except ValueError:
            continue
        date = _parse_date(post.metadata.get("date"))
        articles.append({
            "slug": slug,
            "title": post.metadata.get("title", "Sans titre"),
            "date": date,
            "excerpt": post.metadata.get("excerpt", ""),
            "tags": _clean_tags(post.metadata.get("tags", [])),
            "level": _clean_level(post.metadata.get("level")),
            "serie": _clean_serie(post.metadata.get("serie", "")),
            "serie_ordre": _clean_serie_ordre(post.metadata.get("serie_ordre")),
            "cover": _clean_cover(post.metadata.get("cover", "")),
            "reading_time": _reading_time(post.content),
            "draft": post.metadata.get("draft", False),
        })
    articles.sort(key=lambda a: a["date"], reverse=True)
    return articles


def get_start_here_articles(articles):
    by_slug = {article["slug"]: article for article in articles}
    return [by_slug[slug] for slug in START_HERE_SLUGS if slug in by_slug]


def get_series_navigation(current_slug, serie):
    serie = _clean_serie(serie)
    if not serie:
        return None

    series_articles = [
        article for article in get_all_articles()
        if article.get("serie") == serie
    ]
    if len(series_articles) < 2:
        return None

    series_articles.sort(key=lambda article: (
        article["serie_ordre"] is None,
        article["serie_ordre"] if article["serie_ordre"] is not None else 0,
        article["date"],
        article["slug"],
    ))

    current_index = next(
        (index for index, article in enumerate(series_articles) if article["slug"] == current_slug),
        None,
    )
    if current_index is None:
        return None

    return {
        "name": serie,
        "previous": series_articles[current_index - 1] if current_index > 0 else None,
        "next": series_articles[current_index + 1] if current_index < len(series_articles) - 1 else None,
    }


def _find_article(slug):
    if not os.path.isdir(ARTICLES_DIR):
        return None, None
    try:
        slug = _validate_slug(slug)
    except ValueError:
        return None, None
    for filepath in file_glob.glob(os.path.join(ARTICLES_DIR, "*.md")):
        post = fm.load(filepath)
        try:
            article_slug = _validate_slug(_slug_from(post, filepath))
        except ValueError:
            continue
        if article_slug == slug:
            return filepath, post
    return None, None


# â”€â”€ Existing routes â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/send-message", methods=["POST"])
def send_message():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not subject or not message:
        flash("Tous les champs obligatoires doivent Ãªtre renseignÃ©s.", "error")
        return render_template("contact.html")

    message_with_subject = f"[Objet : {subject}]\n\n{message}"
    send_teams_message(name, email, message_with_subject)

    flash("Votre message a bien Ã©tÃ© envoyÃ© sur Teams. Merci !", "success")
    return render_template("confirmation.html", name=name)


@app.route("/rendez-vous")
def rendez_vous():
    return render_template("rendez-vous.html", bookings_url=BOOKINGS_URL)


@app.route("/a-propos")
def a_propos():
    return render_template("a-propos.html")


@app.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions-legales.html")


@app.route("/confidentialite")
def confidentialite():
    return render_template("confidentialite.html")


# â”€â”€ Articles â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@app.route("/articles")
def articles_index():
    articles = get_all_articles()
    start_here_articles = get_start_here_articles(articles)
    available_level_keys = {a["level"]["key"] for a in articles if a["level"]}
    all_levels = [
        {"key": key, "label": label}
        for key, label in ARTICLE_LEVELS.items()
        if key in available_level_keys
    ]
    all_tags = sorted({tag for a in articles for tag in a["tags"]})
    return render_template(
        "articles_index.html",
        articles=articles,
        start_here_articles=start_here_articles,
        all_levels=all_levels,
        all_tags=all_tags,
    )


@app.route("/articles/feed.xml")
def articles_feed():
    articles = get_all_articles()
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_rfc3339(d):
        return f"{d.isoformat()}T00:00:00Z"

    ET.register_namespace("", "http://www.w3.org/2005/Atom")
    feed = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")
    ET.SubElement(feed, "title").text = "Afamind - Articles"
    ET.SubElement(feed, "link", href=f"{BASE_URL}/articles", rel="alternate")
    ET.SubElement(feed, "link", href=f"{BASE_URL}/articles/feed.xml", rel="self")
    ET.SubElement(feed, "id").text = f"{BASE_URL}/articles/feed.xml"
    ET.SubElement(feed, "updated").text = now_iso
    author = ET.SubElement(feed, "author")
    ET.SubElement(author, "name").text = "Anas Fata"
    ET.SubElement(author, "uri").text = BASE_URL

    for a in articles:
        article_url = f"{BASE_URL}/articles/{a['slug']}"
        entry = ET.SubElement(feed, "entry")
        ET.SubElement(entry, "title").text = str(a["title"])
        ET.SubElement(entry, "link", href=article_url)
        ET.SubElement(entry, "id").text = article_url
        ET.SubElement(entry, "updated").text = to_rfc3339(a["date"])
        ET.SubElement(entry, "summary").text = str(a["excerpt"])

    xml = ET.tostring(feed, encoding="utf-8", xml_declaration=True)
    return Response(xml, mimetype="application/atom+xml; charset=utf-8")

@app.route("/articles/<slug>")
def article_detail(slug):
    filepath, post = _find_article(slug)
    if filepath is None or post.metadata.get("draft", False):
        abort(404)

    meta = post.metadata
    canonical_slug = _validate_slug(str(meta.get("slug") or slug).strip())
    body_html = Markup(_render_md(post.content))
    date = _parse_date(meta.get("date"))
    cover = _clean_cover(meta.get("cover", ""))
    serie = _clean_serie(meta.get("serie", ""))
    serie_ordre = _clean_serie_ordre(meta.get("serie_ordre"))

    article = {
        "slug": canonical_slug,
        "title": meta.get("title", "Sans titre"),
        "date": date,
        "excerpt": meta.get("excerpt", ""),
        "tags": _clean_tags(meta.get("tags", [])),
        "level": _clean_level(meta.get("level")),
        "serie": serie,
        "serie_ordre": serie_ordre,
        "cover": cover,
        "cover_url": _cover_url(cover),
        "reading_time": _reading_time(post.content),
        "body": body_html,
    }
    series_navigation = get_series_navigation(canonical_slug, serie)
    return render_template(
        "article_detail.html",
        article=article,
        base_url=BASE_URL,
        series_navigation=series_navigation,
    )


# â”€â”€ Sitemap â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@app.route("/sitemap.xml")
def sitemap():
    articles = get_all_articles()
    today = datetime.now(timezone.utc).date().isoformat()

    static_pages = [
        {"loc": f"{BASE_URL}/",             "changefreq": "monthly", "priority": "1.0", "lastmod": today},
        {"loc": f"{BASE_URL}/a-propos",     "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{BASE_URL}/rendez-vous",  "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{BASE_URL}/contact",      "changefreq": "yearly",  "priority": "0.5"},
        {"loc": f"{BASE_URL}/articles",     "changefreq": "weekly",  "priority": "0.9", "lastmod": today},
    ]

    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for p in static_pages:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = p["loc"]
        if "lastmod" in p:
            ET.SubElement(url, "lastmod").text = p["lastmod"]
        ET.SubElement(url, "changefreq").text = p["changefreq"]
        ET.SubElement(url, "priority").text = p["priority"]

    for a in articles:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{BASE_URL}/articles/{a['slug']}"
        ET.SubElement(url, "lastmod").text = a["date"].isoformat()
        ET.SubElement(url, "changefreq").text = "monthly"
        ET.SubElement(url, "priority").text = "0.8"

    xml = ET.tostring(urlset, encoding="utf-8", xml_declaration=True)
    return Response(xml, mimetype="application/xml; charset=utf-8")

# â”€â”€ Error handlers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")


