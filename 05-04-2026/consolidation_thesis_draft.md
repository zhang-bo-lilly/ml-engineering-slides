# Compute Consolidation Thesis
**To:** Thomas Fuchs
**From:** Bo Zhang
**Date:** May 2026
**Status:** DRAFT — iteration surface

---

## The Thesis

Compute management inside AIR is still split: AIOS manages MagTrain and LillyPod; Research IT manages md3 and a set of similar purpose-built environments. Two teams, same org, same SVP, separate infrastructure with no shared data namespace. The consolidation thesis is: **LillyPod is the platform.** High-value compute — MagTrain's H100s and H200s, new simulation-class GPUs, fat CPU nodes for bioinformatics — consolidates onto a single Weka fast storage fabric under Run:ai. md3 joins the shared namespace without forced migration. Future LRL compute requests route to the platform rather than spawning new purpose-built environments.

Two compounding risks make this a time-sensitive call.

**Risk 1 — False cost narrative.** Compute demand within LRL is being met through island environments on inexpensive GPUs. In the early phase, these appear successful and cost-effective. But island environments built on commodity GPUs have a ceiling, and what is on the other side of that ceiling is a severe cost problem — modern training-class and simulation-class GPUs on cloud are not cheap at scale, and cloud capacity at that tier requires months of lead time and upfront commitment. The teams generating this demand are not surfacing the future cost trajectory. By the time each island hits its ceiling, the narrative will have already set: the cheap-GPU path worked, and on-prem was the expensive path. Countering that after the fact is significantly harder than making the case now.

**Risk 2 — Structural intake.** Without a deliberate change in how compute requests are handled, the island pattern continues regardless of what the platform builds. Research IT, as the team that has historically fielded LRL compute demand, is the natural on-ramp — and it now sits within AIR, under Thomas's authority. The change is operational: new compute requests route to the platform rather than spawning independent environments. That makes this consolidation durable, not just a one-time hardware deployment.

The 2026 window is real. 750 KW of datacenter capacity exists today, the hardware is available, and the inter-row cabling that enables MagTrain integration is low-cost relative to the GPU value it unlocks.

---

## What We Consolidate

| Hardware | Move | Rationale |
|---|---|---|
| MagTrain (72× H100, 64× H200, 32× L40S) | Into LillyPod (Run:ai) via Weka fabric integration | $6.8M cluster already purchased (GPUs, 500TB Isilon, 400G fabric); Weka is currently NFS-mounted on MagTrain as a staging path for LillyPod — Run:ai-managed GPUs are air-gapped, so Slurm/Grid Engine nodes serve as the data staging layer; inter-row cabling to the Weka fast fabric is the next step to make MagTrain GPUs first-class fabric members |
| 256× RTX 6000 Pro Blackwell | New purchase, LillyPod (Run:ai) — Weka fabric member | Physics simulation (GROMACS, OpenMM); 96GB VRAM; single-GPU fit means NVLink absence is not an issue; Run:ai fractional allocation solves variable-length job utilization; nodes are fabric members (not NFS), same Weka namespace as rest of LillyPod |
| 16× Dell R7625/R7725 fat CPU nodes | New purchase, LillyPod (Run:ai) — Weka fabric member | 4K CPU cores, 32TB RAM total; mmseqs / UniRef100 in-memory search requires 2TB/node; no other environment can serve this workload today; nodes are fabric members, not NFS-mounted |
| Weka hot tier +2PB | Expansion (4PB → 6PB) | Proportional to ~40% GPU capacity increase; validate as additional Weka nodes, not drive expansion, to preserve throughput |

**Why Run:ai for all of the above:** Run:ai provides fine-grained scheduling, quota management, preemption, and dynamic runtime GPU fractionalization. The last point is significant: dynamic fractions adjust GPU allocation at runtime without requiring a specific MIG profile or a node reboot to take effect. That directly increases throughput on heterogeneous, variable-length jobs — simulation, fine-tuning, inference — which is the dominant workload profile across this hardware set.

---

## What We Keep Distributed

| Environment | Stays How | Condition |
|---|---|---|
| md3 (256 GPUs deployed + 256 GPUs planned) | Grid Engine, own scheduler | Research IT built this to meet near-term business demand for FEP and similar workloads; no forced migration — a forward plan is the goal, not an immediate cutover |
| md3 → Weka mount | md3 already has the Weka hot tier NFS-mounted | NFS access is not fabric membership and does not deliver fabric-level throughput. For md3 to serve as a genuine data-local compute tier for platform pipelines, storage fabric membership is the first requirement. |

