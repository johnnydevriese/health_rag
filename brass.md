[Proposal Number: To Be Assigned]
Topic Number: N252-097

BlackMind Research LLC

Battle Rhythm Adaptive Support System (BRASS)
Volume 2: Technical Volume

This proposal includes data that must not be disclosed outside the Government and must not be duplicated, used, or disclosed-in whole or in part-for any purpose other than to evaluate this proposal. If, however, a contract is awarded to this proposer as a result of-or in connection with-the submission of this data, the Government has the right to duplicate, use, or disclose the data to the extent provided in the resulting contract. This restriction does not limit the Government's right to use information contained in this data if it is obtained from another source without restriction. The data subject to this restriction are contained in pages 1-10.

**1.0 Description of Proposed Phase I Technical Effort**

BlackMind Research LLC proposes the Battle Rhythm Adaptive Support System (BRASS), an integrated Artificial Intelligence/Machine Learning (AI/ML) tool designed to significantly enhance battle rhythm management for operators of theater-level command and control (C2) systems, specifically targeting the AN/UYQ-100 Undersea Warfare Decision Support System (USW-DSS), during complex Undersea Warfare (USW) wartime scenarios. The Navy topic N252-097 clearly identifies a critical gap: battle rhythms developed and practiced in peacetime often fail under the stress and complexity of high-intensity warfare. Commanders and staff may inappropriately accelerate the rhythm, leading to reduced analysis time, degraded situational awareness (SA), and increased operator error. BRASS directly addresses this challenge by providing operators with AI/ML-driven insights and recommendations to maintain an _effective_ and _adaptive_ battle rhythm.

The core innovation of BRASS lies in its ability to dynamically assess the operational environment's complexity using authoritative USW-DSS data streams (including bathymetry, sound propagation, track information for friendly, neutral, and threat forces, and planned operations) and recommend adjustments to the battle rhythm's tempo and structure. BRASS will not dictate actions but will serve as an intelligent advisor, helping operators balance the crucial demands of timely reporting/updates with the necessary time for in-depth analysis and planning required for effective courses of action (COA). By analyzing incoming data and ongoing operations, BRASS will provide SA specifically focused on the _state of the battle rhythm itself_, recommending when to adjust meeting cadences, information requirements, or tasking priorities based on the evolving tactical situation. Furthermore, BRASS will incorporate a tasking assistance module, leveraging the situational context provided by the AI/ML core to help operators rapidly and reliably formulate and disseminate battle rhythm-related tasks. This approach moves beyond static, pre-planned schedules to a dynamic, situationally-aware battle rhythm management paradigm, directly addressing the Navy's need for a tool that supports operators across the full spectrum of conflict intensity while complying with stringent Information Assurance (IA) and cybersecurity requirements. Our team, composed of AI/ML experts and retired military officers with extensive C2 and planning experience, is uniquely positioned to develop this capability.

**1.1 Phase I Technical Objectives**

The primary goal of Phase I is to establish the technical feasibility of the BRASS concept. This will be achieved through the following specific objectives:

1.  **Develop Battle Rhythm Complexity Modeling Algorithms:** Define and evaluate initial algorithms capable of ingesting representative USW-DSS data types (simulated or unclassified equivalents) to quantify operational complexity relevant to battle rhythm management. This includes factors like information velocity, decision cycle time pressure, and uncertainty levels.
2.  **Design AI/ML Recommendation Engine Concept:** Conceptualize the core AI/ML engine that uses the complexity model outputs to generate recommendations for battle rhythm adjustments (e.g., adjusting meeting frequency, modifying reporting requirements, suggesting focus areas for analysis). Explore techniques like reinforcement learning or expert systems informed by ML.
3.  **Conceptualize Integrated Tasking Assistance Module:** Design the architecture for a module that integrates with the rhythm recommendations and situational context to assist operators in generating, prioritizing, and potentially pre-populating battle rhythm-related tasks.
4.  **Define USW-DSS Data Interface Requirements:** Analyze the types, formats, and potential access methods for authoritative USW-DSS data required by BRASS. Identify key data elements needed for complexity modeling and situational context. Document preliminary interface specifications.
5.  **Develop Preliminary User Interface (UI) / User Experience (UX) Concepts:** Create mockups and workflow diagrams illustrating how operators would interact with BRASS to visualize rhythm status, receive recommendations, understand the rationale, and utilize the tasking assistance features within a USW-DSS-like environment.
6.  **Establish Feasibility Metrics:** Define quantifiable metrics to assess the feasibility and potential effectiveness of the BRASS concept, such as the correlation between modeled complexity and SME assessment, the logical coherence of generated recommendations, and the potential time savings in task generation based on simulated scenarios.

