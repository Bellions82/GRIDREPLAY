# VideoForge Visual QA Evidence Contract

VideoForge separates provider-reported metadata from independently inspected evidence.

## Evidence hierarchy
1. Artifact evidence — the actual rendered media and its checksum.
2. Technical inspection — decoder/probe evidence for duration, FPS, dimensions, audio presence, integrity and A/V sync.
3. Visual inspection — frame/video analysis for identity, temporal stability, anatomy, composition and environment.
4. Continuity inspection — comparison against approved neighboring shots and locked canon.
5. Timeline evidence — measured relationship to master audio and shot timing.
6. Provider metadata — useful provenance, but never sufficient by itself to prove visual quality.

## Unknown is not pass
A metric that cannot be measured is UNKNOWN. The orchestration layer must not silently convert missing evidence into a production approval.

The development simulation provider is an explicit exception for exercising workflow mechanics; it does not establish generation quality.

## Threshold policy
Initial thresholds are deliberately configurable and provisional. They are not claims about universal visual quality. Benchmark data should calibrate them by shot class, provider/model, reference strategy and project requirements.

Current provisional examples:
- identity similarity: >= 0.90
- temporal stability: >= 0.85
- composition score: >= 0.85
- anatomy score: >= 0.85
- environment similarity: >= 0.85

Threshold calibration requires labeled real-world examples and human-review agreement.

## Why this matters
This prevents a dangerous failure mode in generative-video orchestration: a provider reports that generation succeeded, the API returns success, and the production system incorrectly treats that as evidence that the shot is visually acceptable.