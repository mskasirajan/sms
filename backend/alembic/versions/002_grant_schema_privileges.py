"""Grant schema privileges to app user

Revision ID: 002
Revises: 001
Create Date: 2026-02-18

Ensures the connecting database user (however configured via DATABASE_URL)
can SELECT/INSERT/UPDATE/DELETE on all tables and use all sequences.
This is required when migrations are run by a superuser (e.g. postgres) but
the application connects as a less-privileged role.
"""
import re
from alembic import op
from sqlalchemy import text

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def _app_user() -> str:
    """Extract the username from the runtime DATABASE_URL."""
    from app.core.config import settings

    # postgresql://user:pass@host:port/db  or  postgresql+psycopg2://...
    match = re.match(r"[^:]+://([^:@]+)(?::[^@]*)?@", settings.DATABASE_URL)
    if match:
        return match.group(1)
    return "PUBLIC"  # fallback: grant to everyone


def upgrade() -> None:
    user = _app_user()

    op.execute(text(f'GRANT USAGE ON SCHEMA public TO "{user}"'))
    op.execute(text(f'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "{user}"'))
    op.execute(text(f'GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "{user}"'))

    # Cover tables/sequences created by future migrations
    op.execute(text(f'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "{user}"'))
    op.execute(text(f'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "{user}"'))


def downgrade() -> None:
    user = _app_user()

    op.execute(text(f'REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "{user}"'))
    op.execute(text(f'REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM "{user}"'))
    op.execute(text(f'REVOKE USAGE ON SCHEMA public FROM "{user}"'))
