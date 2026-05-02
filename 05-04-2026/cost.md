# GPU Expansion Cost Options — 141 Datacenter

**From:** Greg A Johnson (Senior Director, Tech, Cloud & Connectivity)
**To:** Thomas Fuchs, Krishnakumar Jagannathan
**CC:** Brian Lewis, Chris Lesniewski, Jonathan A Klinginsmith, Dave Walker
**Date:** April 17, 2026

---

## Summary

Greg and Dave modeled initial 2026 and 2027 options/costs for adding GPUs to the 141 Datacenter.

---

## 2026 Options

**Available capacity:** 750 KW of IT load (cooling-limited)
**Timing:** With a quick decision, potential for end of 2026 / early 2027

### GPU Options

| Option | GPU Type | Quantity | Configuration |
|--------|----------|----------|---------------|
| A | RTX 6000 Pro Datacenter | 1,024 | 128 RTX6000 Servers (96 GB mem each); usable for multiple AI and Research workloads |
| B | DGX B300 | 512 | 64 DGX B300 Servers; added to LillyPod |

### 2026 Cost Table

**IT Equipment** (7-year depreciation)

| Item | Capital | Annual Depreciation |
|------|---------|---------------------|
| Option A — 128 RTX6000 Servers (1024 RTX6000 Pro GPUs) | $22,784,000 | $3,254,857 |
| Option B — 64 DGX B300 Servers (512 B300 GPUs) | $43,904,000 | $6,272,000 |
| Network (4 × 128-port Nvidia switches) | $500,000 | $71,429 |
| Cables | $150,000 | $21,429 |

**Datacenter Infrastructure** (18-year depreciation)

| Item | Capital | Annual Depreciation |
|------|---------|---------------------|
| 2 × UPS 750 KW | $1,500,000 | $83,333 |
| Racks (22 × $15K) | $330,000 | $18,333 |
| PDU (3 × $40K) | $120,000 | $6,667 |
| CDU (4 × $50K) | $200,000 | $11,111 |
| Fire Suppression | $1,000,000 | $55,556 |
| Install / Labor | $3,000,000 | $166,667 |
| **Subtotal** | **$6,150,000** | **$341,667** |
| 15% Buffer | $922,500 | $51,250 |

### 2026 All-In Totals

| Option | GPU | Total Capital | Annual Depreciation |
|--------|-----|---------------|---------------------|
| Option A | RTX 6000 (1,024 GPUs) | **$30,506,500** | **$3,790,631** |
| Option B | DGX B300 (512 GPUs) | **$51,626,500** | **$6,757,774** |

---

## 2027 Options

**New capacity unlocked:** LTC Cooling plant available Q2 2027 removes plant-wide chilled water restriction; ability to add 6 MW of power to the DC.

**Available IT load (Air Cooled):** 4.8 MW
**Available IT load (Direct Liquid to Chip / DLC):** 3.5 MW (requires redundant cooling towers)

**Infrastructure lead time:** 18–20 months from approval to power-on
**Building work required:** Increase building footprint, extend the Dock, add a new freight elevator (LTC site architect is onboard)

**DLC note:** If Direct Liquid to Chip (used by new Vera/Rubin systems) is desired, redundant cooling towers would be required, reducing usable IT load to 3.5 MW. Feasibility can be evaluated.

### GPU Options

| Option | GPU Type | Quantity | Configuration |
|--------|----------|----------|---------------|
| A | DGX B300 | 3,584 | 448 DGX B300 Servers; added to LillyPod |
| B | DGX B300 | 2,048 | 256 DGX B300 Servers; added to LillyPod |

### 2027 Cost Table

**IT Equipment** (7-year depreciation)

| Item | Capital | Annual Depreciation |
|------|---------|---------------------|
| Option A — 448 DGX B300 Servers (3,584 B300 GPUs) | $307,328,000 | $43,904,000 |
| Option B — 256 DGX B300 Servers (2,048 B300 GPUs) | $175,616,000 | $25,088,000 |
| Network (130 × 128-port Nvidia switches) | $16,250,000 | $2,321,429 |
| Cables (8,960) | $2,240,000 | $320,000 |
| Weka Storage | $8,000,000 | $1,142,857 |

**Datacenter Infrastructure** (18-year depreciation)

| Item | Capital | Annual Depreciation |
|------|---------|---------------------|
| 4 × UPS 2 MW | $8,000,000 | $444,444 |
| 2 × 750 KW Mechanical UPS | $1,500,000 | $83,333 |
| Load Center — 6 MW | $2,000,000 | $111,111 |
| Building expansion for Load Center and Dock | $14,000,000 | $350,000 |
| Racks (112 × $15K) | $1,680,000 | $93,333 |
| PDU (12 × $40K) | $480,000 | $26,667 |
| CDU (16 × $50K) | $800,000 | $44,444 |
| Fire Suppression | $2,000,000 | $111,111 |
| Install / Labor | $30,000,000 | $1,666,667 |
| **Subtotal** | **$60,460,000** | **$2,931,111** |
| 15% Buffer | $9,069,000 | $439,667 |

### 2027 All-In Totals

| Option | GPU | Total Capital | Annual Depreciation |
|--------|-----|---------------|---------------------|
| Option A | DGX B300 (3,584 GPUs) | **$403,347,000** | **$52,940,825** |
| Option B | DGX B300 (2,048 GPUs) | **$271,635,000** | **$30,660,540** |
