"""Conservative evidence retrieval baseline. Not a factual truth/NLI model."""
import re
STOP = set("a an the is are was were be to of and or in on for by with from that this it as at you your its has have had".split())
NEGATIONS = {"not", "never", "no", "without", "cannot", "isn't", "wasn't", "don't"}

def tokens(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())

def content_terms(text):
    return set(tokens(text)) - STOP - NEGATIONS

def evaluate_claim(claim, sources, threshold=0.65):
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("claim must be nonempty text")
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources must be a nonempty list")
    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    norm = " ".join(tokens(claim))
    terms = content_terms(claim)
    candidates = []
    for source in sources:
        if not isinstance(source, dict) or any(k not in source for k in ("id", "text")):
            raise ValueError("every source must include id and text")
        sid, passage = source["id"], source["text"]
        if not isinstance(sid, str) or not sid.strip() or not isinstance(passage, str) or not passage.strip():
            raise ValueError("invalid source id or text")
        source_terms = content_terms(passage)
        overlap = len(terms & source_terms) / len(terms) if terms else 0.0
        exact = norm == " ".join(tokens(passage))
        candidates.append({"source_id": sid, "text": passage, "overlap": round(overlap, 3), "exact_match": exact})
    candidates.sort(key=lambda c: (-int(c["exact_match"]), -c["overlap"], c["source_id"]))
    best = candidates[0]
    verdict = "supported_exact" if best["exact_match"] else "needs_review" if best["overlap"] >= threshold else "insufficient_evidence"
    explanation = ("Exact normalized evidence sentence match." if best["exact_match"] else
                   "Lexical similarity is not entailment; human review required." if verdict == "needs_review" else
                   "No sufficiently overlapping evidence found; abstaining.")
    return {"claim": claim, "verdict": verdict, "evidence_id": best["source_id"],
            "overlap": best["overlap"], "candidates": candidates, "explanation": explanation}

def evaluate_dataset(cases, threshold=0.65):
    if not isinstance(cases, list):
        raise ValueError("cases must be a list")
    return [{"id": case["id"], **evaluate_claim(case["claim"], case["sources"], threshold)} for case in cases]
