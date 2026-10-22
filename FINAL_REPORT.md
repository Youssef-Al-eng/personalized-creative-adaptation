# Final Report — Personalized Creative Adaptation

## Question and method

Can deterministic palette adaptation better match an explicit target palette while preserving raster structure? Three original geometric RGBA assets were adapted to three synthetic palette profiles by no-op, global tint and nearest-palette mapping with luminance scaling. The experiment evaluates palette distance, edge-map RMSE, image dimensions and output size across 27 cases. No people rated the results.

## Results and analysis

Across the 27 cases, mean normalized palette distance was .1557 for no-op, .1358 for tint and .0534 for palette mapping. Mean edge RMSE was 0, .0462 and .0339 respectively. Palette mapping improved the objective palette-distance measure for all tested asset/profile pairs, with variable edge error. For asset 0/coastal, distance was .0606 vs .0864 and .1167; edge RMSE was .0148 vs 0 and .0469. Actual outputs and all metrics are in `results/`.

## Validation and limitations

Four tests pass for method/palette validation, no-op identity, alpha preservation, size and generated artifacts. Run `python scripts/run_experiment.py` and `python -m unittest discover -s tests -v`. The assets are generated geometric shapes and palettes stand in for preference profiles; there is no human study, semantic object-preservation test or learned personalization. Palette distance and edge RMSE do not measure subjective quality.

## Status

`IMPLEMENTED`, `TESTED`, `EXPERIMENTS_COMPLETE`, `FINALIZED` for synthetic objective evaluation. Human evaluation requires a separately recruited, consented participant study and is not claimed here.
