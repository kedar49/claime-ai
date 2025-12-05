# 🤖 Claime AI - Detailed Agent Explanation

## Overview

Claime AI uses a **multi-agent architecture** with 4 specialized AI agents working together to verify claims. Each agent has a specific role and uses **LangGraph** for orchestration.

---

## 🔍 Agent 1: The Fact Checker

### Purpose
Verifies claims by searching authoritative sources and analyzing evidence.

### Architecture (3-Node LangGraph)

```
┌─────────────┐
│ Strategist  │ → Generates search queries
└──────┬──────┘
       ↓
┌─────────────┐
│  Executor   │ → Fetches search results (ASYNC PARALLEL)
└──────┬──────┘
       ↓
┌─────────────┐
│   Analyst   │ → Evaluates evidence sufficiency
└──────┬──────┘
       ↓
   Decision: Sufficient? → Output OR Refine (max 2 iterations)
```

### How It Works

#### 1. **Strategist Node**
**Input:** User's claim  
**Process:**
- Uses Gemini AI to generate 3 targeted search queries
- Focuses on:
  - Official sources (government, company press releases)
  - Major news outlets (Reuters, Bloomberg, AP, BBC)
  - Historical data cross-referencing

**Example:**
```
Claim: "Tesla is acquiring Twitter for $100 billion"

Generated Queries:
1. "Tesla Twitter acquisition official announcement"
2. "Elon Musk Twitter deal 100 billion"
3. "Tesla SEC filing Twitter acquisition"
```

**Output:** List of 3 search queries

---

#### 2. **Executor Node**
**Input:** Search queries from Strategist  
**Process:**
- **Async Parallel Execution**: All 3 queries run simultaneously (not sequential!)
- Uses **Tavily Search API** for real-time web search
- **In-memory caching**: Duplicate queries return cached results instantly
- Fetches 4 results per query (optimized for speed)

**Optimizations:**
```python
# Parallel execution
async def _parallel_tavily_search(queries):
    # All queries execute at once
    results = await asyncio.gather(
        search_query_1(),
        search_query_2(),
        search_query_3()
    )
```

**Example Result:**
```json
{
  "query": "Tesla Twitter acquisition",
  "results": [
    {
      "title": "No Evidence of Tesla-Twitter Deal",
      "url": "https://reuters.com/...",
      "content": "No official announcement found...",
      "score": 0.92
    }
  ]
}
```

**Output:** List of search results with sources

---

#### 3. **Analyst Node**
**Input:** Search results from Executor  
**Process:**
- Analyzes all search results using Gemini AI
- Evaluates:
  - **Evidence Quality**: SUFFICIENT or INSUFFICIENT
  - **Source Credibility**: Official vs. unreliable
  - **Consistency**: Do sources agree?

**Decision Logic:**
```
If evidence is SUFFICIENT:
  → Preliminary Verdict: VERIFIED, DEBUNKED, or UNVERIFIED
  → Output final result

If evidence is INSUFFICIENT and iterations < 2:
  → Go back to Strategist (refine queries)
  → Try again with more specific searches

If iterations >= 2:
  → Output with UNVERIFIED verdict
```

**Example Output:**
```json
{
  "preliminary_verdict": "DEBUNKED",
  "evidence_sufficient": true,
  "iterations": 1,
  "analysis": "No credible sources confirm this claim..."
}
```

---

### Key Features

✅ **Async Parallel Search**: 3x faster than sequential  
✅ **Smart Caching**: Duplicate queries return instantly  
✅ **Iterative Refinement**: Tries up to 2 times if evidence is weak  
✅ **Source Scoring**: Prioritizes authoritative sources  

---

## 🕵️ Agent 2: The Forensic Expert

### Purpose
Analyzes text for manipulation, AI generation, and fraud indicators.

### Architecture (3-Node LangGraph)

```
┌─────────────┐
│  Profiler   │ → Linguistic analysis
└──────┬──────┘
       ↓
┌─────────────┐
│  Detector   │ → AI/bot patterns
└──────┬──────┘
       ↓
┌─────────────┐
│   Auditor   │ → Calculates integrity score
└──────┬──────┘
       ↓
   Final Score (0.0 - 1.0)
```

### How It Works

#### 1. **Profiler Node**
**Input:** Raw claim text  
**Process:**
- **Urgency Analysis**: Counts panic words ("URGENT!", "ACT NOW!")
- **Grammar Quality**: Checks for typos, poor writing
- **Tone Detection**: Professional vs. sensationalist
- **Credibility Markers**: Looks for trust signals

