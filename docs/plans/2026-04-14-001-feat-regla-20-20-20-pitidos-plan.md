---
title: "feat: App mínima de pitidos para regla 20-20-20"
type: feat
status: active
date: 2026-04-14
---

# feat: App mínima de pitidos para regla 20-20-20

## Overview

Construir app de escritorio muy ligera que, mientras esté activa, emita:
- pitido sutil al cumplir cada bloque de 20 minutos
- segundo pitido exactamente 20 segundos después

Objetivo: automatizar regla 20-20-20 durante trabajo continuo sin vigilancia manual del reloj.

## Problem Frame

Usuario necesita señal discreta y confiable para pausas visuales periódicas (miopía). El comportamiento debe ser estricto en temporización y suficientemente simple para dejarla corriendo en segundo plano sin fricción.

## Requirements Trace

- R1. Al iniciar la app, arrancar ciclo de 20 minutos inmediatamente.
- R2. Al minuto 20 exacto del ciclo, emitir pitido 1 (sutil).
- R3. A los 20 segundos exactos tras pitido 1, emitir pitido 2 (sutil).
- R4. Repetir ciclo indefinidamente mientras app esté activa.
- R5. Permitir detener/reanudar temporizador sin cerrar app.
- R6. Mantener pitido de bajo volumen/tono no intrusivo.
- R7. Si sistema entra en sleep o hay bloqueo de evento, recuperar ciclo sin disparos acumulados erróneos.
- R8. Incluir documentación de uso y publicación en repositorio público de GitHub.

## Scope Boundaries

- No sincronización cloud.
- No cuentas de usuario.
- No historial avanzado ni analytics.
- No interfaz compleja; solo controles mínimos de estado.

## Context & Research

### Relevant Code and Patterns

- Repositorio actual vacío; no patrones internos reutilizables.
- Se define baseline técnico nuevo priorizando simplicidad operativa:
  - Python 3.11+
  - Tkinter para UI mínima
  - `time.monotonic()` para temporización robusta
  - reproducción de sonido local corto para pitido sutil

### Institutional Learnings

- No se encontraron `docs/solutions/` ni learnings previos en este repo.

### External References

- Python docs (`time.monotonic`) para scheduling resistente a cambios de reloj del sistema.
- Tkinter docs para loop principal y control de estado.

## Key Technical Decisions

- Temporización basada en reloj monotónico: evita drift por cambios en hora del sistema.
- Scheduler por estados (`FOCUS`, `BREAK20S`): reduce ambigüedad y facilita tests.
- Sonido empaquetado (`assets/beep_soft.wav`) en lugar de beep del sistema: asegura perfil sutil consistente.
- UI mínima con botón Start/Pause y estado visible: cumple uso diario sin distracción.
- Arquitectura local-first sin dependencias remotas: menor fricción para ejecutar siempre.

## Open Questions

### Resolved During Planning

- ¿Desktop o web? Desktop; web no garantiza pitido fiable en background sin pestaña activa.
- ¿Motor de tiempo? `time.monotonic()` con tick corto.
- ¿Nivel de complejidad UI? Mínimo viable (estado + start/pause + salida).

### Deferred to Implementation

- Ajuste final de volumen/frecuencia del `beep_soft.wav` según percepción real.
- Frecuencia exacta de polling del loop (p. ej. 100ms vs 250ms) tras pruebas de precisión/consumo.

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

```text
Estados:
  FOCUS_20M -> (t >= focus_deadline) -> BEEP_1 + BREAK_20S
  BREAK_20S -> (t >= break_deadline) -> BEEP_2 + FOCUS_20M (nuevo ciclo)

Eventos:
  START: inicializa deadlines desde now_monotonic
  PAUSE: congela elapsed restante por estado
  RESUME: recompone deadlines desde now_monotonic
  TICK: evalúa transición por deadlines
```

## Implementation Units

- [ ] **Unit 1: Bootstrap de proyecto y contratos de configuración**

**Goal:** Establecer estructura base de app, configuración temporal y contratos de estado.

