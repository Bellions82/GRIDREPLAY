# VideoForge Production Playbook

## Purpose

VideoForge treats the song as the source of truth for the visual system: lyrics drive visual meaning and the mastered audio drives timing. Every production stage creates a versioned artifact and advances only through an explicit human approval gate.

## Operating rules

1. Every stage produces a versioned artifact.
2. The song master is authoritative for timing.
3. Each shot has one primary subject, one primary action, and one emotional beat.
4. Approve keyframes before spending render capacity on motion.
5. AI agents may draft, score, dispatch, and route work; humans own creative approval gates.
6. Every generated asset records prompt, provider/model, seed when supported, generation parameters, source references, and version.
7. Rights/safety checks are explicit. Use authorized artist/reference assets and generic stand-ins where rights are unavailable.

## Production gates

1. Concept — Song Bible + creative brief
2. Identity — approved character/location/prop reference sheets
3. Keyframes — approved stills
4. Shot Approval — generated clips pass QC
5. Rough Cut — beat-synced assembly approved
6. Final — master QA and delivery approval

## Song Bible

Required inputs:
- mastered audio
- measured BPM, time signature, key, duration
- section map and bar counts
- energy score per section
- emotional arc and lyric themes
- delivery targets

Timing is calculated from the actual master:
- seconds/beat = 60 / BPM
- seconds/bar = seconds/beat × beats/bar
- frames/beat = seconds/beat × FPS
- frames/bar = seconds/bar × FPS

The system stores both seconds and frame positions so editing remains deterministic.

## Look Card

Each song receives a song-specific visual identity.

Required fields:
- look seed
- core emotion
- medium
- palette
- lighting/lens language
- texture/grain
- motion language
- recurring motif
- section shifts
- lyric mapping
- identity locks
- never-show list

Lyrics are classified as literal, metaphorical, or abstract to prevent overly literal visualization of wordplay.

Genre is a modifier, not the visual source of truth.

## Identity stress testing

Before a character or key environment is promoted to LOCKED:
- generate representative views and lighting conditions
- test wide, close, profile, backlight, overhead/low-angle and motion conditions
- record drift findings
- approve a reusable reference asset

Identity, wardrobe, hair, accessories, props, environment IDs and silhouette rules are versioned.

## Shot Card

Every shot records:
- shot ID
- section and bar range
- start/end time and frame
- lyric intent
- energy
- visual interpretation
- opening frame
- timed action beats
- performance direction
- environment behavior
- framing/lens
- one deliberate camera move
- locked asset IDs
- transition anchor
- cut target
- provider/model/seed/version

Shot generation uses edit handles and clean first/last frames.

## Generation strategy

- Draft inexpensively, then render approved shots at final quality.
- Run variants in parallel where capacity allows.
- Keep generation clips modular.
- Separate visual generation from soundtrack/audio assembly.
- Use audio-driven generation specifically where lip-sync is required.
- Compose 16:9 shots with a protected center region for 9:16 reframing.

## Adaptive edit intelligence

Cut frequency follows the measured energy curve rather than blindly cutting on every beat.

The editor engine may:
- prefer section/downbeat transitions
- increase cut density during high-energy sections
- hold longer on emotional lines
- preserve screen direction
- use transition anchors to improve continuity

These are recommendations to the editor, not irreversible decisions.

## QC

Each shot is evaluated for:
- identity match
- anatomy/artifacts
- temporal stability/flicker
- physics/environment behavior
- visual DNA adherence
- beat/timing fit

Technical QA additionally checks:
- codec
- resolution
- frame count
- duration
- audio presence where expected
- file integrity

A human approval remains required at the Shot Approval gate.

## Repair routing

- identity drift → regenerate from approved keyframe/reference
- anatomy/warping → shorten, crop, replace or regenerate
- flicker/softness → stabilize/upscale/re-render
- framing/aspect mismatch → reframe
- background defect → replace background
- color mismatch → grade-match before assembly

## Vocal performance

Lip-sync is treated as a high-risk shot class. The system should classify close performance shots separately and apply stricter QA. Cutaways, silhouettes, profiles and wider compositions can be used when they better protect visual quality.

## Finish and delivery

Final finishing includes:
- unified grade
- controlled grain/lens treatment
- final upscale when required
- sync verification
- platform-specific exports
- vertical cutdowns
- visualizer/lyric-video derivatives when requested

## Learning loop

Each project contributes anonymized production lessons to a versioned prompt/preset library:
- successful prompt patterns
- provider/model performance by shot type
- common failure modes
- repair effectiveness
- render cost/time
- QC outcomes

The learning layer improves templates without changing an already-approved project retroactively.
