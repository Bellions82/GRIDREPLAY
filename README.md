# VideoForge

Production-grade generative music-video orchestration platform.

## v4.4 production-control foundation
- FastAPI modular backend with API / Director / Renderer / QA / Assembly boundaries
- Deterministic render fingerprints and database-backed render jobs
- Postgres persistence for projects, scenes, shots, jobs, generation records and QA results
- Redis queue with worker leases, heartbeats, recovery and dead-letter routing
- Versioned generation artifacts with provider/model/parameter/reference provenance
- Structured QA dimensions and failure taxonomy with repair-plan routing
- Canon / prompt compiler / motion specification / composition contracts
- Provider-neutral generation interface plus development simulation provider
- Provider capability contract for model-aware generation strategies
- Artifact and provenance schema
- Artist Impact Engine, Shot Card contracts and production-gate rules
- Production benchmark specification for identity, continuity, timing, repair, cost and throughput
- React/TypeScript Director Studio shell
- Automated contract tests

## Current production loop

CREATE → ANALYZE → DIRECT → LOCK CANON → PLAN SHOTS → GENERATE → QA → REPAIR/REGENERATE → APPROVE → ASSEMBLE → FINAL QA → EXPORT

Every generation is intended to be traceable from final artifact back to shot, generation attempt, prompt, canon, references, provider/model and QA decision.

## Local startup
1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Apply database migrations with Alembic before exercising persistence endpoints.
4. API health: `http://localhost:8000/api/v1/health`.
5. In `frontend`, install dependencies and run `npm run dev`.

The 10-videos/48-hour target is a benchmark, not a guarantee; throughput depends on provider capacity, GPU resources, scene complexity, QA retries and human approval.

## Evidence-first rule

VideoForge does not treat a successful API call as proof of production quality. Production readiness is earned through the benchmark in `docs/PRODUCTION_BENCHMARK.md`, including real provider runs, measurable QA outcomes, repair success, cost/latency data and end-to-end project trials.
