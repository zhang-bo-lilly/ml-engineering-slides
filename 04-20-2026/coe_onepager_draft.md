# CoE One-Pager — Content Draft
<!-- 
POSITIONING NOTES (not for final artifact):
- Audience: Krishna, SVP Infrastructure & Operations (Digital Core). New to Lilly. Replacing Tim Coleman.
- Framed as: Thomas presenting to a peer. Joint initiative, not an ask from a subordinate.
- Subtext goal: Position this as Krishna's flagship opportunity — Infrastructure & Operations is his mandate,
  this CoE is a natural and high-visibility extension of it. Let Krishna see himself as the protagonist.
- Tone: Strategic, collegial, data-grounded. Never alarmist. Never preachy about shadow IT.
- Length target: ~500-600 words. Dense but scannable. Every sentence earns its place.
-->

---

## Working Title
**Establishing a Scientific AI Compute Center of Excellence: A Joint Initiative for AIR and Digital Core**

<!-- 
TITLE NOTE: May want a shorter header for the final artifact. Options:
- "Scientific AI Compute: A Proposal for Tech@Lilly Leadership"
- "A Center of Excellence for Scientific AI at Lilly"
Avoid: "one-pager," "proposal for Krishna," anything that sounds like an internal memo label.
-->

---

## Section 1 — The Inflection Point
*[~2-3 sentences. This is the hook. Frame it as a moment of opportunity, not a crisis.
Subject = the company/the field. Do not open with "we" or a problem statement.
Goal: make Krishna lean forward.]*

The language of scientific AI has shifted — agentic workflows, autonomous discovery, AI-driven pipelines. Beneath the vocabulary, however, the compute challenge is the same one it has always been: executing a directed graph of heterogeneous models, where physics-based simulations, ML inference, and generative AI steps run in sequence and in parallel, each with distinct resource requirements. What has changed is the scale of that graph and the caliber of hardware each node demands. Tech@Lilly has a near-term window to define how this compute is owned, governed, and delivered — before the current pattern of fragmented build-out becomes structurally entrenched.

---

## Section 2 — The Current Pattern
*[1 short paragraph + 3-4 tight bullets. Describe shadow IT objectively — not as a failure,
but as a natural response to urgency that carries long-term risk.
Name the specific teams (confirmed: okay to do so). Keep tone factual, not critical.]*

Across LRL, several business-area teams have independently stood up AI compute environments to serve their scientific communities. Recent examples include the Applied Intelligence for Discovery (AI4D) team under Discovery Oncology, and Data Foundry within Lilly Small Molecule Discovery — which is building a full platform organization structured across four pillars (Architecture4Insight, Methods4Insight, Scale4Insight, Preparedness4Insight), each led at the AVP level under a single org. AI4D is likewise recruiting at AVP level. This pattern reflects genuine urgency — these teams are close to the science and move quickly. However, it creates compounding risks:
<!--
NOTE: Data Foundry (Miguel Camargo) is not just one AVP hire — it is a whole platform org with up to 4
AVP-level pillar leads. The Methods4Insight posting is the active one we have; other pillars were also
posted but are no longer open (may already be filled). This makes the "duplicated investment" point
considerably stronger — this is not shadow IT at the engineer level, it is shadow IT at the VP-org level.
Consider whether to make this more explicit in the final artifact or let the reader infer from "four pillars,
each led at the AVP level."
-->

- **Scalability ceiling:** These platforms were initially built on cheaper, readily available cloud GPU tiers — where cost and availability posed no obvious problem. As scientific workloads demand more capable hardware (H100, H200, B300), the assumptions break down: these GPU classes are expensive, not available on demand at scale, and the cloud cost for them is materially higher and unpredictable. Business leadership, anchored on their early cloud experience, does not yet see the cost cliff ahead.
- **Operational fragility:** At least one team is already operating at significant scale — large active user base, real GPU procurement constraints. What makes this harder is the absence of true HPC expertise: operational patterns that are inexpensive to run on lower-tier compute become very costly at H100/H200/B300 scale. A concrete class of example — using expensive GPU instances as data staging vehicles, copying from object storage to local instance storage while the GPU meter runs — is largely harmless on cheaper tiers but punishing on advanced ones. Pivoting an embedded platform with these ingrained patterns is not a budget decision; it requires months of planning, tooling changes, and operational retraining.
<!-- 
NOTE: The specific team is AI4D / Shawn Cho (reports to Matthew Chang). Shawn shared the GPU
procurement trouble privately. Matthew's own posting does not indicate awareness of the problem —
so "executive-level attention" was overstated and has been removed. Do NOT name Shawn or
attribute the operational example; keep it as a generalized pattern. The S3-to-local-storage example
is real but anonymized here intentionally.
-->
- **Duplicated investment:** Each team building its own platform means duplicated tooling, duplicated staffing, and no shared learning.

