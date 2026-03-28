# GCP Web API and Containerized Application Architecture

## Source References
- GCP Cloud Architecture Center: https://docs.cloud.google.com/architecture
- GCP Three-Tier Web App Jump Start: https://docs.cloud.google.com/architecture/application-development/three-tier-web-app
- GCP Cloud Run Documentation: https://cloud.google.com/run
- GCP Well-Architected Framework: https://cloud.google.com/architecture/framework

## Use Cases
- Developer-friendly containerized APIs and microservices
- Data-intensive and analytics-heavy applications
- AI/ML integrated workloads
- Cost-sensitive startups and scale-ups
- Modern three-tier web applications

## Recommended Core Services

### Compute
- **Cloud Run**: Fully managed serverless containers, scales to zero, pay per request
- **Google Kubernetes Engine (GKE)**: Managed Kubernetes with Autopilot mode
- **Cloud Functions**: Serverless event-driven functions
- **Cloud Endpoints / API Gateway**: Managed API gateway with OpenAPI support

### Database
- **Cloud SQL for PostgreSQL**: Managed PostgreSQL with HA and read replicas
- **AlloyDB**: PostgreSQL-compatible, 4x faster than standard PostgreSQL for analytics
- **Cloud Spanner**: Globally distributed relational database with 99.999% SLA
- **Firestore**: Serverless NoSQL document database
- **Memorystore (Redis)**: Managed Redis for caching and session storage

### Storage
- **Cloud Storage**: Object storage for assets, backups, and data lake
- **Filestore**: Managed NFS file storage
- **Artifact Registry**: Private container image and package registry

### Networking
- **VPC**: Global virtual private cloud with subnets per region
- **Cloud Load Balancing (HTTPS)**: Global anycast load balancer
- **Cloud CDN**: Content delivery network integrated with load balancing
- **Cloud DNS**: Managed DNS with low-latency global resolution
- **Cloud Armor**: WAF and DDoS protection at the load balancer layer
- **Serverless VPC Access**: Private connectivity from Cloud Run to VPC resources

### Security
- **IAM**: Resource-level identity and access management
- **Secret Manager**: Managed secrets and API key storage with versioning
- **Cloud KMS**: Customer-managed encryption keys
- **VPC Service Controls**: Perimeter security for sensitive data
- **Binary Authorization**: Policy enforcement for container deployments

### Observability
- **Cloud Monitoring**: Metrics, dashboards, and alerting
- **Cloud Logging**: Centralized structured log aggregation
- **Cloud Trace**: Distributed tracing for microservices
- **Error Reporting**: Automated exception tracking and grouping
- **Cloud Profiler**: Continuous production CPU and memory profiling

### CI/CD
- **Cloud Build**: Fully managed CI/CD with native GCP integration
- **Artifact Registry**: Source of truth for container images
- **Cloud Deploy**: Managed continuous delivery to GKE and Cloud Run

## High Availability Pattern
- Deploy Cloud Run services to multiple regions with traffic splitting
- Cloud SQL HA with synchronous standby in a different zone
- Global HTTPS Load Balancer with health checks and automatic failover
- Memorystore Redis with read replicas across zones
- Serverless VPC Access for private Cloud Run to Cloud SQL connectivity

## Disaster Recovery Pattern
- Cloud SQL automated backups and point-in-time recovery
- Cross-region Cloud SQL read replicas for fast promotion
- Cloud Storage multi-region buckets for object durability
- Cloud Spanner multi-region instances for zero-RPO globally distributed data
- Global load balancer automatically reroutes traffic on regional failure

## Real-World Deployed Example
**Spotify on GCP**: Migrated from own data centers to GCP, running on GKE
with BigQuery for analytics, Cloud Storage for media assets, and Cloud Pub/Sub
for event streaming across microservices. Processes petabytes of data daily.

**Snapchat on GCP**: One of the largest GCP customers, runs core application
on GCP Compute and GKE, uses Cloud Storage for snaps and stories,
and BigQuery for analytics and ML model training.

**HSBC on GCP**: Uses Cloud Run for containerized banking APIs, Cloud SQL
for transactional data, Cloud Armor for DDoS and WAF protection, and
VPC Service Controls for regulatory data perimeter enforcement.

## Three-Tier Web App Reference (GCP Jump Start)
Frontend and middleware layers containerized and deployed to Cloud Run as
separate serverless services. Cloud SQL attached to customer VPC with internal
IP address only. Serverless VPC Access provides private connectivity from
Cloud Run to Cloud SQL so database traffic never traverses the internet.
Cloud Armor provides WAF and DDoS at the HTTPS Load Balancer layer.

## Cost Profile
- Cloud Run: $0.00002400/vCPU/second + $0.00000250/GB/second (scales to zero)
- Cloud SQL PostgreSQL db-standard-2 (2 vCPU, 7.5 GB): ~$85-100/month
- HTTPS Load Balancer: ~$0.025/hour + $0.008/GB processed
- Cloud Storage: $0.020/GB/month for standard storage
- Sustained use discounts apply automatically (up to 30% off)
- Committed use contracts reduce compute costs up to 57%

## Compliance Certifications
HIPAA, SOC 1/2/3, PCI DSS, ISO 27001, FedRAMP, GDPR, CJIS,
DoD IL2/IL4, Australia IRAP

## Strengths
- Best developer experience for containerized workloads
- Cloud Run scales to zero, ideal for cost-sensitive builds
- Strongest AI/ML platform (Vertex AI, BigQuery ML, TPUs)
- Competitive pricing with automatic sustained use discounts
- Global VPC spans all regions (unique to GCP)
- AlloyDB and Spanner have no AWS/Azure equivalents
- Clean, intuitive console and CLI

## Weaknesses
- Smaller enterprise sales and support presence than AWS or Azure
- Fewer compliance certifications than AWS for niche requirements
- Smaller talent pool than AWS
- Some managed services still maturing compared to AWS equivalents

## Best For
- Developer-first teams prioritizing simplicity and speed
- Cost-sensitive startups and scale-ups
- AI/ML and data-heavy workloads
- Workloads benefiting from Cloud Run scale-to-zero pricing
- Teams wanting the cleanest Kubernetes experience (GKE Autopilot)
- Applications requiring global database consistency (Spanner)