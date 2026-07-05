import argparse
from pathlib import Path

from orm.models import Base
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

ROOT_DIR = Path(__file__).resolve().parents[2]
# Centralized persistent DB location under apps/data
DATA_DIR = ROOT_DIR / "apps" / "data"
DB_FILE = DATA_DIR / "task_management.db"
DB_URL = f"sqlite:///{DB_FILE}"
SCHEMA_SQL = Path(__file__).resolve().parent / "sql" / "schema.sql"
SEED_SQL = Path(__file__).resolve().parent / "sql" / "seed" / "sample_seed.sql"


def get_engine(url: str):
    connect_args = {"check_same_thread": False} if url.startswith("sqlite:///") else {}
    return create_engine(url, connect_args=connect_args, future=True)


def validate_schema() -> None:
    engine = get_engine("sqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            )
            tables = [row[0] for row in result]
        print("Schema validation successful. Tables:", ", ".join(tables))
    except SQLAlchemyError as exc:
        raise SystemExit(f"Schema validation failed: {exc}")


def initialize_database(seed: bool = False) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DB_FILE.exists():
        try:
            DB_FILE.unlink()
        except PermissionError:
            print(
                f"Warning: Could not delete existing database file. Will overwrite schema."
            )
    engine = get_engine(DB_URL)
    try:
        Base.metadata.create_all(engine)
        print(f"Initialized database at {DB_FILE}")
        if seed:
            load_seed(engine)
            print("Sample seed data inserted.")
    except SQLAlchemyError as exc:
        raise SystemExit(f"Database initialization failed: {exc}")


def load_seed(engine):
    if not SEED_SQL.exists():
        raise FileNotFoundError(f"Seed file not found: {SEED_SQL}")

    sql = SEED_SQL.read_text(encoding="utf-8")
    raw_connection = engine.raw_connection()
    try:
        raw_connection.executescript(sql)
        raw_connection.commit()
    finally:
        raw_connection.close()


def verify_database() -> None:
    if not DB_FILE.exists():
        raise SystemExit(f"Database file not found at {DB_FILE}")

    engine = get_engine(DB_URL)
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        )
        tables = [row[0] for row in result]
        task_count = connection.execute(text("SELECT COUNT(*) FROM tasks;"))
        task_rows = task_count.scalar_one()
    print("Verification complete.")
    print("Available tables:", ", ".join(tables))
    print(f"Task rows: {task_rows}")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize and validate the Task Management database."
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate schema in memory without writing a file.",
    )
    parser.add_argument(
        "--init", action="store_true", help="Initialize the persistent SQLite database."
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Load sample seed data after initialization.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify the persistent database contains expected tables and seed records.",
    )

    args = parser.parse_args()
    if args.validate:
        validate_schema()
    if args.init:
        initialize_database(seed=args.seed)
    if args.verify:
        verify_database()
    if not any((args.validate, args.init, args.verify)):
        parser.print_help()


if __name__ == "__main__":
    main()