---

## Section 3 — The Cost Reality
*[Data-forward. ~1 tight paragraph or a 2-row comparison table.
Lead with the most striking stat. Avoid overloading with numbers — pick 2-3 anchors.
Use Savings Plans rates (not on-demand) so it's defensible against "we'd use reserved pricing."]*

The economics of on-premise advanced compute are compelling at Lilly's scale. MagTrain — the first on-premise GPU cluster — was deployed for $6.8M in capital. Equivalent compute on AWS Savings Plans, at Lilly's enterprise rate, would cost $14.8M over three years: **2.2× more expensive**. LillyPod scales this advantage further: its five-year total cost of ownership is $150M. Matching LillyPod's 1,016 B300 GPUs on AWS Savings Plans would cost **$247M over just three years** — already 65% more than the on-premise five-year TCO. Over a five-year horizon, the AWS equivalent reaches $412M, **2.7× the cost of LillyPod**. These figures cover compute only. A high-performance parallel filesystem — essential for the I/O demands of scientific AI workflows — adds substantial cost on top; both MagTrain and LillyPod include this storage infrastructure, while replicating it on cloud would widen the gap further.

<!-- 
OPTIONAL TABLE FORMAT (if visual treatment preferred over prose):

| | MagTrain | LillyPod |
|---|---|---|
| On-premise cost | $6.8M capex | $150M (5-yr TCO) |
| AWS Savings Plans equivalent | $14.8M (3 yr) | $247M (3 yr) / $412M (5 yr) |
| Multiplier | 2.2× | 2.7× |
-->

---

## Section 4 — The Proposal
*[1 paragraph. This is the "what we are proposing." Be concrete.
AIR + Digital Core as co-leads. Not a policing body — a strategic partner.
Frame it as already belonging to Krishna's mandate (Infrastructure & Operations).
End with the proactive expansion angle (NVIDIA / GPU extension).
No role breakdown, no deliverable list — those are for the follow-up conversation.]*

The answer is a Scientific AI Compute Center of Excellence, jointly led by AIR and Digital Core — a shared resource and strategic partner, not a governing body. Scientific AI compute is, at its core, an infrastructure problem: capacity planning, power, advanced hardware procurement, and the operational expertise to run it at scale. That is the mandate of Infrastructure & Operations, and this CoE is its natural expression. Business-area teams that have moved quickly and independently would find in the CoE not a constraint, but a foundation — something to build on rather than maintain alone. With current datacenter headroom and NVIDIA momentum, there is an opportunity now to proactively extend capacity by 1,000–2,000 GPUs. The moment is right — and this is ours to define together.

<!--
NOTE: The closing line ("The moment is right — and this is ours to define together.")
gives Krishna co-authorship without separating him from the "we" established earlier.
Avoids the transactional "pitch ending" register of "we'd welcome your partnership."
-->

---

## Open Items for Iteration
<!-- These are questions/gaps for you to respond to before we finalize -->

- [ ] **Section 1 tone check** — Does "near-term window" feel appropriately urgent without sounding alarmist?
- [ ] **Section 2 naming** — Comfortable naming Matthew Chang and Miguel Camargo by name, or keep to team names only?
- [ ] **Section 3 numbers** — Should I include the on-demand shock number ($18,087/hr) as a parenthetical, or keep it clean with just the Savings Plans comparison?
- [ ] **Overall framing check** — Does this feel like it was written *for* Thomas to present, or does it read as if it came from the AIR team specifically? May need pronoun/voice adjustment.
