# Compute Consolidation Thesis

LillyPod evolves into an enterprise platform for scientific-AI workflows. MagTrain's GPUs, new simulation-class GPUs, and fat CPU nodes consolidate onto a single Weka fast storage fabric under Run:ai. md3 joins the shared namespace without forced migration. Future compute requests route to the platform rather than spawning new purpose-built environments. Two compounding risks make this time-sensitive rather than aspirational.

**Risk 1 — False cost narrative.** Compute demand within LRL is being met through island environments on commodity GPUs. In the early phase these appear cost-effective. But commodity-GPU islands have a ceiling, and on the other side is a severe cost problem: training-class and simulation-class GPUs on cloud are not cheap at scale, and capacity at that tier requires months of lead time and upfront commitment. The teams generating this demand are not surfacing the future cost trajectory. By the time each island hits its ceiling, the narrative will have already set — the cheap-GPU path worked, and on-prem was the expensive option. Countering that after the fact is significantly harder than making the case now.

**Risk 2 — Structural intake.** Without a deliberate change in how compute requests are handled, the island pattern continues regardless of what the platform builds. Research IT, as the team that has historically fielded LRL compute demand, is the natural on-ramp — and it now sits within AIR, under your authority. The change required is operational: new requests route to the platform rather than spawning independent environments. That makes this consolidation durable, not a one-time hardware deployment.

---

## What We Consolidate

| Hardware | Action |
|---|---|
| MagTrain GPUs | Weka fabric integration |
| 256× RTX 6000 Pro Blackwell | New purchase, LillyPod fabric member; physics simulation, 96GB VRAM |
| 16× Dell R7625/R7725 CPU fat nodes | New purchase, LillyPod fabric member; 4K CPU cores, 32TB RAM |
| Weka hot tier +2PB | Expand 4PB → 6PB as additional nodes, not drive expansion |

Every item above joins the Weka fabric as a member, not an NFS mount. NFS accesses the hot tier but does not deliver fabric-level throughput or enable data-local compute.

---

## What We Keep Distributed

md3 stays on Grid Engine for now. The forward step is Weka fabric membership — non-disruptive, no workload migration required.

---

## Cost and Capability Case

| Bucket | Capital (est.) |
|---|---|
| md3 — 256 RTX 6000 Pro (32 servers; expands md3 to 512) | ~$5.7M |
| LillyPod — 256 RTX 6000 Pro + 16 CPU fat nodes + network/cables + Weka +2PB | ~$10.65M |
| Shared DC infrastructure (UPS, racks, PDU, CDU, fire suppression) | ~$7.1M |
| **2026 total** | **~$23.45M** |

**On-prem vs. cloud — LillyPod ask ($10.65M):**

| Line item | On-prem | Cloud equivalent | Advantage |
|---|---|---|---|
| 256× RTX 6000 Pro | ~$5.7M | ~$19.2M (5-yr, AWS SP + 22% discount) | **3.4×** |
| Weka +2PB | ~$3M | ~$10M (3-yr FSx for Lustre at $0.14/GB/mo) | **3.3×** |
| CPU fat nodes | ~$1.3M | Comparable or higher (high-memory EC2 families) | — |
| Network + fabric cabling | ~$650K | No cloud equivalent | — |

To get Savings Plan rates, Lilly commits the full 3-year cost upfront on day one — access, not ownership. On-prem buys ownership and a shared fabric-connected platform that cloud cannot replicate.

**Live example.** The VS team runs simulation on cloud at $5.25/hr per job (L40S) and $3.63/hr (RTX 6000 Pro), at on-demand rates — the actual gap exceeds 7×. Jobs are hitting memory limits and splitting across GPUs, multiplying cost. H200 (141GB) and B300 (192GB) on the consolidated platform eliminate the split.

---

## Migration Path

| Step | Timing | Outcome |
|---|---|---|
| Step 0 — md3 RTX 6000 Pro deployment | Near-term, in progress | 256× GPUs to md3; Grid Engine |
| Step 1 — MagTrain Weka fabric integration | Q3 2026 | H100/H200/L40S join LillyPod under Run:ai |
| Step 2 — CPU fat node deployment | Q3 2026 | Bioinformatics workloads on platform |
| Step 3 — RTX 6000 Pro deployment | Q4 2026 | End-to-end scientific-AI workflows on one fabric |
| Step 4 — Weka +2PB expansion | Q4 2026 | Storage proportional to GPU capacity increase |
| Step 5 — md3 Weka fabric membership | Q1 2027 | Data silo eliminated; md3 remains on Grid Engine |

---

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| MagTrain inter-row cabling physically constrained | High | Validate with Greg Johnson + Jonathan Klinginsmith before committing Step 1 |
| Weka expansion as drive-only creates throughput bottleneck | High | Specify additional nodes in procurement |
| md3 fabric membership stalls at NFS state | High | Fabric membership must be explicit in the forward plan |
| LRL-facing team continues fielding requests independently | High | Requires leadership direction; platform-first intake is not the default without it |

---

## What I Need From You

1. **Endorse end-to-end workflow throughput as the unit of optimization.** The hardware mix is only coherent if the goal is complete workflows on the platform. Confirm before the capital request goes forward.
2. **Sponsor the ~$23.45M capital request** and carry it through the funding process.
3. **Commit to cross-org coordination with Krishna Jagannathan.** Greg Johnson and Jonathan Klinginsmith own execution; a shared commitment at your level removes the coordination tax from the working level.
4. **Direct the md3 storage fabric step.** Fabric membership — non-disruptive, no workload migration required.
5. **Establish platform-first intake as a standing principle.** New LRL compute requests route through the platform. The Research IT merger creates the opportunity; this direction makes it durable.
