# Distributed Document Search Service

A prototype distributed, multi-tenant document search service capable of indexing and searching millions of documents with sub-second latency.

The system demonstrates key architectural patterns used in large-scale backend systems including horizontal scalability, tenant isolation, distributed search indexing, caching, and rate limiting.

---

## Features

* Multi-tenant architecture
* Full-text document search
* Fuzzy search support
* Highlighted search results
* Redis-based caching
* Redis-based rate limiting per tenant
* Elasticsearch-powered search indexing
* PostgreSQL as system of record
* Docker-based local deployment

---

## System Architecture

Client → FastAPI API → Redis → Elasticsearch → PostgreSQL

* **FastAPI** handles API requests and orchestrates services
* **PostgreSQL** stores the source-of-truth document data
* **Elasticsearch** provides fast full-text search capabilities
* **Redis** provides caching and rate limiting
* **Docker Compose** orchestrates the distributed services

---

## API Endpoints

### Create Tenant

POST /tenants

Example request:

{
"name": "Acme Corp"
}

---

### Create Document

POST /tenants/{tenant_id}/documents

Example request:

{
"title": "Distributed Systems",
"content": "Elasticsearch uses inverted indexes"
}

---

### Get Document

GET /tenants/{tenant_id}/documents/{id}

---

### Delete Document

DELETE /tenants/{tenant_id}/documents/{id}

---

### Search Documents

GET /tenants/{tenant_id}/search?q=query

Supports:

* Full text search
* Fuzzy search
* Highlighted results

Example:

GET /tenants/1/search?q=distributed

---

## Running the System

Start all services using Docker:

docker compose up --build

Services started:

* FastAPI API
* PostgreSQL
* Redis
* Elasticsearch

Swagger documentation:
- Swagger API Docs: http://localhost:8000/docs  
- Elasticsearch: http://localhost:9200

## Technology Stack

FastAPI
PostgreSQL
Elasticsearch
Redis
Docker

---

## AI Tool Usage

AI tools were used to assist with:

* architectural brainstorming
* boilerplate generation
* documentation refinement

All architectural decisions and implementations were validated manually.
