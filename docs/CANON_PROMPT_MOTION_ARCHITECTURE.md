# VideoForge Canon, Prompt Compiler & Motion Architecture

## Purpose
VideoForge treats a shot as the atomic production and repair unit. The system compiles stable creative intent into provider-specific generation requests without binding the production to one model.

## Canon hierarchy
GLOBAL -> CHARACTER -> WORLD -> SCENE -> SHOT.
Lower-level instructions cannot silently override a higher-level locked constraint.

## Prompt compiler
The compiler assembles:
- global canon
- character/world canon
- scene state
- shot objective
- opening frame
- action
- motion
- camera
- lighting
- composition
- continuity constraints
- negative constraints

The compiled request is passed through a provider adapter.

## Motion
Appearance and motion are separate contracts. Motion is represented as structured beats, tempo, acceleration, recovery and intensity. Complex action is decomposed into deterministic action beats.

## Continuity
Continuity strategies are provider-aware: reference frames, identity references, location references, style references and latent/conditioning mechanisms where supported. Generation parameters remain model-specific and configurable.

## Composition
Shots can declare face/feet visibility, protected regions, vertical-crop safety, text-safe regions and required props before generation.

## Generation records
Every take records model/provider/version, prompt, negative prompt, seed, parameters, references, timestamp and QC result. Shot versions remain reproducible and independently replaceable.

## Production loop
PLAN -> KEYFRAME -> GENERATE -> CHECK -> REPAIR -> REGENERATE -> APPROVE -> ASSEMBLE -> MASTER.
