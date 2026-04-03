#!/usr/bin/env bash
# Creates an Alembic revision and renames the generated file with a date/time prefix.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

readonly VERSIONS_DIR="migrations/versions"

read -r -p "Enter revision message (e.g., users_table_creation): " MSG

MSG_SLUG=$(printf '%s' "$MSG" | tr ' ' '_' | tr -cd '[:alnum:]_')
if [[ -z "$MSG_SLUG" ]]; then
  echo "Error: revision message cannot be empty after normalization." >&2
  exit 1
fi

if [[ ! -d "$VERSIONS_DIR" ]]; then
  echo "Error: directory not found: ${VERSIONS_DIR}" >&2
  exit 1
fi

shopt -s nullglob
mapfile -t before < <(printf '%s\n' "${VERSIONS_DIR}"/*.py | sort -u)

alembic -c migrations/alembic.ini revision -m "${MSG_SLUG}"

mapfile -t after < <(printf '%s\n' "${VERSIONS_DIR}"/*.py | sort -u)

mapfile -t new_files < <(
  comm -13 <(printf '%s\n' "${before[@]}" | sort) <(printf '%s\n' "${after[@]}" | sort)
)

if [[ ${#new_files[@]} -ne 1 ]]; then
  echo "Error: expected exactly one new migration file; found: ${#new_files[@]}." >&2
  exit 1
fi

FILE="${new_files[0]}"
TIMESTAMP=$(date '+%Y-%m-%d_%H:%M:%S')
NEW_FILE="${VERSIONS_DIR}/${TIMESTAMP}_${MSG_SLUG}.py"

mv -- "${FILE}" "${NEW_FILE}"

printf 'Revision file renamed to:\n%s\n' "${NEW_FILE}"
