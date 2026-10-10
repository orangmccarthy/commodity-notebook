"""Weekly data update for the Commodities & Geopolitics Notebook.

Pulls a year of daily prices for each market below, then writes:
  - _data/markets.json   -> the summary table on the dashboard
  - assets/charts/*.png  -> one price chart per market

Runs automatically every Monday via GitHub Actions (.github/workflows/site.yml).
To change your markets, edit the MARKETS list - that's the only thing you need to touch.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# Your markets: (display name, Yahoo Finance ticker, unit, file name)
# Front-month futures tickers on Yahoo end in "=F".
# ---------------------------------------------------------------------------
MARKETS = [
    ("Brent crude", "BZ=F", "$/bbl", "brent"),
    ("WTI crude", "CL=F", "$/bbl", "wti"),
    ("US natural gas (Henry Hub)", "NG=F", "$/MMBtu", "henry-hub"),
    ("Wheat (CBOT)", "ZW=F", "US¢/bu", "wheat"),
]

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "_data" / "markets.json"
CHART_DIR = ROOT / "assets" / "charts"

# Chart styling (validated reference palette, light surface)
SURFACE = "#fcfcfb"
LINE = "#2a78d6"
INK = "#0b0b0b"
INK_MUTED = "#52514e"
GRID = "#e6e5e1"


def fetch(ticker: str) -> pd.Series:
    """Return a year of daily closing prices for one ticker."""
    import yfinance as yf

    df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=False)
    if df is None or df.empty:
        raise ValueError(f"no data returned for {ticker}")
    close = df["Close"]
    if isinstance(close, pd.DataFrame):  # newer yfinance returns one column per ticker
        close = close.iloc[:, 0]
    return close.dropna()


def pct_change(series: pd.Series, days_back: int) -> float | None:
    """Percentage change from the last price on or before `days_back` calendar days ago."""
    cutoff = series.index[-1] - pd.Timedelta(days=days_back)
    past = series[series.index <= cutoff]
    if past.empty:
        return None
    return round(float(series.iloc[-1] / past.iloc[-1] - 1) * 100, 1)


def make_chart(series: pd.Series, name: str, unit: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ax.plot(series.index, series.values, color=LINE, linewidth=2)

    # Label the latest value directly instead of using a legend
    ax.scatter([series.index[-1]], [series.iloc[-1]], color=LINE, s=40, zorder=3,
               edgecolors=SURFACE, linewidths=2)
    ax.annotate(f"{series.iloc[-1]:,.2f}", (series.index[-1], series.iloc[-1]),
                xytext=(6, 0), textcoords="offset points", va="center",
                fontsize=9, color=INK)

    ax.set_title(f"{name}, past 12 months ({unit})", loc="left", fontsize=11, color=INK)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_MUTED, labelsize=8, length=0)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.margins(x=0.06)

    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def build(fetcher=fetch) -> dict:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, ticker, unit, slug in MARKETS:
        try:
            s = fetcher(ticker)
        except Exception as exc:  # one bad ticker shouldn't stop the others
            print(f"WARNING: skipped {name} ({ticker}): {exc}")
            continue
        make_chart(s, name, unit, CHART_DIR / f"{slug}.png")
        rows.append({
            "name": name,
            "ticker": ticker,
            "unit": unit,
            "slug": slug,
            "last": round(float(s.iloc[-1]), 2),
            "as_of": s.index[-1].strftime("%d %b %Y"),
            "chg_1w": pct_change(s, 7),
            "chg_1m": pct_change(s, 30),
            "chg_1y": round(float(s.iloc[-1] / s.iloc[0] - 1) * 100, 1),  # vs first price in the year
        })
        print(f"OK: {name} last {rows[-1]['last']} {unit}")

    if not rows:
        raise SystemExit("No markets updated - keeping last week's data.")

    out = {"updated": datetime.now(timezone.utc).strftime("%d %b %Y"), "markets": rows}
    DATA_FILE.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    build()