**1.2 Phase I (Base and Option) Statement of Work**

The Phase I effort is structured into a Base period focused on core feasibility and concept development, and an Option period for refining the design and planning for Phase II prototyping.

| Task No.   | Title                                       | Description                                                                                                                                                              | Performer or Subcontractor |
| :--------- | :------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------- |
| **BASE**   |                                             |                                                                                                                                                                          |                            |
| 1          | Requirements & Data Analysis                | Refine understanding of USW battle rhythm challenges via literature review and SME consultation. Analyze representative USW-DSS data types and formats for BRASS inputs. | BlackMind                  |
| 2          | Complexity Modeling Algorithm Development   | Develop and test initial algorithms for quantifying operational complexity based on analyzed data types. Document algorithm design and preliminary results.              | BlackMind, Dr. Aurentz     |
| 3          | AI/ML Recommendation Engine Concept Design  | Design the conceptual architecture for the AI/ML engine generating rhythm recommendations. Evaluate potential AI/ML techniques. Document the conceptual design.          | BlackMind, Dr. Serra       |
| 4          | Tasking Assistance Module Concept           | Design the conceptual architecture for the tasking assistance module and its integration with the recommendation engine. Document the concept.                           | BlackMind                  |
| 5          | Preliminary UI/UX Mockups & Workflow        | Develop initial UI mockups and define user interaction workflows for visualizing rhythm status, recommendations, and tasking assistance.                                 | BlackMind                  |
| 6          | Feasibility Report & Phase I Final Review   | Document findings, algorithm performance, conceptual designs, UI/UX mockups, feasibility assessment against metrics, and present results.                                | BlackMind                  |
| **OPTION** |                                             |                                                                                                                                                                          |                            |
| 7          | Refined Algorithm Design & Evaluation       | Refine complexity and recommendation algorithms based on Base findings. Conduct more rigorous testing using simulated scenario data.                                     | BlackMind, Dr. Aurentz     |
| 8          | Detailed Prototype Architecture             | Develop detailed software architecture specifications for a Phase II BRASS prototype, including module interactions and data flows.                                      | BlackMind                  |
| 9          | USW-DSS Integration & IA Analysis           | Detail data interface specifications for USW-DSS integration. Analyze IA/cybersecurity requirements (per DoD Cloud Computing SRG, etc.) for Phase II prototype.          | BlackMind, Mr. Karcher     |
| 10         | Phase II Prototyping & Transition Plan      | Develop a detailed Phase II SOW, schedule, resource plan, and risk assessment for prototype development, demonstration (on USW-DSS cloud infra), and Fleet user sprints. | BlackMind                  |
| 11         | Option Final Report & Phase II Kickoff Prep | Deliver final Option report detailing refined designs, architecture, integration plan, and Phase II plan. Prepare materials for Phase II kickoff.                        | BlackMind                  |

**1.3 Related Work**

BlackMind Research LLC brings significant relevant experience to the BRASS effort. Our team possesses a unique blend of deep AI/ML expertise and extensive military operational planning and C2 experience, crucial for understanding the nuances of battle rhythm management. Our related work includes:

