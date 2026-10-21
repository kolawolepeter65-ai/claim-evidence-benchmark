import json
from pathlib import Path
import streamlit as st
from evidencebench.core import evaluate_claim, evaluate_dataset

st.set_page_config(page_title="Claim & Evidence Benchmark", page_icon="🔎", layout="wide")
st.title("🔎 Claim & Evidence Benchmark")
st.caption("Evidence retrieval, abstention, and traceability for AI evaluation.")
st.warning("This baseline does NOT determine factual truth, paraphrase entailment, or contradiction. Similarity is not factual confidence.")
mode = st.radio("Mode", ["Inspect a claim", "Benchmark review"], horizontal=True)
if mode == "Inspect a claim":
    claim = st.text_area("Claim to inspect", "Mercury is the closest planet to the Sun.")
    evidence = st.text_area("Evidence passages (one per line)", "Mercury is the closest planet to the Sun.\nVenus is the second planet from the Sun.", height=150)
    threshold = st.slider("Review-candidate word overlap threshold", 0.0, 1.0, 0.65, 0.05)
    if st.button("Run evidence inspection", type="primary"):
        try:
            sources = [{"id": f"evidence-{i+1}", "text": line.strip()} for i, line in enumerate(evidence.splitlines()) if line.strip()]
            result = evaluate_claim(claim, sources, threshold)
            st.subheader("Decision: " + result["verdict"].replace("_", " ").title())
            st.caption(result["explanation"])
            st.metric("Highest lexical overlap (NOT confidence)", f'{result["overlap"]:.0%}')
            st.dataframe(result["candidates"], hide_index=True, use_container_width=True)
            st.download_button("Export JSON evaluation", json.dumps(result, indent=2), file_name="evidence_evaluation.json", mime="application/json")
        except ValueError as exc:
            st.error(str(exc))
else:
    cases = json.loads((Path(__file__).resolve().parent / "data" / "benchmark.json").read_text())
    results = evaluate_dataset(cases)
    st.write("**Six synthetic human-labeled challenge cases.** Labels are illustrative, not independently verified ground truth.")
    st.dataframe([{"ID": r["id"], "Gold label": c["gold_label"], "Baseline verdict": r["verdict"], "Evidence ID": r["evidence_id"], "Overlap": r["overlap"]} for r, c in zip(results, cases)], hide_index=True, use_container_width=True)
    st.download_button("Export benchmark results", json.dumps(results, indent=2), file_name="benchmark_results.json", mime="application/json")
    st.caption("Lexical overlap cannot establish truth; inspect evidence before final judgments.")
st.markdown("[Source code](https://github.com/kolawolepeter65-ai/claim-evidence-benchmark) · [Task specification](https://github.com/kolawolepeter65-ai/claim-evidence-benchmark/blob/main/TASK.md)")
