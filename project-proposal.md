# Project Proposal: Codeset Management System Development

**Client:** Health Catalyst  
**Prepared by:** Silhouette LLC  
**Date:** August 4, 2025  
**Engineer Rate:** $150/hour

---

## Project Summary

Silhouette LLC will develop a modular, Excel-driven Codeset Management Platform. The application enables healthcare clients to upload and manage custom codesets, dynamically render tab-specific UI logic, preserve formulas, and export validated files. Built with Streamlit and Flask, the system is designed for long-term maintainability and integration with vendor workflows.

Phase 2 of the project includes shared Git repository integration via Azure DevOps (ADO), automatic ticket creation in Azure Boards, secure Single Sign-On (SSO) authentication, and full audit tracking. The proposal also includes structured client-side training to ensure smooth onboarding and adoption.

---

## Scope of Work

### Phase 1: Application Core

| Task Category | Description | Estimated Hours |
|---------------|-------------|-----------------|
| UI & Interaction Design | Streamlit interface for upload, tab rendering, and navigation across custom sheet structures. | 12–15 |
| Excel Parsing & Dynamic Handling | Per-tab logic with formula preservation and validation. | 8–12 |
| Dropdowns, Mappings & Logic | Render dropdowns for mappings (e.g., `STANDARD_DESCRIPTION`, `MAPPED_STD_DESCRIPTION`). | 6–8 |
| Excel Export Functionality | Export modified workbooks while retaining formulas and structure. | 6–10 |
| Flask Backend (Optional) | Auxiliary endpoints for file export or API actions. | 6–8 |
| Modular Components | Encapsulated logic for parsing, tab control, dropdowns, and formulas. | 8–12 |
| Testing & QA | Unit and integration testing of UI, exports, and file logic. | 6–10 |
| Codex Documentation & Handoff | Update markdown handoff and YAML task runners. | 4–6 |

**Estimated Time (Phase 1):** 56–81 hours  
**Estimated Cost (Phase 1):** $8,400 – $12,150

---

### Phase 2: Git Integration, Ticketing & SSO

| Task Category | Description | Estimated Hours |
|---------------|-------------|-----------------|
| ADO Git Integration | Configure shared Git repo structure and programmatic commit logic per submission. | 6–8 |
| Azure Boards Ticket Trigger | Automatically create work items in ADO Boards based on submission metadata. | 5–7 |
| SSO Authentication | Enforce client-authenticated access using Azure AD or compatible SSO protocol. | 8–10 |
| Repo & User Access Setup | ADO access and auth testing for client/vendor use. | 4–6 |
| Audit Logging | Track submitter identity, repo updates, and commit metadata. | 4–6 |

**Estimated Time (Phase 2):** 27–37 hours  
**Estimated Cost (Phase 2):** $4,050 – $5,550

---

### Phase 3: Client Training & Enablement

| Task Category | Description | Estimated Hours |
|---------------|-------------|-----------------|
| Live Training Sessions | Host live 60–90 minute virtual training sessions for client users and admins. | 3–5 |
| Training Materials | Develop quick-start guide, annotated screenshots, and workflows. | 4–6 |
| Recording & Playback Support | Provide recorded walkthroughs or screen captures for internal reuse. | 2–3 |
| Q&A / Follow-up Support | Address follow-up questions and issues post-rollout. | 2–3 |

**Estimated Time (Phase 3):** 11–17 hours  
**Estimated Cost (Phase 3):** $1,650 – $2,550

---

## Combined Estimate

| Scope | Hours | Cost |
|-------|--------|------|
| Phase 1: Core App | 56–81 hrs | $8,400 – $12,150 |
| Phase 2: Git/SSO | 27–37 hrs | $4,050 – $5,550 |
| Phase 3: Training | 11–17 hrs | $1,650 – $2,550 |
| **Total Estimate** | **94–135 hrs** | **$14,100 – $20,250** |

---

## Deliverables

- Codeset Management Platform with dynamic UI, Excel parsing, and export logic
- Codex automation integration documentation and YAML runners
- Git integration with Azure DevOps (vendor-hosted repo)
- Automated work item creation in Azure Boards
- SSO authentication and metadata tracking
- Client onboarding training sessions and support materials

---

## Assumptions

- Client IT will coordinate on SSO and Azure DevOps access.
- Training is virtual unless otherwise agreed upon.
- Codex automation framework is already in place; this tool will conform to existing structure.

---

## Next Steps

To proceed, please confirm scope approval and pricing agreement. Upon sign-off, Silhouette LLC will initiate development and schedule client training sessions in parallel with final rollout.