**Metrics Calculated:**
```python
{
  "urgency_level": 0-10,        # How much pressure?
  "grammar_quality": 0-10,      # Writing quality
  "tone_type": "professional" | "sensationalist" | "threatening",
  "credibility_markers": "high" | "medium" | "low",
  "exclamations": 5,            # Count of "!"
  "caps_ratio": 0.15            # % of CAPS
}
```

**Example:**
```
Text: "URGENT!!! Amazon is BANKRUPT! CLICK HERE NOW!!!"

Analysis:
- urgency_level: 10 (extreme)
- grammar_quality: 3 (poor)
- tone_type: "threatening"
- exclamations: 3
- caps_ratio: 0.35 (35% caps)
```

**Output:** Linguistic analysis dict

---

#### 2. **Detector Node**
**Input:** Raw claim text  
**Process:**
- **AI Detection**: Analyzes if text was AI-generated
- **Bot Patterns**: Looks for template/spam patterns
- **Manipulation Tactics**: Identifies fear, urgency, false authority
- **Scam Indicators**: Common fraud red flags

**Detection Methods:**
```python
{
  "ai_probability": 0.0-1.0,    # Likelihood of AI generation
  "bot_patterns": "none" | "template" | "spam",
  "manipulation_tactics": [
    "fear_mongering",
    "false_urgency",
    "fake_authority"
  ],
  "scam_indicators": [
    "click_bait",
    "financial_threat",
    "urgent_action"
  ]
}
```

**Example:**
```
Text: "Your account will be closed in 24 hours! Click here to verify!"

Detection:
- ai_probability: 0.3
- bot_patterns: "template"
- manipulation_tactics: ["fear", "urgency", "false_authority"]
- scam_indicators: ["phishing", "urgent_action"]
```

**Output:** Detection analysis dict

---

#### 3. **Auditor Node**
**Input:** Profiler + Detector results  
**Process:**
- **Penalty System**: Applies weighted penalties for red flags
- **Score Calculation**: Starts at 1.0, subtracts penalties
- **Verdict Generation**: Based on final score

**Penalty System:**
```
Starting Score: 1.0

Penalties Applied:
- Extreme Urgency (8-10):     -0.25
- Poor Grammar (0-3):          -0.30
- Threatening Tone:            -0.20
- Low Credibility:             -0.15
- High AI Probability (>0.7):  -0.25
- Spam Bot Patterns:           -0.20
- Multiple Manipulation (3+):  -0.30
- Multiple Scam Indicators:    -0.35

Final Score = 1.0 - (sum of penalties)
```

**Verdict Mapping:**
```
Score >= 0.85: "HIGH INTEGRITY"
Score >= 0.70: "LIKELY LEGITIMATE"
Score >= 0.50: "SUSPICIOUS"
Score >= 0.30: "LIKELY FRAUDULENT"
Score <  0.30: "CONFIRMED SCAM"
```

**Example:**
```
Penalties Applied:
- Extreme Urgency: -0.25
- Poor Grammar: -0.30
- Threatening Tone: -0.20
- Multiple Scam Indicators: -0.35

Final Score: 1.0 - 1.10 = 0.0 (capped at 0.0)
Verdict: "CONFIRMED SCAM"
```

**Output:** Forensic log with integrity score

---

### Key Features

✅ **Multi-layered Analysis**: Linguistic + AI + Manipulation  
✅ **Weighted Penalty System**: Different red flags have different weights  
✅ **Scam Detection**: Identifies common fraud patterns  
✅ **AI Generation Detection**: Spots bot-generated content  

---

## ⚖️ Agent 3: The Judge

### Purpose
Synthesizes evidence from both agents and renders final verdict.

### Architecture (3-Node LangGraph)

```
┌──────────────┐
│ Synthesizer  │ → Normalizes Agent 1 & 2 outputs
└──────┬───────┘
       ↓
┌──────────────┐
│ Adjudicator  │ → Applies Trust-Weighted Logic
└──────┬───────┘
       ↓
┌──────────────┐
│   Reporter   │ → Generates reasoning & AEP
└──────────────┘
```

### How It Works

#### 1. **Synthesizer Node**
**Input:** Agent 1 + Agent 2 outputs  
**Process:**
- **Normalizes scores** to 0.0-1.0 scale
- **Processes claim metadata** (keywords, type, expiry)
- **Checks agent confidence** levels

**Normalization:**
```python
Agent 1 (Fact Checker):
- VERIFIED → 1.0
- DEBUNKED → 0.0
- UNVERIFIED → 0.5

Agent 2 (Forensic Expert):
- Already 0.0-1.0 (integrity score)
```

