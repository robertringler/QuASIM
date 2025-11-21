"""Formal verification utilities for QNX-AGI.

This package provides deterministic interval arithmetic, abstract interpretation,
symbolic execution scaffolding, and bridges to formal tools such as TLA+ and
Isabelle/HOL. All utilities are deterministic and side-effect free to remain
compatible with safety-critical environments.
"""

from .interval_arithmetic import Interval, IntervalEnvironment, propagate_affine
from .abstract_interpretation import AbstractLattice, AbstractState
from .symbolic_execution import SymbolicExecutor, PathConstraint
from .model_checking import ModelChecker, TLASpecification
from .theorem_proving import IsabelleGoal, ProofObligation
from .runtime_monitor import RuntimeInvariant, RuntimeMonitor
from .safety_case import SafetyCase, SafetyClaim

__all__ = [
    "Interval",
    "IntervalEnvironment",
    "propagate_affine",
    "AbstractLattice",
    "AbstractState",
    "SymbolicExecutor",
    "PathConstraint",
    "ModelChecker",
    "TLASpecification",
    "IsabelleGoal",
    "ProofObligation",
    "RuntimeInvariant",
    "RuntimeMonitor",
    "SafetyCase",
    "SafetyClaim",
]