**Requirements:** R1, R4, R8

**Dependencies:** None

**Files:**
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `src/twenty20_beeper/__init__.py`
- Create: `src/twenty20_beeper/config.py`
- Create: `src/twenty20_beeper/models.py`
- Create: `tests/test_config.py`

**Approach:**
- Declarar constantes por defecto (`FOCUS_SECONDS=1200`, `BREAK_SECONDS=20`).
- Modelar estados del temporizador y evento de transición.
- Documentar cómo ejecutar localmente.

**Execution note:** Start con tests unitarios de configuración y validación de constantes.

**Patterns to follow:**
- Convención estándar src-layout en Python.

**Test scenarios:**
- Happy path: carga de configuración por defecto -> valores 1200/20.
- Edge case: override inválido (valor <= 0) -> error de validación.
- Error path: config incompleta -> fallback explícito a defaults.

**Verification:**
- Estructura de proyecto utilizable y tests de config en verde.

- [ ] **Unit 2: Motor de temporización estricto 20m+20s**

**Goal:** Implementar scheduler determinista con reloj monotónico y máquina de estados.

**Requirements:** R1, R2, R3, R4, R7

**Dependencies:** Unit 1

**Files:**
- Create: `src/twenty20_beeper/timer_engine.py`
- Create: `tests/test_timer_engine.py`

**Approach:**
- Mantener deadlines absolutos monotónicos por estado.
- En transición `FOCUS -> BREAK`, emitir evento `BEEP_1`.
- En transición `BREAK -> FOCUS`, emitir evento `BEEP_2` y reprogramar siguiente ciclo.
- Manejar sleep/lag con estrategia de “advance to current state” sin cola de pitidos atrasados.

**Execution note:** Implement new domain behavior test-first.

**Technical design:** *(directional)*
- Simular timeline monotónico en tests para validar exactitud de transiciones y no-drift.

**Patterns to follow:**
- State machine simple con transición explícita y eventos inmutables.

**Test scenarios:**
- Happy path: start en t=0 -> beep1 en t=1200 -> beep2 en t=1220 -> nuevo ciclo.
- Edge case: pause en foco y resume -> conserva restante correcto.
- Edge case: pause durante ventana 20s y resume -> respeta restante de break.
- Error path: tick con tiempo retrocedido/invalidado -> ignora transición y registra warning interno.
- Integration: múltiples ciclos consecutivos (>=3) -> período estable sin drift acumulado.
- Integration: salto largo por sleep (p. ej. +600s durante foco) -> no lanza pitidos en ráfaga; estado queda consistente al presente.

**Verification:**
- Suite de temporizador valida precisión de ciclo, pausa/reanudación y robustez ante saltos temporales.

- [ ] **Unit 3: Subsistema de audio sutil y consistente**

**Goal:** Emitir pitidos discretos con latencia baja y volumen moderado.

**Requirements:** R2, R3, R6

**Dependencies:** Unit 2

**Files:**
- Create: `assets/beep_soft.wav`
- Create: `src/twenty20_beeper/audio.py`
- Create: `tests/test_audio.py`

**Approach:**
- Cargar asset local único y reproducir en eventos `BEEP_1/BEEP_2`.
- Aislar backend de audio detrás de interfaz simple para mockear en tests.
- Definir estrategia fallback si reproducción falla (log y continuidad del ciclo).

**Patterns to follow:**
- Adapter pattern para I/O periférico (audio).

**Test scenarios:**
- Happy path: evento `BEEP_1` -> llamada única a backend de reproducción.
- Happy path: evento `BEEP_2` -> llamada única a backend de reproducción.
- Error path: backend lanza excepción -> app no se detiene; error queda registrado.
- Integration: timer_engine + audio adapter -> dos reproducciones por ciclo completo.

**Verification:**
- Audio se dispara en momentos correctos, con tolerancia temporal definida y sin romper loop.

- [ ] **Unit 4: UI mínima y control operativo diario**

**Goal:** Proveer ventana simple para activar, pausar y observar estado del ciclo.

