# Austin Armadillos — NFL FP&A Practice Database

A fictional NFL team financial database built for practicing FP&A skills: 12-month forward forecasting, budget construction, and monthly variance reporting.

**Simulated context:** It is December 2026. You are a FP&A Analyst at the Austin Armadillos. You have 5 years of actuals (2022–2026) and a just-drafted 2027 annual budget. Your job is to build forecasts, run scenario analysis, and report variances as each 2027 month closes.

---

## The Team

| | |
|---|---|
| **Team** | Austin Armadillos |
| **Abbreviation** | AAR |
| **Conference / Division** | AFC South |
| **Stadium** | Lone Star Field, Austin TX |
| **Capacity** | 68,500 |
| **Founded** | 2022 (NFL expansion team) |
| **Owner** | Duke Caldwell |
| **Head Coach** | Marcus Webb |
| **General Manager** | Sandra Okafor |
| **Mascot** | Tex the Armadillo |
| **Colors** | Burnt Orange / Midnight Black / Desert Sand |

### Performance History

| Year | W-L% | Playoffs | Revenue | EBITDA | Net Income |
|------|-------|----------|---------|--------|------------|
| 2022 | .350 | No | $383M | -$15M | -$31M |
| 2023 | .470 | No | $448M | +$10M | -$11M |
| 2024 | .590 | Yes | $530M | +$34M | +$8M |
| 2025 | .650 | Yes | $574M | +$37M | +$10M |
| 2026 | .710 | Yes (Super Bowl) | $638M | +$61M | +$30M |
| **2027 Budget** | — | — | **$679M** | **$65M** | **$32M** |

The expansion team story arc (early losses → growing profitability) gives realistic context for trend analysis and driver-based forecasting.

---

## Project Structure

```
NFL Team Forecasting/
├── data/                    # All parquet files (database)
├── generate_data.py         # Data generation script (re-run to regenerate)
├── main.ipynb               # Primary analysis notebook
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Database — Table Reference

All data is stored as `.parquet` files in `./data/`. The schema follows a **star schema** pattern: `dim_*` tables are lookup/reference tables, `fact_*` tables contain transactional or aggregated data.

### Dimension Tables

| Table | Rows | Description |
|-------|------|-------------|
| `dim_team.parquet` | 1 | Team metadata (name, stadium, ownership, coaching staff) |
| `dim_game.parquet` | 109 | Full game schedules 2022–2026: opponent, date, result, home/away, game type (preseason / regular / playoff) |
| `dim_ticket_tier.parquet` | 7 | Ticket categories from General Admission ($75) to Field Pass ($1,200) and Suites ($8,500). Includes section, base price, and capacity allocation % |
| `dim_customer.parquet` | 65,000 | Fan/customer profiles: type (season ticket holder / casual / suite), demographics, join date, loyalty tier, lifetime spend, preferred channel |
| `dim_sponsor.parquet` | 12 | Sponsorship contracts: company, category (naming rights, jersey, official partner), annual value, start/end year |
| `dim_expense_category.parquet` | 24 | Expense taxonomy with department and type (COGS / OpEx / CapEx / Non-OpEx) |
| `dim_revenue_category.parquet` | 23 | Revenue taxonomy with stream groupings (Tickets, Concessions, Broadcasting, Sponsorship, etc.) |
| `dim_date.parquet` | 2,016 | Date dimension: year, month, quarter, week, day of week, NFL season flag |

---

### Fact Tables — Game Level

| Table | Rows | Grain | Description |
|-------|------|-------|-------------|
| `fact_attendance.parquet` | 58 | 1 row per home game | Tickets sold, tickets scanned (actual attendance), no-shows, capacity utilization %, SRO sold, parking vehicles, weather, temperature |
| `fact_ticket_sales.parquet` | 1,215 | 1 row per game × tier × channel | Quantity sold, average price, gross revenue, discount %, broken out by tier (GA / Lower Bowl / Club / Suite / etc.) and sales channel (Online / Box Office / Secondary Market) |
| `fact_concessions.parquet` | 232 | 1 row per game × category | Revenue, COGS, gross profit, and margin % for Food / Beverage / Alcohol / Other |

---

### Fact Tables — Monthly

| Table | Rows | Grain | Description |
|-------|------|-------|-------------|
| `fact_monthly_pnl.parquet` | 60 | 1 row per month (2022–2026) | **Primary income statement.** All `rev_*` revenue lines, all `exp_*` expense lines, plus `gross_profit`, `ebitda`, `ebit`, `ebt`, `net_income`, margin %, home game count, playoff flag |
| `fact_merchandise.parquet` | 1,440 | 1 row per month × category × channel | Revenue, COGS, gross profit, units sold — broken out by 8 categories (Jerseys, T-Shirts, Hats, etc.) and 3 channels (Stadium / Online / Wholesale) |
| `fact_payroll.parquet` | 600 | 1 row per month × department | Base salary, bonuses, benefits, total comp, headcount — for 10 departments (Player Roster, Practice Squad, Coaching Staff, Football Ops, Scouting, Business Ops, Marketing, Stadium Ops, Technology, Finance & Legal) |
| `fact_sponsorship_revenue.parquet` | 540 | 1 row per month × sponsor | Monthly revenue recognized per active sponsorship deal; includes contract year and category |
| `fact_broadcasting.parquet` | 60 | 1 row per month | National TV revenue (NFL rev-share, ~$185–235M/yr recognized during regular season months) and local TV/streaming revenue |
| `fact_sth_renewals.parquet` | 4 | 1 row per season (2023–2026) | Season ticket holder renewal metrics: prior-year holders, renewals, renewal rate %, new sales, upgrades, downgrades, cancellations, average package price |

---

### Annual Rollup

| Table | Rows | Description |
|-------|------|-------------|
| `fact_annual_summary.parquet` | 5 | One row per year (2022–2026). Revenue, expenses, EBITDA, net income, margins, win %, playoff flag, season ticket holder count |

---

### Forecasting & Budget Tables

| Table | Rows | Description |
|-------|------|-------------|
| `budget_2027.parquet` | 12 | Monthly 2027 budget. Each row has a `_budget` column and a `_2026_actual` column for every revenue and expense line — ready for side-by-side comparison. Built from 2026 actuals × management growth assumptions |
| `budget_2027_annual.parquet` | 1 | Annual 2027 budget rollup. Single-row summary with all `_budget` totals |
| `fact_variance_2027.parquet` | 12 | Variance tracking template for 2027. All `_actual` fields are `null`; `status = "Forecast"`. As each month closes, populate actuals and flip status to `"Actuals"` to practice variance reporting |

---

## Key Revenue Streams

| Stream | 2026 Actual | Notes |
|--------|-------------|-------|
| National Broadcasting | $235M | Largest stream. NFL TV deal distributed equally across 32 teams; recognized Sept–Jan |
| Gate — Regular Season | $166M | 9 home games × ~68,500 avg attendance × ~$200 blended avg ticket price |
| Sponsorship | $55M | 12 active deals including naming rights ($18M), jersey ($9.5M), and official partners |
| Merchandise | $49M | All channels: stadium store, e-commerce, wholesale |
| Concessions | $35M | Food / beverage / alcohol / other; ~78% game-day participation rate |
| Premium Suites | $35M | 80 luxury suites + club level (8% of capacity) |
| Parking | $22M | ~$55/vehicle, ~2.2 persons/vehicle |
| Local Broadcasting | $11M | Regional TV + streaming deal |
| Gate — Playoffs | $22M | Playoff home games (Wild Card through Super Bowl in 2026) |

---

## Key Expense Lines

| Line | 2026 Actual | Notes |
|------|-------------|-------|
| Player Salaries | ~$189M | ~94% of $300.5M salary cap |
| Player Benefits | ~$28M | ~15% of salary |
| Front Office & Staff | ~$54M | All non-player, non-coaching staff (4%/yr raises) |
| Player Bonuses | ~$23M | Signing bonuses heavy in March–May; performance bonuses in February |
| Coaching Staff | ~$32M | Scales with salary cap trajectory |
| Stadium Rent | ~$20M | Favorable city lease (naming rights deal offsets) |
| Marketing | ~$22M | Growing investment in fan base development |
| Stadium Operations | ~$17M | Base ops + per-game variable costs |
| Depreciation | ~$16M | Stadium improvements and capital investments |
| Technology | ~$10M | Analytics platform investment growing at 8%/yr |

---

## 2027 Budget Assumptions

The `budget_2027` tables were built by applying these management growth assumptions to 2026 actuals:

| Category | Growth |
|----------|--------|
| Gate (Regular Season) | +6.0% | 
| National Broadcasting | +6.2% (known NFL deal escalator) |
| Sponsorship | +9.0% (new deals in pipeline) |
| Merchandise | +7.0% |
| Gate (Playoffs) | +10.0% (optimistic run assumption) |
| Player Salaries | +7.5% (salary cap increase) |
| Technology | +12.0% (analytics platform build-out) |
| Interest Expense | -3.0% (paying down debt) |

---

## How to Use This Database

### Setup

```bash
# Activate the project venv
source venv/bin/activate

