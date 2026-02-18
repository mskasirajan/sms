# PostgreSQL User Best Practices

## Rule: Never use the superuser (`postgres`) in production

The application must connect as a **dedicated, least-privilege role**.
The superuser is reserved for administration and migrations only.

---

## Two-Role Pattern

| Role | Env var | Permissions | Used by |
|---|---|---|---|
| `sms_app` | `DATABASE_URL` | `SELECT, INSERT, UPDATE, DELETE` | FastAPI app at runtime |
| `sms_migrations` | `MIGRATION_DATABASE_URL` | `CREATE, DROP, ALTER` + DDL | Alembic in CI/CD pipeline |

In **development**, omit `MIGRATION_DATABASE_URL` — Alembic falls back to
`DATABASE_URL`, which keeps local setup simple.

---

## One-Time Provisioning (run as `postgres`)

```sql
-- 1. Create the app runtime user
CREATE ROLE sms_app WITH LOGIN PASSWORD 'strong-random-password';

-- 2. Grant connection and schema access
GRANT CONNECT ON DATABASE sms_db TO sms_app;
GRANT USAGE ON SCHEMA public TO sms_app;

-- 3. Grant DML on all existing tables and sequences
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA public TO sms_app;
GRANT USAGE, SELECT
    ON ALL SEQUENCES IN SCHEMA public TO sms_app;

-- 4. Apply the same grants to tables created by future migrations
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sms_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO sms_app;

-- 5. Create the migration user (DDL rights)
CREATE ROLE sms_migrations WITH LOGIN PASSWORD 'other-strong-password';
GRANT ALL ON DATABASE sms_db TO sms_migrations;
GRANT ALL ON SCHEMA public TO sms_migrations;
```

---

## Environment Variables

```dotenv
# .env (development) — one role is fine locally
DATABASE_URL=postgresql://postgres:password@localhost:5432/sms_db

# .env (production) — two separate roles
DATABASE_URL=postgresql://sms_app:strong-random-password@db:5432/sms_db
MIGRATION_DATABASE_URL=postgresql://sms_migrations:other-strong-password@db:5432/sms_db
```

See `.env.example` for the full template.

---

## How It Works in This Codebase

**`app/core/config.py`** exposes a `migration_url` property:

```python
@property
def migration_url(self) -> str:
    return self.MIGRATION_DATABASE_URL or self.DATABASE_URL
```

**`alembic/env.py`** uses `settings.migration_url` (not `DATABASE_URL`)
so the migration and the app always use the credentials they are meant to use.

**`alembic/versions/002_grant_schema_privileges.py`** automatically grants
DML rights to whichever user `DATABASE_URL` specifies, so you never have to
remember to run the `GRANT` statements manually after a fresh migration.

---

## Why This Matters

| Risk | With superuser | With least-privilege role |
|---|---|---|
| SQL injection | Attacker can `DROP TABLE`, `COPY` files, create backdoor users | Attacker can only read/write app data |
| Accidental query | Can destroy schema | Write-only to its own tables |
| Audit logs | All queries look like DBA actions | App queries are clearly distinct |
| Credential leak | Full database compromise | Limited blast radius |

---

## Rotating Passwords

```sql
-- Change the app user password (no downtime if done with connection pooling)
ALTER ROLE sms_app WITH PASSWORD 'new-strong-password';
```

Then update `DATABASE_URL` in your secrets manager and redeploy.
