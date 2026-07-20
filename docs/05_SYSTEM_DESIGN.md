# System Design

## Purpose

This document describes the high-level design of the AI Data Profiling Platform. It explains how users interact with the system and how the application processes a dataset to generate a data quality report.

---

# User Workflow

```mermaid
flowchart TD
    A[Open Website] --> B[Upload CSV]
    B --> C[Click Analyze]
    C --> D[Wait for Processing]
    D --> E[View Data Quality Report]
```

---

# System Workflow

```mermaid
flowchart TD
    A[User Uploads CSV]
    A --> B[Frontend validates file]
    B --> C[Send HTTP Request]
    C --> D[Backend API]
    D --> E[Validate CSV]
    E --> F[Profiling Engine]
    F --> G[Generate Quality Report]
    G --> H[Return JSON Response]
    H --> I[Frontend displays report]
```

---

# High-Level Architecture

```mermaid
flowchart LR
    User --> Frontend
    Frontend -->|HTTP Request| Backend
    Backend --> ProfilingEngine
    ProfilingEngine --> ReportGenerator
    ReportGenerator --> Backend
    Backend -->|JSON Response| Frontend
```

---

# Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| Frontend | User interface, file upload, display report |
| Backend API | Receive requests, validate input, coordinate processing |
| Profiling Engine | Analyze dataset quality |
| Report Generator | Prepare profiling results for the frontend |

---

# Data Flow

```mermaid
flowchart LR
    CSV --> Backend
    Backend --> DataFrame
    DataFrame --> Profiling
    Profiling --> Report
    Report --> JSON
    JSON --> Frontend
```

---

# Version 1 Scope

- CSV upload
- Data quality profiling
- Quality report generation
- No authentication
- No database
- No automated data cleaning