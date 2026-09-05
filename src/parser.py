import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

HOTEL_ID_PATTERN = re.compile(r"hotel\-id\s?=\s?'(\d+)'")


def parse_hotel_id_from_html(html: str) -> str | None:
    match = HOTEL_ID_PATTERN.search(html)
    if match:
        return match.group(1)

    return None


def ensure_search_scope(url: str) -> str:
    """Ensure the hotel URL requests the server-rendered offer view.

    TUI only server-renders the hotel offer page (which embeds the hotel id)
    when the ``searchScope=HOTEL`` query parameter is present.
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["searchScope"] = ["HOTEL"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))