# Install dependencies (includes pyarrow for parquet reading)
pip install -r requirements.txt
```

> **Note:** Open `main.ipynb` and select the **"NFL FP&A (venv)"** kernel. If it doesn't appear, register it with:
> ```bash
> python -m ipykernel install --user --name "nfl-forecasting" --display-name "NFL FP&A (venv)"
> ```

### Loading Tables

```python
import pandas as pd

pnl     = pd.read_parquet("data/fact_monthly_pnl.parquet")
budget  = pd.read_parquet("data/budget_2027.parquet")
games   = pd.read_parquet("data/dim_game.parquet")
attend  = pd.read_parquet("data/fact_attendance.parquet")
```

### Suggested Exercises

**Forecasting**
- Build a 12-month 2027 revenue forecast using time-series methods (ARIMA, ETS, Prophet) against `fact_monthly_pnl`
- Decompose seasonality (NFL regular season Sept–Jan peaks) vs trend in gate revenue
- Driver-based model: tie gate revenue to game count × attendance × avg price using `fact_ticket_sales` and `fact_attendance`
- Sensitivity analysis on national broadcasting growth rate assumptions

**Variance Reporting**
- Populate `fact_variance_2027` as each month "closes" — compare actuals to `budget_2027`
- Calculate favorable/unfavorable variances by revenue stream and expense line
- Build a monthly business review (MBR) narrative: explain what drove variances
- Bridge analysis: volume vs price vs mix variances on ticket revenue

**Deeper Analysis**
- Correlate win % with gate revenue, merchandise, and attendance using `fact_annual_summary` + `dim_game`
- Cohort analysis on season ticket holder renewals using `fact_sth_renewals` + `dim_customer`
- Concession yield analysis (revenue per attendee by game type/weather) using `fact_concessions` + `fact_attendance`
- Payroll efficiency: player cost per win using `fact_payroll` + `dim_game`

---

## Regenerating the Data

```bash
python3 generate_data.py
```

All 21 parquet files and `schema_manifest.json` will be rewritten. The random seed is fixed (`rng = np.random.default_rng(42)`) so output is deterministic.
