# I/O List — Adaptive Urban Traffic Management System

**Project:** Vehicle Loop Sensor Optimization
**Author:** Sipho Lucky Sibanda
**Target platform:** Siemens S7-1500 (TIA Portal / SCL) — portable to a CODESYS-based
traffic cabinet controller

## Inputs

| Tag Name                | Description                                  | Signal Type      | Range / Units       |
|------------------------------|---------------------------------------------------|--------------------|-------------------------|
| `DI_Loop_N` / `_S` / `_E` / `_W` | In-pavement vehicle presence loop, per approach       | Digital (24VDC) x4     | 0/1                        |
| `DI_PedCall_NS`                 | Pedestrian call button, North-South crosswalk             | Digital (24VDC)          | 0/1                          |
| `DI_PedCall_EW`                   | Pedestrian call button, East-West crosswalk                  | Digital (24VDC)            | 0/1                            |
| `DI_EVP_N` / `_S` / `_E` / `_W`     | Emergency vehicle preemption request, per approach              | Digital (24VDC) x4            | 0/1                              |
| `DI_System_Enable`                    | Master enable                                                      | Digital (24VDC)                  | 0/1                                |

## Outputs

| Tag Name                      | Description                              | Signal Type      |
|------------------------------------|------------------------------------------------|--------------------|
| `DO_NS_Green` / `_Yellow` / `_Red`    | North-South signal head                            | Digital x3 |
| `DO_EW_Green` / `_Yellow` / `_Red`      | East-West signal head                                | Digital x3 |
| `DO_NS_WalkSignal` / `DO_EW_WalkSignal`   | Pedestrian WALK indications                             | Digital x2 |
| `CurrentPhase`                               | Current signal phase (enumeration)                         | Internal / HMI tag |
| `WaitTime_NS_s` / `WaitTime_EW_s`               | Longest-wait registers, per direction group                    | REAL x2 |
| `Alarm_PreemptionActive`                           | Emergency vehicle preemption in progress                           | Digital |
| `SystemStatus`                                        | Human-readable status text                                            | STRING |

## Notes for reviewers

- **Timing constants** (`MinGreen_PT`, `MaxGreen_PT`, `GapTimeout_PT`, `YellowTime_PT`,
  `AllRedTime_PT`, `PedClearance_PT`, `MaxWait_PT`) are declared as internal `VAR`
  constants in `Traffic_Intersection_Control.st`. On a real installation, `YellowTime_PT`
  and `AllRedTime_PT` specifically would be calculated per ITE (Institute of
  Transportation Engineers) guidance from the intersection's actual approach speed and
  geometry, not left at illustrative defaults — see the project manual, Chapter 3.
- **This project uses two phases (NS/EW), not four or eight.** A real signalized
  intersection with protected left turns typically runs more phases via a NEMA dual-ring
  structure. The two-phase scope here is a deliberate choice to keep the actuated-control,
  fairness, and preemption logic legible — see the project manual, Chapter 2, for the
  full reasoning.
- `WaitTime_NS_s` / `WaitTime_EW_s` only accumulate while that direction has genuine
  demand (a loop active or a pedestrian call) **and** is not the currently-green
  direction — this is deliberately not a free-running clock.
