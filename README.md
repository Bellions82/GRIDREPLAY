# VideoForge

Production-grade generative music-video orchestration platform.

## v4.1 foundation
- FastAPI modular backend
- API / Director / Renderer / QA / Assembly boundaries
- Deterministic render fingerprints for idempotency
- Render lifecycle state machine
- Provider-neutral video generation interface
- Artist Impact Engine and Shot Card contracts
- Song Bible / production-gate rules documented in docs
- Postgres + Redis + MinIO local infrastructure
- React/TypeScript Director Studio shell
- Testable core contracts and state transitions

## Local startup
1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. API health: `http://localhost:8000/api/v1/health`.
4. In `frontend`, install dependencies and run `npm run dev`.

The 10-videos/48-hour target is a benchmark, not a guarantee; throughput depends on provider capacity, GPU resources, scene complexity and QA retries.