**The distributed part is not a failure of consolidation.** md3 on Grid Engine is acceptable as a near-term state, but the broader pattern it represents is the problem: traditional HPC clusters at Lilly have been built as a scheduler queue in front of a set of nodes, without fast storage fabric or compute fabric. That is not a cluster in the HPC sense — it is job dispatch with no data locality, no high-bandwidth interconnect, and no ability to run tightly-coupled workloads efficiently. md3 already has the Weka hot tier NFS-mounted — that is the starting point. The immediate forward step is storage fabric membership, which eliminates the data silo without requiring a workload migration. Whether md3 eventually requires full LillyPod integration — compute fabric and Run:ai scheduling — is a separate question that depends on workload evolution; that path is available but not assumed.

---

## Cost & Capability Case

### 2026 — Deployment cost

Greg's April 2026 model provides server pricing and datacenter infrastructure estimates based on the 750 KW envelope available in the 141 Datacenter. Greg modeled for the full envelope — 1,024× RTX 6000 Pro (Option A) or 512× DGX B300 (Option B). Network and cable costs ($650K) from Greg's model are used as-is; our 82-server deployment is well within the envelope they were sized for.

**Committed (soft) — md3:**

| Item | Detail | Capital (est.) |
|---|---|---|
| RTX 6000 Pro — md3 | 256 additional GPUs (32 servers); md3 already has 256 deployed; from Greg Option A per-server rate | ~$5.7M |

**Incremental ask — LillyPod consolidation/expansion:**

| Item | Detail | Capital (est.) |
|---|---|---|
| RTX 6000 Pro — LillyPod | 256 GPUs (32 servers) | ~$5.7M |
| CPU fat nodes | 16× Dell R7625/R7725 (256 cores, 2TB RAM each); ~$80K/node based on Dell configurator | ~$1.3M |
| Network + cables | MagTrain integration to Weka fabric; RTX6000 Pro and CPU fat nodes on Weka fabric | ~$650K |
| Weka hot tier +2PB | ~12 additional Weka nodes (not drive expansion); based on Dell RFP pricing of $1.3M per ~1PB | ~$3M |

**Shared — Datacenter infrastructure:**

| Item | Detail | Capital (est.) |
|---|---|---|
| DC infrastructure | UPS, racks, PDU, CDU, fire suppression, install/labor; Greg's full 750 KW envelope estimate (incl. 15% buffer), shared with md3 deployment | ~$7.1M |

*Carrying the full number forward — DC infrastructure is largely indivisible; UPS, CDU, and fire suppression are per-room costs, not per-rack. Rack and PDU counts will scale down modestly, but the dominant line items do not. Confirm actual number with Greg Johnson once server count and row layout are finalized.*

### 2026 Total Capital Ask

| Bucket | What it buys | Capital (est.) |
|---|---|---|
| md3 — additional RTX 6000 Pro | 256 GPUs (32 servers); expands md3 to 512 total | ~$5.7M |
| LillyPod — consolidation/expansion | 256 RTX 6000 Pro + 16 CPU fat nodes + network/cables + Weka +2PB | ~$10.65M |
| Shared DC infrastructure | UPS, racks, PDU, CDU, fire suppression, install/labor (covers both deployments) | ~$7.1M |
| **Total 2026 capital ask** | | **~$23.45M** |

### On-prem vs. cloud cost comparison

The relevant comparison for the incremental ask is the ~$10.65M LillyPod budget vs. the cloud alternative for that hardware. The following compares on-prem cost against AWS 3-year all-upfront Savings Plans — the maximum discount tier — with Lilly's negotiated 22% enterprise discount:

| Compute tier | GPUs | Cloud rate (SP + 22% discount) | 3-year cloud cost | 5-year cloud cost | On-prem cost | Ratio (5-yr) |
|---|---|---|---|---|---|---|
| RTX 6000 Pro (new 256) | 256 | $1.71/hr/GPU | ~$11.5M | ~$19.2M | ~$5.7M (GPU capex only) | **3.4×** |

*Full-fleet comparison (B300, MagTrain) in Appendix A.*

### Capability delta

**Live example — virtual screening (VS) team:** The VS team currently runs simulation workloads on cloud: L40S at $5.25/hr per job (2 GPUs, 48GB each) and RTX 6000 Pro at $3.63/hr per job (1 GPU, 96GB). Both configurations are hitting memory limits — jobs run out of memory on both hardware tiers. A job that exceeds the memory envelope must be split across additional GPUs, which multiplies the hourly cloud cost proportionally and extends wall-clock time. Appendix A puts the on-prem advantage at 3.4× using the maximum cloud discount; the VS team is paying on-demand rates, so the actual gap in their case exceeds 7×. For jobs already exceeding 96GB, H200 (141GB HBM3e) and B300 (192GB HBM3e) are both available on the consolidated platform — no multi-GPU split required.

