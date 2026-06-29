"""# 📈 Financial Intent & Entity Resolution System

An intelligent, hybrid agentic stock research assistant that delivers low-cost, highly deterministic analysis. This application uses a rule-based deterministic tool pipeline for data fetching and limits Large Language Model (LLM) calls strictly to complex reasoning sub-tasks (unstructured entity resolution and multi-source synthesis).

**Author:** Karthik

---

## 🚀 Core Philosophy & Architectural Edge

Standard agentic workflows often suffer from non-deterministic execution loops, high token consumption, and cascading API costs due to conversational loops. This platform completely mitigates those drawbacks by separating **Data Routing/Fetching** from **Semantic Reasoning**:

* **LLM for Reasoning Only:** LLMs are reserved for unstructured entity extraction when rule-based fuzzy routing falls below a confidence threshold, and for generating final structured summaries from raw facts.
* **Reduced Operational Cost:** Minimizes recurring vendor token charges by avoiding frequent text generation calls during routine data acquisition.
* **Deterministic Pipeline Execution:** Utilizes strict rule/schema validation logic for tool states (`price`, `news`, `financials`) and transparent fallback paths when primary endpoints encounter network constraints.
* **Fuzzy-to-LLM Entity Laddering:** Translates informal user input into valid exchange tickers using local memory maps, elevating queries to LLM processing only when local resolution fails.

---

## 🗺️ System Architecture & Execution Flow

The system orchestrates operations via a linear sequence controlled by an execution controller. Below is the step-by-step query lifecycle:

Code output
File written successfully.

```text
       [ User Stock Query via Streamlit UI ]
                        │
                        ▼
         [ 1. Entity & Intent Extraction ]
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 [ Local Fuzzy Match ]          [ Fallback LLM Call ]
 (COMPANY_DB / Alias Map)       (If confidence < 80%)
        └───────────────┬───────────────┘
                        ▼
         [ 2. Planning & Requirements ]
          (Determines needed variables)
                        │
                        ▼
         [ 3. Dynamic Tool Execution ] 
          (Checks Memory/Cache First)
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 [ Primary APIs Execution ]    [ Fallback API Routing ]
  (Finnhub / NewsAPI)           (AlphaVantage / Backup)
        └───────────────┬───────────────┘
                        ▼
         [ 4. Tool State Validation ]
          (Validates structures & fields)
                        │
                        ▼
        [ 5. LLM Synthesis & Output ]
         (Generates tailored summary)

### Folder structure

├── app/
│   ├── emit_event.py                # System-wide reactive event broadcast pipeline
│   └── ui.py                        # Streamlit visual layer & component renderers
├── config/
│   ├── logger.py                    # Structured diagnostic event logging engine
│   ├── settings.py                  # Environment config, tokens, and credential management
│   └── validate_config.py           # Pre-boot integrity verification for API parameters
├── core/
│   ├── choose_execution_path.py     # Success-rate heuristics for routing execution paths
│   ├── dynamic_tool_execution.py    # Main lifecycle router for data harvesting workflows
│   ├── execute_with_retries.py      # Exponential retry scheduler wrapper
│   ├── execute_tools.py             # Target requirement tool executor orchestration
│   ├── generate_output.py           # Formats internal raw data into structural user insights
│   ├── output_validation.py         # Concrete interface validation constraint mapping
│   ├── plan_tools.py                # Strategy mapping matrix matching rules to intents
│   ├── retry_tool.py                # Safe re-execution logic loop runner
│   └── validate_state.py            # Diagnostic post-execution health inspector
├── models/
│   ├── extract_intent_entity.py     # Aggregated intent mapping front-controller
│   ├── get_requirements.py          # Formulates concrete tool lists based on parsed metadata
│   └── normalize.py                 # String text sanitation and casing standardization
├── storage/
│   ├── promotion_to_alias.py        # Automated loop mapping query tokens to local aliases
│   ├── prompt_map.py                # Centralized context-free semantic prompt templates
│   ├── read_memory.py               # Serialized localized cache loading layer
│   ├── read_tool_stats.py           # Historic performance metadata ingestion reader
│   ├── user_token_log.py            # Performance metric logger tracking resolution scores
│   ├── write_memory.py              # Local JSON document serialization writer
│   └── write_tool_stats.py          # Atomic tool operational performance stat counters
├── tools/
│   ├── api_call.py                  # Low-level corporate network query layer
│   ├── compute_confidence.py        # Validates source metric calculation boundaries
│   ├── compute_metric.py            # Evaluates structural corporate health ratios
│   ├── fallback_compute_metric.py   # Alternative flat balance-sheet evaluation runner
│   ├── fallback_financials.py       # Failover route accessing balance-sheet parameters
│   ├── fallback_news.py             # Failover backup route accessing chronological headlines
│   ├── fallback_price.py            # Failover backup route for tracking stock closing markers
│   ├── fallback_resolve_metric.py   # Hardcoded exact string terminology maps
│   ├── financial_report.py          # Primary historical structural report tracker
│   ├── llmcall.py                   # Low-level Google GenAI client driver integration
│   ├── news_tool.py                 # Primary news title index aggregator
│   ├── price_tool.py                # Primary asset price quote fetcher
│   └── resolve_metric.py            # Multi-tier exact/fuzzy confidence keyword mapper
├── main.py                          # Application bootstrappers & stream orchestration loop
├── alias_map.json                   # Dynamically promoted company-to-ticker maps
├── memory.json                      # Local file persistence database cache layer
└── tool_stats.json                  # Real-time success and error tracking log maps