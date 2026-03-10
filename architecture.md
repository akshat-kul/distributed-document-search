# System Architecture

## Overview

This system implements a distributed document search service designed to handle millions of documents while providing sub-second search responses.

The architecture separates responsibilities across specialized components to ensure scalability, performance, and maintainability.

---

## High-Level Architecture

Client
│
▼
FastAPI API Layer
│
├── Redis (Caching + Rate Limiting)
│
├── Elasticsearch (Search Engine)
│
└── PostgreSQL (Source of Truth)

---

## Component Responsibilities

### FastAPI API Layer

The API layer handles:

* tenant management
* document CRUD operations
* search queries
* rate limiting enforcement
* cache orchestration

FastAPI was chosen due to its asynchronous architecture, allowing high request concurrency with minimal overhead.

---

### PostgreSQL

PostgreSQL acts as the **system of record** for documents and tenants.

Responsibilities:

* persistent document storage
* relational tenant-document relationships
* transactional guarantees
* data consistency

---

### Elasticsearch

Elasticsearch provides fast full-text search capabilities using **inverted indexes**.

Responsibilities:

* indexing document content
* relevance ranking
* fuzzy search
* search result highlighting

This allows search queries across millions of documents to be executed within milliseconds.

---

### Redis

Redis is used for two purposes:

Caching

* stores frequently requested search results
* reduces repeated Elasticsearch queries

Rate Limiting

* enforces request limits per tenant
* prevents abuse and ensures fair resource usage

---

## Search Flow

Client Request
│
▼
FastAPI
│
▼
Redis Cache Check

If cache hit:
Return cached results

If cache miss:
Query Elasticsearch
│
▼
Cache results in Redis
│
▼
Return response

---

## Document Indexing Flow

Create Document API
│
▼
Store in PostgreSQL
│
▼
Index in Elasticsearch
│
▼
Document becomes searchable

---

## Multi-Tenant Strategy

Tenant isolation is achieved using:

* tenant_id stored on every document
* search queries filtered by tenant_id

Example search filter:

term filter on tenant_id

This ensures tenants cannot access documents belonging to other tenants.

---

## Consistency Model

The system follows an **eventual consistency model**.

Document writes are first stored in PostgreSQL and then indexed in Elasticsearch.

There may be a short delay before newly created documents appear in search results.

This tradeoff allows high-performance search queries while maintaining a reliable system of record.
