# Project Proposal: Codeset Management System Development

**Client:** Health Catalyst  
**Prepared by:** Silhouette LLC  
**Date:** August 4, 2025  
**Engineer Rate:** $150/hour

---

## Project Summary

Silhouette LLC will develop a modular, Excel-driven Codeset Automation App. The application allows healthcare clients to upload custom Excel mapping sheets, dynamically render UI based on tab structure, preserve formulas, support dropdown selection, and export modified files.

The system is built on Python using Streamlit and Flask, with structured logic components and documentation to support Codex-driven automation.

Additionally, Phase 2 of the project introduces Git integration, automated ticketing, and secure Single Sign-On (SSO) authentication for clients interacting with the hosted codeset repository.

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

## Combined Estimate

| Scope | Hours | Cost |
|-------|--------|------|
| Phase 1: Core App | 56–81 hrs | $8,400 – $12,150 |
| Phase 2: Git/SSO | 27–37 hrs | $4,050 – $5,550 |
| **Total Estimate** | **83–118 hrs** | **$12,450 – $17,700** |

---

## Deliverables

- Codeset Automation App with dynamic UI, Excel parsing, and formula-safe export
- Codex integration documentation and task automation structure
- Git repo integration with folder-level structure per submission
- Automatic ticket creation in Azure Boards
- SSO authentication and access control
- Metadata logging of all submissions and Git commits

---

## Assumptions

- Repo and Boards access will be coordinated with client IT/DevOps.
- SSO integration will be based on Azure AD or OAuth2 unless otherwise specified.
- Ticket creation rules are predefined (e.g., based on repo path, client name).
- Phase 2 may be delivered after Phase 1 unless bundled into a unified milestone.

---

## Next Steps

To move forward, please confirm approval of the scope and pricing range. Upon sign-off, Silhouette LLC will begin development, staging setup, and delivery milestones.
