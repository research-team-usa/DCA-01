# DCA-01 - Deterministic Cluster Architecture

**From monolithic model to deterministic AI ecosystem**

> Template: Just-in-Sequence Manufacturing (Automotive) + Triple-Modular-Redundancy TMR (Avionics) + CAN-Bus / Blackboard + LRU Principle

Version: 1.2 COMPLETE DOSSIER | Author: Emanuel Schaaf | Status: Implementable

## What is this?

DCA-01 is a build-ready specification for an AI infrastructure that is:

- **Self-optimizable:** Each module learns from its own failures via local LoRA, no global retraining
- **Easier to train:** Local training, isolated weights, no catastrophic forgetting
- **Faster & more accurate:** Only relevant experts active, parallel inference, calibrated confidence c_i
- **Auditable:** Every path logged with dag_id, model_hash, provenance - EU AI Act ready

Instead of one giant model carrying all world knowledge for every token, a cluster of physically separated, domain-specialized base models is orchestrated via a deterministic data bus.

Core principle: Knowledge transfer happens not through mixed weights, but through typed data exchange on a Shared Context Board (Blackboard). Like CAN-Bus in a car.

## Architecture

```
[User Request] -> [TMR Router 2-out-of-3] -> [Task Decomposer DAG] -> [Semantic Bus / Blackboard] <-> [Experts: Physics/HPC, Code/Mid-GPU, Language/CPU] -> [Fusion Layer Delta Check + Micro-Iterations] -> [Final Answer + Audit Log + Provenance] -> [RL Self-Optimization LoRA]
```

See `docs/diagrams/` for DE/EN architecture images.

## Repo Structure

```
/schemas/          - All JSON Schemas (Router, DAG Node, Blackboard Pattern, Expert Output E_i, Final Answer)
/src/router/       - TMR Router A,B,C + Voting
/src/decomposer/   - DAG Builder
/src/blackboard/   - Semantic Bus / Blackboard Publish/Subscribe
/src/experts/      - Isolated domain models: physics, code, language
/src/fusion/       - Deterministic Fusion with Delta Check
/src/observability/- Prometheus metrics, OpenTelemetry tracing
/configs/          - Hardware mapping, budgets
/docs/             - Full dossiers DE/EN + PDFs
```

## Quick Start MVP

```bash
# Phase 0 MVP - 1 Router + 2 Experts + In-Memory Blackboard
docker-compose up --build
python src/router/tmr_router.py --request "Write Python simulation for heat exchanger"
python -m pytest tests/
```

## Formal Output

Every expert returns: E_i(T_i) = (y_i, c_i, t_i, model_hash, provenance)

Fusion checks: delta = |c_physics - c_code|, type_check, unit_check. On fail: Constraint -> Re-run only failing module, max 3 iterations.

## Dossiers

- `DCA-01-COMPLETE.md` - German complete dossier
- `DCA-01-COMPLETE_EN.md` - English complete dossier
- `docs/DCA-01-*.pdf` - PDF versions

## License

MIT - Open Spec for industrial implementation
