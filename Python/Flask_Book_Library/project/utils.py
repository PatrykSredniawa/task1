import re
import bleach
from flask import jsonify

ALLOWED_TAGS = []
ALLOWED_ATTRS = {}


SAFE_TEXT_RE = re.compile(r"^[\w\s\-\.,:;!?'\"()ąćęłńóśżźĄĆĘŁŃÓŚŻŹ]*$", re.UNICODE)

def sanitize_text(value: str, max_len: int = 200):
    """Trim, sanitize HTML (usuń tagi) i sprawdź długość/znaki.
       Zwraca oczyszczony string lub rzuca ValueError."""
    if value is None:
        return ''
    v = str(value).strip()
    if len(v) == 0:
        return ''
    if len(v) > max_len:
        raise ValueError("Too long")
    cleaned = bleach.clean(v, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    if not SAFE_TEXT_RE.match(cleaned):
        raise ValueError("Contains disallowed characters")
    return cleaned
