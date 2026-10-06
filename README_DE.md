# DCA-01 - Deterministische Cluster Architektur

<img width="1344" height="1792" alt="DE" src="https://github.com/user-attachments/assets/70526647-837c-4ef6-a795-c0dd105ed652" />

**Vom monolithischen Modell zum deterministischen KI-Ökosystem**

> Vorlage: Just-in-Sequence Fertigung (Automotive) + Triple-Modular-Redundancy TMR (Avionik) + CAN-Bus / Blackboard + LRU Prinzip

Version: 1.2 COMPLETE DOSSIER | Autor: Emanuel Schaaf | Status: Implementierbar

## Was ist das?

DCA-01 ist eine baufertige Spezifikation für eine KI-Infrastruktur, die:

- **Selbst optimierbar:** Jedes Modul lernt aus seinen eigenen Fehlern via lokalem LoRA, kein globales Retraining
- **Leichter trainierbar:** Lokales Training, isolierte Gewichte, kein Catastrophic Forgetting
- **Schneller & genauer:** Nur relevante Experten aktiv, parallele Inferenz, kalibrierte Confidence c_i
- **Auditierbar:** Jeder Pfad geloggt mit dag_id, model_hash, Provenance - EU AI Act ready

Statt eines Riesenmodells, das bei jedem Token das gesamte Weltwissen mitschleppt, wird ein Cluster aus physisch getrennten, domänenspezialisierten Basis-Modellen über einen deterministischen Datenbus orchestriert.

Kernprinzip: Wissenstransfer findet nicht durch vermischte Gewichte statt, sondern durch getypten Datenaustausch auf einem Shared Context Board (Blackboard). Wie der CAN-Bus in einem Auto.

## Architektur

```text
[User Request] -> [TMR Router 2-aus-3] -> [Task Decomposer DAG] -> [Semantic Bus / Blackboard] <-> [Experten: Physik/HPC, Code/Mid-GPU, Sprache/CPU] -> [Fusions Layer Delta Check + Mikro-Iterationen] -> [Finale Antwort + Audit Log + Provenance] -> [RL Self-Optimization LoRA]
```

Siehe `docs/diagrams/` für Architektur-Bilder in DE/EN.

## Repo Struktur

```text
/schemas/          - Alle JSON Schemas (Router, DAG Node, Blackboard Pattern, Expert Output E_i, Final Answer)
/src/router/       - TMR Router A,B,C + Voting
/src/decomposer/   - DAG Builder
/src/blackboard/   - Semantic Bus / Blackboard Publish/Subscribe
/src/experts/      - Isolierte Domänen-Modelle: Physik, Code, Sprache
/src/fusion/       - Deterministische Fusion mit Delta Check
/src/observability/- Prometheus Metriken, OpenTelemetry Tracing
/configs/          - Hardware Mapping, Budgets
/docs/             - Vollständige Dossiers DE/EN + PDFs
```

## Quick Start MVP

```bash
# Phase 0 MVP - 1 Router + 2 Experten + In-Memory Blackboard
docker-compose up --build
python src/router/tmr_router.py --request "Schreibe Python Simulation für Wärmetauscher"
python -m pytest tests/
```

## Formaler Output

Jeder Experte gibt zurück: E_i(T_i) = (y_i, c_i, t_i, model_hash, provenance)

Fusion prüft: delta = |c_physik - c_code|, type_check, unit_check. Bei Fehlschlag: Constraint -> Re-Run nur für das fehlerhafte Modul, max 3 Iterationen.

## Dossiers

- `DCA-01-COMPLETE.md` - Deutsches vollständiges Dossier
- `DCA-01-COMPLETE_EN.md` - Englisches vollständiges Dossier
- `docs/DCA-01-*.pdf` - PDF Versionen

## Lizenz

MIT - Open Spec für industrielle Umsetzung

[Englische README](README.md)
