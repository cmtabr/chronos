#!/usr/bin/env bash
# Gera segredos e grava um único .env na raiz do repositório (Compose + pydantic-settings).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

readonly GREEN=$'\e[92m'
readonly PURPLE=$'\e[35m'
readonly ORANGE=$'\e[38;5;208m'
readonly RESET=$'\e[0m'
readonly WHITE=$'\e[97m'

readonly ENV_FILE=".env"

secret_generator() {
  python3 -c 'import secrets; print(secrets.token_urlsafe(64))'
}

loading_spinner() {
  local pid=$1
  local delay=0.1
  local spinstr='|/-\'

  tput civis 2>/dev/null || true
  while kill -0 "${pid}" 2>/dev/null; do
    local temp=${spinstr#?}
    printf " ${PURPLE}[%c]${RESET}  " "${spinstr:0:1}"
    spinstr=${temp}${spinstr%"$temp"}
    sleep "${delay}"
    printf '\b\b\b\b\b\b'
  done
  printf '    \b\b\b\b'
  tput cnorm 2>/dev/null || true
}

add_var() {
  local var=$1
  local value=$2

  printf "${PURPLE}Adding %s ${RESET}" "${var}"
  (sleep 0.7) &
  loading_spinner "$!"

  printf "\r${PURPLE}Adding %s${RESET}\n" "${var}"
  printf '%s=%s\n' "${var}" "${value}" >>"${ENV_FILE}"
}

printf "${ORANGE}Generating environment file${RESET}\n"
printf "${WHITE}----------------------------${RESET}\n"

printf '%s\n' \
  '# Chronos — local environment (Docker Compose env_file + pydantic-settings)' \
  >"${ENV_FILE}"

printf '\n%s\n' '# Auth (AUTH_ prefix in app)' >>"${ENV_FILE}"
add_var "AUTH_SECRET" "$(secret_generator)"
add_var "AUTH_ALGORITHM" "HS256"

printf '\n%s\n' '# Postgres' >>"${ENV_FILE}"
add_var "POSTGRES_USER" "postgres"
add_var "POSTGRES_PASSWORD" "password"
add_var "POSTGRES_HOST" "postgres" # Compose service name (API container)
add_var "POSTGRES_PORT" "5432"
add_var "POSTGRES_DATABASE" "database"

printf '\n%s\n' '# Redis (reserved for future services / libs)' >>"${ENV_FILE}"
add_var "REDIS_HOST" "redis"
add_var "REDIS_PORT" "6379"
add_var "REDIS_USERNAME" "default"
add_var "REDIS_PASSWORD" "password"
add_var "REDIS_DB" "fastapi-auth-redis"

printf '\n%sEnvironment setup | Variables written to %s%s\n' \
        "${GREEN}" "${ENV_FILE}" "${RESET}"
