# Slide 3 — GPU Estate Diagram: Background Notes

## What this is for
Slide 3 of the compute layer presentation ("The estate: what we govern vs. what exists").
The goal is NOT a raw table dump — it's a visual that tells the story:
> "We govern a small, high-value cluster. There's a huge fragmented estate around us. Most of it is NOT worth putting under Run:ai."

---

## Raw inventory (from image.png)

| GPU | Count | Location |
|---|---|---|
| B300 GPUs | 1016 | LillyPod |
| L40s GPUs | 32 | MagTrain |
| H100 GPUs | 74 | MagTrain and computational workstation |
| H200 GPUs | 72 | MagTrain and Singapore server |
| L4 GPUs | 600 | Brainiac |
| RTX6000 GPUs | 256 | Brainiac* |
| A16 | 48 | Brainiac |
| L40s GPUs | 1200 | AWS – via Brainiac bursting |
| V100 GPUs | 5 | Alcobendas |
| 4090 GPUs | 66 | San Diego CryoEM and Structural Biology workstations |
| RTX 4000 ADA | 20 | Computational Chemistry workstations |
| RTXA4000 | 1 | Computational workstation |
| RTX 5000 ADA | 1 | Computational workstation |
| Variety | 11 | Azure – A10, A100, V100, T4 |
| Variety | 251 | AWS Non-HPC accounts – T4, A4, A10G |
| Variety | 140 | Loxo Colorado |
| A800 | 8 | DGX station in DC |

---

## Narrative design: TWO images (a transition in the presentation)

### Image A — "The full picture"
Show the entire estate. Key design decisions:
- **Governed GPUs** (B300, H100, H200, L40s on MagTrain) shown prominently with their actual counts
- **Non-governed GPUs** lumped into groups rather than shown row-by-row:
  - Brainiac cluster: L4 + RTX6000 + A16 + 1200 L40s (AWS burst) → one block "~2100 GPUs"
  - AWS non-HPC: 251 mixed → one block
  - Azure: 11 mixed → one block
  - Loxo Colorado: 140 → one block
  - San Diego CryoEM + workstations: 66 + 20 + 1 + 1 → one block
  - Alcobendas: 5 V100 → one block
  - DC: A800 → already governed, small

Visual intent: The estate is LARGE and fragmented. We are a small bright spot in a sea of heterogeneity.

### Image B — "After transition: the Run:ai cost lens"
Same layout but now overlay or highlight which GPUs are worth Run:ai licensing (~$3K/GPU/year):
- **Worth it**: B300 (1016), H100 (~72), H200 (~72), L40s (32) — high utilization, high-end, shared research
- **Not worth it**: Brainiac (L4/RTX6000), workstation GPUs (4090, RTX4000ADA etc.), Azure scattered, Loxo Colorado misc, Alcobendas V100s
- Visual treatment for "not worth it" group: grey out / dim / mark with ✗ or "$$$" callout

The transition from A→B communicates: even if we WANTED to unify everything under Run:ai, the cost math doesn't work for the majority of the estate.

---

## Design approach (consistent with other diagrams)
- Dark theme: BG `#12172b`, cluster fill `#1a2240`
- Governed cluster: teal border `#2e8a78`
- Non-governed / not worth it: dimmed, grey border `#4a5060`
- "Worth Run:ai" highlight: bright teal/blue
- "Not worth Run:ai" in Image B: greyed out with subtle red/orange cost indicator
- Use matplotlib (same `.venv` in project dir) or consider a different layout approach
- Save scripts as `gen_diagram_estate_a.py` and `gen_diagram_estate_b.py`
- Save outputs as `diagram-estate-full.png` and `diagram-estate-runai.png`

---

## Layout sketch for Image A

Two-column or grouped layout:
```
┌─────────────────────────────────────────────────────────────────┐
│  THIS TEAM'S GOVERNANCE                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────┐ │
│  │ B300    │  │  H100   │  │  H200   │  │  L40s   │  │ A800 │ │
│  │ 1016    │  │   72    │  │   72    │  │   32    │  │   8  │ │
│  │LillyPod │  │MagTrain │  │MagTrain │  │MagTrain │  │  DC  │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └──────┘ │
└─────────────────────────────────────────────────────────────────┘

┌────────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Brainiac   │  │ AWS Non-HPC│  │  Azure   │  │  Loxo CO │  │ San Diego│  │Alcobendas│
│ ~2100 GPUs │  │ 251 mixed  │  │ 11 mixed │  │ 140 misc │  │ 66+20+.. │  │  5 V100  │
│(L4,RTX6000 │  │(T4,A4,A10G)│  │(A10,A100,│  │          │  │  CryoEM  │  │          │
│ A16+burst) │  │            │  │  V100,T4)│  │          │  │+workstns │  │          │
└────────────┘  └────────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

---

## Status
- [ ] gen_diagram_estate_a.py — not started
- [ ] gen_diagram_estate_b.py — not started
- Raw source: image.png in project directory
- Reference: presentation-plan.md Slide 3

---

## Resume instructions
1. Read this file (`slide3-estate-notes.md`) for full context
2. Read `presentation-plan.md` for overall slide structure
3. Both architecture diagrams are DONE: `diagram-current-architecture.png` (slide 4) and `diagram-target-architecture.png` (slide 6)
4. Next task: build Image A and Image B for slide 3 using matplotlib in `.venv`
5. After diagrams: build the actual PowerPoint using python-pptx
