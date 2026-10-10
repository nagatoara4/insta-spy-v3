#!/usr/bin/env python3
"""
InstaSpy v3.0 — Command Line Interface
Professional Instagram OSINT Tool — Works on iSH arm64
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from insta_spy.search.username_search import UsernameSearch
from insta_spy.extract.instagram_meta import InstagramMetaExtractor
from insta_spy.extract.contact_extractor import ContactExtractor
from insta_spy.report.json_reporter import JSONReporter

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def banner():
    print(f"""{Colors.RED}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ██╗███╗   ██╗███████╗████████╗ █████╗     ███████╗██████╗ ██╗   ██╗║
║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝██╔══██╗╚██╗ ██╔╝║
║   ██║██╔██╗ ██║███████╗   ██║   ███████║    ███████╗██████╔╝ ╚████╔╝ ║
║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ╚════██║██╔═══╝   ╚██╔╝  ║
║   ██║██║ ╚████║███████║   ██║   ██║  ██║    ███████║██║        ██║   ║
║   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝        ╚═╝   ║
║                                                                      ║
║              InstaSpy v3.0 — Professional Edition                    ║
║              Built by worm shadow for He                             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.END}""")

def cmd_search(args):
    """Search username across platforms"""
    print(f"\n{Colors.CYAN}[*] Searching for: @{args.username}{Colors.END}")
    print(f"{Colors.DIM}[*] Checking 100+ platforms...{Colors.END}\n")

    search = UsernameSearch()
    results = search.search(args.username)
    found = search.get_found_accounts(results)

    print(f"{Colors.GREEN}[+] Found {len(found)} accounts:{Colors.END}\n")

    for site, url in found.items():
        print(f"  {Colors.GREEN}✓{Colors.END} {site}: {url}")

    # Save report
    if args.output:
        reporter = JSONReporter()
        data = {
            'target': args.username,
            'social_accounts': found
        }
        reporter.save(data, args.output)
        print(f"\n{Colors.GREEN}[+] Report saved: {args.output}{Colors.END}")

def cmd_instagram(args):
    """Extract Instagram metadata"""
    print(f"\n{Colors.CYAN}[*] Extracting Instagram data for: @{args.username}{Colors.END}\n")

    extractor = InstagramMetaExtractor()
    meta = extractor.extract(args.username)

    if not meta:
        print(f"{Colors.RED}[-] Could not extract Instagram data{Colors.END}")
        print(f"{Colors.YELLOW}[!] Instagram may be blocking or profile doesn't exist{Colors.END}")
        return

    print(f"  {Colors.GREEN}✓{Colors.END} Username: @{meta.username}")
    if meta.full_name:
        print(f"  {Colors.GREEN}✓{Colors.END} Full Name: {meta.full_name}")
    if meta.followers:
        print(f"  {Colors.GREEN}✓{Colors.END} Followers: {meta.followers}")
    if meta.following:
        print(f"  {Colors.GREEN}✓{Colors.END} Following: {meta.following}")
    if meta.posts:
        print(f"  {Colors.GREEN}✓{Colors.END} Posts: {meta.posts}")
    print(f"  {Colors.GREEN}✓{Colors.END} Private: {'Yes 🔒' if meta.is_private else 'No 🌍'}")
    print(f"  {Colors.GREEN}✓{Colors.END} Verified: {'Yes ✅' if meta.is_verified else 'No'}")

    if meta.biography:
        print(f"\n  {Colors.CYAN}Bio:{Colors.END} {meta.biography[:100]}...")

    if meta.profile_pic:
        print(f"\n  {Colors.CYAN}Profile Pic:{Colors.END} {meta.profile_pic[:80]}...")

    if meta.external_url:
        print(f"  {Colors.CYAN}Website:{Colors.END} {meta.external_url}")

    # Extract contacts from bio
    if meta.biography:
        contact_extractor = ContactExtractor()
        contacts = contact_extractor.extract(meta.biography)

        if contacts.emails or contacts.phones or contacts.whatsapp:
            print(f"\n  {Colors.CYAN}Contacts Found:{Colors.END}")
            for email in contacts.emails:
                print(f"    {Colors.GREEN}✓{Colors.END} Email: {email}")
            for phone in contacts.phones:
                print(f"    {Colors.GREEN}✓{Colors.END} Phone: {phone}")
            if contacts.whatsapp:
                print(f"    {Colors.GREEN}✓{Colors.END} WhatsApp: {contacts.whatsapp}")
            if contacts.telegram:
                print(f"    {Colors.GREEN}✓{Colors.END} Telegram: @{contacts.telegram}")
            if contacts.locations:
                print(f"    {Colors.GREEN}✓{Colors.END} Location: {', '.join(contacts.locations)}")

    # Save report
    if args.output:
        reporter = JSONReporter()
        data = {
            'target': args.username,
            'instagram': {
                'username': meta.username,
                'full_name': meta.full_name,
                'followers': meta.followers,
                'following': meta.following,
                'posts': meta.posts,
                'is_private': meta.is_private,
                'is_verified': meta.is_verified,
                'biography': meta.biography,
                'profile_pic': meta.profile_pic,
                'external_url': meta.external_url
            }
        }
        reporter.save(data, args.output)
        print(f"\n{Colors.GREEN}[+] Report saved: {args.output}{Colors.END}")

def cmd_full(args):
    """Full OSINT scan"""
    print(f"\n{Colors.RED}{Colors.BOLD}[*] FULL OSINT SCAN — @{args.username}{Colors.END}\n")

    # Instagram
    print(f"{Colors.YELLOW}[1] Instagram Analysis{Colors.END}")
    extractor = InstagramMetaExtractor()
    meta = extractor.extract(args.username)

    instagram_data = None
    if meta:
        print(f"  {Colors.GREEN}✓{Colors.END} Profile found")
        print(f"  {Colors.GREEN}✓{Colors.END} Name: {meta.full_name or 'N/A'}")
        print(f"  {Colors.GREEN}✓{Colors.END} Followers: {meta.followers or 'N/A'}")
        instagram_data = meta
    else:
        print(f"  {Colors.RED}✗{Colors.END} Could not extract")

    # Multi-site search
    print(f"\n{Colors.YELLOW}[2] Multi-Platform Search{Colors.END}")
    search = UsernameSearch()
    results = search.search(args.username)
    found = search.get_found_accounts(results)
    print(f"  {Colors.GREEN}✓{Colors.END} Found {len(found)} accounts")

    # Report
    print(f"\n{Colors.YELLOW}[3] Generating Report{Colors.END}")
    reporter = JSONReporter()
    data = {
        'target': args.username,
        'instagram': instagram_data.__dict__ if instagram_data else None,
        'social_accounts': found
    }

    report_file = args.output or f"insta_spy_{args.username}_{int(__import__('time').time())}.json"
    reporter.save(data, report_file)
    print(f"  {Colors.GREEN}✓{Colors.END} Report saved: {report_file}")

    print(f"\n{Colors.GREEN}{Colors.BOLD}[+] SCAN COMPLETE{Colors.END}")

def main():
    banner()

    parser = argparse.ArgumentParser(
        description='InstaSpy v3.0 — Professional Instagram OSINT Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # search
    search_parser = subparsers.add_parser('search', help='Search username across platforms')
    search_parser.add_argument('username', help='Username to search')
    search_parser.add_argument('-o', '--output', help='Save report to file')

    # instagram
    ig_parser = subparsers.add_parser('instagram', help='Extract Instagram data')
    ig_parser.add_argument('username', help='Instagram username')
    ig_parser.add_argument('-o', '--output', help='Save report to file')

    # full
    full_parser = subparsers.add_parser('full', help='Full OSINT scan')
    full_parser.add_argument('username', help='Username to scan')
    full_parser.add_argument('-o', '--output', help='Save report to file')

    args = parser.parse_args()

    if args.command == 'search':
        cmd_search(args)
    elif args.command == 'instagram':
        cmd_instagram(args)
    elif args.command == 'full':
        cmd_full(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
