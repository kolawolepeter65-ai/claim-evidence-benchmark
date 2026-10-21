# Claim & Evidence Benchmark

[![Python Tests](https://github.com/kolawolepeter65-ai/claim-evidence-benchmark/actions/workflows/tests.yml/badge.svg)](https://github.com/kolawolepeter65-ai/claim-evidence-benchmark/actions/workflows/tests.yml)

An evidence-aware AI evaluation portfolio project featuring transparent lexical retrieval, conservative abstention, a synthetic challenge dataset, pytest tests, Docker, and an interactive Streamlit review tool.

## What it does
- Accepts a claim and user-supplied evidence passages.
- Ranks candidate passages with deterministic tie-breaking.
- Identifies normalized exact matches, flags candidates for human review, and abstains on low overlap.
- Demonstrates why lexical similarity **cannot** establish factual truth, using six illustrative human-labeled challenge cases.
- Exports machine-readable JSON.

**Limitations:** Not an autonomous fact checker, external-source verifier, or natural-language inference classifier. Similarity is **not** factual confidence; potential contradiction and paraphrase entailment are not decided automatically.

## Live demo
To deploy on [Streamlit Community Cloud](https://share.streamlit.io/), choose repository `kolawolepeter65-ai/claim-evidence-benchmark`, branch `main`, and entry point `app.py`. Add the resulting live URL here.

## Local setup
```bash
python -m pip install -e '.[test]'
python -m pytest -q
streamlit run app.py
```

Docker: `docker build -t claim-evidence-benchmark . && docker run --rm claim-evidence-benchmark`

## Files
- [Task specification](TASK.md)
- [Reference implementation](src/evidencebench/core.py)
- [Challenge dataset](data/benchmark.json)
- [Tests](tests/test_core.py)
- [Streamlit interface](app.py)
- [Automated CI](.github/workflows/tests.yml)

Gold labels are illustrative annotations, **not independently verified statistical ground truth**. Future validation needs independent sources, multiple annotators, adjudication, class balance, and held-out testing.

## Author
Kolawole Peter Olusola · [Portfolio](https://techbykhay.site/) · [LinkedIn](https://www.linkedin.com/in/kolawole-peter-olusola/)
