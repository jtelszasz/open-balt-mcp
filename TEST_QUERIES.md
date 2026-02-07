# Test Queries for Baltimore City Building Permits Dataset

Verified answers as of February 2026. Use these to test accuracy of queries against the dataset.

| # | Question | WHERE Clause | Expected Answer |
|---|----------|-------------|-----------------|
| 1 | How many permits were issued in Canton in 2023? | `Neighborhood = 'Canton' AND IssuedDate >= DATE '2023-01-01' AND IssuedDate < DATE '2024-01-01'` | 911 |
| 2 | How many permit modifications were issued in 2022? | `IsPermitModification = 1 AND IssuedDate >= DATE '2022-01-01' AND IssuedDate < DATE '2023-01-01'` | 7,423 |
| 3 | How many permits have a cost between $1M and $100M? | `Cost > 1000000 AND Cost < 100000000` | 993 |
| 4 | How many demolition permits (DEM prefix) are in the dataset? | `CaseNumber LIKE 'DEM%'` | 2,624 |
| 5 | How many permits are in Council District 1? | `Council_District = 1` | 22,859 |
| 6 | How many permits involve a change of use? | `ExistingUse <> ProposedUse AND ExistingUse IS NOT NULL AND ProposedUse IS NOT NULL` | 14,182 |
| 7 | How many permits are in Housing Market Typology "J" (weakest market)? | `HousingMarketTypology2017 = 'J'` | 20,213 |
| 8 | How many Use & Occupancy permits are in Fells Point? | `Neighborhood = 'Fells Point' AND CaseNumber LIKE 'USE%'` | 285 |
| 9 | How many permits issued in 2020 had a cost of $500 or less? | `IssuedDate >= DATE '2020-01-01' AND IssuedDate < DATE '2021-01-01' AND Cost > 0 AND Cost <= 500` | 3,361 |
| 10 | How many permits mention "solar" in the description? | `Description LIKE '%solar%' OR Description LIKE '%Solar%' OR Description LIKE '%SOLAR%'` | 2,139 |

## Coverage

These queries test the following fields and patterns:
- **Neighborhood** filtering (Q1, Q8)
- **Date range** filtering (Q1, Q2, Q9)
- **Boolean flag** filtering — IsPermitModification (Q2)
- **Numeric range** filtering — Cost (Q3, Q9)
- **String prefix** matching — CaseNumber (Q4, Q8)
- **Integer equality** — Council_District (Q5)
- **Field comparison** — ExistingUse vs ProposedUse (Q6)
- **Categorical** filtering — HousingMarketTypology2017 (Q7)
- **Text search** — Description (Q10)
- **Multi-field combinations** (Q1, Q2, Q8, Q9)

## Notes

- Answers may drift over time as new permits are added to the dataset.
- Questions 4, 5, 6, 7, and 10 span the full dataset and are most likely to change as new records are added.
- Questions scoped to completed years (Q1, Q2, Q9) should remain stable.
