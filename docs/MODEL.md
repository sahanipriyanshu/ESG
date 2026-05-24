# ESG Data Platform: Domain Model

This document outlines the core domain models used in the ESG Ingestion Prototype. The architecture is designed for multi-tenancy, immutable auditability, and clear separation between raw incoming data and canonical normalized data.

## Entity Relationship Diagram

```mermaid
erDiagram
    ORGANIZATION ||--o{ DATASOURCE : "has many"
    ORGANIZATION ||--o{ NORMALIZEDRECORD : "has many"
    DATASOURCE ||--o{ RAWRECORD : "produces"
    RAWRECORD ||--|| NORMALIZEDRECORD : "is standardized into"
    
    %% Audit logging via GenericForeignKey
    NORMALIZEDRECORD ||--o{ AUDITLOG : "tracked by"
    RAWRECORD ||--o{ AUDITLOG : "tracked by"

    ORGANIZATION {
        UUID id PK
        string name
        datetime created_at
    }

    DATASOURCE {
        UUID id PK
        UUID organization_id FK
        string source_type "sap, utility, travel"
        string ingestion_mode "batch, api"
        file original_file
        datetime uploaded_at
    }

    RAWRECORD {
        UUID id PK
        UUID data_source_id FK
        json raw_payload "Immutable exact source data"
        string ingestion_status "pending, processed, failed"
        string error_message
    }

    NORMALIZEDRECORD {
        UUID id PK
        UUID organization_id FK
        UUID raw_record_id FK "OneToOne"
        string category
        int scope "1, 2, or 3"
        date activity_date
        decimal quantity
        string normalized_unit
        decimal estimated_emissions "kg CO2e"
        string status "pending_review, approved, rejected"
        string suspicious_reason
        boolean locked_for_audit
    }

    AUDITLOG {
        UUID id PK
        UUID object_id "Generic FK ID"
        string content_type "Generic FK Model Type"
        string action "create, update, lock, approve"
        json previous_values
        json new_values
        string actor
        datetime timestamp
    }
```

## Model Descriptions

1. **Organization**: Represents the tenant. All data is scoped to an organization to support SaaS models.
2. **DataSource**: A single ingestion event. If an analyst uploads a CSV with 10,000 rows, there is 1 DataSource.
3. **RawRecord**: The exact, unmodified JSON representation of a single row/payload from the source system. This is crucial for auditability. If normalization logic changes, we can replay from the `RawRecord` without needing the original file.
4. **NormalizedRecord**: The canonical ESG ledger entry. This contains standardized units, categorized scopes, and estimated emissions. It undergoes the analyst review workflow.
5. **AuditLog**: Uses Django's `GenericForeignKey` to attach immutable state change logs to any record in the system, detailing *who* did *what*, *when*, and *how* the state mutated.
