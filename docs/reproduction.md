# Reproduction

Python 3.11+ and Pillow 12.x. Run `python -m pip install -r requirements.txt`, then `python scripts/run_experiment.py`, then `python -m unittest discover -s tests -v`. The script writes `source.png`, `none.png`, `tint.png`, `palette.png`, and `metrics.json` inside `results/`. For local assets call `adapt(source_path, destination_path, [(r,g,b), ...], method)` from `src/adapt.py`.
