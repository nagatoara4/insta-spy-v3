"""
InstaSpy v3.0 — Instagram Meta Extractor
Extract public data from Instagram profile page.
Works on iSH — uses mobile user agent to avoid blocks.
"""

import re
import requests
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class InstagramMeta:
    username: str
    full_name: Optional[str]
    biography: Optional[str]
    followers: Optional[str]
    following: Optional[str]
    posts: Optional[str]
    profile_pic: Optional[str]
    is_private: bool
    is_verified: bool
    external_url: Optional[str]

class InstagramMetaExtractor:
    """Extract public Instagram data from profile page"""

    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout
        self.session = requests.Session()
        # Use mobile user agent — less likely to be blocked
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'

    def extract(self, username: str) -> Optional[InstagramMeta]:
        """Extract Instagram profile metadata"""
        try:
            url = f"https://www.instagram.com/{username}/"
            r = self.session.get(url, timeout=self.timeout)

            if r.status_code != 200:
                return None

            html = r.text

            # Extract og:description (contains follower counts)
            desc = self._extract_og(html, 'description')

            # Extract og:title
            title = self._extract_og(html, 'title')

            # Extract og:image (profile pic)
            image = self._extract_og(html, 'image')

            # Parse description for counts
            followers, following, posts = self._parse_counts(desc)

            # Check if private
            is_private = self._check_private(html, desc)

            # Check if verified
            is_verified = self._check_verified(html, title)

            # Extract external URL
            external_url = self._extract_external_url(html)

            # Extract full name from title
            full_name = self._extract_full_name(title)

            return InstagramMeta(
                username=username,
                full_name=full_name,
                biography=desc[:150] if desc else None,
                followers=followers,
                following=following,
                posts=posts,
                profile_pic=image,
                is_private=is_private,
                is_verified=is_verified,
                external_url=external_url
            )

        except Exception as e:
            print(f"Error extracting Instagram meta: {e}")
            return None

    def _extract_og(self, html: str, property: str) -> Optional[str]:
        """Extract Open Graph meta tag"""
        patterns = [
            rf'property="og:{property}" content="([^"]+)"',
            rf'name="og:{property}" content="([^"]+)"',
            rf'content="([^"]+)" property="og:{property}"',
        ]

        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return None

    def _parse_counts(self, desc: Optional[str]) -> tuple:
        """Parse follower/following/post counts from description"""
        if not desc:
            return None, None, None

        followers = self._extract_number(desc, r'([\d.,]+[KM]?)\s*Followers?')
        following = self._extract_number(desc, r'([\d.,]+[KM]?)\s*Following')
        posts = self._extract_number(desc, r'([\d.,]+[KM]?)\s*Posts?')

        return followers, following, posts

    def _extract_number(self, text: str, pattern: str) -> Optional[str]:
        """Extract number from text using pattern"""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None

    def _check_private(self, html: str, desc: Optional[str]) -> bool:
        """Check if account is private"""
        indicators = [
            '"is_private":true',
            'This Account is Private',
            'Private Account',
            'This account is private',
        ]

        if desc and 'private' in desc.lower():
            return True

        return any(ind in html for ind in indicators)

    def _check_verified(self, html: str, title: Optional[str]) -> bool:
        """Check if account is verified"""
        if title and '✓' in title:
            return True

        return '"is_verified":true' in html or 'verified' in html.lower()[:1000]

    def _extract_external_url(self, html: str) -> Optional[str]:
        """Extract external URL from profile"""
        pattern = r'"external_url":"([^"]+)"'
        match = re.search(pattern, html)

        if match:
            url = match.group(1).replace('\\u0026', '&').replace('\\/', '/')
            return url

        # Try og:url as fallback
        return self._extract_og(html, 'url')

    def _extract_full_name(self, title: Optional[str]) -> Optional[str]:
        """Extract full name from title"""
        if not title:
            return None

        # Title format: "Name (@username) • Instagram" or similar
        match = re.match(r'^([^(@]+)', title)
        if match:
            return match.group(1).strip()

        return None

if __name__ == '__main__':
    extractor = InstagramMetaExtractor()
    print("Extracting Instagram meta for 'zuck'...")
    meta = extractor.extract('zuck')
    if meta:
        print(f"Name: {meta.full_name}")
        print(f"Followers: {meta.followers}")
        print(f"Following: {meta.following}")
        print(f"Posts: {meta.posts}")
        print(f"Private: {meta.is_private}")
        print(f"Verified: {meta.is_verified}")
    else:
        print("Could not extract (Instagram may be blocking)")
