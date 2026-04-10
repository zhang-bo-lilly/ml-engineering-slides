# Compute Layer Presentation Plan

---

## Implementation Instructions (resume from here after /clear)

### Goal
Generate `Compute Layer.pptx` — a 7-slide deck for the AIOS team workshop.

### Environment
- Working directory: `/Users/C271831/Project/compute-layer`
- Virtual env: `/Users/C271831/Project/compute-layer/.venv`
- Activate: `source .venv/bin/activate`
- Installed packages: `matplotlib`, `pillow`, `python-pptx`, `fonttools`
- **Never install to system Python — always use the venv above**

### Full rebuild from scratch
```bash
source .venv/bin/activate
python3 gen_diagram_estate_a.py   # regenerates diagram-estate-full.png
python3 gen_diagram_estate_b.py   # regenerates diagram-estate-runai.png
python3 gen_diagram_quota_flow.py # regenerates diagram-quota-flow.png
python3 gen_slides.py              # generates all 9 PNGs in compute_layer_pptx_slides/
python3 assemble_pptx.py           # packages into Compute Layer.pptx
```

### Directory layout
| Path | Purpose |
|---|---|
| `gen_diagram_estate_a.py` | Draws the full estate diagram (light mode) |
| `gen_diagram_estate_b.py` | Draws the Run:ai cost lens diagram (light mode) |
| `gen_diagram_current.py` | Draws MagTrain ↔ LillyPod current-arch diagram (light mode) |
| `gen_diagram_target.py` | Draws target LillyPod heterogeneous diagram (light mode) |
| `gen_diagram_quota_flow.py` | Draws the biweekly quota adjustment decision flowchart |
| `gen_slides.py` | Generates all slide PNGs (imports Pillow only) |
| `assemble_pptx.py` | Packages PNGs into `Compute Layer.pptx` |
| `compute_layer_pptx_slides/` | Generated slide PNGs — **safe to delete and regenerate** |
| `pptx_slides/` | **DO NOT touch** — extracted reference slides from `ML Engineering.pptx` |
| `diagram-estate-full.png` | Output of `gen_diagram_estate_a.py` — used by slide 3a |
| `diagram-quota-flow.png` | Output of `gen_diagram_quota_flow.py` — used by slide 8 |
| `diagram-current-architecture.png` | Used by slide 4 (already done, not regenerated) |
| `diagram-target-architecture.png` | Used by slide 6 (already done, not regenerated) |

---

### Current slide state

| # | File | Mode | Layout | Status |
|---|---|---|---|---|
| 1 | `slide_01_anchor.png` | **Dark** `#1a2035` | Centred hero "Compute / Layer." + subline + mandate | Done — open for iteration |
| 2 | `slide_02_dag.png` | Light `#f7f7f7` | Hero "A pipeline is / a DAG.", right-side context, 5 tier cards | Done — open for iteration |
| 3a | `slide_03a_estate_full.png` | Light `#f7f7f7` | Title + `diagram-estate-full.png` inset | Done — open for iteration |
| 3b | `slide_03b_estate_runai.png` | Light `#f7f7f7` | Title + `diagram-estate-runai.png` inset | Done — open for iteration |
| 4 | `slide_04_current_arch.png` | Light `#f7f7f7` | Hero "Two environments. / No bridge.", bullets right, `diagram-current-architecture.png` inset | Done — open for iteration |
| 5 | `slide_05_runai_cost.png` | Light `#f7f7f7` | Hero "Run:ai is powerful. / But not free.", advantages left, big `$3K` stat right, callout box | Done — open for iteration |
| 6 | `slide_06_two_paths.png` | Light `#f7f7f7` | Hero "Fix the floor." / "Raise the ceiling.", two large cards (emerald tint + indigo tint) | Done — open for iteration |
| 7 | `slide_07_quota_structure.png` | Light `#f7f7f7` | Hero "Quota by / design.", left: org hierarchy + EQ definition + design principle, right: 4 tier cards | Done — open for iteration |
| 8 | `slide_08_quota_procedure.png` | Light `#f7f7f7` | Hero "Earned. / Biweekly.", left: `diagram-quota-flow.png` inset, right: formula + common pool callouts | Done — open for iteration |

