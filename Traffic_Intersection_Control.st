(*
====================================================================================
  PROJECT   : Adaptive Urban Traffic Management System (UTMS)
              Vehicle Loop Sensor Optimization
  MODULE    : FB_Traffic_Intersection_Control
  PLATFORM  : IEC 61131-3 Structured Text
              Written against Siemens SCL (TIA Portal, S7-1500) syntax,
              portable to CODESYS-based traffic cabinet controllers.
  AUTHOR    : Sipho Lucky Sibanda
  CONTEXT   : A fixed-time traffic signal gives every direction the same
              green duration regardless of whether anyone is actually
              there - wasting cycle time on an empty street while the
              opposite approach queues up. This function block runs a
              genuinely actuated intersection: in-pavement loop
              detectors extend green only while vehicles keep arriving,
              a longest-wait register prevents any approach from being
              starved, and an emergency vehicle preemption path can
              safely interrupt normal operation within one scan.

  ENGINEERING BASIS (simulated against, for realism only):
    - NEMA-style actuated signal control concepts: minimum green,
      maximum green, vehicle extension ("gap"), and gap-out - the
      standard vocabulary real traffic cabinet controllers use.
    - Pedestrian clearance interval: once a WALK indication has been
      given, the signal may not leave green (or extend yellow/all-red)
      until the minimum time needed for a pedestrian already in the
      crosswalk to finish crossing has elapsed.
    - Emergency Vehicle Preemption (EVP): a detector (e.g. an Opticom-
      style optical/GPS system) on an approach requests immediate,
      safe right-of-way for an approaching emergency vehicle, cutting
      short the normal cycle through a safe (not abrupt) transition.
====================================================================================
*)

TYPE E_SignalPhase :
(
    PH_NS_GREEN,
    PH_NS_YELLOW,
    PH_ALLRED_1,
    PH_EW_GREEN,
    PH_EW_YELLOW,
    PH_ALLRED_2,
    PH_PREEMPT_TRANSITION,
    PH_PREEMPT_HOLD
);
END_TYPE

FUNCTION_BLOCK FB_Traffic_Intersection_Control
VAR_INPUT
    DI_Loop_N              : BOOL;   // Vehicle present, North approach
    DI_Loop_S                : BOOL;   // Vehicle present, South approach
    DI_Loop_E                  : BOOL;   // Vehicle present, East approach
    DI_Loop_W                    : BOOL;   // Vehicle present, West approach
    DI_PedCall_NS                  : BOOL;   // Pedestrian call button, N-S crosswalk
    DI_PedCall_EW                    : BOOL;   // Pedestrian call button, E-W crosswalk
    DI_EVP_N                           : BOOL;   // Emergency vehicle preemption request, per approach
    DI_EVP_S                             : BOOL;
    DI_EVP_E                               : BOOL;
    DI_EVP_W                                 : BOOL;
    DI_System_Enable                           : BOOL;
END_VAR

VAR_OUTPUT
    DO_NS_Green           : BOOL := FALSE;
    DO_NS_Yellow            : BOOL := FALSE;
    DO_NS_Red                 : BOOL := TRUE;
    DO_EW_Green                  : BOOL := FALSE;
    DO_EW_Yellow                   : BOOL := FALSE;
    DO_EW_Red                        : BOOL := TRUE;
    DO_NS_WalkSignal                   : BOOL := FALSE;
    DO_EW_WalkSignal                     : BOOL := FALSE;
    CurrentPhase                           : E_SignalPhase := PH_ALLRED_1;
    WaitTime_NS_s                            : REAL := 0.0;   // "Which lane has waited longest" registers
    WaitTime_EW_s                              : REAL := 0.0;
    Alarm_PreemptionActive                       : BOOL := FALSE;
    SystemStatus                                   : STRING[28] := 'STANDBY';
END_VAR

