"""
InstaSpy v3.0 — Contact Extractor
Extract email, phone, social links from bio text.
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ContactInfo:
    emails: List[str]
    phones: List[str]
    whatsapp: Optional[str]
    telegram: Optional[str]
    snapchat: Optional[str]
    tiktok: Optional[str]
    websites: List[str]
    locations: List[str]

class ContactExtractor:
    """Extract contact information from text"""

    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_PATTERN = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
    WEBSITE_PATTERN = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'

    def extract(self, text: str) -> ContactInfo:
        """Extract all contact info from text"""

        # Extract emails
        emails = list(set(re.findall(self.EMAIL_PATTERN, text)))

        # Extract phones
        phones = list(set(re.findall(self.PHONE_PATTERN, text)))
        phones = [p for p in phones if len(re.sub(r'\D', '', p)) >= 10]

        # Extract WhatsApp
        whatsapp = self._extract_whatsapp(text)

        # Extract Telegram
        telegram = self._extract_telegram(text)

        # Extract Snapchat
        snapchat = self._extract_snapchat(text)

        # Extract TikTok
        tiktok = self._extract_tiktok(text)

        # Extract websites
        websites = list(set(re.findall(self.WEBSITE_PATTERN, text)))

        # Extract locations
        locations = self._extract_locations(text)

        return ContactInfo(
            emails=emails,
            phones=phones,
            whatsapp=whatsapp,
            telegram=telegram,
            snapchat=snapchat,
            tiktok=tiktok,
            websites=websites,
            locations=locations
        )

    def _extract_whatsapp(self, text: str) -> Optional[str]:
        """Extract WhatsApp number"""
        patterns = [
            r'(?:wa\.me/|whatsapp:\s*)(\+?\d+)',
            r'(?:WhatsApp|WA)[:\s]*(\+?\d[\d\s\-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_telegram(self, text: str) -> Optional[str]:
        """Extract Telegram username"""
        patterns = [
            r'(?:t\.me/|telegram:|tg:)\s*@?(\w{5,})',
            r'(?:Telegram|TG)[:\s]*@(\w{5,})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_snapchat(self, text: str) -> Optional[str]:
        """Extract Snapchat username"""
        patterns = [
            r'(?:snapchat:|snap:|sc:)\s*@?(\w{3,})',
            r'(?:Snapchat|SC)[:\s]*@(\w{3,})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_tiktok(self, text: str) -> Optional[str]:
        """Extract TikTok username"""
        patterns = [
            r'(?:tiktok:|tt:)\s*@?(\w{3,})',
            r'(?:TikTok|TT)[:\s]*@(\w{3,})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_locations(self, text: str) -> List[str]:
        """Extract location mentions from text"""
        # Common location indicators
        indicators = ['from', 'in', 'based in', 'living in', 'located in', '📍', '🌍', '🏠', '📌']

        locations = []
        text_lower = text.lower()

        for indicator in indicators:
            if indicator in text_lower:
                # Extract text after indicator
                idx = text_lower.index(indicator) + len(indicator)
                remaining = text[idx:idx + 50].strip()

                # Clean up
                location = re.split(r'[,;.\n]', remaining)[0].strip()
                if location and len(location) > 2:
                    locations.append(location)

        return list(set(locations))

if __name__ == '__main__':
    extractor = ContactExtractor()
    test_bio = "📍 Paris, France | Email: test@example.com | WhatsApp: +33612345678 | Telegram: @mychannel"
    contacts = extractor.extract(test_bio)
    print(f"Emails: {contacts.emails}")
    print(f"Phones: {contacts.phones}")
    print(f"WhatsApp: {contacts.whatsapp}")
    print(f"Telegram: {contacts.telegram}")
    print(f"Locations: {contacts.locations}")