**Mode rhythm:** Slide 1 = dark anchor only. Slides 2–8 = all light. No mode switching within content slides.

---

### Design system (gen_slides.py)

#### Canvas
- Size: **2880 × 1620 px**, 16:9

#### Fonts (PIL ImageFont.truetype)
| Constant | Path | Use |
|---|---|---|
| `FONT_BLACK` | `/System/Library/Fonts/Supplemental/Arial Black.ttf` | Hero text, card titles, stats |
| `FONT_BOLD` | `/System/Library/Fonts/Supplemental/Arial Bold.ttf` | Section labels, callout text |
| `FONT_REGULAR` | `/System/Library/Fonts/Supplemental/Arial.ttf` | Body, bullets, breadcrumb |

#### Palette
| Constant | Hex | Use |
|---|---|---|
| `DARK_BG` | `#1a2035` | Slide 1 background |
| `LIGHT_BG` | `#f7f7f7` | Slides 2–6 background |
| `LILLY_RED` | `#e4002b` | Breadcrumb, section labels, hero line 2, bottom bar, accents |
| `BLACK_TEXT` | `#1a1a1a` | Hero line 1 (light slides) |
| `GREY_TEXT` | `#999999` | Body/context paragraphs |
| `DARK_TEXT` | `#333333` | Bullets on light bg |
| `EMERALD` | `#10b981` | Compute Layer green — near-term card, tier card |
| `INDIGO` | `#6366f1` | Long-term meta-orchestrator card |
| `BLUE` | `#3b82f6` | Inference tier card |
| `GREY_CARD` | `#9ca3af` | Tier 4 card (under-utilizing quota) |

#### Chrome (every slide — `draw_chrome`)
- **Breadcrumb** at px (95, 52): `"COMPUTE LAYER  ·  ADVANCED INTELLIGENCE  ·  ELI LILLY"` — Arial Regular 28px, `#e4002b`
- **Bottom red bar**: full width, 18px tall, `#e4002b`, bottom edge

#### Hero pattern (`draw_hero`)
- Line 1: Arial Black, size varies, `#1a1a1a` (light) or `#ffffff` (dark)
- Line 2: Arial Black, same size, `#e4002b` — always ends with period
- Top-left at approximately x=95, y=110 on content slides

---

### Estate diagram design (gen_diagram_estate_a/b.py)

Both diagrams use **light mode** (`#f7f7f7` bg, white cards, dark text). They have **no floating title** — the title is provided by the slide in `gen_slides.py`.

Key palette for estate diagrams:
| Role | Hex |
|---|---|
| Background | `#f7f7f7` |
| Card background | `#ffffff` |
| Governed zone border | `#10b981` (emerald) |
| Governed zone fill | `#f0faf6` |
| Non-governed border | `#b0bac5` (grey) |
| Non-governed fill | `#f0f2f5` |
| Primary text | `#1a1a1a` |
| Dim text | `#888888` |
| Green accent (B300 count, zone label) | `#0a7c57` |
| Stamps (NOT JUSTIFIED) | `#e4002b` (Lilly Red) |

In diagram B (`gen_diagram_estate_b.py`): A800 card has a `$$$\nNOT JUSTIFIED` stamp; the entire "REST OF ESTATE" zone has a large `$$$  NOT JUSTIFIED` diagonal stamp, both in Lilly Red.

---

