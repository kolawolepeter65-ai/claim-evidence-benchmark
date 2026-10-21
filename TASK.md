# Task specification: Conservative claim-evidence retrieval

Implement `evaluate_claim(claim: str, sources: list[dict], threshold: float = 0.65)`.

Each source requires nonempty string fields `id` and `text`. Return ranked passages, the best source ID, lexical overlap, verdict, and explanation; reject malformed inputs with `ValueError`.

1. Normalize casing and punctuation for exact matching.
2. Overlap score = content-term intersection divided by the number of claim content terms. Remove common stop words and negations from similarity terms, but **never** infer factual contradiction from this removal.
3. Rank exact matches first, then overlap descending, then source ID ascending.
4. Assign `supported_exact` only when normalized claim and evidence text match.
5. Assign `needs_review` when non-exact overlap reaches the threshold.
6. Assign `insufficient_evidence` otherwise.
7. Do not fabricate sources, infer entailment from keyword overlap, or call an overlap score probability of truth.

The six example cases are synthetic and carry illustrative human labels. They test entity substitution, unsupported claims, numerical matching, and negation. They do not demonstrate NLI ability.

Run `python -m pip install -e '.[test]'` and `python -m pytest -q`.
