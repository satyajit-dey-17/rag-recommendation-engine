# AWS Web API and Containerized Application Architecture

## Source References
- AWS Architecture Center: https://aws.amazon.com/architecture/
- AWS Guidance: Containerized and Scalable Web Application: https://aws.amazon.com/solutions/guidance/building-a-containerized-and-scalable-web-application-on-aws/
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/

## Use Cases
- Containerized REST APIs and microservices
- Three-tier web applications (frontend, backend, database)
- Serverless event-driven APIs
- High-traffic consumer applications

## Recommended Core Services

### Compute
- **ECS Fargate**: Serverless containers, no cluster management, auto scaling
- **EKS**: Managed Kubernetes for complex microservice orchestration
- **Lambda**: Serverless functions for event-driven or lightweight APIs
- **API Gateway**: Managed API layer, handles throttling, auth, caching

### Database
- **Amazon RDS for PostgreSQL**: Managed relational DB, Multi-AZ for HA
- **Amazon Aurora PostgreSQL**: 5x faster than standard PostgreSQL, auto-scaling storage
- **DynamoDB**: Fully managed NoSQL, single-digit millisecond latency
- **ElastiCache (Redis)**: In-memory caching layer for session and query caching

### Storage
- **Amazon S3**: Object storage for static assets, backups, logs
- **EFS**: Managed NFS for shared file storage across containers
- **ECR**: Private container image registry

### Networking
- **VPC**: Isolated network with public/private subnets across 2+ AZs
- **Application Load Balancer (ALB)**: Layer 7 load balancing, path-based routing
- **CloudFront**: Global CDN for static assets and API acceleration
- **Route 53**: DNS with health check-based failover routing
- **AWS WAF**: Web application firewall, OWASP top 10 protection

### Security
- **IAM**: Fine-grained roles and policies for all services
- **AWS Secrets Manager**: Secure storage and rotation of DB credentials and API keys
- **ACM**: Free managed TLS certificates
- **Security Groups + NACLs**: Network-level access control
- **AWS Shield**: DDoS protection (Standard free, Advanced paid)

### Observability
- **CloudWatch Logs + Metrics**: Centralized logging and metrics
- **CloudWatch Alarms**: Alerting on thresholds
- **AWS X-Ray**: Distributed tracing for microservices
- **CloudTrail**: API audit logging across all AWS services
- **AWS Config**: Configuration compliance and change tracking

### CI/CD
- **CodePipeline + CodeBuild**: Fully managed CI/CD pipeline
- **ECR**: Container image storage and scanning

## High Availability Pattern
- Deploy ECS services across 2+ Availability Zones
- ALB health checks auto-route away from unhealthy tasks
- RDS Multi-AZ: synchronous standby replica with automatic failover
- Auto Scaling for ECS tasks based on CPU/memory/request count
- ElastiCache Multi-AZ replication group

## Disaster Recovery Pattern
- RDS automated backups (point-in-time recovery up to 35 days)
- Cross-region RDS read replica promotable to primary
- S3 Cross-Region Replication for object storage
- Route 53 latency or failover routing across regions
- AWS Backup for centralized backup management

## Real-World Deployed Example
**Airbnb on AWS**: Uses ECS for containerized microservices, RDS Aurora for relational data,
DynamoDB for high-throughput lookups, CloudFront for global asset delivery, and ElastiCache
for session management. Multi-region active-passive setup with Route 53 failover.

**Netflix on AWS**: Runs on EC2 with Auto Scaling, uses S3 for content storage, DynamoDB
for metadata at scale, and CloudFront as the global CDN. Known for chaos engineering
and multi-region resilience patterns.

## Cost Profile
- Fargate: ~$0.04048/vCPU/hour + $0.004445/GB/hour
- RDS PostgreSQL Multi-AZ db.t3.medium: ~$100-120/month
- ALB: ~$0.008/LCU/hour + $0.018/hour base
- S3: $0.023/GB/month for standard storage
- Savings Plans or Reserved Instances reduce compute costs 30-60%
- Savings Plans reduce compute costs 30-60% with 1 or 3 year commitment
- Spot Instances save up to 90% for fault-tolerant workloads
- AWS Free Tier covers most services for development and testing
- Cost Explorer and AWS Budgets provide granular cost visibility and alerts

## Compliance Certifications
HIPAA, SOC 1/2/3, PCI DSS, FedRAMP, ISO 27001, GDPR, HITRUST

## Strengths
- Largest global infrastructure (30+ regions, 90+ AZs)
- Broadest service catalog of any cloud provider
- Best-in-class container and serverless tooling
- Largest community, talent pool, and third-party ecosystem
- Most compliance certifications available
- Strong free tier for development and testing

## Weaknesses
- Steeper learning curve than GCP or Azure
- Pricing can be complex and unpredictable at scale
- Console UI can be overwhelming for new users

## Best For
- Teams with existing AWS expertise
- Startups to large enterprise scale
- Workloads requiring broad compliance coverage
- Container-first or serverless-first architectures
- High-traffic consumer-facing applications