- **DefenseOS Integration Platform:** We developed a platform integrating disparate high-end military systems, providing us with critical experience in creating interoperable data formats and system architectures relevant to integrating BRASS with USW-DSS.
- **LLM Classification & RAG Pipelines:** Our work developing novel Large Language Model (LLM) classification pipelines for scoring response quality and implementing Retrieval-Augmented Generation (RAG) pipelines for processing large volumes of messages (30,000/month) provides foundational expertise for BRASS's potential use of NLP/LLMs in analyzing situational reports or generating tasking language, and for evaluating the quality/relevance of information influencing the battle rhythm.
- **High-Confidence ML Systems (Changi Airport):** Our development of the ML lifecycle for drone detection at Singapore Changi Airport, achieving a 10x reduction in false positives, demonstrates our capability to build reliable, high-confidence AI/ML systems essential for operational C2 support.
- **Military Domain Expertise:** Our team includes retired U.S. Army officers (Mr. Karcher, Mr. Myers) with thousands of hours leading and executing military planning processes (MDMP/MCPP equivalents) in training and combat, from battalion to brigade levels. This ensures BRASS is grounded in operational reality and addresses the practical challenges faced by C2 staff.
- **Preliminary Research:** We have conducted initial reviews of literature on battle rhythm (e.g., Prescott, JFQ 102) and C2 systems like USW-DSS, confirming the need identified in the topic description and informing our technical approach.

We differentiate BRASS from generic scheduling or task management tools through its focus on _dynamic adaptation_ driven by AI/ML analysis of the complex, real-time USW operational environment, specifically addressing the balance between analytical depth and reporting tempo.

**2.0 Key Personnel**

The BRASS Phase I effort will be led by a highly qualified team with direct experience in AI/ML development, military operations, and DoD programs.

| Name and Title                           | Employer                      | Qualifications                                                                                                                                                                                                                                                        | \*Foreign National (Y/N) | Publications                                                                                                                                                                    |
| :--------------------------------------- | :---------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Johnny Devriese, Principal Investigator  | BlackMind                     | 10+ years building AI/ML data platforms for military/private applications. BS Physics (WSU), Grad AI (Stanford). Led \$4M AF LiDAR project, Changi Airport ML (10x FP reduction), RAG pipelines (30k msg/mo), LLM classification pipelines.                           | N                        | "The nonlinear optical response of a simple molecule"                                                                                                                           |
| Dr. Jared Aurentz, AI Research Scientist | BlackMind                     | PhD Applied Math (WSU), Postdoc (Oxford). Distinguished investigator (U. Huelva). Developed interpretable AI (Zhegalkin polynomials) for game rule learning. Expertise in algorithm development, complex systems modeling.                                            | N                        | "Interpretable AI through Zhegalkin Polynomials," J. Comp. Intel., 2023; "Efficient Rule Learning in Complex Game Systems," Int. Conf. AI, 2022.                                |
| John Karcher, VP of Government Solutions | BlackMind                     | Retired U.S. Army Officer (21 yrs), Bn Cdr (1/82 ABN). Expertise in defense innovation, gov contracting, strategic consulting. Leads SBIR/STTR initiatives, ensures alignment with DoD operational needs.                                                             | N                        | "Integrating Commercial Innovation into Military Operations," Joint Force Quarterly, 2021.                                                                                      |
| Eli Myers, Chief Operating Officer       | BlackMind                     | Retired U.S. Army Officer (20 yrs), Airborne/SOF Infantry, Bn Cdr (82nd ABN). Extensive military planning & requirements expertise informing product development for warfighter relevance.                                                                            | N                        | "The Rate of Fire Against Men," Infantry Journal, 2024; "Decentralizing the Fight," Modern War Institute, 2020                                                                  |
| Dr. Edoardo Serra, Senior AI Advisor     | Boise State University / PNNL | Assoc. Professor (BSU), Sr. Research Scientist (PNNL). Leading AI expert (100+ pubs). Research in robust ML for NLP, agentic AI, graph representation learning. PI for NSA grant on graph ML for cybersecurity. _(Role limited to unclassified fundamental research)_ | Y                        | "Graph Neural Networks for Cybersecurity Event Processing," ACM T. Knowl. Disc. Data, 2023; "Robust Machine Learning for NLP in Adversarial Environments," Int J Info Sec, 2022 |

