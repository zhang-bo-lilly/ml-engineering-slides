# Presentation Plan — Scientific AI CoE

**Deck name (breadcrumb):** `SCIENTIFIC AI COE  ·  AIR + DIGITAL CORE  ·  ELI LILLY`
**Canvas:** 2880 × 1620 px, 16:9
**Slide count:** 5
**Audience:** ML Engineering LT weekly (internal); content will later be adapted for Thomas → Krishna

---

## Slide 1 — Dark Anchor (Title)
**Mode:** Dark (`#1a2035`)
**Layout:** Centered title block

- **Line 1 (Arial Black ~118px, white):** A Center of Excellence
- **Line 2 (Arial Black ~118px, Lilly Red):** for Scientific AI Compute.
- **Subtitle (~48px, `#aaaaaa`):** A Joint Initiative for AIR and Digital Core
- **No diagram**

---

## Slide 2 — The Inflection Point
**Mode:** Light (`#f7f7f7`)
**Layout:** Hero top-left, body text full width below, DAG diagram at bottom

- **Hero Line 1:** The language has changed.
- **Hero Line 2:** The compute problem hasn't.
- **Body:** Agentic workflows, autonomous discovery, AI-driven pipelines — beneath the vocabulary, the challenge is the same: a directed graph of heterogeneous model execution, where physics-based simulations, ML inference, and generative AI steps each carry distinct resource requirements. What has changed is the scale of that graph and the caliber of hardware each node demands. Tech@Lilly has a near-term window to define how this compute is owned before fragmentation becomes entrenched.
- **Diagram:** `diagram_dag.png` — horizontal DAG of compute tiers, full width at bottom

---

## Slide 3 — The Current Pattern
**Mode:** Light (`#f7f7f7`)
**Layout:** Hero top-left, 3 bullets below with tight spacing

- **Hero Line 1:** Multiple teams are building
- **Hero Line 2:** in isolation.
- **Intro sentence:** AI4D (Discovery Oncology) and Data Foundry (LSMD) — each recruiting at AVP level, each building independently. A natural response to urgency. A compounding risk.
- **3 bullets:**
  - **Scalability ceiling** — Built on cheap cloud GPU tiers. As workloads demand H100/H200/B300-class compute, cost and availability assumptions break down. Leadership doesn't see the cliff ahead.
  - **Operational fragility** — Teams lack true HPC expertise. Inefficient patterns (e.g., using expensive GPU instances as data staging vehicles) are tolerable at low tiers; punishing at scale. Pivoting takes months, not a budget line.
  - **Duplicated investment** — Separate tooling, separate staffing, no shared learning across functions.
- **No diagram**

---

## Slide 4 — The Cost Reality
**Mode:** Light (`#f7f7f7`)
**Layout:** Hero top-left, bar chart centered below

- **Hero Line 1:** On-premise compute costs
- **Hero Line 2:** 2.7× less at scale.
- **Framing sentence:** These numbers cover compute only — a comparable high-performance parallel filesystem on cloud would widen the gap further.
- **Diagram:** `diagram_cost.png` — grouped bar chart (log scale), all AWS figures at 22% Lilly enterprise discount
  - MagTrain: $6.8M on-prem vs $14.8M AWS SP 3-yr (2.2×) / $24.7M AWS SP 5-yr (3.6×)
  - LillyPod: $150M on-prem vs $247M AWS SP 3-yr (1.6×) / $412M AWS SP 5-yr (2.7×)
  - Callout: "AWS SP 3-yr alone ($247M) exceeds LillyPod's full 5-yr TCO ($150M)"

---

## Slide 5 — The Proposal
**Mode:** Light (`#f7f7f7`)
**Layout:** Hero top-left, avatar diagram centered below

- **Hero Line 1:** AIR and Digital Core
- **Hero Line 2:** own this together.
- **Diagram:** `diagram_venn.png` — two Lilly-template avatars (AIR in emerald, Digital Core in blue), label "Trusted Advisor Team to LRL teams" below
- **No closing quote**
