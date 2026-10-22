# personalized-creative-adaptation

Local raster image pipeline that adapts color palettes while retaining source image dimensions and edge structure, comparing identity, global tint and nearest-palette mapping across generated assets and explicit color profiles.

![Python](https://img.shields.io/badge/python-3.11%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) [![CI](https://github.com/Youssef-Al-eng/personalized-creative-adaptation/actions/workflows/ci.yml/badge.svg)](https://github.com/Youssef-Al-eng/personalized-creative-adaptation/actions/workflows/ci.yml)

## Quickstart

```bash
pip install -r requirements.txt     # install (Pillow)
python scripts/run_experiment.py    # run the study
python -m unittest discover -s tests -v    # run tests
```

## Run

Python 3.11+ and Pillow:

```powershell
python -m pip install -r requirements.txt
python scripts/run_experiment.py
python -m unittest discover -s tests -v
```

Outputs include `results/source.png`, profile/asset/method PNG comparisons (27 cases), and `results/metrics.json`. The script accepts a generated fixture now; use `adapt(source, destination, palette, method)` from `src/adapt.py` for a local RGBA image.

## Evaluation and limits

The report computes nearest-palette RGB distance, edge-map RMSE, output size and dimension preservation. No people rated these outputs; target palettes are explicit synthetic preference representations. These objective measures do not establish subjective appeal or semantic identity preservation. No image-generation service is used.

See [technical specification](TECHNICAL_SPEC.md), [final report](FINAL_REPORT.md), and [reproduction guide](docs/reproduction.md).

## License

MIT — see [LICENSE](LICENSE).

## Citation

See [CITATION.cff](CITATION.cff), or cite as:

```bibtex
@software{personalized_creative_adaptation,
  author = {Al-eng, Youssef},
  title  = {personalized-creative-adaptation},
  year   = {2026},
  url    = {https://github.com/Youssef-Al-eng/personalized-creative-adaptation}
}
```