**Pipeline throughput — the staging bottleneck:** A representative end-to-end scientific-AI workflow: simulation job writes trajectory files → featurization/preprocessing → model retraining or scoring on a GPU. In the current fragmented state, this pipeline crosses cluster boundaries. The inter-cluster data transfer is a blocking step — the simulation output must be fully staged before the downstream job can be queued on a different cluster. For large trajectory datasets (hundreds of GB per run), that staging step is hours of wall-clock time and a manual handoff point that prevents the pipeline from being automated end-to-end. On a shared Weka fabric, the staging step is eliminated: simulation output is written once and is immediately available to any fabric-connected job — featurization on a CPU fat node, retraining on a B300 — without a copy. The pipeline becomes a scheduler problem, not a data movement problem.

Today's fragmented state: teams manually stage data between clusters; no cross-cluster dependency management; traditional HPC environments at Lilly have been built as scheduler queues in front of nodes — no fast storage fabric, no compute fabric, no high-bandwidth interconnect. md3 is the current example: it can dispatch jobs, but it cannot run tightly-coupled workloads or serve as a data-local compute tier for pipelines that land on LillyPod.

Consolidated state: a cluster that is on the Weka fabric — not NFS-mounted, but connected at the fabric layer — can read and write data at full storage bandwidth with no inter-cluster copy step. One Weka namespace shared across fabric-connected nodes means data is written once and available to any job on the platform. Cross-cluster jobs become a scheduler problem, not a data problem. A consolidated LillyPod — heterogeneous by design, spanning training-class GPUs, simulation-class GPUs, and fat CPU nodes on a single fabric — becomes the natural landing point for future GPU requests rather than each request spawning a new purpose-built environment.

**The NFS distinction matters.** A Weka NFS mount accesses the hot tier but is not fabric membership — it does not deliver fabric-level throughput. Fabric membership — a direct connection to the Weka storage fabric — is what enables data-local compute at scale. These are not interchangeable, and the integration spec for any cluster joining the platform must be explicit on this point.

---

## Migration Path

**First capacity online Q3 2026; full consolidation complete Q1 2027.**

Sequenced to minimize disruption and validate each step before the next:

**Step 0 — md3 RTX 6000 Pro deployment (near-term, in progress)**
- 256× RTX 6000 Pro Blackwell to md3; 32 8-way servers on Grid Engine
- md3 has no fast storage or compute fabric; nodes run under Grid Engine as currently architected
- Weka hot tier already NFS-mounted on md3 — no change to that access path
- Storage fabric integration (Step 5) is the forward step; this deployment does not depend on it

**Step 1 — MagTrain Weka integration (Q3 2026)**
- Inter-row 400G cabling between MagTrain row and LillyPod Weka fabric
- Dependency owners: Greg Johnson (DC infrastructure), Jonathan Klinginsmith (HPC admin)
- Risk: inter-row cabling physical constraints; validate before committing
- Outcome: H100, H200, and L40S capacity joins LillyPod under Run:ai; immediate utilization gain

**Step 2 — CPU fat node deployment (Q3 2026, parallel with Step 1)**
- 16× Dell R7625/R7725, 2× AMD CPUs, 256 cores, 2TB RAM each
- Run:ai CPU node pool construct; no scheduler change for existing GPU jobs
- Unlocks mmseqs / UniRef100 in-memory indexing workloads on platform

**Step 3 — RTX 6000 Pro Blackwell deployment (Q4 2026)**
- 256× cards (32 8-way servers), Run:ai simulation pool
- Physics-based simulation workloads moved off ad-hoc environments
- With Steps 1–3 complete, the platform has the hardware to orchestrate scientific-AI workflows end-to-end — training, simulation, and bioinformatics on a single Weka fabric with no inter-cluster data movement
- Run:ai fractional allocation for variable simulation job lengths
- Fabric switches and cabling for Step 5 md3 integration covered in the $650K network + cables budget

**Step 4 — Weka hot tier expansion +2PB (Q4 2026, parallel with Step 3)**
- Validates as additional Weka nodes, not drive expansion within existing nodes
- Coordinate with Greg Johnson and Jonathan Klinginsmith on Weka node procurement lead time

**Step 5 — md3 Weka fast fabric mount (Q1 2027)**
- md3 has no existing fabric infrastructure
- md3 nodes get Weka fabric membership (not NFS — NFS already mounts the hot tier but does not deliver fabric-level throughput)
- md3 remains on Grid Engine; no workload migration forced
- Eliminates data silo; md3 teams gain access to hot-tier data for preprocessing

---

