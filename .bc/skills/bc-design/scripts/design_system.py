"""Focused design-system generation API for the BC Design skill family."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _legacy():
    path = Path(__file__).with_name("bc_design.py")
    spec = importlib.util.spec_from_file_location("bc_design_design_system_compat", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def generate_design_system(query, project_name=None, variance=None, motion=None, density=None):
    """Generate a subject-grounded design direction and implementation checklist."""
    return _legacy().generate_design_system(
        query,
        project_name=project_name,
        variance=variance,
        motion=motion,
        density=density,
    )


def persist_master(data, output_dir=".", page=None, force=False):
    """Persist a generated design contract without overwriting by default."""
    return _legacy().persist_master(data, output_dir=output_dir, page=page, force=force)

