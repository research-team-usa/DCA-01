# DCA-01 - Deterministische Cluster Architektur

**Vom monolithischen Modell zum deterministischen KI-Ökosystem**

> Vorlage: Just-in-Sequence Fertigung (Automotive) + Triple-Modular-Redundancy TMR (Avionik) + CAN-Bus / Blackboard + LRU Prinzip

Version: 1.2 COMPLETE DOSSIER | Autor: Emanuel Schaaf | Status: Implementierbar

## Was ist das?

DCA-01 ist eine baufertige Spezifikation für eine KI-Infrastruktur die:

- **Selbst optimierbar:** Jedes Modul lernt aus eigenen Fehlern via lokalem LoRA, kein globales Retraining
- **Leichter trainierbar:** Lokales Training, isolierte Gewichte, kein Catastrophic Forgetting
- **Schneller und genauer:** Nur relevante Experten aktiv, parallele Inferenz, kalibrierte Confidence c_i
- **Auditierbar:** Jeder Pfad geloggt mit dag_id, model_hash, Provenance - EU AI Act ready

Statt eines Riesenmodells das bei jedem Token das ganze Weltwissen mitschleppt, orchestriert ein deterministischer Datenbus viele kleine, spezialisierte Modelle.

## Architektur

Siehe `docs/diagrams/` für Diagramme DE/EN.

## Repo Struktur

Gleich wie in README.md beschrieben.

## Quick Start

```bash
docker-compose up --build
```

## Vollständige Dossiers

- `DCA-01-COMPLETE.md`
- `DCA-01-COMPLETE_EN.md`
