# AWS Microservices Architecture Pattern

## Source References
- AWS Microservices: https://aws.amazon.com/microservices/
- AWS Container Services: https://aws.amazon.com/containers/
- AWS App Mesh: https://aws.amazon.com/app-mesh/
- AWS Well-Architected: https://aws.amazon.com/architecture/well-architected/

## Use Cases
- Decomposed backend services communicating over HTTP/gRPC or messaging
- Independent deployments and scaling per service
- Polyglot architectures with different runtimes per service
- High-traffic platforms requiring per-service autoscaling

## Recommended Core Services

### Compute
- **ECS Fargate**: Serverless containers per microservice, no cluster management
- **EKS**: Managed Kubernetes for complex service orchestration
- **AWS Lambda**: Lightweight event-driven microservices
- **App Runner**: Simplified container deployment for individual services

### Service Communication
- **Amazon API Gateway**: External-facing API layer with auth, throttling, routing
- **AWS App Mesh**: Service mesh using Envoy proxy for inter-service traffic
- **AWS Cloud Map**: Service discovery for dynamic service registration
- **Amazon SQS**: Async decoupled messaging between services
- **Amazon SNS**: Fan-out pub/sub messaging
- **Amazon EventBridge**: Event bus for event-driven microservice choreography

### Database (per service)
- **Amazon RDS**: Relational data per service (PostgreSQL, MySQL)
- **DynamoDB**: High-throughput NoSQL per service
- **ElastiCache**: Shared caching layer per service domain
- **Amazon Keyspaces**: Managed Cassandra for wide-column workloads

### Networking
- **VPC with private subnets**: Services communicate privately
- **ALB with path/host routing**: Route traffic to correct service
- **AWS PrivateLink**: Private connectivity between services without internet exposure
- **Transit Gateway**: Hub-and-spoke connectivity across VPCs

### Security
- **IAM roles per service**: Least privilege per microservice task role
- **AWS Secrets Manager**: Per-service secret injection at runtime
- **AWS WAF on API Gateway**: Protect external-facing APIs
- **mTLS via App Mesh**: Mutual TLS between internal services

### Observability
- **AWS X-Ray**: Distributed tracing across service boundaries
- **CloudWatch Container Insights**: ECS/EKS metrics and logs
- **CloudWatch ServiceLens**: Combined tracing, metrics, and logs view
- **AWS Distro for OpenTelemetry**: Standards-based telemetry collection

## High Availability Pattern
- Each service deployed across 2+ AZs via ECS or EKS
- ALB health checks per service with automatic rerouting
- SQS dead-letter queues for failed async messages
- Circuit breaker patterns via App Mesh retries and timeouts
- Per-service auto scaling based on CPU, memory, or SQS queue depth

## Disaster Recovery Pattern
- Multi-region active-passive with Route 53 failover
- DynamoDB global tables for multi-region active-active data
- EventBridge cross-region event replication
- Service-level RTO/RPO definitions per criticality tier

## Real-World Example
**Amazon.com itself**: Pioneered microservices architecture on AWS. Each product
page, cart, checkout, and recommendation engine is a separate service. Uses SQS
for async order processing, DynamoDB for cart and session data, and X-Ray for
distributed tracing across hundreds of services.

**Lyft on AWS**: Runs 300+ microservices on EKS, uses Envoy as service proxy
(which became the basis for App Mesh), SQS for ride event queuing, and
X-Ray for tracing across the entire ride lifecycle.

## Cost Profile
- ECS Fargate per service: ~$0.04048/vCPU/hour + $0.004445/GB/hour
- SQS: First 1M requests/month free, then $0.40/million
- API Gateway REST: $3.50/million API calls
- App Mesh: Free (pay only for underlying compute)
- X-Ray: First 100k traces/month free, then $5/million

## Strengths
- Most mature container and service mesh tooling of any cloud
- EventBridge is best-in-class event bus for microservice choreography
- Deep X-Ray integration across all AWS services
- EKS is production-grade with large community support
- Strong per-service IAM isolation

## Best For
- Large engineering teams with independent service ownership
- Platforms requiring per-service independent scaling
- Teams already on AWS wanting native service mesh and tracing
- Event-driven architectures with complex routing requirements