## Risks

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| Inter-row cabling for MagTrain integration is physically constrained | Medium | High | Validate with Greg + Jonathan before committing to Step 1 timeline; this is the single largest physical dependency |
| Weka expansion as drive-only (not new nodes) creates throughput bottleneck | Medium | High | Specify additional nodes in procurement |
| md3 fabric membership stalls at existing NFS state | High (default path) | High | md3 already has Weka hot tier NFS-mounted — risk is that this is treated as sufficient and Step 5 is deprioritized; storage fabric membership must be explicit in the forward plan |
| Internal org alignment — LRL-facing team continues to field compute requests independently | Medium | High | Without a shared intake process, new island environments will continue to be created even after consolidation; requires a leadership-level direction that new compute requests route through the platform |

---

## What I Need From You

Five concrete decisions, each one where Thomas's authority is the unblocking factor:

1. **Endorse end-to-end scientific-AI workflow throughput as the unit of optimization.** The hardware mix — training-class GPUs, simulation-class GPUs, fat CPU nodes — is only coherent if the goal is to run complete workflows on the platform rather than optimizing individual compute tiers in isolation. The budget ask and the platform architecture both depend on this framing. Confirm before the capital request goes forward.

2. **Sponsor the capital request and carry it forward through the funding process.** Separate from the ~$5.7M md3 commitment (256 additional RTX 6000 Pro cards), the incremental ask is approximately $10.65M to make LillyPod suitable for end-to-end scientific-AI workflows (256× RTX 6000 Pro + CPU nodes + network/cables + Weka expansion), plus ~$7.1M in shared DC infrastructure covered by Greg's model. The expected outcome is significant traffic consolidation onto the platform, which improves utilization on the B300 side. A platform that visibly serves end-to-end workloads — not just training — counters the narrative that cheap-GPU island environments are sufficient. That visibility matters across Lilly, not just within AIR.

3. **Commit to cross-org coordination with Krishna Jagannathan.** Greg Johnson and Jonathan Klinginsmith (Digital Core) are the execution owners for the inter-row cabling and Weka integration. A shared commitment between AIR and Digital Core at your level and Krishna's level removes the coordination tax from the working level.

4. **Direct the md3 storage fabric step.** md3 already has the Weka hot tier NFS-mounted — that is the current state, not the destination. The immediate ask is a direction to proceed with storage fabric membership: non-disruptive, no workload migration required. Whether md3 eventually requires full LillyPod integration — compute fabric and Run:ai scheduling — is a separate question; that path is available if workload needs evolve, but it is not the immediate ask.

5. **Establish platform-first intake as a standing principle.** Without a clear direction that new LRL compute requests route through the platform rather than spawning independent environments, the island pattern will continue even after this consolidation. The merger of Research IT into AIR creates the opportunity but not the guarantee. The ask is a standing principle, not a one-time decision.

---

*Next step: iterate this draft, then produce final Word doc for Thomas.*

---

## Appendix A — Full-fleet on-prem vs. cloud comparison

B300 and MagTrain hardware is already purchased or committed; the incremental budget ask does not change these numbers. The table below covers the full hardware estate for context.

Compared against AWS 3-year all-upfront Savings Plans — the maximum discount tier — with Lilly's negotiated 22% enterprise discount applied:

| Compute tier | GPUs | Cloud rate (SP + 22% discount) | 3-year cloud cost | 5-year cloud cost | On-prem cost | Ratio (5-yr) |
|---|---|---|---|---|---|---|
| LillyPod B300 | 1,016 | $9.25/hr/GPU | ~$247M | ~$412M | $150M (5-yr TCO incl. storage) | **2.7×** |
| MagTrain H100 | 72 | $3.58/hr/GPU | ~$6.8M | ~$12.3M | $6.8M (capex incl. storage) | — |
| MagTrain H200 | 64 | $4.12/hr/GPU | ~$6.9M | ~$11.5M | incl. above | — |
| MagTrain L40S | 32 | $1.38/hr/GPU | ~$1.2M | ~$1.9M | incl. above | — |
| **MagTrain total** | **168** | | **~$14.9M** | **~$25.8M** | **$6.8M** | **3.8×** |
| RTX 6000 Pro (new 256) | 256 | $1.71/hr/GPU | ~$11.5M | ~$19.2M | ~$5.7M (GPU capex only) | **3.4×** |

**The "discount" requires paying more upfront, not less.** To get these Savings Plan rates, Lilly would commit the full 3-year cost as a single all-upfront payment — $247M for the B300 tier alone, $14.9M for MagTrain, $11.5M for the new RTX 6000 Pro cards. That is ~$273M in cash committed on day one for compute only, before cloud storage costs (EBS, FSx, S3). The equivalent on-prem capital outlay — including storage — is a fraction of that: $150M for the B300 5-year TCO, $6.8M for MagTrain, $5.7M for the RTX 6000 Pro cards. The cloud "discount" costs more than on-prem at full price, buys only 3 years of access instead of ownership, does not include storage, and cannot serve as a shared fabric-connected platform.
