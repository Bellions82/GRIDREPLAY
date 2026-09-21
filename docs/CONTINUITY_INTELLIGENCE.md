# VideoForge Continuity Intelligence

Continuity is evaluated against the **approved production state**, not the latest generated attempt.

## Continuity dimensions
- character identity
- wardrobe/costume
- location/world
- Visual DNA
- lighting
- screen direction
- camera language
- action state
- required props

## Evidence states
- PASS: measured/declared continuity satisfies policy.
- REPAIR: a locked contradiction or continuity score below threshold is detected.
- UNKNOWN: insufficient evidence exists; UNKNOWN is not silently converted to PASS.

## Approved-state rule
A generation attempt cannot become canonical merely because it was generated later. A shot becomes a reference only after explicit approval.

## Continuity graph
VideoForge stores approved shot state as a graph-like reference structure. Future shots can retrieve the nearest approved predecessor rather than accidentally inheriting state from a rejected generation.

## Future evidence adapters
The current implementation compares structured shot state. Production adapters should add:
- face/identity embedding similarity
- wardrobe appearance similarity
- environment/image similarity
- lighting/color measurements
- camera/framing measurements
- screen-direction estimation
- pose/action similarity
- required-prop detection

Those adapters must report evidence and confidence rather than silently asserting continuity.

## Repair behavior
Continuity failures should route to targeted repair:
- identity/location/Visual DNA → regenerate with locked approved references
- wardrobe/props → lock the approved asset
- camera/framing → reframe or regenerate
- action/screen direction → revise motion/camera plan
- insufficient evidence → human review or additional inspection
