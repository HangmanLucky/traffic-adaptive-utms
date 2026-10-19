# Functional Test Procedure — Adaptive Traffic Intersection Control

**Project:** Adaptive Urban Traffic Management System (UTMS)
**Document type:** Factory Acceptance Test (FAT) — simulated / desktop validation
**Author:** Sipho Lucky Sibanda

| # | Test Case | Precondition | Action | Expected Result | Pass/Fail |
|---|------------|----------------|---------|--------------------|-------------|
| 1 | Minimum green is enforced | NS green, just started | Remove all NS demand immediately | NS stays green until `MinGreen_PT` elapses regardless of demand loss | |
| 2 | Gap-out ends green with no further demand | NS green, past minimum, no new arrivals | Wait `GapTimeout_PT` with no loop actuation | Transitions to yellow once the gap timer expires | |
| 3 | Vehicle extension resets the gap timer | NS green, past minimum | Pulse `DI_Loop_N` just before gap-out | Gap timer resets; green continues | |
| 4 | Maximum green is a hard ceiling | NS green, continuous vehicle arrivals (gap never expires) | Wait `MaxGreen_PT` | Transitions to yellow at the ceiling regardless of continued demand | |
| 5 | Resting in green when the cross-street is empty | EW just cleared, no NS demand | Observe | Returns to serving the side with demand rather than cycling through an empty phase | |
| 6 | Longest-wait fairness override | EW green continuously (steady traffic), NS demand waiting beyond `MaxWait_PT` | Observe | EW green ends early (once its own `MinGreen_PT` is satisfied) in favour of NS | |
| 7 | Pedestrian clearance cannot be cut short | WALK active, pedestrian clearance timer running | Force all vehicle demand to zero | Phase does not leave green until `PedClearance_PT` has elapsed | |
| 8 | Emergency preemption interrupts normal operation | EW green | Force `DI_EVP_N = TRUE` | Transitions through `PH_PREEMPT_TRANSITION` (all red) into `PH_PREEMPT_HOLD` with NS green | |
| 9 | Preemption still respects pedestrian clearance | WALK active when preemption is requested | Force an EVP request mid-WALK | Transition does not begin until the pedestrian clearance interval completes | |
| 10 | Preemption recovery returns to a clean state | Preemption active, then clears | Clear the EVP input | Returns to `PH_ALLRED_1` (not directly to a green) before normal service resumes | |
| 11 | Simultaneous preemption requests resolve to NS | Both `DI_EVP_N` and `DI_EVP_E` asserted together | Observe | NS is held, per the defined priority order | |
| 12 | System disable forces a safe all-red | Any active phase | Force `DI_System_Enable = FALSE` | `CurrentPhase` forces to `PH_ALLRED_1` | |

## Why Test 6 is the one that actually demonstrates "intelligence"

Tests 1 through 4 describe a conventional actuated signal — genuinely useful, but not
distinct from any standard traffic cabinet controller. Test 6 is where this project's
longest-wait registers do something a plain gap-out/max-green controller wouldn't: cut a
green short, inside its own normal operating range, specifically because the *other*
direction's accumulated wait has crossed a fairness threshold. That's the actual
adaptive, demand-responsive behaviour the "intelligent" in the project title refers to.

## How to exercise these tests without physical hardware

As with the rest of this portfolio, these cases were run by forcing input tags in a
PLCSIM-style watch table (or an equivalent CODESYS soft-PLC harness), with loop inputs
pulsed at varying intervals to simulate realistic, irregular vehicle arrivals rather than
only steady or entirely absent demand.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Test performed by | Sipho Lucky Sibanda | |
| Reviewed by | | |