**Example:**
```
Agent 1: DEBUNKED (0.0), HIGH confidence
Agent 2: 0.15 (LIKELY FRAUDULENT), HIGH confidence

Normalized:
- s1 = 0.0
- s2 = 0.15
- Both agents agree (both say FALSE)
```

**Output:** Normalized scores + claim metadata

---

#### 2. **Adjudicator Node**
**Input:** Normalized scores  
**Process:**
- **Dynamic Weighting**: Adjusts weights based on evidence quality
- **Agreement Check**: Do agents agree or conflict?
- **Final Score Calculation**: Weighted average

**Weighting Logic:**
```python
If Agent 1 has DEFINITIVE evidence (0.9 or 0.1):
  → Weight: 85% Fact Checker, 15% Forensic
  → Reason: "Strong factual evidence found"

If Agent 1 has SUPPORTING evidence (0.8 or 0.2):
  → Weight: 70% Fact Checker, 30% Forensic
  → Reason: "Fact-check found supporting evidence"

If Agent 1 is UNCERTAIN (0.5):
  → Weight: 25% Fact Checker, 75% Forensic
  → Reason: "No factual evidence - relying on forensics"

Otherwise:
  → Weight: 50% Fact Checker, 50% Forensic
  → Reason: "Balanced weighting - mixed signals"
```

**Final Score Calculation:**
```python
final_score = (s1 × weight_facts) + (s2 × weight_forensics)
```

**Example:**
```
s1 = 0.0 (DEBUNKED)
s2 = 0.15 (LIKELY FRAUDULENT)
weights = 85% / 15% (strong evidence)

final_score = (0.0 × 0.85) + (0.15 × 0.15) = 0.0225
```

**Verdict Mapping (Probability Language):**
```
Score >= 0.75: "TRUE" (75%+ likely true)
Score >= 0.60: "PROBABLY_TRUE" (60-75% likely true)
Score 0.40-0.60: "UNCERTAIN" (insufficient evidence)
Score <= 0.40: "PROBABLY_FALSE" (60-75% likely false)
Score <= 0.25: "FALSE" (75%+ likely false)
```

**Conflict Resolution:**
```
If agents DISAGREE (one says TRUE, other says FALSE):
  → Override to "UNCERTAIN"
  → Confidence: "LOW"
  → Reason: "Conflicting signals - needs review"
```

**Output:** Final score + verdict + confidence level

---

#### 3. **Reporter Node**
**Input:** Final verdict + all evidence  
**Process:**
- **Generates reasoning** using Gemini AI
- **Creates AEP** (Audit Evidence Package)
- **Prepares blockchain metadata**

**Reasoning Generation:**
```python
Prompt to AI:
"This claim is {verdict_text}.
Based on: {agent_summaries}
Write 2 sentences:
1. State probability (use % language)
2. Give ONE key action"

Example Output:
"This claim is 92% likely to be false based on 
contradicting news sources. Verify with official 
company announcements before sharing."
```

**AEP Structure:**
```json
{
  "claim_id": "abc123...",
  "verdict": {
    "decision": "FALSE",
    "truth_probability": 92,
    "confidence_score": 0.08,
    "confidence_level": "VERY HIGH"
  },
  "reasoning": "This claim is 92% likely false...",
  "methodology": {
    "weights_used": {
      "fact_checker": 0.85,
      "forensic_expert": 0.15
    },
    "agents_in_agreement": true
  },
  "chain_metadata": {
    "claim_hash": "sha256...",
    "keywords": ["tesla", "twitter", "acquisition"],
    "claim_type": 2,
    "expires_at": 1234567890
  }
}
```

**Output:** Complete AEP ready for PDF generation

---

### Key Features

✅ **Dynamic Weighting**: Adjusts based on evidence quality  
✅ **Conflict Resolution**: Handles agent disagreements  
✅ **Probability Language**: Uses % instead of binary TRUE/FALSE  
✅ **Blockchain Ready**: Generates metadata for on-chain storage  

---

## 🏷️ Agent 4: Claim Processor (Helper)

### Purpose
Processes claims for blockchain storage and freshness tracking.

### What It Does

#### 1. **Keyword Extraction**
```python
Claim: "Tesla is acquiring Twitter for $100 billion"

Extracted Keywords:
- tesla
- twitter
- acquisition
- 100b
- 2025
```

#### 2. **Claim Type Detection**
```
Types:
0 = TIMELESS (scientific facts) → Never expires
1 = HISTORICAL (past events) → Never expires
2 = BREAKING_NEWS (recent) → 7 days
3 = ONGOING (live prices) → 24 hours
4 = PREDICTION (future) → Until target date
5 = STATUS (current state) → 30 days
```

