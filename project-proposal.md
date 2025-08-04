# Project Proposal: Codeset Management System Development

**Client:** Health Catalyst  
**Prepared by:** Silhouette LLC  
**Date:** August 4, 2025  
**Engineer Rate:** $150/hour

---

## Project Summary

Silhouette LLC will develop a modular, Excel-driven Codeset Management Platform. The application enables healthcare clients to upload and manage custom codesets, dynamically render tab-specific UI logic, preserve formulas, and export validated files. Built with Streamlit and Flask, the system is designed for long-term maintainability and integration with vendor workflows.

Phase 2 of the project includes shared Git repository integration via Azure DevOps (ADO), automatic ticket creation in Azure Boards, secure Single Sign-On (SSO) authentication, and full audit tracking. This proposal now also lays out a multi-phase roadmap for advanced features—UI enhancements, validation/reporting, AI-driven automation, and performance scaling—and structured client-side training to ensure smooth onboarding and adoption.

---

## Scope of Work

### Phase 1: Application Core

| Task Category                   | Description                                                                       | Estimated Hours |
|---------------------------------|-----------------------------------------------------------------------------------|-----------------|
| UI & Interaction Design         | Streamlit interface for upload, tab rendering, and navigation across custom sheets | 12–15           |
| Excel Parsing & Dynamic Handling| Per-tab logic with formula preservation and validation                             | 8–12            |
| Dropdowns, Mappings & Logic     | Render dropdowns for mappings (`STANDARD_DESCRIPTION`, `MAPPED_STD_DESCRIPTION`)   | 6–8             |
| Excel Export Functionality      | Export modified workbooks while retaining formulas and structure                   | 6–10            |
| Flask Backend (Optional)        | Auxiliary endpoints for file export or API actions                                 | 6–8             |
| Modular Components              | Encapsulated logic for parsing, tab control, dropdowns, and formulas               | 8–12            |
| Testing & QA                    | Unit and integration testing of UI, exports, and file logic                        | 6–10            |
| Codex Documentation & Handoff   | Update Markdown handoff and YAML task runners                                      | 4–6             |

**Estimated Time (Phase 1):** 56–81 hrs  
**Estimated Cost (Phase 1):** \$8,400 – \$12,150

---

### Phase 2: Git Integration, Ticketing & SSO

| Task Category               | Description                                                                                   | Estimated Hours |
|-----------------------------|-----------------------------------------------------------------------------------------------|-----------------|
| ADO Git Integration         | Configure shared Git repo structure and programmatic commit logic per submission              | 6–8             |
| Azure Boards Ticket Trigger | Automatically create work items in ADO Boards based on submission metadata                    | 5–7             |
| SSO Authentication          | Enforce client-authenticated access using Azure AD or compatible SSO protocol                  | 8–10            |
| Repo & User Access Setup    | ADO access and auth testing for client/vendor use                                             | 4–6             |
| Audit Logging               | Track submitter identity, repo updates, and commit metadata                                   | 4–6             |

**Estimated Time (Phase 2):** 27–37 hrs  
**Estimated Cost (Phase 2):** \$4,050 – \$5,550

---

### Phase 3: Client Training & Enablement

| Task Category             | Description                                                        | Estimated Hours |
|---------------------------|--------------------------------------------------------------------|-----------------|
| Live Training Sessions    | Host live 60–90 minute virtual training sessions for client users  | 3–5             |
| Training Materials        | Develop quick-start guide, annotated screenshots, and workflows    | 4–6             |
| Recording & Playback      | Provide recorded walkthroughs or screen captures for internal reuse| 2–3             |
| Q&A / Follow-up Support   | Address follow-up questions and issues post-rollout                | 2–3             |

**Estimated Time (Phase 3):** 11–17 hrs  
**Estimated Cost (Phase 3):** \$1,650 – \$2,550

---

### Phase 4: UI & Usability Enhancements

| Task Category             | Description                                                            | Estimated Hours |
|---------------------------|------------------------------------------------------------------------|-----------------|
| Row Filtering & Search    | Add a text-search bar and/or filter controls to find unmapped rows     | 8–10            |
| Pagination & Virtual Scroll| Implement paging or lazy-loading for very large sheets               | 10–12           |
| Undo/Redo Stack           | Maintain a history of user actions so changes can be reverted easily  | 8–10            |
| Dark Mode / Theme Selector| Offer light/dark toggle and custom branding via configuration file    | 4–6             |
| Inline Help & Tooltips    | Embed contextual “?” icons explaining columns, rules, and best practices | 6–8           |

