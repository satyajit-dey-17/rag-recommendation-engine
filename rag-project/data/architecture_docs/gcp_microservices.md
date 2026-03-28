# GCP Microservices Architecture Pattern

## Source References
- GCP Microservices Architecture: https://cloud.google.com/architecture/microservices-architecture-introduction
- GCP Cloud Run for Microservices: https://cloud.google.com/run/docs/tutorials/deploy-multi-container
- Google Cloud Service Mesh: https://cloud.google.com/service-mesh/docs/overview
- Anthos: https://cloud.google.com/anthos

## Use Cases
- Developer-first containerized microservices with fast iteration cycles
- Event-driven architectures with Pub/Sub choreography
- Polyglot microservices with per-service Cloud Run deployments
- Kubernetes-native microservices on GKE with Anthos Service Mesh

## Recommended Core Services

### Compute
- **Cloud Run**: Fully managed serverless containers per microservice, scales to zero
- **GKE Autopilot**: Managed Kubernetes with fully automated node management
- **GKE Standard**: Full Kubernetes control for complex service orchestration
- **Cloud Functions**: Lightweight event-triggered microservices

### Service Communication
- **Cloud Endpoints / API Gateway**: External-facing managed API layer
- **Anthos Service Mesh (ASM)**: Istio-based service mesh for GKE workloads
- **Cloud Pub/Sub**: Fully managed async messaging and event streaming
- **Eventarc**: Event routing from GCP services to Cloud Run and GKE
- **Cloud Tasks**: Managed task queue for async service invocation
- **gRPC with Cloud Run**: Native gRPC support for high-performance inter-service calls

### Database (per service)
- **Cloud SQL**: Managed PostgreSQL or MySQL per service
- **Firestore**: Serverless NoSQL document database per service domain
- **Cloud Spanner**: Globally consistent relational DB for critical services
- **Bigtable**: High-throughput wide-column store for time-series or analytics services
- **Memorystore (Redis)**: Managed Redis for caching and session per service

### Networking
- **VPC with private subnets**: Services communicate over private Google network
- **Serverless VPC Access**: Private connectivity from Cloud Run to VPC resources
- **Internal Cloud Load Balancing**: Private load balancing between services
- **Cloud Armor**: WAF and DDoS at the external load balancer layer
- **Private Service Connect**: Private connectivity to managed GCP services

### Security
- **IAM with service accounts**: Per-service identity with least privilege
- **Workload Identity**: Kubernetes service accounts mapped to GCP IAM
- **Secret Manager**: Per-service secret injection at runtime
- **Cloud KMS**: Customer-managed encryption keys per service
- **mTLS via Anthos Service Mesh**: Automatic mutual TLS between GKE services
- **Binary Authorization**: Policy enforcement for container image deployments

### Observability
- **Cloud Trace**: Distributed tracing across Cloud Run and GKE services
- **Cloud Monitoring**: Metrics, SLOs, and alerting per service
- **Cloud Logging**: Structured log aggregation with per-service filtering
- **Error Reporting**: Automatic exception grouping and alerting
- **Cloud Profiler**: Continuous CPU and memory profiling in production
- **OpenTelemetry with GCP**: Standards-based telemetry for polyglot services

## High Availability Pattern
- Cloud Run services auto-replicate across zones within a region
- GKE Autopilot spreads pods across zones automatically
- Cloud Pub/Sub is globally replicated with at-least-once delivery
- Cloud SQL HA with synchronous standby in separate zone
- Multi-region Cloud Run with global HTTPS load balancer and health checks

## Disaster Recovery Pattern
- Cloud Run multi-region deployment with traffic splitting
- Cloud SQL cross-region read replicas promotable to primary
- Pub/Sub message retention up to 7 days for replay on recovery
- Cloud Storage multi-region buckets for service artifacts
- Spanner multi-region instances for zero-RPO globally distributed services

## Real-World Example
**Google Maps Platform on GCP**: Runs hundreds of internal microservices on
GKE with Anthos Service Mesh for traffic management and mTLS, Pub/Sub for
location event streaming, and Spanner for globally consistent geo-data storage
serving billions of requests per day.

**Spotify on GCP**: 300+ microservices running on GKE, uses Cloud Pub/Sub
for event streaming between services, BigQuery for analytics, Cloud Storage
for media, and Cloud Trace for distributed tracing across the entire platform.

**Delivery Hero on GCP**: Food delivery platform runs microservices on GKE
Autopilot across multiple regions, uses Pub/Sub for order event choreography,
Cloud SQL per service domain, and Anthos Service Mesh for inter-service mTLS
and traffic policies across 50+ countries.

## Cost Profile
- Cloud Run: $0.00002400/vCPU/second + $0.00000250/GB/second (scales to zero)
- GKE Autopilot: $0.10/vCPU/hour + $0.01/GB/hour (no node management cost)
- Cloud Pub/Sub: $0.04/GB of message throughput after free tier
- Cloud Tasks: $0.40/million task operations
- Eventarc: $0.40/million events after first 100k free
- Anthos Service Mesh: Included with GKE, no extra charge

## Strengths
- Cloud Run is the simplest way to deploy independent microservices
- Scales to zero per service, ideal for cost-sensitive multi-service deployments
- Anthos Service Mesh (Istio) is most mature open-source service mesh available
- Pub/Sub is extremely reliable and cost-effective for async choreography
- GKE has the most mature Kubernetes implementation of any cloud
- Workload Identity is the cleanest service-to-service auth model
- Global VPC means services in different regions share a flat private network

## Weaknesses
- Anthos Service Mesh complexity can be high for smaller teams
- Cloud Run cold starts can affect latency for infrequently called services
- Smaller enterprise support presence than AWS or Azure
- API Gateway product is less mature than AWS API Gateway or Azure APIM

## Best For
- Developer-first teams wanting the simplest microservice deployment model
- Cost-sensitive architectures where scale-to-zero per service saves significantly
- Teams wanting the most mature Kubernetes experience (GKE)
- Event-driven microservices using Pub/Sub choreography
- Polyglot services where each team picks its own runtime and language
- AI/ML integrated microservices leveraging Vertex AI alongside Cloud Run