#### 3. **Hash Generation**
```python
claim_hash = SHA256(normalized_claim)
# Used for exact matching on blockchain

claim_signature = SHA256(sorted_keywords)
# Used for finding similar claims
```

#### 4. **Expiry Calculation**
```python
If claim_type == BREAKING_NEWS:
  expires_at = now + 7 days

If claim_type == TIMELESS:
  expires_at = 0 (never)
```

---

## 🔄 Complete Flow

```
User submits claim
       ↓
┌──────────────────────────────────┐
│ Agent 1: Fact Checker            │
│ - Strategist generates queries   │
│ - Executor searches (parallel)   │
│ - Analyst evaluates evidence     │
└──────────────┬───────────────────┘
               │
               ↓
       Agent 1 Output
       (preliminary verdict)
               │
               ↓
┌──────────────────────────────────┐
│ Agent 2: Forensic Expert         │
│ - Profiler analyzes language     │
│ - Detector checks AI/manipulation│
│ - Auditor calculates score       │
└──────────────┬───────────────────┘
               │
               ↓
       Agent 2 Output
       (integrity score)
               │
               ↓
┌──────────────────────────────────┐
│ Agent 3: The Judge               │
│ - Synthesizer normalizes         │
│ - Adjudicator weighs evidence    │
│ - Reporter generates AEP         │
└──────────────┬───────────────────┘
               │
               ↓
       Final Verdict
       (with probability %)
               │
               ↓
┌──────────────────────────────────┐
│ Agent 4: Claim Processor         │
│ - Extracts keywords              │
│ - Detects claim type             │
│ - Calculates expiry              │
└──────────────┬───────────────────┘
               │
               ↓
       PDF Report + Blockchain Data
```

---

## 📊 Example: Complete Verification

### Input
```
Claim: "URGENT!!! Tesla is acquiring Twitter for $100 billion! ACT NOW!!!"
```

### Agent 1: Fact Checker
```
Strategist: Generates 3 queries
Executor: Searches in parallel (2.3s)
Analyst: Evaluates results

Result:
- Verdict: DEBUNKED
- Evidence: No credible sources found
- Confidence: HIGH
- Score: 0.0
```

### Agent 2: Forensic Expert
```
Profiler: Detects urgency, poor grammar
Detector: Finds manipulation tactics
Auditor: Applies penalties

Result:
- Integrity Score: 0.15
- Verdict: LIKELY FRAUDULENT
- Penalties: -0.85 total
- Red Flags: 7
```

### Agent 3: The Judge
```
Synthesizer: Normalizes (0.0, 0.15)
Adjudicator: Applies 85/15 weighting
Reporter: Generates reasoning

Result:
- Final Score: 0.0225
- Verdict: FALSE
- Truth Probability: 2% (98% likely false)
- Confidence: VERY HIGH
- Reasoning: "This claim is 98% likely to be false 
  based on no credible sources and multiple scam 
  indicators. Do not share or click any links."
```

### Agent 4: Claim Processor
```
Keywords: [tesla, twitter, acquisition, 100b]
Type: BREAKING_NEWS (expires in 7 days)
Hash: abc123...
Signature: def456...
```

### Final Output
```json
{
  "verdict": "FALSE",
  "truth_probability": 2,
  "confidence": "VERY HIGH",
  "reasoning": "98% likely false...",
  "processing_time": "4.2s"
}
```

---

## 🎯 Key Innovations

1. **Parallel Processing**: Agent 1 searches run simultaneously
2. **Dynamic Weighting**: Judge adjusts weights based on evidence quality
3. **Probability Language**: Uses % instead of binary TRUE/FALSE
4. **Iterative Refinement**: Agent 1 can retry with better queries
5. **Multi-layered Analysis**: Fact-checking + Forensics + Synthesis
6. **Blockchain Ready**: Generates metadata for on-chain storage

---

## 💡 Why This Architecture Works

✅ **Specialization**: Each agent focuses on one task  
✅ **Redundancy**: Two independent verification methods  
✅ **Conflict Resolution**: Judge handles disagreements  
✅ **Speed**: Parallel execution + caching  
✅ **Transparency**: Full audit trail in AEP  
✅ **Scalability**: Can add more agents easily  

---

**Built with ❤️ by Kedar Sathe & Riddhi Shende**  
**7th Semester Major Project**  
**Under the guidance of Prof. Gopal Deshmukh Sir**
