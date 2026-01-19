#!/usr/bin/env python3.11
"""
Comprehensive test suite for Baltimore Permit MCP Server
"""

import asyncio
from server import app, call_tool, list_tools


async def test_list_tools():
    """Test that all tools are registered."""
    print("Testing tool registration...")
    tools = await list_tools()
    print(f"✓ Found {len(tools)} tools")

    expected_tools = [
        'search_permits_by_address',
        'search_permits_by_date_range',
        'search_permits_by_neighborhood',
        'search_permits_by_case_number',
        'get_recent_permits',
        'count_permits'
    ]

    tool_names = [t.name for t in tools]
    for expected in expected_tools:
        assert expected in tool_names, f"Missing tool: {expected}"

    print("✓ All expected tools are registered\n")


async def test_count_permits():
    """Test counting permits."""
    print("Testing count_permits...")
    result = await call_tool('count_permits', {'where_clause': '1=1'})
    text = result[0].text
    assert 'permit(s) matching the query' in text
    print(f"✓ {text}\n")


async def test_search_by_neighborhood():
    """Test searching by neighborhood."""
    print("Testing search_permits_by_neighborhood...")
    result = await call_tool('search_permits_by_neighborhood', {
        'neighborhood': 'Canton',
        'limit': 2
    })
    text = result[0].text
    assert 'Canton' in text or 'CANTON' in text
    print(f"✓ Found permits in Canton")
    print(f"  Sample: {text[:200]}...\n")


async def test_search_by_address():
    """Test searching by address."""
    print("Testing search_permits_by_address...")
    result = await call_tool('search_permits_by_address', {
        'address': 'FOSTER',
        'limit': 2
    })
    text = result[0].text
    assert 'permit' in text.lower()
    print(f"✓ Address search working")
    print(f"  Sample: {text[:200]}...\n")


async def test_search_by_date_range():
    """Test searching by date range."""
    print("Testing search_permits_by_date_range...")
    result = await call_tool('search_permits_by_date_range', {
        'start_date': '2019-01-01',
        'end_date': '2019-12-31',
        'limit': 2
    })
    text = result[0].text
    assert 'permit' in text.lower()
    print(f"✓ Date range search working")
    print(f"  Sample: {text[:200]}...\n")


async def test_get_recent_permits():
    """Test getting recent permits."""
    print("Testing get_recent_permits...")
    result = await call_tool('get_recent_permits', {
        'limit': 5,
        'days': 365
    })
    text = result[0].text
    assert 'permit' in text.lower()
    print(f"✓ Recent permits search working")
    print(f"  Result: {text[:100]}...\n")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Baltimore Permit MCP Server - Comprehensive Test Suite")
    print("=" * 60 + "\n")

    try:
        await test_list_tools()
        await test_count_permits()
        await test_search_by_neighborhood()
        await test_search_by_address()
        await test_search_by_date_range()
        await test_get_recent_permits()

        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
