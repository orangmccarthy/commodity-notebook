---
layout: page
title: Trade log
permalink: /trades/
---

A paper-traded book. Every idea is logged **before** the outcome is known, with an entry,
stop and target. Nothing is deleted or edited after the fact — losing trades stay up with
a write-up of what I got wrong.

{% assign trades = site.data.trades %}
{% if trades and trades.size > 0 %}
| Opened | Market | Direction | Entry | Stop | Target | Status | Closed | Exit | P&L (%) | Write-up |
|---|---|---|--:|--:|--:|---|---|--:|--:|---|
{% for t in trades %}| {{ t.date_opened }} | {{ t.market }} | {{ t.direction }} | {{ t.entry }} | {{ t.stop }} | {{ t.target }} | {{ t.status }} | {{ t.date_closed }} | {{ t.exit }} | {{ t.pnl_pct }} | {% if t.note_url != "" and t.note_url %}[note]({{ t.note_url }}){% endif %} |
{% endfor %}
{% else %}
*No trades yet — the first ideas go up once I've spent a few weeks getting to know my markets.*
{% endif %}

**Rules I follow:** fixed risk per trade, every trade has a stop, ideas are published before
entry, and costs are included in P&L.
