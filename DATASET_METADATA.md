# Baltimore City Building Permits Dataset Metadata

**Source:** Baltimore City Department of Housing & Community Development (DHCD)
**API Endpoint:** `https://egisdata.baltimorecity.gov/egis/rest/services/Housing/DHCD_Open_Baltimore_Datasets/FeatureServer/3`
**Total Records:** ~272,887 (as of February 2026)
**Date Range:** 2019–present (no data prior to 2019)

---

## Fields

### OBJECTID
- **Type:** Integer (OID)
- **Description:** Auto-generated unique row identifier from ArcGIS. Not meaningful for analysis.

### CaseNumber
- **Type:** String (max 250 chars)
- **Required:** Yes
- **Description:** Unique permit identifier. Prefixed with a code indicating permit type.
- **Known prefixes:**
  | Prefix | Count | Meaning |
  |--------|-------|---------|
  | COM | 220,468 | Unknown (most common — likely general/commercial permits) |
  | BRC | 21,235 | Unknown |
  | USE | 21,133 | Likely Use & Occupancy permits |
  | BUS | 2,657 | Likely Business-related permits |
  | DEM | 2,624 | Likely Demolition permits |
  | BCC | 2,386 | Unknown |
  | BMZ | 1,611 | Unknown |
  | TMP | 576 | Likely Temporary permits |
  | BDE | 148 | Unknown |
  | BTE | 49 | Unknown |

### Description
- **Type:** String (max ~1 billion chars)
- **Description:** Free-text description of the permitted work. Often includes boilerplate legal language (e.g., "Approved For Work only. Subject to the permitted uses and regulations under the provisions of the Zoning Ordinance.").

### IssuedDate
- **Type:** Date (stored as milliseconds since epoch)
- **Description:** Date the permit was issued.
- **Note:** Dataset only contains permits from 2019 onward. Reason for absence of earlier data is unknown.

### ExpirationDate
- **Type:** Date (stored as milliseconds since epoch)
- **Description:** Date the permit expires.

### Address
- **Type:** String (max 250 chars)
- **Description:** Street address of the permitted property.

### BLOCKLOT
- **Type:** String (max 30 chars)
- **Description:** Baltimore City tax parcel identifier combining block number and lot number (e.g., `4778B050`, `3565 018`). Can be used to link to property/tax records.

### prc_block_no
- **Type:** String (max 5 chars)
- **Description:** Parcel block number. Together with `prc_lot`, forms the unique parcel identifier. Component of `BLOCKLOT`.

### prc_lot
- **Type:** String (max 4 chars)
- **Description:** Parcel lot number. Together with `prc_block_no`, forms the unique parcel identifier. Component of `BLOCKLOT`.

### ExistingUse
- **Type:** String (max 4 chars)
- **Populated:** ~242,175 records (~89%)
- **Description:** The existing use classification of the building at the time of permit application. Uses a numeric coding system (e.g., `1-08`, `1-05`, `3-42`) as well as some abbreviated text codes (e.g., `SF`, `MF`, `VAC`, `COM`).
- **Most common values:**
  | Code | Count |
  |------|-------|
  | 1-08 | 146,304 |
  | 1-05 | 42,255 |
  | 1-09 | 8,535 |
  | 3-42 | 6,284 |
  | 1-07 | 5,870 |
- **Note:** The codebook for these use codes is unknown. They appear to be an internal DHCD classification and do not correspond to Baltimore City zoning districts. There are ~127 distinct values.

### ProposedUse
- **Type:** String (max 4 chars)
- **Populated:** ~238,000+ records
- **Description:** The proposed use classification for the building after the permitted work is complete. Same coding system as `ExistingUse`. When `ProposedUse` differs from `ExistingUse`, the permit involves a change of use (e.g., warehouse to apartments).
- **Most common values:**
  | Code | Count |
  |------|-------|
  | 1-08 | 148,587 |
  | 1-05 | 42,442 |
  | 1-09 | 8,588 |
  | 1-07 | 7,149 |
- **Note:** Same unknown codebook as `ExistingUse`.

### csm_projname
- **Type:** String (max 30 chars)
- **Populated:** 6 records (all empty strings)
- **Description:** Likely an internal project name field. Effectively unused in this dataset.

### Neighborhood
- **Type:** String
- **Description:** Baltimore City neighborhood name (e.g., "Hampden", "Fells Point", "Canton"). Populated for all or nearly all records. Uses the city's official neighborhood boundaries.

### Cost
- **Type:** Double
- **Populated:** ~198,015 records (~73%)
- **Description:** Estimated project cost associated with the permit.
- **Data quality note:** Some values appear to be data entry errors (e.g., $4.4 billion for a residential rowhouse). Outliers should be treated with caution.
- **Open question:** It is unclear whether this cost is self-reported by the applicant or assessed by the city.

### Council_District
- **Type:** Integer
- **Description:** Baltimore City Council district number (1–14).

### HousingMarketTypology2017
- **Type:** String
- **Populated:** All 272,887 records
- **Description:** Baltimore City Planning Department's [2017 Housing Market Typology](https://planning.baltimorecity.gov/housing-market-typology/descriptions-housing-market-typology-map) classification for the property's location. Categories range from the strongest housing markets (A) to the weakest (J), plus rental and non-residential categories.
- **Categories:**
  | Code | Description |
  |------|-------------|
  | A | Competitive — highest sales prices, lowest vacancy |
  | B | Above-average prices, high ownership, high residential density |
  | C | Above-average prices, high subsidized rental, high density |
  | D | Near-average prices, high ownership, low density |
  | E | Near-average prices, higher foreclosure activity |
  | F | 30–50% below average prices, significant ownership |
  | G | Lowest ownership, highest subsidized housing (19%) |
  | H | 30–50% below average prices, significant ownership |
  | I | Low prices, high vacancy |
  | J | Lowest prices (80–90% below avg), highest vacancy, greatest population loss |
  | Mixed Market/Subsd Rental | Mixed market and subsidized rental |
  | NonResidential | Non-residential properties |
  | Rental Market 1 | Rental market subcategory |
  | Rental Market 2 | Rental market subcategory |
  | Subsidized Rental Market | Subsidized rental properties |

### IsPermitModification
- **Type:** Integer (boolean: 0 or 1)
- **Description:** Flag indicating whether this permit is a modification of a previously issued permit. ~42,977 permits (~16%) are modifications.

### Geometry (Point)
- **Type:** GeoJSON Point (longitude, latitude)
- **Description:** Geographic coordinates of the permitted property. Present on most records.

---

## Open Questions

1. **Use codes:** What codebook defines the `ExistingUse` and `ProposedUse` values (e.g., what does `1-08` mean)? These appear to be internal DHCD classifications.
2. **Case number prefixes:** What do `COM`, `BRC`, `BCC`, `BMZ`, `BDE`, and `BTE` stand for?
3. **Date range:** Why does the dataset only contain permits from 2019 onward? Was earlier data removed or migrated elsewhere?
4. **Cost field:** Is the cost self-reported by the permit applicant, or assessed/estimated by the city?
5. **BLOCKLOT consistency:** Are `prc_block_no` + `prc_lot` always consistent with the `BLOCKLOT` field?