**Estimated Time (Phase 4):** 36–46 hrs  
**Estimated Cost (Phase 4):** \$5,400 – \$6,900

---

### Phase 5: Validation & Data Profiling  
#### + Collaboration & Version Control

| Task Category                | Description                                                                                      | Estimated Hours |
|------------------------------|--------------------------------------------------------------------------------------------------|-----------------|
| Schema Comparison Reports    | Auto-generate printable PDF/HTML reports summarizing differences between repo workbooks          | 10–12           |
| ADO Repo Alerts & Ticketing  | Trigger Azure Boards work items when the hosted spreadsheet is updated                           | 8–10            |

**Estimated Time (Phase 5):** 18–22 hrs  
**Estimated Cost (Phase 5):** \$2,700 – \$3,300

---

### Phase 6: AI-Driven & Automation Features

| Task Category         | Description                                                                                              | Estimated Hours |
|-----------------------|----------------------------------------------------------------------------------------------------------|-----------------|
| Mapping Suggestions   | Use Codex/LLM to auto-suggest `MAPPED_STD_DESCRIPTION` based on similar entries                          | 12–15           |
| Anomaly Detection     | Flag outlier codes or display values that deviate from established patterns                              | 8–10            |
| Scheduled Validations | Nightly/weekly automated validation runs with emailed summary reports                                     | 6–8             |

**Estimated Time (Phase 6):** 26–33 hrs  
**Estimated Cost (Phase 6):** \$3,900 – \$4,950

---

### Phase 7: Performance & Scalability

| Task Category                   | Description                                                                                      | Estimated Hours |
|---------------------------------|--------------------------------------------------------------------------------------------------|-----------------|
| Asynchronous Processing         | Offload heavy workbook loads and exports to background jobs (e.g., Celery)                       | 10–12           |
| Caching & Incremental Loads     | Cache parsed workbook data (in memory or Redis) and only re-parse changed sheets                  | 8–10            |
| Dockerization & Deployment      | Provide a `Dockerfile` plus Helm/Terraform scripts for easy, repeatable deployment               | 6–8             |

**Estimated Time (Phase 7):** 24–30 hrs  
**Estimated Cost (Phase 7):** \$3,600 – \$4,500

---

## Combined Estimate

| Scope                                     | Hours       | Cost                  |
|-------------------------------------------|-------------|-----------------------|
| Phase 1: Core App                         | 56–81 hrs    | \$8,400 – \$12,150    |
| Phase 2: Git/SSO                          | 27–37 hrs    | \$4,050 – \$5,550     |
| Phase 3: Training                         | 11–17 hrs    | \$1,650 – \$2,550     |
| Phase 4: UI/Usability                     | 36–46 hrs    | \$5,400 – \$6,900     |
| Phase 5: Validation & Collaboration       | 18–22 hrs    | \$2,700 – \$3,300     |
| Phase 6: AI & Automation                  | 26–33 hrs    | \$3,900 – \$4,950     |
| Phase 7: Performance & Scalability        | 24–30 hrs    | \$3,600 – \$4,500     |
| **Total Estimate**                       | **198–266 hrs** | **\$30,600 – \$39,900** |

---

## Deliverables

- Codeset Management Platform with dynamic UI, Excel parsing, and export logic  
- Codex automation integration documentation and YAML runners  
- Git integration with Azure DevOps (vendor-hosted repo)  
- Automated work item creation in Azure Boards  
- SSO authentication and metadata tracking  
- Advanced UI enhancements, reporting, AI-driven features, and performance scaling  
- Client onboarding training sessions and support materials  

---

## Assumptions

- Client IT will coordinate on SSO and Azure DevOps access.  
- Training is virtual unless otherwise agreed upon.  
- Codex automation framework is already in place; this tool will conform to the existing structure.  

---

## Next Steps

Please review and confirm scope approval and pricing. Upon sign-off, Silhouette LLC will initiate development and schedule parallel training and rollout activities.  
