from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from drain_doctor.exceptions import DrainDoctorError
from drain_doctor.models import RawFixture


def load_fixture(fixtures_dir: Path) -> RawFixture:
    path = fixtures_dir / "cluster.json"
    try:
        return RawFixture.model_validate(json.loads(path.read_text()))
    except FileNotFoundError as error:
        raise DrainDoctorError(f"fixture file not found: {path}") from error
    except ValidationError as error:
        raise DrainDoctorError(f"invalid fixture file: {path}: {error}") from error
