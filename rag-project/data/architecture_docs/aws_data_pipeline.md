# AWS Data Pipeline Architecture Pattern

## Source References
- AWS Big Data Analytics: https://aws.amazon.com/big-data/datalakes-and-analytics/
- AWS Glue: https://aws.amazon.com/glue/
- AWS Data Pipeline Patterns: https://aws.amazon.com/architecture/analytics/
- AWS Well-Architected Data Analytics Lens: https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/

## Use Cases
- Batch and streaming data ingestion from multiple sources
- ETL/ELT pipelines transforming raw data into analytics-ready datasets
- Data lake architecture with raw, refined, and curated zones
- Real-time event processing and analytics
- Business intelligence and reporting pipelines

## Recommended Core Services

### Ingestion
- **Amazon Kinesis Data Streams**: Real-time streaming data ingestion
- **Amazon Kinesis Firehose**: Managed delivery of streaming data to S3, Redshift, OpenSearch
- **AWS Glue**: Serverless ETL for batch data ingestion and transformation
- **AWS Database Migration Service (DMS)**: Migrate and replicate databases into data lake
- **Amazon MSK (Managed Kafka)**: Fully managed Apache Kafka for high-throughput streaming
- **AWS Transfer Family**: Managed SFTP/FTP for file-based ingestion

### Storage
- **Amazon S3**: Central data lake storage with lifecycle policies
- **S3 Intelligent-Tiering**: Automatic cost optimization across storage tiers
- **AWS Lake Formation**: Centralized data lake governance and access control
- **Amazon Redshift**: Petabyte-scale data warehouse with columnar storage

### Processing
- **AWS Glue ETL**: Serverless Spark-based batch transformation
- **Amazon EMR**: Managed Hadoop/Spark clusters for large-scale processing
- **AWS Lambda**: Lightweight event-triggered data processing
- **Amazon Kinesis Data Analytics**: SQL or Flink for real-time stream processing
- **AWS Step Functions**: Workflow orchestration for multi-step pipelines

### Orchestration
- **Apache Airflow on MWAA**: Managed Airflow for complex DAG-based pipeline orchestration
- **AWS Step Functions**: Native serverless workflow orchestration
- **AWS Glue Workflows**: Trigger-based ETL job orchestration

### Serving and Analytics
- **Amazon Redshift**: SQL analytics over structured warehouse data
- **Amazon Athena**: Serverless SQL queries directly over S3 data lake
- **Amazon OpenSearch**: Full-text search and log analytics
- **Amazon QuickSight**: Managed BI and visualization tool
- **Amazon SageMaker Feature Store**: ML feature storage and serving

### Catalog and Governance
- **AWS Glue Data Catalog**: Centralized metadata catalog for all data assets
- **AWS Lake Formation**: Fine-grained access control at row and column level
- **Amazon Macie**: Automated PII detection and data classification in S3

## High Availability Pattern
- S3 is 99.999999999% durable with cross-AZ replication by default
- Redshift Multi-AZ cluster for production warehouses
- MSK multi-AZ broker deployment with replication factor 3
- MWAA runs across multiple AZs automatically
- Kinesis Data Streams with multiple shards for parallel processing

## Disaster Recovery Pattern
- S3 Cross-Region Replication for data lake disaster recovery
- Redshift automated snapshots with cross-region copy
- MSK MirrorMaker2 for cross-region Kafka topic replication
- Glue job bookmarks for resumable batch processing after failure
- Step Functions retry and catch logic for pipeline fault tolerance

## Real-World Example
**Netflix Data Pipeline on AWS**: Processes petabytes of viewing data daily
using Kinesis for real-time event ingestion, S3 as the central data lake,
EMR with Spark for batch processing, and Redshift for analytics. Apache Iceberg
table format on S3 enables time-travel queries and schema evolution.

**Airbnb on AWS**: Uses Kinesis Firehose for event streaming, S3 for data lake
storage, EMR for large-scale Spark processing, Redshift for business analytics,
and Athena for ad-hoc SQL queries. MWAA (Airflow) orchestrates thousands
of daily pipeline DAGs across all data domains.

## Cost Profile
- S3 Standard: $0.023/GB/month
- Glue ETL: $0.44/DPU/hour (serverless, pay per job run)
- Kinesis Data Streams: $0.015/shard/hour + $0.014/million PUT records
- Redshift ra3.xlplus node: ~$1.086/hour on-demand
- Athena: $5/TB of data scanned (use Parquet + partitioning to reduce)
- MWAA small environment: ~$0.49/hour
- EMR on EC2: cluster cost + 25% EMR premium on EC2 prices

## Strengths
- Most comprehensive data and analytics service catalog of any cloud
- Athena + S3 + Glue is the most cost-effective serverless analytics stack
- Kinesis ecosystem handles real-time ingestion through to analytics
- Lake Formation provides enterprise-grade data governance
- Deep integration between all analytics services
- Redshift Spectrum queries S3 directly without loading data

## Weaknesses
- Pricing complexity across many services can lead to bill surprises
- EMR cluster management adds operational overhead
- Glue Studio UI is less polished than Azure Data Factory
- Redshift can be expensive for variable workloads vs Athena

## Best For
- Organizations building large-scale data lakes on S3
- Teams needing both real-time and batch processing pipelines
- Workloads requiring serverless SQL analytics with Athena
- Enterprises needing fine-grained data governance with Lake Formation
- Teams already on AWS wanting native integration across analytics services