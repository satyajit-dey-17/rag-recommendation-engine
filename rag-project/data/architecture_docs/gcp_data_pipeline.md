# GCP Data Pipeline Architecture Pattern

## Source References
- GCP Data Analytics: https://cloud.google.com/solutions/data-analytics
- BigQuery: https://cloud.google.com/bigquery
- Dataflow: https://cloud.google.com/dataflow
- Cloud Composer: https://cloud.google.com/composer
- GCP Architecture Center Analytics: https://cloud.google.com/architecture/data-lifecycle-cloud-platform

## Use Cases
- Serverless batch and streaming pipelines with unified Apache Beam model
- BigQuery-centric analytics with massive scale SQL
- AI/ML integrated data pipelines with Vertex AI
- Cost-efficient data lake with automatic query optimization
- Real-time analytics on streaming event data

## Recommended Core Services

### Ingestion
- **Cloud Pub/Sub**: Fully managed real-time messaging and event ingestion
- **Dataflow**: Unified batch and streaming pipeline using Apache Beam
- **Cloud Data Fusion**: Visual ETL/ELT pipeline builder (CDAP-based)
- **Cloud Storage Transfer Service**: Bulk data transfer from on-premises or other clouds
- **Database Migration Service**: Managed migration from PostgreSQL, MySQL, SQL Server
- **Pub/Sub Lite**: Cost-optimized high-volume event ingestion

### Storage
- **Cloud Storage**: Central data lake object storage with lifecycle management
- **BigQuery**: Serverless data warehouse and analytics engine
- **BigLake**: Unified storage engine over Cloud Storage and BigQuery
- **Cloud Bigtable**: High-throughput NoSQL for time-series and wide-column data
- **AlloyDB**: PostgreSQL-compatible for transactional and analytical hybrid workloads

### Processing
- **Dataflow**: Managed Apache Beam for unified batch and streaming ETL
- **Dataproc**: Managed Hadoop and Spark clusters for large-scale processing
- **BigQuery SQL**: In-place SQL transformation without moving data
- **Cloud Data Fusion**: No-code/low-code visual data pipeline builder
- **Cloud Functions**: Lightweight event-triggered data processing
- **Dataform**: SQL-based data transformation framework inside BigQuery

### Orchestration
- **Cloud Composer**: Fully managed Apache Airflow for DAG-based orchestration
- **Cloud Workflows**: Serverless workflow orchestration for simpler pipelines
- **Dataform Schedules**: SQL transformation scheduling inside BigQuery
- **Eventarc**: Event-driven pipeline triggering from GCP service events

### Serving and Analytics
- **BigQuery**: Primary analytics engine with petabyte-scale SQL
- **BigQuery ML**: Train and serve ML models directly in SQL inside BigQuery
- **Looker**: Enterprise BI and data exploration (Google-owned)
- **Looker Studio**: Free self-service BI and dashboarding
- **Vertex AI Feature Store**: ML feature storage and serving
- **BigQuery BI Engine**: In-memory analysis layer for sub-second dashboard queries

### Catalog and Governance
- **Dataplex**: Unified data governance, quality, and cataloging across GCP
- **Data Catalog**: Managed metadata catalog with auto-discovery
- **Cloud DLP**: Automated PII detection and data de-identification
- **VPC Service Controls**: Data perimeter enforcement for sensitive datasets
- **BigQuery column-level security**: Fine-grained access at column level

## High Availability Pattern
- Cloud Pub/Sub is globally replicated with 99.99% SLA by default
- BigQuery is a fully managed multi-region serverless service with built-in HA
- Dataflow jobs automatically rebalance work across workers on failure
- Cloud Composer deployed across multiple zones automatically
- Dataproc with preemptible workers for cost efficiency plus standard nodes for HA

## Disaster Recovery Pattern
- Cloud Storage multi-region buckets for data lake DR
- BigQuery cross-region dataset copies for critical warehouse data
- Pub/Sub message retention up to 7 days for replay after pipeline failure
- Cloud Composer DAG definitions stored in Cloud Storage for recovery
- Dataflow checkpointing for resumable streaming pipeline recovery

## Real-World Example
**Twitter (now X) on GCP**: Migrated large portions of data infrastructure
to GCP, uses BigQuery for petabyte-scale analytics on tweet data, Pub/Sub
for real-time event streaming, Dataflow for stream processing pipelines,
and Looker for internal analytics dashboards.

**Spotify on GCP**: Processes over 600TB of data daily, uses Cloud Pub/Sub
for event ingestion from 400M+ users, Dataflow for real-time and batch
processing, BigQuery as the central analytics warehouse, and Cloud Composer
(Airflow) to orchestrate thousands of daily pipeline DAGs.

**The New York Times on GCP**: Runs entire data platform on GCP with
Cloud Storage as the data lake, BigQuery for content analytics, Pub/Sub
for reader event streaming, Dataflow for ETL, and Looker Studio for
editorial and business dashboards.

## Cost Profile
- Cloud Pub/Sub: $0.04/GB after first 10GB/month free
- Dataflow: $0.056/vCPU/hour + $0.003557/GB/hour for batch
- BigQuery Storage: $0.020/GB/month active, $0.010/GB/month long-term
- BigQuery Queries: $5/TB scanned (use partitioning + clustering to reduce)
- BigQuery Editions (Enterprise): slot-based pricing ~$0.06/slot/hour
- Cloud Composer: ~$0.10/hour for small environment + underlying GKE
- Dataproc: cluster cost + 1 cent/vCPU/hour Dataproc premium
- Sustained use discounts apply automatically on Dataproc and Composer

## Strengths
- BigQuery is the best serverless data warehouse of any cloud provider
- Dataflow unified batch and streaming model reduces pipeline complexity
- BigQuery ML enables ML model training without moving data
- Pub/Sub is the simplest and most reliable event ingestion service
- Looker provides the most powerful semantic layer for enterprise BI
- Dataplex gives unified governance across all GCP storage services
- Serverless pricing on BigQuery and Dataflow scales to zero
- Best AI/ML integration via Vertex AI for ML-enriched pipelines

## Weaknesses
- Cloud Data Fusion less mature than Azure Data Factory for visual ETL
- Dataproc cluster management adds operational overhead vs serverless
- Cloud Composer (Airflow) can be expensive for small pipeline workloads
- Smaller connector library than Azure Data Factory for enterprise sources

## Best For
- Data teams wanting the best serverless analytics warehouse (BigQuery)
- Organizations building AI/ML enriched data pipelines with Vertex AI
- Teams wanting unified batch and streaming with a single Beam/Dataflow model
- Cost-conscious teams benefiting from BigQuery scale-to-zero query pricing
- Analytics-first organizations where SQL is the primary transformation tool
- Startups and scale-ups wanting minimal infrastructure management