[*RESTRICTION ON PERFORMANCE BY FOREIGN NATIONALS: This topic (N252-097) is ITAR Restricted. Dr. Serra is a Foreign National. His participation in Phase I will be strictly limited to fundamental research aspects not subject to ITAR controls. He will not have access to export-controlled technical data or be involved in Phase II/III activities requiring security clearances unless specific mitigating procedures are approved by cognizant authorities. Details are provided in Volume 5.]

**3.0 Commercialization/Transition Plan Summary**

BRASS has a clear primary transition path to operational use within the U.S. Navy and significant potential in adjacent DoD, federal, and commercial markets.

**DoD Transition Strategy:** The primary transition target for BRASS is integration into operational builds of the AN/UYQ-100 USW-DSS provided to Fleet operators. Our Phase I Option and Phase II efforts will explicitly focus on defining integration pathways, adhering to USW-DSS architecture standards, and meeting IA/cybersecurity requirements (e.g., DoD Cloud Computing SRG). We plan to engage early with relevant stakeholders, including NAVSEA PEO IWS (specifically IWS 5.0) and the USW-DSS Program Office, leveraging our team’s operational and contracting experience (Mr. Karcher, Mr. Myers). The Phase II plan includes user sprints with Fleet operators and testing on government-provided USW-DSS cloud infrastructure, culminating in validation support in accordance with the IWS 5.0 USW-DSS Peer Review Group, as specified in the topic description.

**Additional Government Markets:** The core capability of dynamically managing operational tempo and tasking based on AI/ML analysis of situational complexity is applicable to:

- Other Navy/Joint C2 systems (e.g., GCCS-M, JADC2 efforts)
- Combatant Command and Joint Task Force planning staffs
- Intelligence Community agencies managing complex analysis workflows
- Department of Homeland Security (DHS) operations centers

**Commercial Applications:** The underlying technology for adaptive workflow/tempo management based on real-time complexity assessment has commercial potential in:

- **Emergency Management & Disaster Response:** Optimizing C2 and resource allocation during rapidly evolving crises (e.g., FEMA, state/local EOCs).
- **Complex Project Management:** Industries like large-scale construction, logistics, or event management requiring dynamic adjustment of schedules and tasks.
- **Financial Operations Centers:** Managing responses to market volatility or cybersecurity incidents.
- **Healthcare Command Centers:** Optimizing patient flow and resource allocation during high-demand periods or emergencies.

**Market Size:** The global Command and Control (C2) market is substantial, projected to exceed \$40 billion USD annually, with AI integration being a major growth driver. The specific market for AI in military C2 and decision support is rapidly expanding.

**Phase III Strategy:** BlackMind will pursue direct transition to the USW-DSS program via Phase III funding. We will also explore integration partnerships with prime defense contractors involved in USW-DSS and other relevant C2 systems. Commercialization will be pursued through direct sales or licensing agreements targeting the identified commercial sectors.

**4.0 Facilities/Equipment**

BlackMind Research LLC operates from its facilities in Boise, ID, and possesses the necessary infrastructure and equipment to successfully execute the proposed Phase I effort. We leverage a secure, scalable cloud environment:

- **High-Performance Computing Environment:** Access to AWS GovCloud resources, including GPU-accelerated instances (comparable to NVIDIA A100 capabilities) suitable for demanding AI/ML model training and inference required for BRASS algorithm development and testing.
- **Secure Development Environment:** Our development practices align with NIST SP 800-171 standards, utilizing AWS GovCloud to provide an environment suitable for handling CUI and preparing for future classified work in Phase II. This includes secure code repositories, access controls, and data handling procedures.
- **Software Development Infrastructure:** We employ a modern DevOps toolchain supporting agile development, continuous integration/continuous deployment (CI/CD), and robust testing frameworks.

These facilities and resources are immediately available and sufficient for all planned Phase I Base and Option tasks. No additional capital equipment purchases are anticipated for Phase I.

All facilities where work will be performed comply with applicable environmental laws and regulations of Federal, state, and local governments for airborne emissions, waterborne effluents, external radiation levels, outdoor noise, solid and bulk waste disposal practices, and handling and storage of toxic and hazardous materials.

**5.0 Letters of Support**

[None provided at this time.]
