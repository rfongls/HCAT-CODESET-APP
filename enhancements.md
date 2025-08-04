# Codeset Automation App: Phased Feature Roadmap

*All features will continue to read from spreadsheets hosted in the Azure DevOps (ADO) repository.*

## Phase 1: UI & Usability Enhancements

1. **Row Filtering & Search**

   * Add a text‑search bar and/or filter controls to quickly zero in on unmapped rows or specific code ranges.
2. **Pagination & Virtual Scrolling**

   * Implement paging or lazy‑loading for very large sheets to keep the UI responsive.
3. **Undo/Redo Stack**

   * Maintain a history of user actions so mappings or edits can be reverted without full workbook reload.
4. **Dark Mode / Theme Selector**

   * Offer a light/dark toggle and allow custom branding (colors, logo) via a config file.
5. **Inline Help & Tooltips**

   * Embed contextual “?” icons that explain each column, validation rules, and best practices.

## Phase 2: Validation & Data Profiling + Collaboration & Version Control

1. **Schema Comparison Reports**

   * Auto‑generate printable PDF or HTML reports summarizing differences between two or more repo workbooks.
2. **GitHub/GitLab (ADO) Integration**

   * Connect directly to the ADO repo.
   * Create alerts when the hosted spreadsheet is updated, triggering an automatic ticket or workflow to review and update the codeset.

## Phase 3: AI‑Driven & Automation Features

1. **Mapping Suggestions**

   * Leverage the Codex agent (or another LLM) to auto-suggest `MAPPED_STD_DESCRIPTION` based on similar entries.
2. **Anomaly Detection**

   * Flag outlier codes or display values that deviate from established patterns (e.g., typos, unexpected formats).
3. **Scheduled Validations**

   * Enable users to schedule nightly or weekly runs that automatically validate the repo and email summary reports.

## Phase 4: Performance & Scalability

1. **Asynchronous Processing**

   * Offload heavy workbook loads and exports to background jobs (e.g., Celery) so the UI remains snappy.
2. **Caching & Incremental Loads**

   * Cache parsed workbook data (in memory or Redis) and only re‑parse sheets when the underlying file changes.
3. **Dockerization & Deployment Scripts**

   * Provide a `Dockerfile` and Helm/Terraform scripts so teams can deploy the app in any environment easily.

---

*Use this roadmap as a reference for CODEX to sequentially build and integrate features into the Codeset Automation App.*
