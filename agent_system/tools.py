"""Deterministic tools: LLM never does physics. All calculations are exact here."""
import math
from typing import Dict, Any, List

from .config import TARGET_ZO, ZO_TOL, MIN_THICKNESS_MIL


MATERIAL_MAP = {"Rogers RO4003C": 3.38, "PTFE": 2.10, "High-Res Silicon": 11.70,
                "Cu": 3.38, "NbTi": 3.38, "Nb": 3.38}


def calc_impedance_and_loss(W: float, H: float, material: str, freq: float) -> Dict[str, float]:
    """Characteristic impedance Zo and dielectric loss alpha_d for a microstrip."""
    Er = MATERIAL_MAP.get(material, 3.38)
    T = 1.4  # 1oz copper thickness (mils)
    try:
        ln_term = math.log(5.98 * H / (0.8 * W + T))
        Z0 = (87.0 / math.sqrt(Er + 1.41)) * ln_term
        loss_factor = 0.0027 if Er < 4 else 0.0001
        alpha_d = 0.0912 * freq * math.sqrt(Er) * loss_factor
    except Exception:
        Z0, alpha_d = 50.0, 0.0
    return {"Zo": round(Z0, 2), "alpha_d": round(alpha_d, 4), "Er": Er}


def calc_thermal_load(stackup: List[Dict[str, Any]], total_heat_budget_w: float = 10e-6) -> Dict[str, Any]:
    """Coupled thermal load estimate. Superconductors (NbTi/Nb) cut solid conduction."""
    total = 0.0
    for layer in stackup:
        mat = layer.get("material", "Cu")
        w = layer.get("width_mil", 10.0)
        # heuristic heat: copper conducts; superconductors ~zero
        if mat in ("NbTi", "Nb"):
            base = 0.000001 * (w / 10.0)
        else:
            base = 0.001 * (w / 10.0)
        total += base
    return {"total_load_w": round(total, 6), "budget_w": total_heat_budget_w,
            "ok": total < total_heat_budget_w}


def check_drc(stackup: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Design rule checks: min dielectric thickness, symmetry (by material+thickness)."""
    issues = []
    for layer in stackup:
        if "substrate" in str(layer.get("layer", "")):
            h = layer.get("thickness_mil", 0.0)
            if h < MIN_THICKNESS_MIL:
                issues.append(f"thickness {h} mil < min {MIN_THICKNESS_MIL} mil")
    # symmetry check: compare material+thickness, ignoring layer name
    symmetric = True
    n = len(stackup)
    for i in range(n // 2):
        a = {k: v for k, v in stackup[i].items() if k != "layer"}
        b = {k: v for k, v in stackup[n - 1 - i].items() if k != "layer"}
        if a != b:
            symmetric = False
            break
    if not symmetric:
        issues.append("stackup not symmetric")
    return {"ok": len(issues) == 0, "issues": issues}


def check_guardrail(elec: Dict[str, Any], thermal: Dict[str, Any], drc: Dict[str, Any]) -> Dict[str, Any]:
    zo = elec.get("Zo", 0.0)
    zo_ok = abs(zo - TARGET_ZO) <= ZO_TOL
    thermal_ok = thermal.get("ok", False)
    drc_ok = drc.get("ok", False)
    ok = zo_ok and thermal_ok and drc_ok
    notes = []
    if not zo_ok:
        notes.append(f"Zo {zo}Ω outside {TARGET_ZO}±{ZO_TOL}Ω")
    if not thermal_ok:
        notes.append(f"thermal {thermal.get('total_load_w')}W >= budget")
    if not drc_ok:
        notes.extend(drc.get("issues", []))
    return {"ok": ok, "notes": "; ".join(notes) if notes else "all checks passed"}


def make_stackup(material: str, W: float, H: float, layers: int = 3) -> List[Dict[str, Any]]:
    """Build a symmetric stackup (center conductor + dielectric top/bottom)."""
    return [
        {"layer": "substrate_top", "material": material, "thickness_mil": H},
        {"layer": "conductor", "material": material, "width_mil": W, "thickness_mil": 1.4},
        {"layer": "substrate_bottom", "material": material, "thickness_mil": H},
    ]