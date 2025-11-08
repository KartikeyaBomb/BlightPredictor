#!/usr/bin/env python3
"""
Add neighborhood names to the filtered enforcement CSV using geopy reverse geocoding.
"""

import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json
import os


def get_neighborhood(lat, lon, geolocator, cache, retry_count=3):
    """
    Get neighborhood name from coordinates using reverse geocoding with caching.
    
    Args:
        lat: Latitude
        lon: Longitude
        geolocator: Geopy geolocator instance
        cache: Dictionary to cache results
        retry_count: Number of retries on timeout
        
    Returns:
        Neighborhood name or 'Unknown' if not found
    """
    if pd.isna(lat) or pd.isna(lon):
        return 'Unknown'
    
    # Round coordinates to 5 decimal places for caching (approx 1 meter precision)
    cache_key = f"{round(lat, 5)},{round(lon, 5)}"
    
    # Check cache first
    if cache_key in cache:
        return cache[cache_key]
    
    for attempt in range(retry_count):
        try:
            location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True, language='en')
            if location and location.raw.get('address'):
                address = location.raw['address']
                # Try to get neighborhood from various fields
                neighborhood = (
                    address.get('neighbourhood') or 
                    address.get('suburb') or 
                    address.get('hamlet') or
                    address.get('city_district') or
                    address.get('quarter') or
                    'Unknown'
                )
                cache[cache_key] = neighborhood
                return neighborhood
            cache[cache_key] = 'Unknown'
            return 'Unknown'
        except GeocoderTimedOut:
            if attempt < retry_count - 1:
                time.sleep(1)
                continue
            cache[cache_key] = 'Unknown'
            return 'Unknown'
        except GeocoderServiceError:
            cache[cache_key] = 'Unknown'
            return 'Unknown'
        except Exception as e:
            print(f"Error geocoding ({lat}, {lon}): {e}")
            cache[cache_key] = 'Unknown'
            return 'Unknown'
    
    cache[cache_key] = 'Unknown'
    return 'Unknown'


def save_cache(cache, filename):
    """Save cache to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(cache, f, indent=2)


def load_cache(filename):
    """Load cache from a JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}


def main():
    input_file = 'data/historical-code-enforcement-requests-filtered.csv'
    output_file = 'data/historical-code-enforcement-requests-filtered-with-neighborhoods.csv'
    cache_file = 'data/geocode_cache.json'
    
    print("="*60)
    print("Adding Neighborhoods to Filtered Enforcement CSV")
    print("="*60)
    
    print(f"\nReading {input_file}...")
    df = pd.read_csv(input_file, delimiter=';')
    
    print(f"Found {len(df)} rows")
    
    # Load cache
    cache = load_cache(cache_file)
    print(f"Loaded {len(cache)} cached locations")
    
    # Count unique coordinates
    unique_coords = df[['lat', 'lon']].drop_duplicates()
    print(f"Unique coordinate pairs: {len(unique_coords)}")
    
    # Check how many are already cached
    cached_count = 0
    for _, row in unique_coords.iterrows():
        if not pd.isna(row['lat']) and not pd.isna(row['lon']):
            cache_key = f"{round(row['lat'], 5)},{round(row['lon'], 5)}"
            if cache_key in cache:
                cached_count += 1
    
    print(f"Already cached: {cached_count}")
    print(f"Need to geocode: {len(unique_coords) - cached_count}")
    print(f"Estimated time: ~{(len(unique_coords) - cached_count)} seconds")
    
    print("\nAdding neighborhood column...")
    
    # Initialize geolocator
    geolocator = Nominatim(user_agent="memphis_filtered_enforcement_mapper")
    
    # Add neighborhood column
    neighborhoods = []
    api_calls = 0
    for idx, row in df.iterrows():
        if (idx + 1) % 500 == 0:
            print(f"Processing row {idx + 1}/{len(df)}... (API calls: {api_calls})")
            # Save cache periodically
            save_cache(cache, cache_file)
        
        cache_key = f"{round(row['lat'], 5) if not pd.isna(row['lat']) else 'nan'},{round(row['lon'], 5) if not pd.isna(row['lon']) else 'nan'}"
        
        if cache_key in cache:
            neighborhood = cache[cache_key]
        else:
            neighborhood = get_neighborhood(row['lat'], row['lon'], geolocator, cache)
            api_calls += 1
            # Rate limiting - Nominatim requires 1 second between requests
            time.sleep(1)
        
        neighborhoods.append(neighborhood)
    
    df['neighborhood'] = neighborhoods
    
    # Save final cache
    save_cache(cache, cache_file)
    print(f"\nTotal API calls made: {api_calls}")
    
    print(f"\nWriting to {output_file}...")
    df.to_csv(output_file, index=False, sep=';')
    print(f"Done! Created {output_file}")
    
    # Print summary
    neighborhood_counts = df['neighborhood'].value_counts()
    print("\nNeighborhood distribution:")
    print(neighborhood_counts.head(15))
    
    print("\n" + "="*60)
    print("Processing complete!")
    print("="*60)


if __name__ == "__main__":
    main()
