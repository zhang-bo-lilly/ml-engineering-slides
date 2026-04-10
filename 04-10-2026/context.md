The AIOS team is a new area under the Advanced Intelligence and Research organization, led by Brian Lewis.
I am moved to Brian's team and is responsible for the compute layer. This Friday is a full day workshop for this new team. And I am presenting some information about compute layer.

I am providing raw materials here. The materials are dumped here without particular order. I want to iterate with you to come up with a presentation for Friday.

The execution on these compute is not one model. A more relasitic setting is a workflow or a directed ayclic graph of models. The word modell is used in a loose term. It can be ML model, or can represent an scientific application.

It is important to realize that the workflow execution is the key here. And the component of the workflow is not necessarily ML model, or GPU heavy models. In drug discovery setting, it is completely normal where you run some physics based model in some steps of your workflow, some cpu-only processing step, some light-GPU step (meaning does not need the most expensive GPU), and some high-end GPU stuff.

Equally important is the data transfer between those individual steps. The volume of the data can be huge. And when on-prem and cloud is mixed, egress cost becomes a serious concern here.


The image.png file contains an inventory of Lilly's GPU resources. The one under this team's goverance are the 1016 ones under LillyPod, 32 L40s, 72 H100, and 64 H200 on MagTrain, and a A800 server.

MagTrain and LillyPod use two different management system. MagTrain is Slurm, and LillyPod is Runai. MagTrain can access internet and LillyPod is air-gapped.

The current setup is roughly sketched in image-1.png

One of the issue with this setup is users may accidentally run jobs on MagTrain consuming data on the weka side. As that filesystem is not physically within the MagTrain cluster, it is can cause GPU idling.

HPC team is aligned on the plan to unify the different environment with weka.


Runai has several advantages in terms of quota management, dynamic GPU fractioning. But Runai has a per GPU annual charge about $3000. So not all the GPUs in Lilly will be put to Runai.

It will remain a segregated envrionment, in terms of the scheduling system used. Then, there lacks a meta orchestrator that can schedule and chain pipeline execution across different environment. As a concrete example, A->B->C->D->E is a pipeline, where A->B->C is done in Runai and then D->E is done in Slurm. We can schedule two parts separately as workflows but cannot chain them together. This will force user to be aware of the compute environment. In some sense, leaking information from the compute layer (in terms of abstraction)

Developing such a meta orchestrator is a long-term plan.

The near-term plan for that is consolidate resources into LillyPod, as shown in image-2.png file. This has been communted with Greg and Jon since the RFP in 2025. Aligned in principle, but execution plan is pending. Some investigation work is needed as the network cards on H100/H200/L40s are different generation from B300. The MagTrain's private system is also different (that triggers different IO best practice)

The image-2 represents a stage where application can be effectively developed for the end-user. It completely abstract the different compute needs, and the user does not need to worry about the data transfer. Again, it is not realistic to put everything under Run:ai due to its license cost. So meta orchestrator part is a novel area to consider as the long term plan.