VAR
    MinGreen_PT          : TIME := T#8S;
    MaxGreen_PT             : TIME := T#45S;
    GapTimeout_PT             : TIME := T#3S;     // Vehicle extension / "gap" interval
    YellowTime_PT                : TIME := T#3S;
    AllRedTime_PT                   : TIME := T#2S;
    PedClearance_PT                    : TIME := T#12S;
    MaxWait_PT                            : TIME := T#60S;    // Fairness override ceiling

    T_MinGreen             : TON;
    T_MaxGreen               : TON;
    T_Gap                      : TON;
    T_Clearance                   : TON;   // Shared: yellow / all-red / preempt transition
    T_PedClearance                   : TON;
    T_WaitNS                           : TON;
    T_WaitEW                             : TON;

    DemandNS                 : BOOL;
    DemandEW                   : BOOL;
    PedActiveThisPhase            : BOOL;
    EVP_Requested_NS                 : BOOL;
    EVP_Requested_EW                   : BOOL;
    PreemptDirection_IsNS                 : BOOL;
    ReturnPhaseAfterPreempt                  : E_SignalPhase;

    Prev_Loop_N             : BOOL;   Prev_Loop_S : BOOL;
    Prev_Loop_E               : BOOL;   Prev_Loop_W : BOOL;
    AnyNewArrival_NS              : BOOL;
    AnyNewArrival_EW                : BOOL;
END_VAR

// ------------------------------------------------------------------
// 1. DEMAND DETECTION
// ------------------------------------------------------------------
DemandNS := DI_Loop_N OR DI_Loop_S OR DI_PedCall_NS;
DemandEW := DI_Loop_E OR DI_Loop_W OR DI_PedCall_EW;

AnyNewArrival_NS := (DI_Loop_N AND NOT Prev_Loop_N) OR (DI_Loop_S AND NOT Prev_Loop_S);
AnyNewArrival_EW := (DI_Loop_E AND NOT Prev_Loop_E) OR (DI_Loop_W AND NOT Prev_Loop_W);
Prev_Loop_N := DI_Loop_N;  Prev_Loop_S := DI_Loop_S;
Prev_Loop_E := DI_Loop_E;  Prev_Loop_W := DI_Loop_W;

// ------------------------------------------------------------------
// 2. LONGEST-WAIT REGISTERS
//    Accumulate only while that direction has genuine demand and is
//    NOT the one currently green - the literal "which lane has been
//    waiting the longest" counter.
// ------------------------------------------------------------------
T_WaitNS(IN := DemandNS AND (CurrentPhase <> PH_NS_GREEN), PT := MaxWait_PT);
T_WaitEW(IN := DemandEW AND (CurrentPhase <> PH_EW_GREEN), PT := MaxWait_PT);
WaitTime_NS_s := TIME_TO_REAL(T_WaitNS.ET) / 1000.0;
WaitTime_EW_s := TIME_TO_REAL(T_WaitEW.ET) / 1000.0;

// ------------------------------------------------------------------
// 3. EMERGENCY VEHICLE PREEMPTION - evaluated before the normal
//    sequencer, and able to interrupt it from any state.
// ------------------------------------------------------------------
EVP_Requested_NS := DI_EVP_N OR DI_EVP_S;
EVP_Requested_EW := DI_EVP_E OR DI_EVP_W;
Alarm_PreemptionActive := EVP_Requested_NS OR EVP_Requested_EW;

IF Alarm_PreemptionActive AND (CurrentPhase <> PH_PREEMPT_TRANSITION) AND (CurrentPhase <> PH_PREEMPT_HOLD) THEN
    PreemptDirection_IsNS := EVP_Requested_NS;   // NS takes priority if both request simultaneously
    IF PedActiveThisPhase THEN
        // Never cut a pedestrian clearance interval short, even for
        // an emergency vehicle - the transition waits for it.
        ; // T_PedClearance continues running below; transition begins once it completes
    ELSE
        ReturnPhaseAfterPreempt := CurrentPhase;
        CurrentPhase := PH_PREEMPT_TRANSITION;
        T_Clearance(IN := TRUE, PT := YellowTime_PT + AllRedTime_PT);
    END_IF
