# Performance Review Tracker - System Architecture

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PERFORMANCE REVIEW TRACKER                            │
│                                                                                 │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────────┐ │
│  │   DATA SOURCES  │    │   PROCESSING     │    │        OUTPUT               │ │
│  │                 │    │    PIPELINE      │    │                             │ │
│  │ ┌─────────────┐ │    │                  │    │ ┌─────────────────────────┐ │ │
│  │ │ Azure DevOps│◄┼────┤ 1. Data Loading  │    │ │    Annual Review        │ │ │
│  │ │   (ADO API) │ │    │ 2. Normalization │    │ │    - Communication      │ │ │
│  │ └─────────────┘ │    │ 3. Validation    │    │ │    - Flexibility        │ │ │
│  │       OR        │    │ 4. Date Filtering│    │ │    - Initiative         │ │ │
│  │ ┌─────────────┐ │    │ 5. Analysis      │    │ │    - Member Service     │ │ │
│  │ │  CSV Files  │◄┼────┤ 6. Report Gen    │    │ │    - Personal Cred.     │ │ │
│  │ └─────────────┘ │    │                  │    │ │    - Quality/Quantity   │ │ │
│  │       OR        │    │                  │    │ │    - Teamwork           │ │ │
│  │ ┌─────────────┐ │    │                  │    │ └─────────────────────────┘ │ │
│  │ │   Hybrid    │◄┼────┤                  │    │           OR                │ │
│  │ │ (ADO→CSV)   │ │    │                  │    │ ┌─────────────────────────┐ │ │
│  │ └─────────────┘ │    │                  │    │ │  Competency Assessment  │ │ │
│  └─────────────────┘    │                  │    │ │  - Programming/SoftDev  │ │ │
│                         │                  │    │ │  - Solution Architecture│ │ │
│                         │                  │    │ │  - Systems Design       │ │ │
│                         │                  │    │ │  - Project Management   │ │ │
│                         │                  │    │ │  - Requirements Def     │ │ │
│                         │                  │    │ │  - Testing              │ │ │
│                         │                  │    │ │  - Problem Management   │ │ │
│                         │                  │    │ │  - Innovation           │ │ │
│                         │                  │    │ │  - Release/Deployment   │ │ │
│                         │                  │    │ │  - Accountability       │ │ │
│                         │                  │    │ │  - Influence            │ │ │
│                         │                  │    │ │  - Agility              │ │ │
│                         │                  │    │ │  - Inclusion            │ │ │
│                         │                  │    │ └─────────────────────────┘ │ │
│                         └──────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Processing Pipeline

```
DATA INPUT FLOW:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Source    │    │    Raw      │    │ Processed   │
│ Selection   │───▶│    Data     │───▶│    Data     │
│ (ADO/CSV)   │    │ (43 items)  │    │   (JSON)    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                   │
                          ▼                   ▼
                  ┌─────────────┐    ┌─────────────┐
                  │    Data     │    │   Filter    │
                  │Normalization│    │ by Date     │
                  │& Validation │    │   Range     │
                  └─────────────┘    └─────────────┘

ANALYSIS FLOW:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Processed   │    │    AI       │    │   Manual    │    │   Final     │
│    Data     │───▶│  Analysis   │───▶│ Fallback    │───▶│   Report    │
│   (JSON)    │    │ (Roo Code)  │    │ Analysis    │    │ (Markdown)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                   ▲
                          ▼                   │
                  ┌─────────────┐             │
                  │   Empty?    │─────────────┘
                  │ Auto-detect │ (If empty/failed)
                  └─────────────┘
```

