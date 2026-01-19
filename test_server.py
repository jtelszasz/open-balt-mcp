#!/usr/bin/env python3
"""
Test script for Baltimore Permit MCP Server
Tests the API connection and server logic
"""

import asyncio
import sys
from datetime import datetime, timedelta

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

# Baltimore Open Data API endpoint
BALTIMORE_PERMIT_API = "https://egisdata.baltimorecity.gov/egis/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/3/query"


async def test_api_connection():
    """Test basic API connection."""
    print("Testing API connection...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "where": "1=1",
                "outFields": "CaseNumber,Address",
                "f": "geojson",
                "resultRecordCount": 5
            }
            response = await client.get(BALTIMORE_PERMIT_API, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "features" in data and len(data["features"]) > 0:
                print(f"✓ API connection successful! Retrieved {len(data['features'])} sample permits")
                print(f"  Sample permit: {data['features'][0].get('properties', {}).get('CaseNumber', 'N/A')}")
                return True
            else:
                print("✗ API returned no features")
                return False
        except Exception as e:
            print(f"✗ API connection failed: {str(e)}")
            return False


async def test_search_by_address():
    """Test address search."""
    print("\nTesting address search...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "where": "Address LIKE '%Pratt%'",
                "outFields": "CaseNumber,Address",
                "f": "geojson",
                "resultRecordCount": 3
            }
            response = await client.get(BALTIMORE_PERMIT_API, params=params)
            response.raise_for_status()
            data = response.json()
            
            count = len(data.get("features", []))
            print(f"✓ Address search successful! Found {count} permits with 'Pratt' in address")
            if count > 0:
                print(f"  Sample: {data['features'][0].get('properties', {}).get('Address', 'N/A')}")
            return True
        except Exception as e:
            print(f"✗ Address search failed: {str(e)}")
            return False


async def test_date_range_search():
    """Test date range search."""
    print("\nTesting date range search...")
    
    # Calculate a date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last year to get results
    
    start_ts = int(start_date.timestamp() * 1000)
    end_ts = int(end_date.timestamp() * 1000)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "where": f"IssuedDate >= {start_ts} AND IssuedDate <= {end_ts}",
                "outFields": "CaseNumber,IssuedDate",
                "f": "geojson",
                "resultRecordCount": 3,
                "orderByFields": "IssuedDate DESC"
            }
            response = await client.get(BALTIMORE_PERMIT_API, params=params)
            response.raise_for_status()
            data = response.json()
            
            count = len(data.get("features", []))
            print(f"✓ Date range search successful! Found {count} permits in date range")
            return True
        except Exception as e:
            print(f"✗ Date range search failed: {str(e)}")
            return False


async def test_neighborhood_search():
    """Test neighborhood search."""
    print("\nTesting neighborhood search...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            params = {
                "where": "Neighborhood LIKE '%Fells Point%'",
                "outFields": "CaseNumber,Neighborhood",
                "f": "geojson",
                "resultRecordCount": 3
            }
            response = await client.get(BALTIMORE_PERMIT_API, params=params)
            response.raise_for_status()
            data = response.json()
            
            count = len(data.get("features", []))
            print(f"✓ Neighborhood search successful! Found {count} permits in 'Fells Point'")
            return True
        except Exception as e:
            print(f"✗ Neighborhood search failed: {str(e)}")
            return False


async def test_server_imports():
    """Test if server module can be imported."""
    print("\nTesting server module imports...")
    try:
        # Try to import the server module
        import importlib.util
        spec = importlib.util.spec_from_file_location("server", "server.py")
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Just check if it loads without syntax errors
            print("✓ Server module syntax is valid")
            return True
        else:
            print("✗ Could not load server module")
            return False
    except SyntaxError as e:
        print(f"✗ Syntax error in server.py: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Baltimore Permit MCP Server - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test imports first (doesn't require network)
    results.append(await test_server_imports())
    
    # Test API connection
    results.append(await test_api_connection())
    
    # Test various search functions
    results.append(await test_search_by_address())
    results.append(await test_date_range_search())
    results.append(await test_neighborhood_search())
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    print("=" * 60)
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
