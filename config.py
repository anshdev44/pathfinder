"""Configuration settings for the Flask application."""
import os

# SECURITY WARNING: Keep this file secure and don't commit it to public repositories!
# You should ideally use environment variables or a secret management system.

# ---------------------------------------------------------------------------- #
#                        !!! PASTE YOUR API KEY HERE !!!                       #
# ---------------------------------------------------------------------------- #
# Replace "YOUR_API_KEY_HERE" with your actual Google Maps API Key
# Ensure you have enabled: Maps JavaScript API, Directions API, Geocoding API, Distance Matrix API
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "AIzaSyCZ-ONBo_Q8bJRm8yAoF8N2m_I6wOnTtF0")
# ---------------------------------------------------------------------------- #

if GOOGLE_MAPS_API_KEY == "YOUR_API_KEY_HERE":
    print("\n" + "="*60)
    print("  WARNING: Google Maps API key is not set!")
    print("  Please replace 'YOUR_API_KEY_HERE' in config.py with your actual key.")
    print("="*60 + "\n") 