END_IF

// ------------------------------------------------------------------
// 4. MAIN PHASE STATE MACHINE
// ------------------------------------------------------------------
IF NOT DI_System_Enable THEN
    CurrentPhase := PH_ALLRED_1;
END_IF

CASE CurrentPhase OF

    PH_NS_GREEN:
        DO_NS_Green := TRUE; DO_NS_Red := FALSE; DO_EW_Red := TRUE;
        DO_NS_WalkSignal := TRUE; PedActiveThisPhase := TRUE;
        T_MinGreen(IN := TRUE, PT := MinGreen_PT);
        T_MaxGreen(IN := TRUE, PT := MaxGreen_PT);
        T_Gap(IN := NOT AnyNewArrival_NS, PT := GapTimeout_PT);
        IF AnyNewArrival_NS THEN T_Gap(IN := FALSE); END_IF
        T_PedClearance(IN := TRUE, PT := PedClearance_PT);

        IF T_MinGreen.Q AND T_PedClearance.Q THEN
            // Three independent reasons a green can end, once the
            // non-negotiable minimums (vehicle AND pedestrian) are met:
            IF T_MaxGreen.Q THEN
                CurrentPhase := PH_NS_YELLOW;                                  // Ceiling reached
            ELSIF T_Gap.Q AND (NOT DemandNS) THEN
                CurrentPhase := PH_NS_YELLOW;                                  // Gapped out, no demand left
            ELSIF T_Gap.Q AND DemandEW AND (WaitTime_EW_s >= TIME_TO_REAL(MaxWait_PT)/1000.0) THEN
                CurrentPhase := PH_NS_YELLOW;                                  // Fairness override
            END_IF
        END_IF
        IF CurrentPhase <> PH_NS_GREEN THEN
            DO_NS_WalkSignal := FALSE; PedActiveThisPhase := FALSE;
            T_MinGreen(IN := FALSE); T_MaxGreen(IN := FALSE); T_Gap(IN := FALSE); T_PedClearance(IN := FALSE);
            T_Clearance(IN := TRUE, PT := YellowTime_PT);
        END_IF

    PH_NS_YELLOW:
        DO_NS_Green := FALSE; DO_NS_Yellow := TRUE;
        T_Clearance(IN := TRUE, PT := YellowTime_PT);
        IF T_Clearance.Q THEN
            DO_NS_Yellow := FALSE; DO_NS_Red := TRUE;
            T_Clearance(IN := TRUE, PT := AllRedTime_PT);
            CurrentPhase := PH_ALLRED_1;
        END_IF

    PH_ALLRED_1:
        T_Clearance(IN := TRUE, PT := AllRedTime_PT);
        IF T_Clearance.Q THEN
            T_Clearance(IN := FALSE);
            IF DemandEW THEN
                CurrentPhase := PH_EW_GREEN;
            ELSIF DemandNS THEN
                CurrentPhase := PH_NS_GREEN;   // Nobody waiting across - rest in green, don't waste a cycle
            END_IF
            // If neither has demand, remains in PH_ALLRED_1 (resting at red both ways) until a call arrives.
        END_IF

    PH_EW_GREEN:
        DO_EW_Green := TRUE; DO_EW_Red := FALSE; DO_NS_Red := TRUE;
        DO_EW_WalkSignal := TRUE; PedActiveThisPhase := TRUE;
        T_MinGreen(IN := TRUE, PT := MinGreen_PT);
        T_MaxGreen(IN := TRUE, PT := MaxGreen_PT);
        T_Gap(IN := NOT AnyNewArrival_EW, PT := GapTimeout_PT);
        IF AnyNewArrival_EW THEN T_Gap(IN := FALSE); END_IF
        T_PedClearance(IN := TRUE, PT := PedClearance_PT);

        IF T_MinGreen.Q AND T_PedClearance.Q THEN
            IF T_MaxGreen.Q THEN
                CurrentPhase := PH_EW_YELLOW;
            ELSIF T_Gap.Q AND (NOT DemandEW) THEN
                CurrentPhase := PH_EW_YELLOW;
            ELSIF T_Gap.Q AND DemandNS AND (WaitTime_NS_s >= TIME_TO_REAL(MaxWait_PT)/1000.0) THEN
                CurrentPhase := PH_EW_YELLOW;
            END_IF
        END_IF
        IF CurrentPhase <> PH_EW_GREEN THEN
            DO_EW_WalkSignal := FALSE; PedActiveThisPhase := FALSE;
            T_MinGreen(IN := FALSE); T_MaxGreen(IN := FALSE); T_Gap(IN := FALSE); T_PedClearance(IN := FALSE);
            T_Clearance(IN := TRUE, PT := YellowTime_PT);
        END_IF

    PH_EW_YELLOW:
        DO_EW_Green := FALSE; DO_EW_Yellow := TRUE;
        T_Clearance(IN := TRUE, PT := YellowTime_PT);
        IF T_Clearance.Q THEN
            DO_EW_Yellow := FALSE; DO_EW_Red := TRUE;
            T_Clearance(IN := TRUE, PT := AllRedTime_PT);
            CurrentPhase := PH_ALLRED_2;
        END_IF

    PH_ALLRED_2:
        T_Clearance(IN := TRUE, PT := AllRedTime_PT);
        IF T_Clearance.Q THEN
            T_Clearance(IN := FALSE);
            IF DemandNS THEN
                CurrentPhase := PH_NS_GREEN;
            ELSIF DemandEW THEN
                CurrentPhase := PH_EW_GREEN;
            ELSE
                CurrentPhase := PH_ALLRED_1;   // Rest at red both ways until a call arrives
            END_IF
        END_IF

    PH_PREEMPT_TRANSITION:
        // Safe transition from whatever was running: force red on both
        // until the shared clearance timer (yellow + all-red worth of
        // time) has elapsed, then hold green for the requesting direction.
        DO_NS_Green := FALSE; DO_NS_Yellow := FALSE; DO_NS_Red := TRUE;
        DO_EW_Green := FALSE; DO_EW_Yellow := FALSE; DO_EW_Red := TRUE;
        DO_NS_WalkSignal := FALSE; DO_EW_WalkSignal := FALSE;
        IF T_Clearance.Q THEN
            T_Clearance(IN := FALSE);
            CurrentPhase := PH_PREEMPT_HOLD;
        END_IF

    PH_PREEMPT_HOLD:
        IF PreemptDirection_IsNS THEN
            DO_NS_Green := TRUE; DO_NS_Red := FALSE; DO_EW_Red := TRUE;
        ELSE
            DO_EW_Green := TRUE; DO_EW_Red := FALSE; DO_NS_Red := TRUE;
        END_IF
        IF NOT Alarm_PreemptionActive THEN
            // Emergency vehicle has cleared - return to normal service,
            // starting from a clean all-red rather than resuming mid-phase.
            DO_NS_Green := FALSE; DO_EW_Green := FALSE;
            T_Clearance(IN := TRUE, PT := AllRedTime_PT);
            CurrentPhase := PH_ALLRED_1;
        END_IF

    ELSE
        CurrentPhase := PH_ALLRED_1;
END_CASE

// ------------------------------------------------------------------
// 5. STATUS TEXT
// ------------------------------------------------------------------
IF NOT DI_System_Enable THEN
    SystemStatus := 'STANDBY';
ELSIF Alarm_PreemptionActive THEN
    SystemStatus := 'EMERGENCY PREEMPTION';
ELSE
    CASE CurrentPhase OF
        PH_NS_GREEN, PH_NS_YELLOW:  SystemStatus := 'NS SERVING TRAFFIC';
        PH_EW_GREEN, PH_EW_YELLOW:  SystemStatus := 'EW SERVING TRAFFIC';
        ELSE                          SystemStatus := 'CLEARANCE / ALL RED';
    END_CASE
END_IF

END_FUNCTION_BLOCK
