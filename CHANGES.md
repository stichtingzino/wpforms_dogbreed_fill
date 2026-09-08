# Changelog - WPForms Dog Breed Generation Tool

All notable changes to the data-generation framework and architectural design are documented below, 
tracking the critical transition from the legacy AI/LLM-driven engine to the modern 
deterministic hybrid-pipeline.

---

## - 2026-09-07

### 🚨 Architectural Paradigm Shift (LLM Deprecation)
* **Removed AI Engine:** Completely deprecated and removed all AI infrastructure modules, including `llm_functions/`, `onepw/` integration, and requirements for external cloud platforms (Google Gemini API, Groq LPU Cluster, local Ollama nodes).
* **Reasoning:** AI large language models (LLMs) proved structurally unfit for authoritative cynological data generation. Even frontier-class models (Qwen-32B, Llama-4, Gemini Pro) introduced critical runtime blockades:
  1. **Linguistic Hallucinations:** AI treated breed mapping as translation, fabricating terms like *"Vlaamse Herdershond"* (for Belgian Shepherd) or *"Engelse Speen"* (for English Toy Terrier).
  2. **Syntax Instability:** Gekwantiseerde models (q5_K_M) failed to consistently maintain strict JSON array token counts during multi-batch attention pre-fills.
  3. **Cloud API Starvation:** Cloud endpoints frequently choked on high-speed data streams, triggering severe `429 Too Many Requests` (Quota Exhausted) and `503 Service Unavailable` failures.

### ✨ New Hybrid Deterministic Features
* **Isolated Repository Architecture:** Split the data generation framework into a dedicated standalone pipeline engine, decoupling python infrastructure completely from the core WordPress plugin.
* **Added Live Net-Scrape Track (`nl`):** Implemented an automated live web scraper that streams HTML directly from the official Dutch Kennel Club (*Raad van Beheer op Kynologisch Gebied*).
* **Authoritative Local Expansion:** The `nl` scrape track bypasses international FCI constraints to unlock exact local stamboek-registrations, expanding the database from 360 to **416 authentic breeds** (capturing all 9 Teckel variëteiten and specific native breeds like the *Markiesje*).
* **Added Static Repo Convert Track (`en`, `fr`, `de`):** Implemented a high-speed parser engine that downloads raw international stamboek CSV files from verified upstream repositories, mapping arrays instantly via Pandas.
* **Dynamic Metadata Scraping:** Erased all hardcoded local dictionaries and maps from `config.py`. The pipeline now live-scrapes active group schemas and translation matrices directly from `fci.be/nomenclature/` and `houdenvanhonden.nl` during runtime.

### 🐛 Bug Fixes & Code Refactoring
* **Fixed Typography Corruption:** Integrated `html.unescape()` across all stream processors to perfectly reconstruct complex native diacritics and tremas (e.g., *Aïdi*, *Briquet Griffon Vendéen*, *Alpenländische Dachsbracke*).
* **Fixed Column Layout Alignment:** Rewrote the Pandas groupby logic to dynamically scan headers instead of calling strict index positions, preventing empty objects `{}` on non-English columns (*groupe/gruppe*).
* **Fixed SSL Context Starvation:** Configured an explicit public `ssl.create_default_context()` bypass layer inside the network sockets to neutralize unexpected `SSL: CERTIFICATE_VERIFY_FAILED` blocks on remote servers.
* **Clean-Code Optimizations:**
  - Implemented an optimized, pythonic dictionary `.values()` iterator loops to dramatically lower visual noise during alphabetical sorting arrays.
  - Upgraded sorting lambda algorithms to use `.rsplit('_', maxsplit=1)[-1]` to securely isolate numerical group keys under all conditions.
  - Standardized all module namespaces to pass 100% clean, error-free checks under Pylint and Pylance.

---

## - Legacy AI Release

* **Initial LLM Release:** Deploys automated multi-batch loop frameworks parsing breed tables via asynchronous prompt completions.
* **Feature Set:** Managed credential resolution via 1Password CLI pipelines (`op://`) and generated cross-language files via few-shot context injections.
