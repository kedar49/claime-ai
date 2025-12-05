import os
import logging
import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents import FactChecker, ForensicExpert, TheJudge

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Claime-API")

app = FastAPI(title="Claime API", description="AI Fact-Checking API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClaimRequest(BaseModel):
    claim: str

from fastapi.staticfiles import StaticFiles
from agents.shelby import Shelby

# Define absolute path for storage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# Ensure storage directory exists with proper permissions
try:
    os.makedirs(STORAGE_DIR, exist_ok=True)
    logger.info(f"Storage directory ready: {STORAGE_DIR}")
except Exception as e:
    logger.error(f"Failed to create storage directory: {e}")
    import tempfile
    STORAGE_DIR = tempfile.gettempdir()
    logger.warning(f"Using temp directory: {STORAGE_DIR}")

# Set BACKEND_URL environment variable for Shelby to use in download URLs
if not os.getenv("BACKEND_URL"):
    # Try to detect from environment or use default
    os.environ["BACKEND_URL"] = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
    logger.info(f"BACKEND_URL set to: {os.environ['BACKEND_URL']}")

# Instantiate agents
fact_checker = FactChecker()
forensic_expert = ForensicExpert()
judge = TheJudge()
shelby = Shelby(storage_dir=STORAGE_DIR)

# Mount storage directory for downloads
app.mount("/download", StaticFiles(directory=STORAGE_DIR), name="download")

@app.get("/")
def read_root():
    return {"status": "online", "service": "Claime API"}

@app.post("/verify_stream")
async def verify_claim_stream(request: ClaimRequest):
    claim = request.claim.strip()
    if not claim:
        raise HTTPException(status_code=400, detail="Claim cannot be empty")

    # Track processing time
    start_time = time.time()

    async def event_generator():
        yield f"data: {json.dumps({'type': 'status', 'message': 'Initializing agents...'})}\n\n"
        
        a1_result = {}
        a2_result = {}
        queue = asyncio.Queue()
        
        async def run_fact_checker():
            try:
                async for event in fact_checker.astream_verify(claim):
                    for node, state in event.items():
                        if node == "strategist":
                             await queue.put({"type": "log", "agent": "FactChecker", "message": "Strategist generated search queries."})
                        elif node == "executor":
                             count = len(state.get('search_results', []))
                             await queue.put({"type": "log", "agent": "FactChecker", "message": f"Executor found {count} sources."})
                             await queue.put({"type": "sources", "data": state.get('search_results', [])})
                        elif node == "analyst":
                             await queue.put({"type": "log", "agent": "FactChecker", "message": "Analyst completed evaluation."})
                             if "evidence_dossier" in state:
                                  a1_result.update(state["evidence_dossier"])
            except Exception as e:
                logger.error(f"FactChecker error: {e}")
                await queue.put({"type": "error", "message": str(e)})

        async def run_forensic_expert():
            try:
                async for event in forensic_expert.astream_analyze(claim):
                    for node, state in event.items():
                        if node == "profiler":
                            await queue.put({"type": "log", "agent": "ForensicExpert", "message": "Profiler analyzed linguistic patterns."})
                        elif node == "detector":
                            await queue.put({"type": "log", "agent": "ForensicExpert", "message": "Detector checked for AI/manipulation."})
                        elif node == "auditor":
                            await queue.put({"type": "log", "agent": "ForensicExpert", "message": "Auditor calculated integrity score."})
                            if "forensic_log" in state:
                                a2_result.update(state["forensic_log"])
            except Exception as e:
                logger.error(f"ForensicExpert error: {e}")
                await queue.put({"type": "error", "message": str(e)})

        # Run agents in parallel
        task1 = asyncio.create_task(run_fact_checker())
        task2 = asyncio.create_task(run_forensic_expert())
        
        pending = {task1, task2}
        while pending:
            while not queue.empty():
                item = await queue.get()
                yield f"data: {json.dumps(item)}\n\n"
            
            done, pending = await asyncio.wait(pending, timeout=0.1, return_when=asyncio.FIRST_COMPLETED)
            
        # Drain remaining queue items
        while not queue.empty():
            item = await queue.get()
            yield f"data: {json.dumps(item)}\n\n"

        yield f"data: {json.dumps({'type': 'status', 'message': 'Adjudicating verdict...'})}\n\n"

        try:
            # Get base AEP from judge
            aep = await judge.aadjudicate(a1_result, a2_result)
            
            # ===================================================================
            # CRITICAL: Build COMPLETE AEP with all agent data for comprehensive PDF
            # ===================================================================
            processing_time = time.time() - start_time
            
            complete_aep = {
                "claim": claim,
                "claim_id": aep.get("claim_id", "N/A"),
                "evidence": {
                    "agent_1_fact_checker": a1_result,  # ← Full Agent 1 results
                    "agent_2_forensic_expert": a2_result # ← Full Agent 2 results
                },
                "verdict": aep.get("verdict", {}),
                "reasoning": aep.get("reasoning", ""),
                "chain_metadata": aep.get("chain_metadata", {}),
                "storage": aep.get("storage", {}),
                "processing_time": f"{processing_time:.1f}s",
                "timestamp": aep.get("timestamp", "")
            }
            
            # Generate comprehensive PDF Report via Shelby
            yield f"data: {json.dumps({'type': 'status', 'message': 'Generating comprehensive AEP Report...'})}\n\n"
            
            pdf_path = shelby.generate_report(complete_aep)
            
            # Upload to Shelby Protocol
            yield f"data: {json.dumps({'type': 'status', 'message': 'Uploading to Shelby...'})}\n\n"
            download_url = shelby.upload_report(pdf_path)
            
            # Update storage info with download URL
            complete_aep["storage"]["download_url"] = download_url
            complete_aep["storage"]["pdf_path"] = pdf_path
            
            # Blockchain functionality removed - system works without it
            logger.info("✅ Verification complete - PDF report generated")
            
            # Build final response for frontend
            verdict_data = complete_aep.get("verdict", {})
            truth_prob = verdict_data.get("truth_probability", 50)
            storage_info = complete_aep.get("storage", {})
            
            final_response = {
                "claim": claim,
                "verdict": verdict_data.get("decision", "UNKNOWN"),
                "confidence_score": verdict_data.get("confidence_score", 0),
                "truth_probability": truth_prob,
                "verdict_text": verdict_data.get("verdict_text", ""),
                "confidence_level": verdict_data.get("confidence_level", "UNKNOWN"),
                "summary": complete_aep.get("reasoning", ""),
                "sources": a1_result.get("search_results", []),
                "forensic_analysis": {
                    "integrity_score": a2_result.get("integrity_score", 0),
                    "verdict": a2_result.get("verdict", "UNKNOWN"),
                    "ai_probability": a2_result.get("detection_summary", {}).get("ai_probability", 0),
                    "ai_indicators": a2_result.get("detection_summary", {}).get("indicators_found", []),
                    "penalties": a2_result.get("penalties_applied", []),
                    "checks_performed": a2_result.get("checks_performed", [])
                },
                "chain_metadata": complete_aep.get("chain_metadata", {}),
                "download_url": download_url,
                "processing_time": f"{processing_time:.1f}s"
            }
            
            yield f"data: {json.dumps({'type': 'result', 'data': final_response})}\n\n"
            
        except Exception as e:
            logger.error(f"Judge/Shelby error: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
            
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/verify")
async def verify_claim(request: ClaimRequest):
    """
    Non-streaming endpoint for simple verification.
    Returns complete results including PDF download URL.
    """
    claim = request.claim.strip()
    if not claim:
        raise HTTPException(status_code=400, detail="Claim cannot be empty")
    
    start_time = time.time()
    
    try:
        # Run agents in parallel
        logger.info("Running agents in parallel...")
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_a1 = executor.submit(fact_checker.verify_claim, claim)
            future_a2 = executor.submit(forensic_expert.analyze_text, claim)
            
            a1_result = future_a1.result()
            a2_result = future_a2.result()
        
        # Get verdict from judge
        logger.info("Adjudicating verdict...")
        aep = judge.adjudicate(a1_result, a2_result)
        
        # Build complete AEP with all data
        processing_time = time.time() - start_time
        
        complete_aep = {
            "claim": claim,
            "claim_id": aep.get("claim_id", "N/A"),
            "evidence": {
                "agent_1_fact_checker": a1_result,
                "agent_2_forensic_expert": a2_result
            },
            "verdict": aep.get("verdict", {}),
            "reasoning": aep.get("reasoning", ""),
            "chain_metadata": aep.get("chain_metadata", {}),
            "storage": aep.get("storage", {}),
            "processing_time": f"{processing_time:.1f}s"
        }
        
        # Generate PDF
        logger.info("Generating PDF report...")
        pdf_path = shelby.generate_report(complete_aep)
        download_url = shelby.upload_report(pdf_path)
        
        complete_aep["storage"]["download_url"] = download_url
        complete_aep["storage"]["pdf_path"] = pdf_path
        
        # Return response
        verdict_data = complete_aep.get("verdict", {})
        storage_info = complete_aep.get("storage", {})
        
        return {
            "claim": claim,
            "verdict": verdict_data.get("decision", "UNKNOWN"),
            "confidence_score": verdict_data.get("confidence_score", 0),
            "truth_probability": verdict_data.get("truth_probability", 50),
            "summary": complete_aep.get("reasoning", ""),
            "sources": a1_result.get("search_results", []),
            "forensic_analysis": {
                "integrity_score": a2_result.get("integrity_score", 0),
                "ai_probability": a2_result.get("detection_summary", {}).get("ai_probability", 0),
                "penalties": a2_result.get("penalties_applied", [])
            },
            "download_url": download_url,
            "processing_time": f"{processing_time:.1f}s"
        }
        
    except Exception as e:
        logger.error(f"Verification error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))