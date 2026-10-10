---
layout: page
title: Dashboard
permalink: /dashboard/
---

{% assign d = site.data.markets %}

Data last updated: **{{ d.updated | default: "not yet — runs every Monday" }}**
(daily settlement prices, so figures lag real time).

{% if d.markets and d.markets.size > 0 %}
| Market | Last price | 1 week | 1 month | 1 year |
|---|--:|--:|--:|--:|
{% for m in d.markets %}| {{ m.name }} | {{ m.last }} {{ m.unit }} | {{ m.chg_1w | default: "–" }}% | {{ m.chg_1m | default: "–" }}% | {{ m.chg_1y | default: "–" }}% |
{% endfor %}

{% for m in d.markets %}
### {{ m.name }}

![{{ m.name }} price over the past year]({{ "/assets/charts/" | append: m.slug | append: ".png" | relative_url }})
{% endfor %}
{% else %}
*No data yet. The first automatic update will fill this page.*
{% endif %}

<p style="font-size:0.85em;color:#52514e">Source: Yahoo Finance front-month futures via the yfinance library.
Front-month series roll between contracts, so jumps around expiry can partly reflect the roll rather than a price move.</p>
