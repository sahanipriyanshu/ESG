# Architectural Decisions Record (ADR)

## 1. Django & DRF for Backend
**Decision**: Use Django with Django REST Framework (DRF) instead of FastAPI or Node.js.
**Rationale**: Django provides a robust ORM, built-in migration management, and excellent administrative scaffolding. For a data ingestion platform where schema enforcement, database transactions, and relational integrity are paramount, Django significantly accelerates development while maintaining enterprise quality.

## 2. Explicit Service Layer over Django Signals
**Decision**: Handle business logic (like approving/rejecting records and writing audit logs) in explicit `Service` classes rather than using Django `post_save` signals.
**Rationale**: 
- Signals hide side-effects, making workflows harder to debug.
- Explicit service calls (e.g., `RecordWorkflowService.approve_record`) make the code interview-defensible, self-documenting, and easier to unit test.
- We have fine-grained control over exactly what `actor` is passed into the `AuditLog`.

## 3. Separation of Raw vs. Normalized Records
**Decision**: Store every incoming payload twice: once as an immutable `RawRecord` (JSON) and once as a `NormalizedRecord` (relational columns).
**Rationale**: ESG data is heavily scrutinized. If an auditor asks "Where did this 5,000 kg CO2e number come from?", we can trace the `NormalizedRecord` back to the exact `RawRecord` payload received from SAP, proving data lineage.

## 4. GenericForeignKey for Audit Logging
**Decision**: Use Django's `GenericForeignKey` for the `AuditLog` model.
**Rationale**: Instead of creating `NormalizedRecordAuditLog` and `DataSourceAuditLog` tables, a generic log allows us to build a unified timeline view of all actions happening within the system, easily querying by `object_id`.

## 5. React & Tailwind for Frontend
**Decision**: Use a Vite-based React SPA styled with Tailwind CSS.
**Rationale**: Tailwind allows for rapid, bespoke UI development without fighting component libraries. The "glassmorphic" and modern aesthetic required for this prototype is much easier to achieve with Tailwind utility classes.
