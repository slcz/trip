#!/usr/bin/env python3
"""
Generate working Google Maps pb= directions embed URLs.
Usage: python3 generate_route_map.py
"""

import urllib.request
import sys

# Known working Google Place IDs
PLACE_IDS = {
    'London': '0x47d8a00baf21de75%3A0x52963a5addd52a99',
    'Heathrow': '0x47d8a00baf21de75%3A0x52963a5addd52a99',
    'York': '0x4878e5c3d8c7e6fd%3A0xe72c07de76ce4237',
    'Edinburgh': '0x4887b800f6498cb9%3A0x5e9a5e6e9811e7',
}

def build_directions_url(waypoints, mode='3'):
    """
    waypoints: list of (place_id_or_name, display_name, lat, lng)
    mode: '2' = walking, '3' = transit/train
    Returns: full embed URL
    """
    # Map parameters — keep these consistent with the known-working UK embed
    base = ['1m40', '1m12', '1m3', '1d2444914', '2d-2.0', '3d53.0',
            '2m3', '1f0', '2f0', '3f0', '3m2', '1i1024', '2i768', '4f13.1']

    # Directions — must match the exact token count from the working template
    dir_tokens = [f'4m25', f'3e{mode}']
    for pid, name, lat, lng in waypoints:
        dir_tokens += ['4m5', f'1s{pid}', f'2s{name}', '3m2', f'1d{lat}', f'2d{lng}']

    dir_tokens += ['5e0', '3m2', '1sen', '2sus']

    url = 'https://www.google.com/maps/embed?pb=!' + '!'.join(base + dir_tokens)
    return url

def test_url(url):
    """Test if the embed URL returns HTTP 200"""
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status == 200
    except:
        return False

# Example: UK trip route
if __name__ == '__main__':
    waypoints = [
        (PLACE_IDS['London'], 'London', 51.5072178, -0.1275862),
        (PLACE_IDS['York'], 'York', 53.959965, -1.0872979),
        (PLACE_IDS['Edinburgh'], 'Edinburgh', 55.953251, -3.188267),
        (PLACE_IDS['Heathrow'], 'Heathrow', 51.4700223, -0.4542955),
    ]

    url = build_directions_url(waypoints, mode='3')
    print(f"Generated URL ({len(url)} chars)")

    if test_url(url):
        print("✅ HTTP 200 — embed works!")
        print(f"\nEmbed code:\n{url}")
    else:
        print("❌ URL returned error")
        sys.exit(1)
