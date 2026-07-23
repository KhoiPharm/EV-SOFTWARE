"""Establish the Alembic migration baseline without domain tables.

Revision ID: 0001_bootstrap
Revises:
Create Date: 2026-07-24
"""

from __future__ import annotations

from collections.abc import Sequence

revision: str = "0001_bootstrap"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create no application tables; Alembic owns schema versioning from this point."""


def downgrade() -> None:
    """Remove no application data because the bootstrap migration creates none."""