**Requirements:** R4, R5

**Dependencies:** Unit 2, Unit 3

**Files:**
- Create: `src/twenty20_beeper/app.py`
- Create: `src/twenty20_beeper/ui.py`
- Create: `tests/test_ui_state.py`

**Approach:**
- Ventana compacta con:
  - estado actual (`Focus` / `Break 20s` / `Paused`)
  - countdown
  - botón Start/Pause
  - botón Exit
- Tick UI desacoplado de motor para refresco estable.

**Patterns to follow:**
- Separación controller (timer/audio) vs view (Tkinter widgets).

**Test scenarios:**
- Happy path: Start -> estado cambia a Focus con countdown decreciente.
- Happy path: transición automática a Break y regreso a Focus visible en UI.
- Edge case: múltiples clics rápidos Start/Pause -> no duplica timers internos.
- Error path: excepción en refresh de UI -> fallback controlado sin cierre abrupto.
- Integration: UI + timer_engine + audio -> secuencia completa observable.

**Verification:**
- Uso diario posible sin CLI; controles responden y estado es coherente.

- [ ] **Unit 5: Empaquetado, documentación y publicación GitHub pública**

**Goal:** Dejar app ejecutable, documentada y publicada en repo público.

**Requirements:** R8

**Dependencies:** Unit 1, Unit 2, Unit 3, Unit 4

**Files:**
- Modify: `README.md`
- Create: `.gitignore`
- Create: `scripts/run_local.sh`
- Create: `.github/workflows/ci.yml`
- Create: `docs/usage.md`
- Create: `docs/release.md`

**Approach:**
- Documentar instalación/ejecución local, comportamiento exacto 20-20-20 y troubleshooting.
- Configurar CI para tests unitarios básicos.
- Preparar checklist de publicación:
  - inicializar git
  - commit base
  - crear repo público en GitHub
  - push main

**Patterns to follow:**
- README de proyecto Python simple con quickstart + arquitectura breve.

**Test scenarios:**
- Happy path: entorno limpio sigue quickstart -> app arranca sin pasos ocultos.
- Error path: dependencia faltante -> mensaje claro en docs de resolución.
- Integration: CI ejecuta tests y falla correctamente ante regresión.

**Verification:**
- Repositorio público accesible con instrucciones reproducibles y CI operativa.

## System-Wide Impact

- **Interaction graph:** UI -> timer_engine -> audio adapter; config compartida por engine/UI.
- **Error propagation:** Fallo audio o UI no debe romper scheduler; errores se aíslan por capa.
- **State lifecycle risks:** Riesgo de timers duplicados tras pause/resume; mitigación con fuente única de verdad en engine.
- **API surface parity:** Contratos internos (`tick`, `start`, `pause`, `resume`) deben mantenerse consistentes entre engine y UI.
- **Integration coverage:** Validar flujo extremo a extremo de transición temporal + sonido + render de estado.
- **Unchanged invariants:** Regla base 20m + 20s fija por defecto; no se introduce lógica adaptativa ni sincronización externa.

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Drift temporal por loop UI | Deadline monotónico absoluto + tests multi-ciclo |
| Pitido demasiado alto o molesto | Asset dedicado y ajuste iterativo de beep_soft.wav |
| Comportamiento extraño tras sleep del sistema | Política explícita de recuperación de estado al presente |
| Fricción de instalación en máquina nueva | Quickstart mínimo + script de arranque + CI |

## Documentation / Operational Notes

- Incluir nota de salud visual: app es recordatorio conductual, no tratamiento médico.
- Incluir sección “modo trabajo”: dejar app abierta y no pausar salvo descanso largo.
- Añadir guía breve para autoarranque opcional en sistema operativo (fase posterior, fuera de alcance MVP).

## Sources & References

- Related code: `src/twenty20_beeper/timer_engine.py`
- Related code: `src/twenty20_beeper/audio.py`
- External docs: https://docs.python.org/3/library/time.html#time.monotonic
- External docs: https://docs.python.org/3/library/tkinter.html
