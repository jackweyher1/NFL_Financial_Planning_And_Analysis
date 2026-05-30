"""
Austin Armadillos NFL Team - Financial Database Generator
Fictional expansion team, AFC South. Data covers 2022-2026 actuals.
Context: We are in December 2026, building 2027 12-month forward forecast.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import date, timedelta

rng = np.random.default_rng(42)
random.seed(42)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

TEAM_NAME = "Austin Armadillos"
TEAM_ABR  = "AAR"
STADIUM   = "Lone Star Field"
CAPACITY  = 68_500
CITY      = "Austin, TX"
DIVISION  = "AFC South"

AFC_SOUTH_OPPONENTS = ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars"]
OTHER_AFC           = ["Kansas City Chiefs", "Buffalo Bills", "Baltimore Ravens",
                       "Cincinnati Bengals", "Miami Dolphins", "Cleveland Browns",
                       "Pittsburgh Steelers", "Tennessee Titans", "New England Patriots",
                       "Denver Broncos", "Las Vegas Raiders", "Los Angeles Chargers"]
NFC_OPPONENTS       = ["Dallas Cowboys", "Philadelphia Eagles", "New York Giants",
                       "Washington Commanders", "San Francisco 49ers", "Los Angeles Rams",
                       "Seattle Seahawks", "Arizona Cardinals", "Green Bay Packers",
                       "Chicago Bears", "Detroit Lions", "Minnesota Vikings",
                       "New Orleans Saints", "Atlanta Falcons", "Tampa Bay Buccaneers",
                       "Carolina Panthers"]

TICKET_TIERS = [
    {"tier_id": 1, "tier_name": "General Admission",    "section": "Upper Bowl",   "base_price": 75.0,   "capacity_alloc": 0.35},
    {"tier_id": 2, "tier_name": "Lower Bowl",           "section": "Lower Bowl",   "base_price": 145.0,  "capacity_alloc": 0.28},
    {"tier_id": 3, "tier_name": "Club Level",           "section": "Club",         "base_price": 285.0,  "capacity_alloc": 0.15},
    {"tier_id": 4, "tier_name": "Premium Club",         "section": "Premium Club", "base_price": 450.0,  "capacity_alloc": 0.08},
    {"tier_id": 5, "tier_name": "Suite",                "section": "Suites",       "base_price": 8500.0, "capacity_alloc": 0.04},  # per-suite price
    {"tier_id": 6, "tier_name": "Standing Room Only",   "section": "SRO",          "base_price": 45.0,   "capacity_alloc": 0.05},
    {"tier_id": 7, "tier_name": "Field Pass",           "section": "Field",        "base_price": 1200.0, "capacity_alloc": 0.005},
]

EXPENSE_CATEGORIES = [
    # Player-related
    {"cat_id": 1,  "category": "Player Salaries",         "department": "Football Operations",   "type": "COGS"},
    {"cat_id": 2,  "category": "Player Bonuses",          "department": "Football Operations",   "type": "COGS"},
    {"cat_id": 3,  "category": "Player Benefits",         "department": "Football Operations",   "type": "COGS"},
    # Coaching & Staff
    {"cat_id": 4,  "category": "Coaching Staff Salaries", "department": "Football Operations",   "type": "OpEx"},
    {"cat_id": 5,  "category": "Front Office Salaries",   "department": "G&A",                   "type": "OpEx"},
    {"cat_id": 6,  "category": "Scouting & Draft",        "department": "Football Operations",   "type": "OpEx"},
    # Stadium
    {"cat_id": 7,  "category": "Stadium Rent/Lease",      "department": "Facilities",            "type": "OpEx"},
    {"cat_id": 8,  "category": "Stadium Operations",      "department": "Facilities",            "type": "OpEx"},
    {"cat_id": 9,  "category": "Maintenance & Capital",   "department": "Facilities",            "type": "CapEx"},
    # Game Day
    {"cat_id": 10, "category": "Game Day Operations",     "department": "Game Day",              "type": "COGS"},
    {"cat_id": 11, "category": "Security & Staffing",     "department": "Game Day",              "type": "COGS"},
    {"cat_id": 12, "category": "Concessions COGS",        "department": "Food & Beverage",       "type": "COGS"},
    {"cat_id": 13, "category": "Merchandise COGS",        "department": "Retail",                "type": "COGS"},
    # Marketing & Sales
    {"cat_id": 14, "category": "Marketing & Advertising", "department": "Marketing",             "type": "OpEx"},
    {"cat_id": 15, "category": "Ticket Sales & CRM",      "department": "Sales",                 "type": "OpEx"},
    {"cat_id": 16, "category": "Community Relations",     "department": "Marketing",             "type": "OpEx"},
    # G&A
    {"cat_id": 17, "category": "Legal & Compliance",      "department": "G&A",                   "type": "OpEx"},
    {"cat_id": 18, "category": "Finance & Accounting",    "department": "G&A",                   "type": "OpEx"},
    {"cat_id": 19, "category": "Technology & IT",         "department": "G&A",                   "type": "OpEx"},
    {"cat_id": 20, "category": "Travel & Lodging",        "department": "Football Operations",   "type": "COGS"},
    {"cat_id": 21, "category": "Insurance",               "department": "G&A",                   "type": "OpEx"},
    {"cat_id": 22, "category": "League Dues & Assessments","department": "G&A",                  "type": "OpEx"},
    {"cat_id": 23, "category": "Depreciation & Amortiz.", "department": "G&A",                   "type": "OpEx"},
    {"cat_id": 24, "category": "Interest Expense",        "department": "Finance",               "type": "Non-OpEx"},
]

REVENUE_CATEGORIES = [
    {"cat_id": 1,  "category": "Gate Revenue – Regular Season",  "stream": "Tickets"},
    {"cat_id": 2,  "category": "Gate Revenue – Preseason",       "stream": "Tickets"},
    {"cat_id": 3,  "category": "Gate Revenue – Playoffs",        "stream": "Tickets"},
    {"cat_id": 4,  "category": "Premium Seating & Suites",       "stream": "Tickets"},
    {"cat_id": 5,  "category": "Season Ticket Packages",         "stream": "Tickets"},
    {"cat_id": 6,  "category": "Concessions – Food",             "stream": "Concessions"},
    {"cat_id": 7,  "category": "Concessions – Beverage",         "stream": "Concessions"},
    {"cat_id": 8,  "category": "Concessions – Alcohol",          "stream": "Concessions"},
    {"cat_id": 9,  "category": "Concessions – Other",            "stream": "Concessions"},
    {"cat_id": 10, "category": "Merchandise – Stadium",          "stream": "Merchandise"},
    {"cat_id": 11, "category": "Merchandise – Online",           "stream": "Merchandise"},
    {"cat_id": 12, "category": "Merchandise – Wholesale",        "stream": "Merchandise"},
    {"cat_id": 13, "category": "National Broadcasting (NFL Share)","stream": "Broadcasting"},
    {"cat_id": 14, "category": "Local Broadcasting & Streaming", "stream": "Broadcasting"},
    {"cat_id": 15, "category": "Naming Rights",                  "stream": "Sponsorship"},
    {"cat_id": 16, "category": "Jersey Sponsorship",             "stream": "Sponsorship"},
    {"cat_id": 17, "category": "Official Partner Sponsorships",  "stream": "Sponsorship"},
    {"cat_id": 18, "category": "In-Stadium Advertising",         "stream": "Sponsorship"},
    {"cat_id": 19, "category": "Parking & Transportation",       "stream": "Parking"},
    {"cat_id": 20, "category": "Licensing & Royalties",          "stream": "Other"},
    {"cat_id": 21, "category": "Player Appearance Fees",         "stream": "Other"},
    {"cat_id": 22, "category": "Event Rental (non-NFL)",         "stream": "Other"},
    {"cat_id": 23, "category": "Interest & Investment Income",   "stream": "Other"},
]

SPONSORS = [
    {"sponsor_id": 1,  "company": "LoneStar Energy Co.",      "category": "Naming Rights",            "annual_value": 18_000_000, "start_year": 2022, "end_year": 2032},
    {"sponsor_id": 2,  "company": "Texan Trust Bank",         "category": "Jersey Sponsorship",       "annual_value": 9_500_000,  "start_year": 2023, "end_year": 2028},
    {"sponsor_id": 3,  "company": "CapTech Wireless",         "category": "Official Telecom Partner", "annual_value": 6_200_000,  "start_year": 2022, "end_year": 2027},
    {"sponsor_id": 4,  "company": "ArmadilloAuto Group",      "category": "Official Auto Partner",    "annual_value": 4_800_000,  "start_year": 2024, "end_year": 2029},
    {"sponsor_id": 5,  "company": "BlueSky Airlines",         "category": "Official Airline",         "annual_value": 3_500_000,  "start_year": 2022, "end_year": 2026},
    {"sponsor_id": 6,  "company": "Texas Premier Health",     "category": "Official Health Partner",  "annual_value": 2_800_000,  "start_year": 2023, "end_year": 2028},
    {"sponsor_id": 7,  "company": "RanchHand Boots",          "category": "Official Apparel Partner", "annual_value": 2_200_000,  "start_year": 2022, "end_year": 2027},
    {"sponsor_id": 8,  "company": "Hill Country Beer Co.",    "category": "Official Beer Partner",    "annual_value": 3_100_000,  "start_year": 2022, "end_year": 2025},
    {"sponsor_id": 9,  "company": "Pedernales Brewing Co.",   "category": "Official Beer Partner",    "annual_value": 3_600_000,  "start_year": 2026, "end_year": 2031},
    {"sponsor_id": 10, "company": "StreamVault Media",        "category": "Digital Content Partner",  "annual_value": 1_800_000,  "start_year": 2025, "end_year": 2028},
    {"sponsor_id": 11, "company": "Gulf Coast Insurance",     "category": "Official Insurance",       "annual_value": 1_500_000,  "start_year": 2024, "end_year": 2027},
    {"sponsor_id": 12, "company": "Mesquite Grill Restaurants","category": "Official Restaurant",     "annual_value": 1_200_000,  "start_year": 2023, "end_year": 2026},
]

MERCHANDISE_CATEGORIES = ["Jerseys", "T-Shirts", "Hats/Caps", "Jackets/Hoodies",
                           "Accessories", "Youth Apparel", "Collectibles", "Home Goods"]

CONCESSION_CATEGORIES = [
    {"cat": "Food",      "avg_spend_per_head": 14.50, "cogs_pct": 0.38},
    {"cat": "Beverage",  "avg_spend_per_head": 8.00,  "cogs_pct": 0.25},
    {"cat": "Alcohol",   "avg_spend_per_head": 22.00, "cogs_pct": 0.20},
    {"cat": "Other",     "avg_spend_per_head": 4.50,  "cogs_pct": 0.45},
]

# Team performance by season — expansion team builds over time
SEASON_PROFILE = {
    2022: {"win_pct": 0.35, "playoff": False, "brand_multiplier": 0.72, "st_holders": 28_000},
    2023: {"win_pct": 0.47, "playoff": False, "brand_multiplier": 0.85, "st_holders": 36_000},
    2024: {"win_pct": 0.59, "playoff": True,  "brand_multiplier": 1.00, "st_holders": 48_000},
    2025: {"win_pct": 0.65, "playoff": True,  "brand_multiplier": 1.12, "st_holders": 54_000},
    2026: {"win_pct": 0.71, "playoff": True,  "brand_multiplier": 1.22, "st_holders": 58_500},
}

# NFL national TV deal per team per year (all 32 teams split equally, growing)
NFL_TV_SHARE = {2022: 185_000_000, 2023: 195_000_000, 2024: 208_000_000,
                2025: 221_000_000, 2026: 235_000_000}

# NFL salary cap
SALARY_CAP = {2022: 208_200_000, 2023: 224_800_000, 2024: 255_400_000,
              2025: 279_200_000, 2026: 300_500_000}


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def noise(base, pct=0.05, n=1):
    """Return base value with ~pct random noise."""
    if n == 1:
        return base * (1 + rng.normal(0, pct))
    return base * (1 + rng.normal(0, pct, n))

def month_date(year, month):
    return date(year, month, 1)


# ─────────────────────────────────────────────
# 1. DIMENSION TABLES
# ─────────────────────────────────────────────

def build_dim_team():
    df = pd.DataFrame([{
        "team_id": 1, "team_name": TEAM_NAME, "abbreviation": TEAM_ABR,
        "city": CITY, "stadium": STADIUM, "stadium_capacity": CAPACITY,
        "conference": "AFC", "division": DIVISION,
        "founded_year": 2022, "owner": "Duke Caldwell",
        "head_coach_current": "Marcus Webb",
        "gm_current": "Sandra Okafor",
        "team_colors": "Burnt Orange / Midnight Black / Desert Sand",
        "mascot": "Tex the Armadillo",
    }])
    df.to_parquet(DATA_DIR / "dim_team.parquet", index=False)
    print("  dim_team: 1 row")

def build_dim_ticket_tier():
    df = pd.DataFrame(TICKET_TIERS)
    df.to_parquet(DATA_DIR / "dim_ticket_tier.parquet", index=False)
    print(f"  dim_ticket_tier: {len(df)} rows")

def build_dim_expense_category():
    df = pd.DataFrame(EXPENSE_CATEGORIES)
    df.to_parquet(DATA_DIR / "dim_expense_category.parquet", index=False)
    print(f"  dim_expense_category: {len(df)} rows")

def build_dim_revenue_category():
    df = pd.DataFrame(REVENUE_CATEGORIES)
    df.to_parquet(DATA_DIR / "dim_revenue_category.parquet", index=False)
    print(f"  dim_revenue_category: {len(df)} rows")

def build_dim_sponsor():
    df = pd.DataFrame(SPONSORS)
    df.to_parquet(DATA_DIR / "dim_sponsor.parquet", index=False)
    print(f"  dim_sponsor: {len(df)} rows")

def build_dim_date():
    rows = []
    for y in range(2022, 2028):
        for m in range(1, 13):
            for d_offset in range(0, 28):  # simplified – not full calendar
                try:
                    dt = date(y, m, d_offset + 1)
                except:
                    continue
                rows.append({
                    "date_id": dt.isoformat(),
                    "full_date": dt,
                    "year": y, "month": m, "day": dt.day,
                    "quarter": (m - 1) // 3 + 1,
                    "week_of_year": dt.isocalendar()[1],
                    "day_of_week": dt.strftime("%A"),
                    "is_nfl_season": m in [8, 9, 10, 11, 12, 1, 2],
                    "month_name": dt.strftime("%B"),
                    "fiscal_year": y,
                })
    df = pd.DataFrame(rows)
    df.to_parquet(DATA_DIR / "dim_date.parquet", index=False)
    print(f"  dim_date: {len(df)} rows")

def build_dim_customer():
    """Season ticket holders + registered fans."""
    rows = []
    customer_id = 1
    first_names = ["James","Maria","David","Sarah","Michael","Jennifer","Robert","Linda",
                   "William","Barbara","Richard","Susan","Thomas","Jessica","Charles","Karen",
                   "Christopher","Nancy","Daniel","Lisa","Matthew","Betty","Anthony","Margaret",
                   "Mark","Sandra","Donald","Ashley","Steven","Dorothy","Paul","Kimberly",
                   "Andrew","Emily","Joshua","Donna","Kenneth","Michelle","Kevin","Carol",
                   "Brian","Amanda","George","Melissa","Timothy","Deborah","Ronald","Stephanie",
                   "Edward","Rebecca","Jason","Sharon","Jeffrey","Laura","Ryan","Cynthia",
                   "Jacob","Kathleen","Gary","Amy","Nicholas","Angela","Eric","Shirley",
                   "Jonathan","Anna","Stephen","Brenda","Larry","Pamela","Justin","Emma"]
    last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
                   "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson",
                   "Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White",
                   "Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young",
                   "Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green",
                   "Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts"]
    zip_codes   = ["78701","78702","78703","78704","78705","78712","78721","78723","78741",
                   "78745","78748","78750","78752","78756","78757","78758","78759","78660",
                   "78681","78613","78664","78758","76574","78628","78130"]

    for i in range(65_000):
        first = random.choice(first_names)
        last  = random.choice(last_names)
        join_year = random.choices([2022, 2023, 2024, 2025, 2026], weights=[5, 12, 25, 30, 28])[0]
        cust_type = random.choices(
            ["Season Ticket Holder", "Mini Plan", "Single Game Buyer", "Online Fan", "Suite Holder"],
            weights=[35, 15, 30, 18, 2]
        )[0]
        rows.append({
            "customer_id": customer_id,
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{random.randint(10,999)}@{'gmail' if random.random()<0.5 else 'yahoo' if random.random()<0.6 else 'hotmail'}.com",
            "zip_code": random.choice(zip_codes),
            "city": random.choices(["Austin", "Round Rock", "Cedar Park", "Georgetown",
                                    "San Marcos", "Kyle", "Buda", "Pflugerville"],
                                   weights=[45, 12, 10, 8, 7, 6, 6, 6])[0],
            "state": "TX",
            "customer_type": cust_type,
            "join_date": date(join_year, random.randint(1, 12), random.randint(1, 28)),
            "is_active": random.random() < 0.78,
            "lifetime_spend": round(rng.uniform(50, 15000), 2),
            "preferred_channel": random.choice(["Mobile App", "Website", "Box Office", "Phone"]),
            "age_group": random.choices(["18-24","25-34","35-44","45-54","55-64","65+"],
                                         weights=[10,22,25,20,14,9])[0],
            "gender": random.choices(["Male","Female","Other/Unspecified"],weights=[54,42,4])[0],
            "loyalty_tier": random.choices(["Bronze","Silver","Gold","Platinum"],
                                            weights=[40,30,20,10])[0],
        })
        customer_id += 1

    df = pd.DataFrame(rows)
    df["join_date"] = pd.to_datetime(df["join_date"])
    df.to_parquet(DATA_DIR / "dim_customer.parquet", index=False)
    print(f"  dim_customer: {len(df)} rows")


# ─────────────────────────────────────────────
# 2. GAME SCHEDULE / RESULTS
# ─────────────────────────────────────────────

def _make_season_schedule(year):
    """Generate a plausible 17-game schedule + 3 preseason games."""
    profile   = SEASON_PROFILE[year]
    win_pct   = profile["win_pct"]

    # Preseason: late July / August
    opponents_pool = AFC_SOUTH_OPPONENTS + OTHER_AFC[:8] + NFC_OPPONENTS[:8]
    random.shuffle(opponents_pool)

    games = []
    game_id_base = (year - 2022) * 300

    # Preseason (3 games)
    pre_start = date(year, 8, 10)
    for i in range(3):
        opp  = opponents_pool[i]
        gdate = pre_start + timedelta(weeks=i)
        home  = (i % 2 == 0)
        win   = random.random() < 0.50  # preseason less meaningful
        team_pts = random.randint(14, 35)
        opp_pts  = random.randint(14, 35) if not win else random.randint(7, team_pts - 1)
        if not win: team_pts = random.randint(7, opp_pts - 1)
        games.append({
            "game_id": game_id_base + i + 1,
            "season": year,
            "week": f"PRE{i+1}",
            "game_type": "Preseason",
            "game_date": gdate,
            "opponent": opp,
            "home_away": "Home" if home else "Away",
            "team_score": team_pts,
            "opp_score": opp_pts,
            "result": "W" if win else "L",
            "day_of_week": gdate.strftime("%A"),
        })

    # Regular season (17 weeks, starting first Thursday of September)
    # Approximate first game = first Thursday in September
    sep1 = date(year, 9, 1)
    days_to_thu = (3 - sep1.weekday()) % 7
    rs_start = sep1 + timedelta(days=days_to_thu)

    all_opponents = (AFC_SOUTH_OPPONENTS * 2 + OTHER_AFC[:6] + NFC_OPPONENTS[:8])
    random.shuffle(all_opponents)
    all_opponents = all_opponents[:17]

    wins = 0
    for i in range(17):
        opp   = all_opponents[i]
        wk    = i + 1
        # Games on Sundays mostly, a few on Thursday/Monday
        if i == 0:
            gdate = rs_start  # Thursday opener
        else:
            gdate = rs_start + timedelta(weeks=i, days=3)  # mostly Sundays
        home  = (i % 2 == 0)
        win   = random.random() < win_pct
        if win: wins += 1
        team_pts = random.randint(17, 38)
        opp_pts  = random.randint(10, team_pts - 1) if win else random.randint(team_pts + 1, team_pts + 17)
        games.append({
            "game_id": game_id_base + 10 + i,
            "season": year,
            "week": f"W{wk:02d}",
            "game_type": "Regular Season",
            "game_date": gdate,
            "opponent": opp,
            "home_away": "Home" if home else "Away",
            "team_score": team_pts,
            "opp_score": opp_pts,
            "result": "W" if win else "L",
            "day_of_week": gdate.strftime("%A"),
        })

    # Playoffs (conditional)
    if profile["playoff"]:
        playoff_rounds = ["Wild Card", "Divisional", "Conference Championship"]
        if year == 2024:
            playoff_rounds = ["Wild Card", "Divisional"]  # early exit
        if year == 2026:
            playoff_rounds = ["Wild Card", "Divisional", "Conference Championship", "Super Bowl"]

        jan_base = date(year + 1, 1, 13)
        for r_i, rnd in enumerate(playoff_rounds):
            opp  = random.choice(AFC_SOUTH_OPPONENTS + OTHER_AFC[:4])
            gdate = jan_base + timedelta(weeks=r_i)
            home  = (r_i == 0)  # home field for wild card
            win   = (r_i < len(playoff_rounds) - 1) or (year == 2026)
            team_pts = random.randint(20, 38)
            opp_pts  = random.randint(10, team_pts - 1) if win else random.randint(team_pts + 1, team_pts + 14)
            games.append({
                "game_id": game_id_base + 100 + r_i,
                "season": year,
                "week": rnd.replace(" ", "_"),
                "game_type": "Playoff",
                "game_date": gdate,
                "opponent": opp,
                "home_away": "Home" if home else "Away",
                "team_score": team_pts,
                "opp_score": opp_pts,
                "result": "W" if win else "L",
                "day_of_week": gdate.strftime("%A"),
            })

    return games

def build_dim_game():
    all_games = []
    for yr in range(2022, 2027):
        all_games.extend(_make_season_schedule(yr))
    df = pd.DataFrame(all_games)
    df["game_date"] = pd.to_datetime(df["game_date"])
    df.to_parquet(DATA_DIR / "dim_game.parquet", index=False)
    print(f"  dim_game: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 3. ATTENDANCE
# ─────────────────────────────────────────────

def build_fact_attendance(games_df):
    home_games = games_df[games_df["home_away"] == "Home"].copy()
    rows = []
    for _, g in home_games.iterrows():
        profile  = SEASON_PROFILE.get(g["season"], SEASON_PROFILE[2026])
        mult     = profile["brand_multiplier"]
        cap_util = min(1.0, noise(0.91 * mult, 0.04))
        if g["game_type"] == "Preseason":
            cap_util = noise(0.68, 0.05)
        elif g["game_type"] == "Playoff":
            cap_util = min(1.0, noise(0.985, 0.01))

        tickets_sold = int(CAPACITY * cap_util)
        tickets_scanned = int(tickets_sold * noise(0.94, 0.03))
        parking_vehicles = int(tickets_scanned * noise(0.38, 0.05))
        rows.append({
            "game_id": g["game_id"],
            "season": g["season"],
            "game_date": g["game_date"],
            "game_type": g["game_type"],
            "opponent": g["opponent"],
            "tickets_sold": tickets_sold,
            "tickets_scanned": tickets_scanned,
            "no_shows": tickets_sold - tickets_scanned,
            "capacity_utilization_pct": round(tickets_scanned / CAPACITY * 100, 2),
            "standing_room_sold": int(CAPACITY * 0.05 * noise(0.7, 0.1)) if cap_util > 0.95 else 0,
            "parking_vehicles": parking_vehicles,
            "weather_conditions": random.choices(
                ["Clear","Partly Cloudy","Overcast","Light Rain","Hot & Humid","Windy","Perfect"],
                weights=[25, 20, 20, 10, 10, 10, 5]
            )[0],
            "temp_fahrenheit": int(noise(72 if g["game_date"].month in [9,10] else 58, 0.12)),
        })
    df = pd.DataFrame(rows)
    df["game_date"] = pd.to_datetime(df["game_date"])
    df.to_parquet(DATA_DIR / "fact_attendance.parquet", index=False)
    print(f"  fact_attendance: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 4. TICKET SALES (per game per tier)
# ─────────────────────────────────────────────

def build_fact_ticket_sales(games_df):
    home_games = games_df[games_df["home_away"] == "Home"].copy()
    rows = []
    for _, g in home_games.iterrows():
        profile = SEASON_PROFILE.get(g["season"], SEASON_PROFILE[2026])
        mult    = profile["brand_multiplier"]
        base_fill = 0.91 * mult
        if g["game_type"] == "Preseason": base_fill = 0.68
        if g["game_type"] == "Playoff":   base_fill = 0.99

        for tier in TICKET_TIERS:
            tier_id    = tier["tier_id"]
            tier_cap   = int(CAPACITY * tier["capacity_alloc"])
            fill_rate  = min(1.0, noise(base_fill, 0.05))
            qty        = int(tier_cap * fill_rate)
            # Suites priced per suite, not per seat
            if tier_id == 5:
                n_suites    = 80
                suites_sold = int(n_suites * min(1.0, noise(0.88 * mult, 0.06)))
                suite_price = noise(tier["base_price"], 0.08) * (1 + 0.03 * (g["season"] - 2022))
                qty         = suites_sold
                avg_price   = suite_price
            else:
                premium     = 1.0 + 0.10 * (g["season"] - 2022)  # price escalation YoY
                matchup_adj = 1.15 if g["opponent"] in ["Kansas City Chiefs","Dallas Cowboys","New England Patriots"] else 1.0
                playoff_adj = 1.40 if g["game_type"] == "Playoff" else 1.0
                avg_price   = noise(tier["base_price"] * premium * matchup_adj * playoff_adj, 0.06)

            channel_split = rng.dirichlet([3, 2, 1])  # online, box_office, secondary
            channels = ["Online", "Box Office", "Secondary Market"]

            for ch_i, ch in enumerate(channels):
                ch_qty = int(qty * channel_split[ch_i])
                if ch_qty == 0:
                    continue
                rows.append({
                    "game_id": g["game_id"],
                    "season": g["season"],
                    "game_date": g["game_date"],
                    "game_type": g["game_type"],
                    "tier_id": tier_id,
                    "tier_name": tier["tier_name"],
                    "channel": ch,
                    "quantity_sold": ch_qty,
                    "avg_price": round(avg_price, 2),
                    "gross_revenue": round(ch_qty * avg_price, 2),
                    "discount_pct": round(noise(0.03 if ch == "Online" else 0.05, 0.5), 4),
                })

    df = pd.DataFrame(rows)
    df["game_date"] = pd.to_datetime(df["game_date"])
    df.to_parquet(DATA_DIR / "fact_ticket_sales.parquet", index=False)
    print(f"  fact_ticket_sales: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 5. CONCESSIONS (per game per category)
# ─────────────────────────────────────────────

def build_fact_concessions(games_df, attendance_df):
    rows = []
    attend_map = attendance_df.set_index("game_id")["tickets_scanned"].to_dict()

    for _, g in games_df[games_df["home_away"] == "Home"].iterrows():
        attendance = attend_map.get(g["game_id"], 55000)
        # not everyone buys concessions; participation ~75%
        buyers = int(attendance * noise(0.75, 0.05))

        for cc in CONCESSION_CATEGORIES:
            rev = round(buyers * noise(cc["avg_spend_per_head"], 0.10), 2)
            # alcohol lower in early cold months
            if cc["cat"] == "Alcohol" and g["game_date"].month in [1, 2]:
                rev *= 0.88
            cogs = round(rev * noise(cc["cogs_pct"], 0.05), 2)
            rows.append({
                "game_id": g["game_id"],
                "season": g["season"],
                "game_date": g["game_date"],
                "game_type": g["game_type"],
                "category": cc["cat"],
                "attendance": attendance,
                "revenue": rev,
                "cogs": cogs,
                "gross_profit": round(rev - cogs, 2),
                "gross_margin_pct": round((rev - cogs) / rev * 100, 2) if rev > 0 else 0,
            })

    df = pd.DataFrame(rows)
    df["game_date"] = pd.to_datetime(df["game_date"])
    df.to_parquet(DATA_DIR / "fact_concessions.parquet", index=False)
    print(f"  fact_concessions: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 6. MERCHANDISE (monthly)
# ─────────────────────────────────────────────

def build_fact_merchandise():
    rows = []
    for year in range(2022, 2027):
        profile = SEASON_PROFILE[year]
        mult    = profile["brand_multiplier"]
        base_annual_merch = 38_000_000 * mult  # ~$38M at 1.0x brand

        for month in range(1, 13):
            # Seasonality: peaks at season start (Sept), Christmas, post-Super Bowl
            seasonality = {
                1: 1.35, 2: 1.10, 3: 0.70, 4: 0.60, 5: 0.55, 6: 0.60,
                7: 0.75, 8: 1.05, 9: 1.30, 10: 1.15, 11: 1.10, 12: 1.20
            }
            month_base = base_annual_merch / 12 * seasonality[month]

            # Extra bump if in playoffs (Jan/Feb)
            if profile["playoff"] and month in [1, 2]:
                month_base *= 1.50

            for cat in MERCHANDISE_CATEGORIES:
                cat_weights = {
                    "Jerseys": 0.28, "T-Shirts": 0.20, "Hats/Caps": 0.15,
                    "Jackets/Hoodies": 0.12, "Accessories": 0.08,
                    "Youth Apparel": 0.07, "Collectibles": 0.06, "Home Goods": 0.04
                }
                w = cat_weights[cat]
                cat_rev = month_base * w

                # Three channels
                for ch, ch_w, margin in [("Stadium", 0.45, 0.52), ("Online", 0.38, 0.48), ("Wholesale", 0.17, 0.30)]:
                    rev  = round(noise(cat_rev * ch_w, 0.08), 2)
                    cogs = round(rev * (1 - noise(margin, 0.05)), 2)
                    rows.append({
                        "year": year, "month": month,
                        "month_date": month_date(year, month),
                        "category": cat,
                        "channel": ch,
                        "revenue": rev,
                        "cogs": cogs,
                        "gross_profit": round(rev - cogs, 2),
                        "units_sold": int(rev / noise(35, 0.15)),  # rough avg unit price $35
                    })

    df = pd.DataFrame(rows)
    df["month_date"] = pd.to_datetime(df["month_date"])
    df.to_parquet(DATA_DIR / "fact_merchandise.parquet", index=False)
    print(f"  fact_merchandise: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 7. PAYROLL (monthly by department)
# ─────────────────────────────────────────────

def build_fact_payroll():
    rows = []
    depts = [
        # dept, base_annual (2022), headcount, type
        ("Player Roster",        SALARY_CAP[2022] * 0.92, 53,  "Player"),
        ("Practice Squad",       6_000_000,                16,  "Player"),
        ("Coaching Staff",       28_000_000,                28,  "Staff"),
        ("Football Operations",  12_000_000,                35,  "Staff"),
        ("Scouting & Analytics",  5_500_000,                22,  "Staff"),
        ("Business Operations",  18_000_000,                90,  "Staff"),
        ("Marketing & Sales",    11_000_000,                55,  "Staff"),
        ("Stadium Operations",    9_000_000,               120,  "Staff"),
        ("Technology",            6_500_000,                30,  "Staff"),
        ("Finance & Legal",       7_200_000,                28,  "Staff"),
    ]

    for year in range(2022, 2027):
        cap_ratio = SALARY_CAP[year] / SALARY_CAP[2022]
        staff_raise = 1.04 ** (year - 2022)  # 4% annual staff raises

        for month in range(1, 13):
            for dept, base_ann, headcount, emp_type in depts:
                if emp_type == "Player":
                    ann = base_ann * cap_ratio
                else:
                    ann = base_ann * staff_raise

                # Bonuses: players get signing bonuses heavy in March-May, staff bonuses in Feb/March
                base_monthly = ann / 12
                bonus = 0.0
                if emp_type == "Player" and month in [3, 4, 5]:
                    bonus = (ann * 0.12) / 3  # signing bonus spread
                if emp_type == "Player" and month == 2:
                    bonus = ann * 0.04  # playoff/performance bonuses
                if emp_type == "Staff" and month == 3:
                    bonus = base_monthly * 0.20

                benefits = base_monthly * (0.22 if emp_type == "Player" else 0.28)
                total = base_monthly + bonus + benefits

                rows.append({
                    "year": year, "month": month,
                    "month_date": month_date(year, month),
                    "department": dept,
                    "employee_type": emp_type,
                    "headcount": headcount + int(noise(0, 0.03) * headcount),
                    "base_salary": round(base_monthly, 2),
                    "bonuses": round(bonus, 2),
                    "benefits": round(benefits, 2),
                    "total_comp": round(total, 2),
                })

    df = pd.DataFrame(rows)
    df["month_date"] = pd.to_datetime(df["month_date"])
    df.to_parquet(DATA_DIR / "fact_payroll.parquet", index=False)
    print(f"  fact_payroll: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 8. SPONSORSHIP REVENUE (monthly recognition)
# ─────────────────────────────────────────────

def build_fact_sponsorship_revenue():
    rows = []
    for year in range(2022, 2027):
        for sp in SPONSORS:
            if not (sp["start_year"] <= year <= sp["end_year"]):
                continue
            annual = sp["annual_value"] * noise(1.0, 0.01)
            # straight-line monthly recognition with a small seasonal bump in season
            for month in range(1, 13):
                season_bump = 1.10 if month in [8, 9, 10, 11, 12] else 0.94
                base_monthly = annual / 12
                # Normalize so it still sums to annual
                rows.append({
                    "year": year, "month": month,
                    "month_date": month_date(year, month),
                    "sponsor_id": sp["sponsor_id"],
                    "company": sp["company"],
                    "category": sp["category"],
                    "recognized_revenue": round(base_monthly, 2),
                    "contract_year": year - sp["start_year"] + 1,
                })

    df = pd.DataFrame(rows)
    df["month_date"] = pd.to_datetime(df["month_date"])
    df.to_parquet(DATA_DIR / "fact_sponsorship_revenue.parquet", index=False)
    print(f"  fact_sponsorship_revenue: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 9. BROADCASTING REVENUE (monthly)
# ─────────────────────────────────────────────

def build_fact_broadcasting():
    rows = []
    for year in range(2022, 2027):
        national = NFL_TV_SHARE[year]
        local_deal = 8_500_000 * (1.06 ** (year - 2022))
        # National is recognized in 17 installments during regular season
        game_months = [9, 10, 11, 12, 1]
        national_per_month = national / len(game_months)

        for month in range(1, 13):
            nat_rev = national_per_month if month in game_months else 0
            loc_rev = local_deal / 12  # straight-line local deal
            rows.append({
                "year": year, "month": month,
                "month_date": month_date(year, month),
                "national_tv_revenue": round(nat_rev, 2),
                "local_tv_streaming_revenue": round(noise(loc_rev, 0.04), 2),
                "total_broadcasting": round(nat_rev + noise(loc_rev, 0.04), 2),
            })

    df = pd.DataFrame(rows)
    df["month_date"] = pd.to_datetime(df["month_date"])
    df.to_parquet(DATA_DIR / "fact_broadcasting.parquet", index=False)
    print(f"  fact_broadcasting: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 10. MONTHLY P&L SUMMARY (income statement rollup)
# ─────────────────────────────────────────────

def build_fact_monthly_pnl(games_df):
    """
    Rolled-up monthly income statement. Each row = 1 month.
    Revenue and expense buckets aligned to the revenue/expense dimension tables.
    """
    rows = []

    for year in range(2022, 2027):
        profile = SEASON_PROFILE[year]
        mult    = profile["brand_multiplier"]

        home_games_in_year = games_df[
            (games_df["home_away"] == "Home") & (games_df["season"] == year)
        ].copy()
        home_games_in_year["month"] = pd.to_datetime(home_games_in_year["game_date"]).dt.month

        # Precompute game count per month
        games_by_month = home_games_in_year.groupby("month").size().to_dict()

        # Salary cap utilization grows as roster matures (expansion teams start under cap)
        cap_util_pct = {2022: 0.82, 2023: 0.87, 2024: 0.91, 2025: 0.93, 2026: 0.94}.get(year, 0.94)
        # Ticket price (blended avg across tiers) escalates 5.5%/yr from $168 base in 2022
        avg_price_blended = noise(168 * (1.055 ** (year - 2022)), 0.03)
        # Per-head concession spend grows ~3%/yr from 2022 base
        conc_per_head = (14.5 + 8.0 + 22.0 + 4.5) * (1.03 ** (year - 2022))
        # Attendance capped at stadium capacity; brand mult drives sellout rate
        avg_attend_rs  = min(CAPACITY, int(CAPACITY * min(1.0, noise(0.88 * mult, 0.03))))
        avg_attend_pre = int(CAPACITY * noise(0.70, 0.04))
        # Premium seating: 80 suites + club level (8% of capacity)
        n_suites       = 80
        suite_fill     = min(1.0, noise(0.88 * mult, 0.04))
        club_fill      = min(1.0, noise(0.90 * mult, 0.03))
        suite_price_yr = noise(8500 * (1.04 ** (year - 2022)), 0.04)
        club_price_yr  = noise(320 * (1.05 ** (year - 2022)), 0.04)
        n_club_seats   = int(CAPACITY * 0.08)

        for month in range(1, 13):
            n_home = games_by_month.get(month, 0)
            has_playoff = (profile["playoff"] and month == 1)
            n_playoff_home = 1 if has_playoff else 0
            n_home_rs = n_home - n_playoff_home

            # TICKET REVENUE
            gate_rs      = n_home_rs * avg_attend_rs * avg_price_blended * noise(1, 0.03)
            gate_pre     = (1 if month == 8 else 0) * avg_attend_pre * 68 * noise(1, 0.05)
            gate_playoff = n_playoff_home * avg_attend_rs * avg_price_blended * 1.45 * noise(1, 0.03)

            # Premium: suites + club seats (sold separately from general gate)
            suite_rev_game = n_suites * suite_price_yr * suite_fill
            club_rev_game  = n_club_seats * club_price_yr * club_fill
            premium_rev    = (n_home_rs + n_playoff_home) * (suite_rev_game + club_rev_game)

            # CONCESSIONS (game-day attendees, ~78% participate)
            conc_rev = n_home * avg_attend_rs * 0.78 * conc_per_head * noise(1, 0.05)
            if n_home == 0: conc_rev = 0.0

            # MERCHANDISE (full-channel monthly — seasonality + playoff bumps)
            merch_season = {1:1.35,2:1.10,3:0.70,4:0.60,5:0.55,6:0.60,
                            7:0.75,8:1.05,9:1.30,10:1.15,11:1.10,12:1.20}
            merch_base   = 38_000_000 * mult / 12 * merch_season[month]
            if profile["playoff"] and month in [1, 2]:
                merch_base *= 1.50

            # BROADCASTING
            nat_tv = NFL_TV_SHARE[year] / 5 if month in [9, 10, 11, 12, 1] else 0
            loc_tv = 8_500_000 * (1.06 ** (year - 2022)) / 12

            # SPONSORSHIP
            active_sponsors = [s for s in SPONSORS if s["start_year"] <= year <= s["end_year"]]
            sponsor_rev = sum(s["annual_value"] for s in active_sponsors) / 12

            # PARKING (~40% of attendees drive, avg $52/vehicle, growing 3%/yr)
            avg_vehicle_price = noise(52 * (1.03 ** (year - 2022)), 0.05)
            parking_rev = n_home * (avg_attend_rs / 2.2) * avg_vehicle_price

            # OTHER
            licensing     = noise(3_200_000 * mult / 12, 0.08)
            events_rental = noise(180_000 if month not in [8, 9, 10, 11, 12] else 45_000, 0.20)

            total_revenue = (gate_rs + gate_pre + gate_playoff + premium_rev +
                             conc_rev + merch_base + nat_tv + loc_tv +
                             sponsor_rev + parking_rev + licensing + events_rental)

            # ── EXPENSES ───────────────────────────────────────────────────────
            # Player compensation (expansion team starts below cap; matures to ~94%)
            player_sal   = SALARY_CAP[year] * cap_util_pct / 12
            player_bonus = player_sal * (0.24 if month in [3,4,5] else (0.08 if month==2 else 0.01))
            player_ben   = player_sal * 0.15   # benefits (~15% of salary)

            # Coaching/football staff (scales with salary cap trajectory)
            coach_sal    = 22_000_000 * (SALARY_CAP[year] / SALARY_CAP[2022]) / 12

            # All other staff: FO, marketing, ops, tech, finance (~4% annual raise)
            fo_sal       = 45_000_000 * (1.04 ** (year - 2022)) / 12

            scouting     = noise(5_500_000 * (1.04 ** (year - 2022)) / 12, 0.10)
            stadium_rent = noise(20_000_000 / 12, 0.02)   # favorable city lease
            stadium_ops  = noise(15_000_000 / 12 + n_home * 140_000, 0.06)
            gameday_ops  = n_home * noise(195_000, 0.07)
            security     = n_home * noise(375_000, 0.06)
            conc_cogs    = conc_rev * noise(0.30, 0.04)
            merch_cogs   = merch_base * 0.48
            marketing    = noise(18_000_000 * (1.05 ** (year - 2022)) / 12, 0.10)
            ticket_sales = noise(7_000_000 / 12, 0.06)
            travel       = noise(4_000_000 / 12, 0.06) if month in [9,10,11,12,1] else noise(400_000 / 12, 0.10)
            insurance    = noise(7_500_000 / 12, 0.03)
            league_dues  = noise(5_000_000 / 12, 0.01)
            tech_it      = noise(6_500_000 * (1.08 ** (year - 2022)) / 12, 0.05)
            legal_fin    = noise(9_500_000 / 12, 0.06)
            capex_depr   = noise(16_000_000 / 12, 0.03)
            interest_exp = noise(8_500_000 * (0.97 ** (year - 2022)) / 12, 0.01)  # paying down debt

            total_expenses = (player_sal + player_bonus + player_ben + coach_sal + fo_sal +
                              scouting + stadium_rent + stadium_ops + gameday_ops + security +
                              conc_cogs + merch_cogs + marketing + ticket_sales + travel +
                              insurance + league_dues + tech_it + legal_fin + capex_depr + interest_exp)

            ebitda  = total_revenue - (total_expenses - capex_depr - interest_exp)
            ebit    = ebitda - capex_depr
            ebt     = ebit - interest_exp
            net_income = ebt * (1 - 0.21)  # simplified corp tax

            rows.append({
                "year": year, "month": month,
                "month_date": month_date(year, month),
                "quarter": (month - 1) // 3 + 1,
                # Revenue
                "rev_gate_regular_season": round(max(0, gate_rs), 0),
                "rev_gate_preseason": round(max(0, gate_pre), 0),
                "rev_gate_playoffs": round(max(0, gate_playoff), 0),
                "rev_premium_suites": round(max(0, premium_rev), 0),
                "rev_concessions": round(max(0, conc_rev), 0),
                "rev_merchandise": round(max(0, merch_base), 0),
                "rev_national_broadcasting": round(max(0, nat_tv), 0),
                "rev_local_broadcasting": round(max(0, loc_tv), 0),
                "rev_sponsorship": round(max(0, sponsor_rev), 0),
                "rev_parking": round(max(0, parking_rev), 0),
                "rev_licensing_other": round(max(0, licensing + events_rental), 0),
                "total_revenue": round(max(0, total_revenue), 0),
                # Expenses
                "exp_player_salaries": round(player_sal, 0),
                "exp_player_bonuses": round(player_bonus, 0),
                "exp_player_benefits": round(player_ben, 0),
                "exp_coaching_staff": round(coach_sal, 0),
                "exp_front_office_staff": round(fo_sal, 0),
                "exp_scouting": round(scouting, 0),
                "exp_stadium_rent": round(stadium_rent, 0),
                "exp_stadium_operations": round(stadium_ops, 0),
                "exp_gameday_operations": round(gameday_ops, 0),
                "exp_security": round(security, 0),
                "exp_concessions_cogs": round(conc_cogs, 0),
                "exp_merchandise_cogs": round(merch_cogs, 0),
                "exp_marketing": round(marketing, 0),
                "exp_ticket_sales": round(ticket_sales, 0),
                "exp_travel": round(travel, 0),
                "exp_insurance": round(insurance, 0),
                "exp_league_dues": round(league_dues, 0),
                "exp_technology": round(tech_it, 0),
                "exp_legal_finance": round(legal_fin, 0),
                "exp_depreciation": round(capex_depr, 0),
                "exp_interest": round(interest_exp, 0),
                "total_expenses": round(total_expenses, 0),
                # P&L
                "gross_profit": round(total_revenue - conc_cogs - merch_cogs, 0),
                "ebitda": round(ebitda, 0),
                "ebit": round(ebit, 0),
                "ebt": round(ebt, 0),
                "net_income": round(net_income, 0),
                "ebitda_margin_pct": round(ebitda / total_revenue * 100, 2) if total_revenue > 0 else 0,
                "net_margin_pct": round(net_income / total_revenue * 100, 2) if total_revenue > 0 else 0,
                # Meta
                "home_games_in_month": n_home,
                "is_playoff_month": has_playoff,
            })

    df = pd.DataFrame(rows)
    df["month_date"] = pd.to_datetime(df["month_date"])
    df.to_parquet(DATA_DIR / "fact_monthly_pnl.parquet", index=False)
    print(f"  fact_monthly_pnl: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 11. ANNUAL SUMMARY (quick view)
# ─────────────────────────────────────────────

def build_fact_annual_summary(pnl_df):
    annual = pnl_df.groupby("year").agg(
        total_revenue=("total_revenue", "sum"),
        total_expenses=("total_expenses", "sum"),
        gross_profit=("gross_profit", "sum"),
        ebitda=("ebitda", "sum"),
        ebit=("ebit", "sum"),
        net_income=("net_income", "sum"),
        home_games=("home_games_in_month", "sum"),
    ).reset_index()
    annual["ebitda_margin_pct"] = (annual["ebitda"] / annual["total_revenue"] * 100).round(2)
    annual["net_margin_pct"]    = (annual["net_income"] / annual["total_revenue"] * 100).round(2)
    for yr in annual["year"]:
        p = SEASON_PROFILE[yr]
        annual.loc[annual["year"]==yr, "win_pct"]        = p["win_pct"]
        annual.loc[annual["year"]==yr, "playoff"]        = p["playoff"]
        annual.loc[annual["year"]==yr, "season_ticket_holders"] = p["st_holders"]

    annual.to_parquet(DATA_DIR / "fact_annual_summary.parquet", index=False)
    print(f"  fact_annual_summary: {len(annual)} rows")
    return annual


# ─────────────────────────────────────────────
# 12. 2027 BUDGET / FORWARD FORECAST
# ─────────────────────────────────────────────

def build_budget_2027(pnl_df):
    """
    Bottom-up 2027 budget. Built from 2026 actuals with growth assumptions.
    This is what the FP&A analyst is building in December 2026.
    """
    actuals_2026 = pnl_df[pnl_df["year"] == 2026].copy().set_index("month")

    # Growth assumptions (management targets / analyst estimates)
    assumptions = {
        "rev_gate_regular_season":  1.06,   # 6% ticket price increase + capacity
        "rev_gate_preseason":       1.04,
        "rev_gate_playoffs":        1.10,   # optimistic playoff run
        "rev_premium_suites":       1.08,
        "rev_concessions":          1.05,
        "rev_merchandise":          1.07,
        "rev_national_broadcasting":1.062,  # known NFL TV deal escalator
        "rev_local_broadcasting":   1.06,
        "rev_sponsorship":          1.09,   # new deals pipeline
        "rev_parking":              1.05,
        "rev_licensing_other":      1.04,
        # Expenses
        "exp_player_salaries":      1.075,  # salary cap increase ~7.5%
        "exp_player_bonuses":       1.05,
        "exp_player_benefits":      1.07,
        "exp_coaching_staff":       1.06,
        "exp_front_office_staff":   1.045,
        "exp_scouting":             1.05,
        "exp_stadium_rent":         1.03,
        "exp_stadium_operations":   1.04,
        "exp_gameday_operations":   1.04,
        "exp_security":             1.05,
        "exp_concessions_cogs":     1.05,
        "exp_merchandise_cogs":     1.07,
        "exp_marketing":            1.08,   # increased brand investment
        "exp_ticket_sales":         1.05,
        "exp_travel":               1.04,
        "exp_insurance":            1.06,
        "exp_league_dues":          1.03,
        "exp_technology":           1.12,   # investing in analytics platform
        "exp_legal_finance":        1.04,
        "exp_depreciation":         1.05,
        "exp_interest":             0.97,   # paying down debt
    }

    budget_rows = []
    for month in range(1, 13):
        row_2026 = actuals_2026.loc[month] if month in actuals_2026.index else actuals_2026.iloc[-1]
        brow = {"year": 2027, "month": month, "month_date": month_date(2027, month),
                "quarter": (month - 1) // 3 + 1, "version": "Budget_v1.0",
                "created_date": date(2026, 12, 15)}

        for col, growth in assumptions.items():
            base = float(row_2026[col]) if col in row_2026.index else 0
            brow[col + "_budget"] = round(base * growth, 0)
            brow[col + "_2026_actual"] = round(base, 0)

        # Totals
        rev_cols = [k for k in assumptions if k.startswith("rev_")]
        exp_cols = [k for k in assumptions if k.startswith("exp_")]
        brow["total_revenue_budget"]  = round(sum(brow[c+"_budget"] for c in rev_cols), 0)
        brow["total_expenses_budget"] = round(sum(brow[c+"_budget"] for c in exp_cols), 0)
        brow["ebitda_budget"] = round(
            brow["total_revenue_budget"] - brow["total_expenses_budget"]
            + brow["exp_depreciation_budget"] + brow["exp_interest_budget"], 0)
        brow["net_income_budget"] = round(
            (brow["ebitda_budget"] - brow["exp_depreciation_budget"] - brow["exp_interest_budget"]) * 0.79, 0)

        budget_rows.append(brow)

    df_budget = pd.DataFrame(budget_rows)
    df_budget["month_date"] = pd.to_datetime(df_budget["month_date"])
    df_budget["created_date"] = pd.to_datetime(df_budget["created_date"])
    df_budget.to_parquet(DATA_DIR / "budget_2027.parquet", index=False)
    print(f"  budget_2027: {len(df_budget)} rows")

    # Also write a clean annual budget summary
    annual_budget = {
        "year": 2027,
        "version": "Budget_v1.0",
        "created_date": date(2026, 12, 15),
    }
    for col in [c+"_budget" for c in list(assumptions.keys())] + ["total_revenue_budget","total_expenses_budget","ebitda_budget","net_income_budget"]:
        annual_budget[col] = df_budget[col].sum()

    pd.DataFrame([annual_budget]).to_parquet(DATA_DIR / "budget_2027_annual.parquet", index=False)
    print(f"  budget_2027_annual: 1 row")

    return df_budget


# ─────────────────────────────────────────────
# 13. VARIANCE TRACKING TABLE (skeleton for future months)
# ─────────────────────────────────────────────

def build_fact_variance_template():
    """
    Empty variance table structure (actuals vs budget).
    Will be filled in as each 2027 month closes.
    Includes rows for all 2027 months, all pre-populated with budget values.
    """
    rows = []
    for month in range(1, 13):
        rows.append({
            "year": 2027, "month": month,
            "month_date": month_date(2027, month),
            "quarter": (month - 1) // 3 + 1,
            "status": "Forecast",  # will flip to "Actuals" when month closes
            "total_revenue_actual": None,
            "total_revenue_budget": None,
            "total_revenue_variance": None,
            "total_revenue_variance_pct": None,
            "total_expenses_actual": None,
            "total_expenses_budget": None,
            "total_expenses_variance": None,
            "ebitda_actual": None,
            "ebitda_budget": None,
            "ebitda_variance": None,
            "net_income_actual": None,
            "net_income_budget": None,
            "net_income_variance": None,
            "commentary": None,
            "last_updated": date(2026, 12, 15),
        })
    df = pd.DataFrame(rows)
    df["month_date"] = pd.to_datetime(df["month_date"])
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df.to_parquet(DATA_DIR / "fact_variance_2027.parquet", index=False)
    print(f"  fact_variance_2027: {len(df)} rows (template – awaiting actuals)")


# ─────────────────────────────────────────────
# 14. SEASON TICKET HOLDER RENEWALS
# ─────────────────────────────────────────────

def build_fact_sth_renewals():
    rows = []
    for year in range(2023, 2027):  # renewals for seasons 2023-2026
        profile = SEASON_PROFILE[year]
        prev    = SEASON_PROFILE[year - 1]
        base_sth = prev["st_holders"]
        renew_rate = 0.88 if profile["win_pct"] > 0.55 else 0.82
        renewed = int(base_sth * noise(renew_rate, 0.02))
        new_sales = profile["st_holders"] - renewed
        upgrades  = int(renewed * noise(0.08, 0.03))
        downgrades= int(renewed * noise(0.04, 0.02))
        cancels   = base_sth - renewed

        rows.append({
            "season": year,
            "prior_year_holders": base_sth,
            "renewals": renewed,
            "renewal_rate_pct": round(renewed / base_sth * 100, 2),
            "new_sales": new_sales,
            "upgrades": upgrades,
            "downgrades": downgrades,
            "cancellations": cancels,
            "ending_holders": profile["st_holders"],
            "avg_package_price": round(noise(145 * 10 * profile["brand_multiplier"], 0.04), 2),
            "total_sth_revenue": round(profile["st_holders"] * 145 * 10 * profile["brand_multiplier"] * noise(1, 0.03), 0),
            "renewal_window_open": date(year - 1, 2, 1),
            "renewal_window_close": date(year - 1, 4, 30),
        })

    df = pd.DataFrame(rows)
    df["renewal_window_open"]  = pd.to_datetime(df["renewal_window_open"])
    df["renewal_window_close"] = pd.to_datetime(df["renewal_window_close"])
    df.to_parquet(DATA_DIR / "fact_sth_renewals.parquet", index=False)
    print(f"  fact_sth_renewals: {len(df)} rows")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\nBuilding Austin Armadillos database → {DATA_DIR}\n")

    print("Dimension tables:")
    build_dim_team()
    build_dim_ticket_tier()
    build_dim_expense_category()
    build_dim_revenue_category()
    build_dim_sponsor()
    build_dim_date()
    build_dim_customer()

    print("\nGame & event tables:")
    games_df = build_dim_game()

    print("\nFact tables:")
    attend_df = build_fact_attendance(games_df)
    build_fact_ticket_sales(games_df)
    build_fact_concessions(games_df, attend_df)
    build_fact_merchandise()
    build_fact_payroll()
    build_fact_sponsorship_revenue()
    build_fact_broadcasting()

    print("\nFinancial rollups:")
    pnl_df = build_fact_monthly_pnl(games_df)
    annual_df = build_fact_annual_summary(pnl_df)
    build_budget_2027(pnl_df)
    build_fact_variance_template()
    build_fact_sth_renewals()

    print("\nAnnual P&L snapshot (2022-2026):")
    print(annual_df[["year","total_revenue","total_expenses","ebitda","net_income",
                      "ebitda_margin_pct","net_margin_pct","win_pct","playoff"]].to_string(index=False))

    # Write a schema manifest
    import json
    manifest = {}
    for f in sorted(DATA_DIR.glob("*.parquet")):
        df = pd.read_parquet(f)
        manifest[f.name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        }
    with open(DATA_DIR / "schema_manifest.json", "w") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"\nAll files written to {DATA_DIR}")
    files = sorted(DATA_DIR.glob("*.parquet"))
    total_mb = sum(f.stat().st_size for f in files) / 1e6
    print(f"Parquet files: {len(files)}  |  Total size: {total_mb:.1f} MB")
