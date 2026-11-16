"""Measurements that can be taken from a URL string alone, with no page fetch.

Both the notebook and the Streamlit app import this file, so the numbers used to train the
model are computed by exactly the same code that later scores a typed address.
"""

import re
from urllib.parse import urlparse

FEATURE_NAMES = [
    "URLLength",
    "DomainLength",
    "TLDLength",
    "NoOfSubDomain",
    "IsHTTPS",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsDomainIP",
]


def features_from_url(url):
    """Return the fifteen measurements for one URL string."""
    url = str(url)
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    top_level = host.split(".")[-1] if host else ""
    length = len(url)

    letters = 0
    digits = 0
    specials = 0
    for character in url:
        if character.isalpha():
            letters += 1
        elif character.isdigit():
            digits += 1
        elif not character.isalnum():
            specials += 1

    address = host.split(":")[0]
    is_ip_address = 1 if re.fullmatch(r"[\d.]+", address or "x") else 0

    return {
        "URLLength": length,
        "DomainLength": len(host),
        "TLDLength": len(top_level),
        "NoOfSubDomain": max(host.count(".") - 1, 0),
        "IsHTTPS": 1 if parsed.scheme == "https" else 0,
        "NoOfLettersInURL": letters,
        "LetterRatioInURL": letters / length,
        "NoOfDegitsInURL": digits,
        "DegitRatioInURL": digits / length,
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "NoOfOtherSpecialCharsInURL": specials,
        "SpacialCharRatioInURL": specials / length,
        "IsDomainIP": is_ip_address,
    }
