# VideoForge Production Benchmark v1

## Purpose
Measure whether VideoForge can reliably convert real music-video inputs into approved, traceable deliverables. This benchmark is evidence collection, not a marketing claim.

## Evaluation unit
A benchmark case contains:
- source audio and normalized timing analysis
- lyrics/semantic annotations where available
- creator brief and Visual DNA
- canon, character, location and reference assets
- planned scene/shot manifest
- provider/model/version and generation parameters
- generated artifact and immutable artifact metadata
- automated QA result
- human review result
- repair attempts and outcomes
- generation latency, cost, retry count and compute/provider utilization

## Failure taxonomy
IDENTITY_DRIFT, WARDROBE_DRIFT, FACE_DRIFT, ANATOMY, HAND_FAILURE, PROP_FAILURE, BACKGROUND_DRIFT, LOCATION_DRIFT, MOTION_FAILURE, TEMPORAL_FLICKER, PHYSICS_FAILURE, COMPOSITION_FAILURE, LYRIC_MISMATCH, BEAT_MISMATCH, AUDIO_SYNC, TECHNICAL_FAILURE.

## Required measurements
- first-pass approval rate
- final approval rate
- identity/continuity acceptance
- temporal stability
- timeline alignment error
- repair success rate
- generation attempts per approved shot
- cost per approved minute
- wall-clock time per finished minute
- human review time
- provider/model failure rate

## Benchmark phases
1. 50-100 representative projects/cases.
2. 500-1,000 generated shots across supported providers/models.
3. Human-label a representative subset.
4. Run repair experiments and measure before/after outcomes.
5. Run 10 complete end-to-end projects.
6. Freeze a regression set; never rewrite historical results after approval.

## Torture suite
Include identity stress, complex motion, difficult anatomy, reflective/wet environments, low light, crowds, props, long continuity chains, lyric-heavy shots, beat-sparse sections, rapid transitions, and high-risk performance/lip-sync shots.

## Decision rule
Do not claim a production throughput target until the measured benchmark demonstrates it under the actual provider/model mix, infrastructure limits, retry policy, and human approval requirements.
