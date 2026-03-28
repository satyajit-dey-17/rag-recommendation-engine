# Azure Data Pipeline Architecture Pattern

## Source References
- Azure Data Factory: https://learn.microsoft.com/en-us/azure/data-factory/
- Azure Synapse Analytics: https://learn.microsoft.com/en-us/azure/synapse-analytics/
- Azure Architecture Center Analytics: https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/analytics-start-here
- Microsoft Fabric: https://learn.microsoft.com/en-us/fabric/

## Use Cases
- Enterprise ETL/ELT pipelines with visual low-code authoring
- Unified analytics combining data integration, warehousing, and BI
- Real-time event streaming from IoT and operational systems
- Microsoft-stack data modernization from SQL Server and on-premises
- Regulated industry data pipelines requiring strong governance

## Recommended Core Services

### Ingestion
- **Azure Data Factory (ADF)**: Visual ETL/ELT with 90+ connectors, trigger-based scheduling
- **Azure Event Hubs**: High-throughput event streaming, Kafka-compatible
- **Azure IoT Hub**: Managed IoT device ingestion at scale
- **Azure Stream Analytics**: Real-time SQL-based stream processing
- **Azure Data Share**: Secure data sharing across organizations
- **Azure Database Migration Service**: Online migration from on-premises databases

### Storage
- **Azure Data Lake Storage Gen2 (ADLS Gen2)**: Hierarchical namespace object storage
- **Azure Blob Storage**: General object storage with lifecycle management
- **Azure Synapse Analytics**: Unified analytics workspace with dedicated SQL pools
- **Azure SQL Database**: Relational storage for refined and curated data layers
- **Microsoft Fabric OneLake**: Unified SaaS data lake across all Fabric workloads

### Processing
- **Azure Data Factory Mapping Data Flows**: Code-free Spark-based transformations
- **Azure Synapse Spark Pools**: Managed Apache Spark for large-scale processing
- **Azure Databricks**: Best-in-class managed Spark with Delta Lake support
- **Azure Stream Analytics**: Real-time event stream processing with SQL
- **Azure Functions**: Lightweight event-triggered processing

### Orchestration
- **Azure Data Factory Pipelines**: Visual drag-and-drop pipeline orchestration
- **Azure Synapse Pipelines**: ADF-compatible pipelines inside Synapse workspace
- **Apache Airflow on Azure (MWAA equivalent)**: Managed Airflow via ADF integration
- **Azure Logic Apps**: Low-code workflow automation for data triggers

### Serving and Analytics
- **Azure Synapse Analytics Dedicated SQL Pool**: Enterprise data warehouse
- **Azure Synapse Serverless SQL**: Pay-per-query SQL over ADLS Gen2
- **Azure Analysis Services**: Tabular semantic model for BI tools
- **Power BI**: Industry-leading BI and visualization tightly integrated with Azure
- **Microsoft Fabric**: Unified SaaS analytics platform covering all data workloads
- **Azure Data Explorer (ADX)**: Fast analytics for time-series and log data

### Catalog and Governance
- **Microsoft Purview**: Unified data governance, cataloging, and lineage tracking
- **Azure Policy**: Enforce data residency and compliance rules
- **Azure Private Endpoints**: Keep data pipeline traffic off public internet
- **Azure Monitor + Diagnostic Logs**: Pipeline run monitoring and alerting

## High Availability Pattern
- ADF is a fully managed SaaS service with built-in HA
- Synapse Dedicated SQL Pool with geo-redundant backups
- Event Hubs with zone-redundant namespaces (Premium/Dedicated tier)
- ADLS Gen2 with zone-redundant storage (ZRS) or geo-redundant (GRS)
- Azure Databricks deployed across multiple AZs with auto-scaling clusters

## Disaster Recovery Pattern
- ADLS Gen2 geo-redundant storage with read access (RA-GRS)
- Synapse Dedicated SQL Pool geo-backup with cross-region restore
- ADF pipeline definitions stored in Git for infrastructure-as-code recovery
- Event Hubs geo-disaster recovery with namespace pairing
- Azure Databricks workspace export and cross-region redeployment via ARM

## Real-World Example
**Unilever on Azure**: Global consumer goods company runs enterprise data
platform on Azure Synapse Analytics ingesting data from 400+ factories,
uses ADF for ETL across SAP, Salesforce, and operational databases,
Power BI for executive dashboards, and Microsoft Purview for global
data governance across 190 countries.

**Shell on Azure**: Energy company uses Azure Data Factory for pipeline
orchestration, Azure Databricks for large-scale refinery sensor data
processing, Azure Synapse for analytics, and Microsoft Purview for
data lineage tracking across petabytes of operational data.

**Volkswagen Group on Azure**: Connected vehicle platform uses Azure Event
Hubs to ingest telemetry from millions of vehicles, Azure Stream Analytics
for real-time anomaly detection, ADLS Gen2 as the central data lake, and
Azure Synapse for fleet analytics and reporting.

## Cost Profile
- Azure Data Factory: $1/1000 pipeline runs + $0.25/DIU-hour for data flows
- Event Hubs Standard: ~$0.028/million events + $11/throughput unit/month
- ADLS Gen2: $0.018/GB/month for LRS hot tier
- Synapse Dedicated SQL Pool DW100c: ~$1.51/hour (pause when not in use)
- Synapse Serverless SQL: $5/TB processed
- Azure Databricks Premium: ~$0.40/DBU/hour on Standard_DS3_v2
- Power BI Premium Per User: ~$20/user/month

## Strengths
- Azure Data Factory has the best visual ETL authoring experience of any cloud
- Power BI + Synapse integration is unmatched for enterprise BI
- Microsoft Purview provides the most comprehensive data governance available
- Microsoft Fabric unifies all analytics workloads in one SaaS platform
- Strongest integration with on-premises SQL Server and SAP workloads
- Azure Hybrid Benefit reduces costs for existing Microsoft license holders
- Event Hubs Kafka compatibility enables lift-and-shift of Kafka pipelines

## Weaknesses
- Synapse Dedicated SQL Pool pricing is high for variable workloads
- Azure Databricks is a third-party service (additional cost vs native Spark)
- Microsoft Fabric is still maturing as a unified platform
- Complexity of choosing between ADF, Synapse, and Fabric for new projects

## Best For
- Enterprises with existing Microsoft and SQL Server data investments
- Teams wanting visual low-code ETL with ADF
- Organizations needing unified governance with Microsoft Purview
- Power BI-heavy analytics organizations
- Regulated industries requiring strong data lineage and compliance
- Hybrid scenarios pulling data from on-premises SQL Server into cloud