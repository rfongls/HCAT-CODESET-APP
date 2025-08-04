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

## Estimation Methodology

All feature estimates are sized according to **industry-standard complexity buckets** rather than proprietary historical data:

- **Simple features (4–8 hrs)**  
  E.g., dark-mode toggle, inline tooltips, basic reporting templates.
- **Moderate features (8–12 hrs)**  
  E.g., pagination/virtual scrolling, undo/redo stack, anomaly-detection rules.
- **Complex features (10–15 hrs)**  
  E.g., asynchronous job queues, AI-driven mapping suggestions, API integrations.

These ranges align with COCOMO II and other function-point sizing models for web applications, ensuring transparent, benchmark-driven estimates.

---

## Scope of Work

### Phase 1: Application Core

| Task Category                   | Description                                                                       | Estimated Hours |
|---------------------------------|-----------------------------------------------------------------------------------|-----------------|
| UI & Interaction Design         | Streamlit interface for upload, tab rendering, and navigation across custom sheets | 12–15 (moderate)|
| Excel Parsing & Dynamic Handling| Per-tab logic with formula preservation and validation                             | 8–12 (moderate) |
| Dropdowns, Mappings & Logic     | Render dropdowns for mappings (`STANDARD_DESCRIPTION`, `MAPPED_STD_DESCRIPTION`)   | 6–8 (simple)    |
| Excel Export Functionality      | Export workbooks while retaining formulas and structure                            | 6–10 (simple)   |
| Flask Backend (Optional)        | Auxiliary endpoints for file export or API actions                                 | 6–8 (simple)    |
| Modular Components              | Encapsulated logic for parsing, tab control, dropdowns, and formulas               | 8–12 (moderate) |
| Testing & QA                    | Unit and integration testing of UI, exports, and file logic                        | 6–10 (simple)   |
| Codex Documentation & Handoff   | Update Markdown handoff and YAML task runners                                      | 4–6 (simple)    |

**Phase 1 Total:** 56 – 81 hrs | \$8,400 – \$12,150

---

### Phase 2: Git Integration, Ticketing & SSO

| Task Category               | Description                                                                                   | Estimated Hours |
|-----------------------------|-----------------------------------------------------------------------------------------------|-----------------|
| ADO Git Integration         | Configure shared repo structure and programmatic commit logic per submission                  | 6–8 (simple)    |
| Azure Boards Ticket Trigger | Auto-create work items in ADO Boards based on submission metadata                             | 5–7 (simple)    |
| SSO Authentication          | Enforce client-authenticated access via Azure AD or compatible SSO                             | 8–10 (moderate) |
| Repo & User Access Setup    | ADO access and auth testing for client/vendor                                                  | 4–6 (simple)    |
| Audit Logging               | Track submitter identity, repo updates, and commit metadata                                   | 4–6 (simple)    |

**Phase 2 Total:** 27 – 37 hrs | \$4,050 – \$5,550

---

### Phase 3: Client Training & Enablement

| Task Category             | Description                                                        | Estimated Hours |
|---------------------------|--------------------------------------------------------------------|-----------------|
| Live Training Sessions    | 60–90 min virtual sessions for client users                        | 3–5 (simple)    |
| Training Materials        | Quick-start guide, annotated screenshots, workflow docs            | 4–6 (simple)    |
| Recording & Playback      | Recorded walkthroughs / screen captures                            | 2–3 (simple)    |
| Q&A / Follow-up Support   | Post-rollout questions and issue resolution                        | 2–3 (simple)    |

**Phase 3 Total:** 11 – 17 hrs | \$1,650 – \$2,550

---

### Phase 4: UI & Usability Enhancements

| Task Category             | Description                                                            | Estimated Hours |
|---------------------------|------------------------------------------------------------------------|-----------------|
| Row Filtering & Search    | Text-search bar and filter controls for unmapped rows                  | 8–10 (moderate) |
| Pagination & Virtual Scroll| Paging or lazy-loading for very large sheets                         | 10–12 (moderate)|
| Undo/Redo Stack           | History of user actions for safe reversion                             | 8–10 (moderate) |
| Dark Mode / Theme Selector| Light/dark toggle and custom branding                                  | 4–6 (simple)    |
| Inline Help & Tooltips    | Contextual “?” icons explaining columns, rules, best practices         | 6–8 (simple)    |

**Phase 4 Total:** 36 – 46 hrs | \$5,400 – \$6,900

---

### Phase 5: Validation & Data Profiling  
#### + Collaboration & Version Control

| Task Category                | Description                                                                                      | Estimated Hours |
|------------------------------|--------------------------------------------------------------------------------------------------|-----------------|
| Schema Comparison Reports    | Auto-generate printable PDF/HTML reports of workbook diffs                                        | 10–12 (complex) |
| ADO Repo Alerts & Ticketing  | Trigger Azure Boards tickets when the spreadsheet updates                                          | 8–10 (moderate)|

**Phase 5 Total:** 18 – 22 hrs | \$2,700 – \$3,300

---

### Phase 6: AI-Driven & Automation Features

| Task Category         | Description                                                                                              | Estimated Hours |
|-----------------------|----------------------------------------------------------------------------------------------------------|-----------------|
| Mapping Suggestions   | Codex/LLM–driven auto-suggestions for `MAPPED_STD_DESCRIPTION`                                           | 12–15 (complex) |
| Anomaly Detection     | Flag outlier codes or values that deviate from norms                                                     | 8–10 (moderate) |
| Scheduled Validations | Nightly/weekly automated validation runs with summary emails                                              | 6–8 (simple)    |

**Phase 6 Total:** 26 – 33 hrs | \$3,900 – \$4,950

---

### Phase 7: Performance & Scalability

| Task Category                   | Description                                                                                      | Estimated Hours |
|---------------------------------|--------------------------------------------------------------------------------------------------|-----------------|
| Asynchronous Processing         | Background job queue (e.g., Celery) for heavy loads                                              | 10–12 (complex) |
| Caching & Incremental Loads     | In-memory/Redis caching and delta-only re-parsing                                                 | 8–10 (moderate) |
| Dockerization & Deployment      | Dockerfile plus Helm/Terraform scripts for portable deployments                                   | 6–8 (simple)    |

**Phase 7 Total:** 24 – 30 hrs | \$3,600 – \$4,500

---

## Combined Estimate

| Scope                                     | Hours        | Cost                   |
|-------------------------------------------|--------------|------------------------|
| Phase 1: Core App                         | 56 – 81 hrs   | \$8,400 – \$12,150      |
| Phase 2: Git/SSO                          | 27 – 37 hrs   | \$4,050 – \$5,550       |
| Phase 3: Training                         | 11 – 17 hrs   | \$1,650 – \$2,550       |
| Phase 4: UI/Usability                     | 36 – 46 hrs   | \$5,400 – \$6,900       |
| Phase 5: Validation & Collaboration       | 18 – 22 hrs   | \$2,700 – \$3,300       |
| Phase 6: AI & Automation                  | 26 – 33 hrs   | \$3,900 – \$4,950       |
| Phase 7: Performance & Scalability        | 24 – 30 hrs   | \$3,600 – \$4,500       |
| **Total Estimate**                       | **198 – 266 hrs** | **\$30,600 – \$39,900** |

---

## Deliverables

- Codeset Management Platform with dynamic UI, Excel parsing, and export logic  
- Codex automation integration documentation and YAML runners  
- Git integration with Azure DevOps (ADO)  
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

Please review and confirm scope approval and pricing. Upon sign-off, Silhouette LLC will initiate development, beginning with a short discovery spike to validate complexity assumptions, and proceed in two-week sprints with regular demos.  
