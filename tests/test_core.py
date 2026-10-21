import copy
import json
from pathlib import Path
import pytest
from evidencebench.core import evaluate_claim, evaluate_dataset

def source(text, sid="s1"):
    return [{"id": sid, "text": text}]

def test_exact_supported():
    assert evaluate_claim("Hello, World!", source("hello world"))["verdict"] == "supported_exact"

def test_case_and_punctuation_normalize():
    assert evaluate_claim("Revenue rose 18%.", source("REVENUE ROSE 18 percent"))["verdict"] == "needs_review"

def test_similar_does_not_imply_support():
    assert evaluate_claim("Venus is the closest planet to the Sun.", source("Mercury is the closest planet to the Sun."))["verdict"] != "supported_exact"

def test_negation_not_claimed_as_contradiction():
    assert evaluate_claim("The product is not waterproof.", source("The product is waterproof."))["verdict"] == "needs_review"

def test_absent_evidence_abstains():
    assert evaluate_claim("The warranty lasts five years.", source("Free delivery is included."))["verdict"] == "insufficient_evidence"

def test_sorting_is_deterministic():
    assert evaluate_claim("Hello world", [{"id": "z", "text": "Hello world"}, {"id": "a", "text": "Hello world"}])["evidence_id"] == "a"

def test_does_not_mutate_input():
    s = source("testing")
    original = copy.deepcopy(s)
    evaluate_claim("testing", s)
    assert s == original

@pytest.mark.parametrize("claim,sources,threshold", [
    ("", source("a"), .5), ("x", [], .5), ("x", source("y"), -1), ("x", source("y"), 2),
    ("x", [{}], .5), ("x", [{"id": 3, "text": "foo"}], .5),
    ("x", [{"id": "a", "text": ""}], .5)])
def test_invalid_inputs(claim, sources, threshold):
    with pytest.raises(ValueError):
        evaluate_claim(claim, sources, threshold)

def test_benchmark_cases():
    cases = json.loads((Path(__file__).resolve().parents[1] / "data" / "benchmark.json").read_text())
    results = evaluate_dataset(cases)
    assert len(results) == 6
    assert results[0]["verdict"] == "supported_exact"
    assert results[1]["verdict"] != "supported_exact"
