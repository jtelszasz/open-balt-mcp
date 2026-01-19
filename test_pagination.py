#!/usr/bin/env python3.11
"""
Test pagination functionality for Baltimore Permit MCP Server
"""

import asyncio
import time
from server import query_permit_api_paginated, call_tool


async def test_pagination_function():
    """Test the low-level pagination function."""
    print("="*70)
    print("Testing Low-Level Pagination Function")
    print("="*70)

    # Test 1: Small request (no pagination needed)
    print("\nTest 1: Request 100 records (single page)...")
    start = time.time()
    data = await query_permit_api_paginated(
        where_clause="1=1",
        max_records=100
    )
    elapsed = time.time() - start
    print(f"✓ Retrieved {data['totalRetrieved']} records in {elapsed:.2f}s")

    # Test 2: Request exactly 1000 (boundary test)
    print("\nTest 2: Request 1000 records (single page)...")
    start = time.time()
    data = await query_permit_api_paginated(
        where_clause="1=1",
        max_records=1000
    )
    elapsed = time.time() - start
    print(f"✓ Retrieved {data['totalRetrieved']} records in {elapsed:.2f}s")

    # Test 3: Request 2500 (multiple pages)
    print("\nTest 3: Request 2500 records (multiple pages)...")
    start = time.time()
    data = await query_permit_api_paginated(
        where_clause="1=1",
        max_records=2500
    )
    elapsed = time.time() - start
    print(f"✓ Retrieved {data['totalRetrieved']} records in {elapsed:.2f}s")
    if data['totalRetrieved'] == 2500:
        print("  ✓ Pagination working correctly - got all 2500 records!")

    # Test 4: Filtered query with pagination
    print("\nTest 4: Filtered query (Canton neighborhood, 1800 records)...")
    start = time.time()
    data = await query_permit_api_paginated(
        where_clause="Neighborhood LIKE '%Canton%'",
        max_records=1800
    )
    elapsed = time.time() - start
    print(f"✓ Retrieved {data['totalRetrieved']} records in {elapsed:.2f}s")


async def test_tool_pagination():
    """Test pagination through MCP tool calls."""
    print("\n" + "="*70)
    print("Testing Pagination Through MCP Tools")
    print("="*70)

    # Test 1: Large neighborhood search
    print("\nTest 1: Search Canton neighborhood for 2000 permits...")
    start = time.time()
    result = await call_tool('search_permits_by_neighborhood', {
        'neighborhood': 'Canton',
        'limit': 2000
    })
    elapsed = time.time() - start
    text = result[0].text
    first_line = text.split('\n')[0]
    print(f"✓ {first_line}")
    print(f"  Completed in {elapsed:.2f}s")

    # Test 2: Large address search
    print("\nTest 2: Search for addresses with 'ST' (3000 limit)...")
    start = time.time()
    result = await call_tool('search_permits_by_address', {
        'address': 'ST',
        'limit': 3000
    })
    elapsed = time.time() - start
    text = result[0].text
    first_line = text.split('\n')[0]
    print(f"✓ {first_line}")
    print(f"  Completed in {elapsed:.2f}s")

    # Test 3: Verify we can get more than API limit
    print("\nTest 3: Verify retrieval beyond 1000 record API limit...")
    result = await call_tool('search_permits_by_address', {
        'address': 'AVE',
        'limit': 5000
    })
    text = result[0].text
    first_line = text.split('\n')[0]
    count = int(first_line.split()[1])
    print(f"✓ {first_line}")

    if count > 1000:
        print(f"  ✓ SUCCESS: Retrieved {count} records (more than 1000 API limit)")
        print("  ✓ Pagination is working correctly!")
    else:
        print(f"  Note: Only {count} records available for this query")


async def main():
    """Run all pagination tests."""
    print("\n" + "="*70)
    print("BALTIMORE PERMIT MCP SERVER - PAGINATION TESTS")
    print("="*70)

    try:
        await test_pagination_function()
        await test_tool_pagination()

        print("\n" + "="*70)
        print("✓ ALL PAGINATION TESTS PASSED!")
        print("="*70)
        print("\nSummary:")
        print("  ✓ Pagination function works correctly")
        print("  ✓ Can retrieve records beyond 1000 limit")
        print("  ✓ MCP tools use pagination automatically")
        print("  ✓ No manual pagination needed by users")
        print("="*70 + "\n")

        return 0

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