## Context
Presentation for the AIOS team full-day workshop. Each lead presents to start a conversation for their sub-area. Audience knows the AIOS vision (Brian's re-org deck) but does NOT know the full GPU inventory. Brian's keyword framing is "scientific AI." The goal is to open a discussion, not deliver a comprehensive briefing.

---

## Visual Style — ML Engineering.pptx

All slides must match `ML Engineering.pptx` exactly. The deck uses **full-bleed PNG images** (2880×1620 px, 16:9) as slide content — every slide is a rendered image, not a native PPTX text layout. Build slides as Python-generated images (matplotlib / PIL / Cairo), then insert as full-bleed pictures.

### Slide dimensions
- Canvas: **2880 × 1620 px**
- All coordinates below are in pixels at this resolution

### Backgrounds
Two modes used across the deck:

| Mode | Hex | Usage |
|---|---|---|
| **Dark** | `#1a2035` (dark navy) | Title/anchor/closing slides, high-impact content |
| **Light** | `#ffffff` / `#f7f7f7` | Detail/content slides |

### Persistent chrome (every slide)
- **Top-left breadcrumb**: `COMPUTE LAYER · ADVANCED INTELLIGENCE · ELI LILLY` — small caps, spaced ~3px, ~22px, Lilly Red (`#e4002b`) on dark slides / same red on light slides. Position: ~95px from left, ~70px from top.
- **Bottom red bar**: solid `#e4002b`, full width, ~18px tall, pinned to bottom edge.
- **No other footer text** — no copyright line, no slide numbers.

### Typography
All text uses a **heavy geometric sans-serif** (Inter Black / Barlow ExtraBold / or equivalent bold sans). Never serif.

| Role | Weight | Size (approx) | Color |
|---|---|---|---|
| Hero line 1 | Black / 900 | 110–130px | White (dark bg) or Black `#1a1a1a` (light bg) |
| Hero line 2 | Black / 900 | 110–130px | **Lilly Red** `#e4002b` — always ends with a period |
| Section label | Medium, ALLCAPS, tracked +200 | 24px | `#e4002b` |
| Body / description | Regular | 32–36px | White (dark) or `#333333` (light) |
| Sub-caption (right side context) | Regular | 28px | `#999999` grey |
| Stat number | Black / 900 | 120–160px | `#e4002b` |
| Card title | Bold | 36–42px | White (on coloured card) or `#1a1a1a` (on white) |
| Card body | Regular | 28–30px | White or `#555555` |

### Hero title pattern
Every content slide has a 2-line hero in the **top-left**:
```
[Line 1 — white/black]
[Line 2 — red, ends with period.]
```
Example: "The engine" / "behind the **science.**"

### Card / panel colours (layer system)
| Layer | Background | Text |
|---|---|---|
| Application Layer | `#6366f1` (indigo) | White |
| Model Layer | `#3b82f6` (blue) | White |
| Compute Layer | `#10b981` (emerald) | White |
| Data Layer | `#f59e0b` (amber) | White |

Cards have rounded corners (~12px), a bold layer label at top-left in small caps, a large reverse-out number at right, and body text below.

### Divider lines
Thin `#e4002b` horizontal rules used between agenda items (1–2px, ~60% slide width).

### Numbered agenda items
Red number (`#e4002b`, ~36px, small caps), then white bold item name, separated by thin red rule.

### Slide type catalogue (from ML Engineering.pptx)

| Type | Background | Layout |
|---|---|---|
| **Agenda / TOC** | Dark | Hero title top-left; numbered list with red dividers, left-aligned |
| **Two-column intro** | Dark | Hero left; right column has categorised names with red small-caps labels |
| **Stats + phases** | Dark | Hero left; 4 stat cards right (large red number + label + body); 3 phase boxes bottom |
| **Four-layer stack** | Light | Bold black hero; right: context paragraph; 4 horizontal coloured cards stacked |
| **Capability cards** | Light | Bold black hero; 5 cards in a row with coloured headers |
| **Two priorities** | Light | Bold black hero; 2 large side-by-side cards (coloured full-height) |
| **Six info boxes** | Light | Bold black hero; 6 equal cards in 2×3 grid with red ALLCAPS labels |
| **Closing** | Dark | Centred very large white headline; small grey subtitle below |

---

## Slide Plan

### Slide 1 — Anchor
**Compute Layer: running the full pipeline, not just the GPU**

*Style: **Dark background, centred closing-style layout** (or left-aligned hero). Hero: "Compute" / "Layer." in red. Subline in white regular: "Running the full pipeline, not just the GPU." Breadcrumb top-left. Red bar bottom.*

One-sentence mandate: our job is to make heterogeneous scientific AI workflows run end to end, invisibly to the scientist.

---

### Slide 2 — The problem space
**A scientific AI pipeline is a DAG, not a model**

*Style: **Light background, four-layer stack type.** Hero: "A pipeline is" / "a DAG." Bold black/red. Right side: short context paragraph in grey. Below: 4–5 horizontal cards showing compute tiers (CPU-only, Physics GPU, Light GPU, Heavy GPU, Data Transfer), each with its own colour and label. Use Compute Layer green `#10b981` as dominant accent.*

- Different steps need different compute tiers
- CPU-only steps (data prep, processing)
- Physics-based simulation (GPU-accelerated, but different GPU profile than ML — e.g. molecular dynamics)
- Light GPU (inference, scoring — L40s)
- High-end GPU (training, large-scale docking — H100/H200/B300)
- Data transfer between steps is a first-class concern — volume can be large, egress costs matter when on-prem/cloud is mixed

> The compute layer must handle all tiers and hide the complexity from the scientist.

*Note: anchor on "scientific AI pipeline" — not "drug discovery pipeline" — per Brian's framing.*

---

### Slide 3 — What we have
**The estate: what we govern vs. what exists**

*Style: **Two-image transition using the pre-built PNGs.** The diagrams already match the dark-navy palette used in the deck. Slide 3a = `diagram-estate-full.png` (insert full-bleed, add breadcrumb + red bar overlay if not already present). Slide 3b = `diagram-estate-runai.png` (same). These images are DONE — do not regenerate, just embed.*

Two diagrams for a transition:
- **Image A** (`diagram-estate-full.png`) — full estate, non-governed GPUs lumped by group
- **Image B** (`diagram-estate-runai.png`) — same layout, cheaper/misc GPUs greyed out to show Run:ai cost math doesn't work for them

**Under this team's governance:**
| System | GPUs | Scheduler | Notes |
|---|---|---|---|
| LillyPod | 1016 B300 | Run:ai | Air-gapped, Weka FS, 800G fabric |
| MagTrain | 72 H100 + 64 H200 + 32 L40s | Slurm | Internet access, 400G fabric |
| DC | 8 A800 | — | DGX station |

**Broader Lilly estate (not directly governed):**
| System | GPUs | Notes |
|---|---|---|
| Brainiac | 600 L4 + 256 RTX6000 + 48 A16 | + AWS bursting (1200 L40s) |
| AWS (non-HPC) | 251 mixed (T4, A4, A10G) | — |
| Azure | 11 mixed (A10, A100, V100, T4) | — |
| Loxo Colorado | 140 mixed | — |
| San Diego CryoEM | 66 A4090 | Structural biology workstations |
| Alcobendas | 5 V100 | — |
| Computational workstations | Various | RTX6000, RTXA4000, RTX5000 ADA, etc. |

*Visual goal: make it immediately clear we sit at the center of a much larger, fragmented picture.*

---

### Slide 4 — The current architecture and its pain
**Two environments. No bridge.**

*Style: **Light background, six-info-boxes type** (or diagram-centred). Hero: "Two environments." / "No bridge." Red/black. Use `diagram-current-architecture.png` as the main visual, inset below the hero with generous margins. If the diagram is dark-bg itself, place on a dark panel taking the lower 60% of slide. Red small-caps labels: "THE PAIN" or "TODAY'S REALITY".*

*(Use: `diagram-current-architecture.png`)*

- Both MagTrain and LillyPod have their own fast in-cluster filesystems
- LillyPod's Weka filesystem is also mounted as NFS on MagTrain — giving the *appearance* of direct access
- Inexperienced users may assume they can use Weka data directly from MagTrain jobs — but that path is NFS, not in-cluster; it causes GPU idling while waiting on IO
- A pipeline split across Run:ai and Slurm requires two separate manual submissions — no chaining
- Users must know which environment to target — **the abstraction leaks**

---

### Slide 5 — Why we can't just unify everything under Run:ai
**Run:ai is powerful — but priced per GPU (~$3K/year)**

*Style: **Dark background, stats-type layout.** Hero: "Run:ai is powerful." / "But not free." (or "~$3K / GPU / year."). Left: 3 bullet advantages. Right: 1 large red stat "$3K" with label "per GPU · per year", then a blockquote-style callout box: "Unification of the full estate under one scheduler is not on the roadmap. We design around that." White text on dark card with red left border.*

Run:ai has real advantages:
- Dynamic GPU fractioning
- Quota management
- Fine-grained workload scheduling

But at ~$3K/GPU/year, putting the full estate under Run:ai is not viable.

> **The reality: unification of the full estate under one scheduler is not on the roadmap. We design around that.**

This is the constraint that shapes everything downstream.

---

### Slide 6 — Two paths forward
**Two schedulers. One experience.**

*Style: **Light background, two-priorities type.** Hero: "Two schedulers." / "One experience." Left card: Compute Layer green `#10b981` — "Near-term: Consolidate into LillyPod" with bullets. Right card: indigo/blue `#6366f1` — "Long-term: Meta-orchestrator" with bullets. Bottom: `diagram-target-architecture.png` embedded as a small inset in the left card or below. Conversation-opener line in grey italics at bottom: "What workflows in your squad hit this wall today?"*

**Given that separation is the reality we're planning for — how do we still hide it from users?**

*Style: **Light background, two-priorities type.** Hero: "Two paths" / "forward." Left card: Compute Layer green `#10b981` — "Near-term: Consolidate into LillyPod" with bullets. Right card: indigo/blue `#6366f1` — "Long-term: Meta-orchestrator" with bullets. Bottom: `diagram-target-architecture.png` embedded as a small inset in the left card or below. Conversation-opener line in grey italics at bottom: "What workflows in your squad hit this wall today?"*

*(Use: `diagram-target-architecture.png`)*

**Near-term: Consolidate what we govern into LillyPod**
- Move H100/H200/L40s under LillyPod (Run:ai)
- Add fat CPU-only nodes to LillyPod
- Result: LillyPod becomes a heterogeneous environment — B300, H100, H200, L40s, CPU-only, all on unified Weka
- Users get the right tier without knowing where it lives
- Status: aligned with Greg & Jon since 2025 RFP. Execution plan in progress.

**Long-term: Meta-orchestrator**
- A routing layer above Run:ai and Slurm
- Chains pipeline steps across schedulers transparently
- Novel work — significant engineering effort
- This is what completes the abstraction for the GPUs that remain outside LillyPod

*Conversation opener: What workflows in your squad hit this wall today?*

---

## Flow Summary

| # | Slide | Purpose |
|---|---|---|
| 1 | Anchor | What this layer is for |
| 2 | Scientific AI pipeline = DAG | Why it's hard — heterogeneity is the norm |
| 3 | Estate inventory | Ground the conversation — show what we govern and what surrounds it |
| 4 | Current pain | Two environments, no bridge, abstraction leaks |
| 5 | Run:ai cost constraint | Establish why unification isn't the plan — before presenting solutions |
| 6 | Two paths forward | Near-term (consolidate into heterogeneous LillyPod) + long-term (meta-orchestrator) |
| 7 | Quota governance structure | How the compute layer governs GPU allocation — Run:ai hierarchy, EQ definition, tier system |
| 8 | Biweekly quota procedure | The adjustment algorithm — decision flow, weight formulas, common pool |
| 6 | Two paths forward | Near-term (consolidate into heterogeneous LillyPod) + long-term (meta-orchestrator) |

---

## Key changes from prior draft
- "Drug discovery pipeline" → "scientific AI pipeline" (Brian's language)
- Slide 3 table redesigned: split into "governed" vs "broader estate"
- Slides 5–6 restructured: establish the Run:ai cost constraint *first*, then present consolidation and meta-orchestrator as the two responses to that permanent reality — rather than presenting consolidation as the end state
- CPU-only nodes explicitly added to the LillyPod consolidation plan

---

## Diagrams (completed)

| File | Used in | Status | Description |
|---|---|---|---|
| `diagram-estate-full.png` | Slide 3 (image A) | **DONE** | Full estate, two-zone layout — see details below |
| `diagram-estate-runai.png` | Slide 3 (image B) | **DONE** | Same layout, cheaper GPUs greyed out (Run:ai cost lens) — see details below |
| `diagram-current-architecture.png` | Slide 4 | **DONE** | MagTrain ↔ LillyPod, NFS pain, dashed yellow slow path — see details below |
| `diagram-target-architecture.png` | Slide 6 | **DONE** | LillyPod heterogeneous: B300, H100, H200, L40s, CPU-only on unified Weka — see details below |

All four diagrams share the same light mode palette (`#f7f7f7` background) as the content slides.

---

### `diagram-current-architecture.png` — Design details

Dark navy background. Title: **"Current Architecture"** — centred top, white bold.

**Two side-by-side cluster boxes:**

**Left — MagTrain** (blue rounded border):
- Subtitle: "Slurm · Internet access"
- Yellow dashed inner box: **"Weka FS (NFS mount)"** — body: *"appears local — but is not"* — red warning text: *"GPU idle waiting on IO if not careful"*
- Blue box: **"Isilon Filesystem"**
- Blue box: **"GPUs"** — "72 × H100   64 × H200   32 × L40s"
- "400G" label between Isilon and GPUs

**Right — LillyPod** (teal rounded border):
- Green pill badge: "Run:ai · Air-gapped"
- Teal box: **"Weka Filesystem"** — "GPU Direct"
- Teal box: **"GPUs"** — "1016 × B300"
- "800G" teal bidirectional arrow connecting Weka to GPUs

**Cross-cluster connection:** Yellow dashed arrow from MagTrain's Weka NFS box to LillyPod, labelled **"10G"** — visually shows the slow, deceptive NFS path.

---

### `diagram-target-architecture.png` — Design details

Dark navy background. Single large **teal-bordered** outer box.

**Header:** "LillyPod" (white bold, large) — "Heterogeneous compute" (teal, smaller) — "Run:ai · Air-gapped" (grey, small)

**Five node cards in a row**, each with vertical connector down to the Weka bar:
| Card | Border colour | Fill | Count |
|---|---|---|---|
| B300 | Teal | Dark green fill | 1016 × |
| H100 | Blue | Dark navy | 72 × |
| H200 | Blue | Dark navy | 64 × |
| L40s | Blue | Dark navy | 32 × |
| CPU-only | Purple | Dark navy | 1024 cores |

**Bottom bar (full width):** **"Weka Filesystem"** — "Unified storage · GPU Direct"

**"800G"** label on the vertical connectors between cards and Weka bar.

---

### `diagram-estate-full.png` — Design details

Dark navy background. Title: **"The GPU Estate: What We Govern vs. What Exists"**

**Top zone — "THIS TEAM'S GOVERNANCE"** (solid teal border, dark green fill):
Five cards in a row, each showing GPU type / count / platform:
| Card | GPUs | Platform |
|---|---|---|
| B300 | **1,016** (teal highlight) | LillyPod |
| H100 | **72** | MagTrain |
| H200 | **64** | MagTrain |
| L40s | **32** | MagTrain |
| A800 | **8** | Standalone server |

**Bottom zone — "REST OF ESTATE"** (dashed border, dimmer styling):
Six cards in a row:
| Card | Count | GPU types |
|---|---|---|
| Brainiac | **~2,100** | L4 · RTX6000 · A16 + AWS burst (L40s) |
| AWS Non-HPC | **251** | T4 · A4 · A10G mixed |
| Azure | **11** | A10 · A100 · V100 · T4 mixed |
| Loxo Colorado | **140** | misc GPU types |
| San Diego + Workstns | **~88** | CryoEM · 4090 · RTX4000ADA etc. |
| Alcobendas | **5** | V100 |

---

### `diagram-estate-runai.png` — Design details

Same two-zone layout as `diagram-estate-full.png`. Title: **"Run:ai Licensing: Where the Cost Math Works"**

**Top zone — "THIS TEAM'S GOVERNANCE"** with sub-label: *"WORTH RUN:AI LICENSING (~$3K / GPU / year)"*

Cards B300, H100, H200, L40s shown normally (solid). **A800 card has a red "NOT JUSTIFIED" stamp** overlay — standalone server, too few GPUs to justify per-seat cost.

**Bottom zone — "REST OF ESTATE"**: all six cards are heavily dimmed/greyed out with a large red **"$$$ NOT JUSTIFIED"** stamp overlaid across the entire zone. The implied message: Run:ai licensing only makes economic sense for the high-utilisation, high-GPU-count governed clusters.