## Core Components Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 src/                                            │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │    main.py      │  │competency_      │  │   validation.py │  │config_      │ │
│  │                 │  │formatter.py     │  │                 │  │validation.py│ │
│  │ • Entry Point   │  │                 │  │ • Data          │  │             │ │
│  │ • Orchestration │  │ • Report        │  │   Validation    │  │ • Config    │ │
│  │ • CLI Interface │  │   Templates     │  │ • Criteria      │  │   Testing   │ │
│  │ • Config Mgmt   │  │ • Formatting    │  │   Loading       │  │ • ADO       │ │
│  │ • Data Flow     │  │ • Export        │  │ • Structure     │  │   Connection│ │
│  │                 │  │   (MD/DOCX)     │  │   Checks        │  │   Validation│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│                                                                                 │
│  ┌─────────────────┐                      ┌─────────────────┐                  │
│  │competency_      │                      │                 │                  │
│  │keywords.py      │                      │ (other modules) │                  │
│  │                 │                      │                 │                  │
│  │ • Keyword       │                      │                 │                  │
│  │   Mapping       │                      │                 │                  │
│  │ • Competency    │                      │                 │                  │
│  │   Classification│                      │                 │                  │
│  └─────────────────┘                      └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL FILES                                    │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   config.json   │  │   criteria/     │  │   templates/    │  │    data/    │ │
│  │                 │  │                 │  │                 │  │             │ │
│  │ • ADO Settings  │  │ • annual_review │  │ • MD Templates  │  │ • CSV Files │ │
│  │ • API Keys      │  │   _criteria.json│  │ • Report        │  │ • JSON Data │ │
│  │ • Output Dirs   │  │ • competency_   │  │   Layouts       │  │ • Backups   │ │
│  │ • LLM Config    │  │   assessment_   │  │                 │  │ • Processed │ │
│  │                 │  │   criteria.json │  │                 │  │   Results   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Processing Flow Detail

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DUAL ANALYSIS SYSTEM                                 │
│                                                                                 │
│  INPUT: 43 Work Items from Azure DevOps                                        │
│     │                                                                           │
│     ▼                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      DATA PROCESSING PIPELINE                           │   │
│  │                                                                         │   │
│  │  1. load_data_from_ado() ──── ADO API Queries ──── 43 items           │   │
│  │                   │                                                     │   │
│  │  2. normalize_data_structure() ──── Add missing columns ──── Standard   │   │
│  │                   │                                          Format     │   │
│  │  3. validate_data() ──── Check structure/content ──── Validated        │   │
│  │                   │                                                     │   │
│  │  4. filter_by_date_range() ──── Sept 2024 - Aug 2025 ──── Filtered     │   │
│  │                   │                                                     │   │
│  │  5. Save processed_annual.json ──── 43 items ready for analysis        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                           │
│                                   ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      DUAL ANALYSIS ENGINE                              │   │
│  │                                                                         │   │
│  │  ┌─────────────────────────┐         ┌─────────────────────────────────┐ │   │
│  │  │      AI ANALYSIS        │  FAIL   │       MANUAL ANALYSIS           │ │   │
│  │  │                         │ ──────▶ │                                 │ │   │
│  │  │ • Roo Code Integration  │ EMPTY   │ • Python-based analysis        │ │   │
│  │  │ • VS Code CLI Commands  │         │ • Statistical analysis         │ │   │
│  │  │ • Natural Language      │         │ • Keyword classification       │ │   │
│  │  │   Processing            │         │ • Impact assessment            │ │   │
│  │  │                         │         │ • Template-driven reports      │ │   │
│  │  │ Result: Empty (!)       │         │                                 │ │   │
│  │  └─────────────────────────┘         │ Result: Complete Analysis ✓     │ │   │
│  │                                      └─────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                   │                                           │
│                                   ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      REPORT GENERATION                                  │   │
│  │                                                                         │   │
│  │  Template Selection ──── Annual Review Template                         │   │
│  │           │                                                             │   │
│  │  Content Integration ──── Manual Analysis + Template                    │   │
│  │           │                                                             │   │
│  │  Format Application ──── Professional Markdown Report                   │   │
│  │           │                                                             │   │
│  │  Final Output ──── output/annual_review_YYYYMMDD_HHMMSS.md             │   │
│  │                                                                         │   │
│  │  RESULT: Complete annual review with 43 accomplishments analyzed ✓      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Decision Tree: Analysis Method Selection

```
Start: User runs annual review
        │
        ▼
┌───────────────────┐
│ Load 43 ADO Items │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Try AI Analysis   │
│ (Roo Code)        │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐     YES    ┌─────────────────────┐
│ Analysis Empty?   │ ─────────▶ │ Auto-Generate       │
│ (0 bytes)         │            │ Manual Analysis     │
└─────────┬─────────┘            └─────────┬───────────┘
          │ NO                            │
          ▼                               │
┌───────────────────┐                     │
│ Use AI Analysis   │ ◄───────────────────┘
│ (Successful)      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Generate Final    │
│ Professional      │
│ Report            │
└───────────────────┘
```

## File System Layout

```
performance-review-tracker/
├── src/
│   ├── main.py                      # 🎯 Entry point & orchestration
│   ├── competency_formatter.py      # 📝 Report templates & formatting  
│   ├── competency_keywords.py       # 🔤 Keyword mapping system
│   ├── validation.py                # ✅ Data validation & criteria loading
│   └── config_validation.py         # ⚙️ Configuration management
├── criteria/
│   ├── annual_review_criteria.json  # 📋 7 workplace performance areas
│   └── competency_assessment_criteria.json # 🎯 13 technical competency areas
├── templates/
│   └── annual_review_template.md    # 📄 Markdown report template
├── data/
│   ├── processed_annual.json        # 📊 43 processed work items
│   ├── analyzed_annual.md           # 🤖 Analysis results (AI/Manual)
│   └── ado_backup_*.csv             # 💾 ADO data backups
├── output/
│   └── annual_review_*.md           # 📈 Final professional reports
├── config.json                     # ⚙️ ADO & system configuration
└── scripts/
    └── run_assessment.sh            # 🚀 Quick execution scripts
```

## System Reliability Features

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            BULLETPROOF DESIGN                                  │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      REDUNDANCY LAYERS                                  │   │
│  │                                                                         │   │
│  │  Data Sources: ADO API ──── CSV Files ──── Hybrid Mode                 │   │
│  │                  │             │             │                         │   │
│  │  Analysis:    AI Analysis ──── Manual Fallback (AUTO-DETECT)           │   │
│  │                  │             │                                       │   │
│  │  Output:      Markdown ──── DOCX ──── JSON                             │   │
│  │                                                                         │   │
│  │  Validation:  ✅ Config validation                                      │   │
│  │               ✅ Data structure checks                                  │   │
│  │               ✅ Connection testing                                     │   │
│  │               ✅ Error handling & recovery                              │   │
│  │               ✅ Automatic data backup                                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

This diagram shows how your Performance Review Tracker is architected as a robust, multi-layered system with automatic failover capabilities, ensuring it always produces professional results from your 43 Azure DevOps work items! 🚀