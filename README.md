# Baltimore Permit MCP Server

An MCP (Model Context Protocol) server that provides access to Baltimore City's housing and building permit data from the [Baltimore Open Data Portal](https://egisdata.baltimorecity.gov/egis/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/3).

## Features

This MCP server provides tools to query Baltimore's building permit database:

- **Search by Address**: Find permits for specific addresses or address patterns
- **Search by Date Range**: Get permits issued within a date range
- **Search by Neighborhood**: Find all permits in a specific neighborhood
- **Search by Case Number**: Look up a specific permit by its case number
- **Recent Permits**: Get the most recently issued permits
- **Count Permits**: Count permits matching specific criteria

## Installation

1. Install Python 3.10 or higher (Python 3.11 recommended):
   ```bash
   brew install python@3.11
   ```

2. Install dependencies:
   ```bash
   pip3.11 install -r requirements.txt
   ```

## Configuration

No configuration is required. The server connects directly to Baltimore's public API endpoint.

## Usage

### Running the Server

Run the server using stdio (standard input/output):

```bash
python3.11 server.py
```

Or use the provided run script:

```bash
./run_server.sh
```

### Testing

Run the comprehensive test suite:

```bash
python3.11 test_comprehensive.py
```

### MCP Client Configuration

To use this server with an MCP client (like Claude Desktop), add it to your MCP configuration file:

**For Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "balt-permit": {
      "command": "python3.11",
      "args": ["/path/to/balt-permit-mcp-server/server.py"]
    }
  }
}
```

Replace `/path/to/balt-permit-mcp-server` with the actual absolute path to this directory.

**For other MCP clients**, configure according to your client's documentation.

## Available Tools

### `search_permits_by_address`

Search for permits by address or address pattern.

**Parameters:**
- `address` (required): Address or part of address to search (e.g., "100 Main St" or "Main")
- `limit` (optional): Maximum results to return (default: 50, max: 1000)

**Example:**
```json
{
  "address": "Pratt St",
  "limit": 20
}
```

### `search_permits_by_date_range`

Search for permits issued within a date range.

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `limit` (optional): Maximum results to return (default: 50, max: 1000)

**Example:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "limit": 100
}
```

### `search_permits_by_neighborhood`

Search for permits in a specific neighborhood.

**Parameters:**
- `neighborhood` (required): Neighborhood name (e.g., "Fells Point", "Canton")
- `limit` (optional): Maximum results to return (default: 50, max: 1000)

**Example:**
```json
{
  "neighborhood": "Fells Point",
  "limit": 50
}
```

### `search_permits_by_case_number`

Get a specific permit by its case number.

**Parameters:**
- `case_number` (required): Permit case number (e.g., "COM2018-86246")

**Example:**
```json
{
  "case_number": "COM2018-86246"
}
```

### `get_recent_permits`

Get recently issued permits.

**Parameters:**
- `limit` (optional): Maximum results to return (default: 50, max: 1000)
- `days` (optional): Number of days to look back (default: 30)

**Example:**
```json
{
  "limit": 25,
  "days": 7
}
```

### `count_permits`

Count permits matching a SQL WHERE clause.

**Parameters:**
- `where_clause` (required): SQL WHERE clause for filtering

**Example:**
```json
{
  "where_clause": "Council_District = 1 AND Cost > 10000"
}
```

## Data Source

This server connects to Baltimore City's ArcGIS FeatureServer:

- **Endpoint**: `https://egisdata.baltimorecity.gov/egis/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/3`
- **Format**: GeoJSON
- **Data**: Building Permits from the Department of Housing & Community Development (DHCD)

## Permit Data Fields

Each permit includes the following information:

- **CaseNumber**: Unique permit case number
- **Address**: Property address
- **Neighborhood**: Neighborhood name
- **IssuedDate**: Date permit was issued
- **ExpirationDate**: Date permit expires
- **Cost**: Estimated project cost
- **Description**: Detailed work description
- **BLOCKLOT**: Block and lot number
- **Council_District**: City council district number
- **ExistingUse**: Existing land use code
- **ProposedUse**: Proposed land use code
- **IsPermitModification**: Whether this is a permit modification
- **Location**: Geographic coordinates (latitude, longitude)

## License

This MCP server is provided as-is. The data source is Baltimore City's open data, available under their [Open Data Policy](https://technology.baltimorecity.gov/open-data-policy).

## Notes

- The API may return results with `exceededTransferLimit: true` when there are many matching permits. In such cases, results may be truncated.
- Date queries use timestamp comparisons (milliseconds since epoch) based on the API's internal format.
- Address and neighborhood searches are case-insensitive and support partial matches.

## Support

For issues or questions about this MCP server, please open an issue in the repository.

For questions about the underlying data, contact Baltimore City's open data team.
=======
# open-balt-mcp
MCP for accessing Baltimore's open data
