---
title: Introdução
description: Visão geral do repositório Chronos e como usar esta documentação.
---

## O que é o Chronos

O Chronos é uma API HTTP construída com **FastAPI**. O pacote Python na raiz do repositório (`pyproject.toml`) expõe dependências como Pydantic, SQLAlchemy, psycopg e as extensões do FastAPI para desenvolvimento.

## Onde está o código

- **Entrada da aplicação**: `src/main.py` — cria a app FastAPI, regista routers e handlers de exceção.
- **Routers e esquemas**: sob `src/core/` (por exemplo utilizadores e contratos de API).
- **Domínio e infraestrutura**: `src/domain/` e `src/infrastructure/` (persistência, sessões de base de dados, etc.).

## Documentação OpenAPI

Com o servidor em execução, a interface Swagger/ReDoc configurada em `docs_url` (por exemplo `/api/v1/docs`) documenta e permite testar os endpoints. Este site Starlight complementa esse contrato com texto orientado ao repositório e à arquitetura.

## Este site

As páginas vivem em `docs/src/content/docs/`. Para pré-visualizar localmente, na pasta `docs/` execute `npm install` (se ainda não instalou) e `npm run dev`.
