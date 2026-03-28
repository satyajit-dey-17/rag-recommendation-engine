# Azure Microservices Architecture Pattern

## Source References
- Azure Microservices Architecture: https://learn.microsoft.com/en-us/azure/architecture/microservices/
- Azure Container Apps with Dapr: https://learn.microsoft.com/en-us/azure/container-apps/dapr-overview
- Azure Service Bus: https://learn.microsoft.com/en-us/azure/service-bus-messaging/
- Azure Well-Architected Framework: https://learn.microsoft.com/en-us/azure/well-architected/

## Use Cases
- Enterprise microservices with Microsoft-stack integration
- Event-driven service choreography at scale
- Hybrid microservices connecting on-premises and cloud services
- .NET-based distributed application modernization

## Recommended Core Services

### Compute
- **Azure Container Apps**: Serverless containers with built-in Dapr sidecar support
- **Azure Kubernetes Service (AKS)**: Managed Kubernetes for complex orchestration
- **Azure Functions**: Lightweight event-triggered microservices
- **Azure App Service**: Managed PaaS for individual service hosting

### Service Communication
- **Azure API Management (APIM)**: Enterprise API gateway with policies, versioning, auth
- **Dapr (via Container Apps)**: Sidecar for service discovery, pub/sub, state, secrets
- **Azure Service Bus**: Enterprise messaging with queues and topics (pub/sub)
- **Azure Event Grid**: Event routing for event-driven microservice choreography
- **Azure Event Hubs**: High-throughput event streaming (Kafka-compatible)
- **Azure Service Fabric**: Stateful and stateless microservice runtime

### Database (per service)
- **Azure Database for PostgreSQL Flexible Server**: Relational data per service
- **Azure Cosmos DB**: Globally distributed NoSQL with multiple consistency levels
- **Azure SQL Database**: Managed SQL Server for .NET-aligned services
- **Azure Cache for Redis**: Distributed caching and session storage per service

### Networking
- **VNet with private subnets**: Services communicate over private network
- **Internal Azure Container Apps Environment**: Fully private service-to-service traffic
- **Azure Private Link**: Private endpoints for PaaS services
- **Azure Front Door**: Global load balancing and WAF for external APIs
- **Azure Virtual WAN**: Hub-and-spoke network topology for complex topologies

### Security
- **Azure Active Directory (Entra ID)**: Service-to-service OAuth2 and managed identities
- **Managed Identities**: Passwordless auth from services to Azure resources
- **Azure Key Vault**: Centralized secrets and certificate management
- **Azure Policy**: Governance enforcement across all microservice resources
- **mTLS via Dapr**: Automatic mutual TLS between Dapr-enabled services

### Observability
- **Application Insights**: APM, distributed tracing, dependency tracking
- **Azure Monitor**: Centralized metrics and alerting
- **Log Analytics Workspace**: Centralized structured log querying with KQL
- **Azure Managed Grafana**: Dashboards over Azure Monitor data sources
- **OpenTelemetry with Azure Monitor**: Standards-based telemetry export

## High Availability Pattern
- Container Apps deployed with zone redundancy across AZs
- AKS node pools spread across availability zones
- Service Bus Premium tier with geo-disaster recovery
- Cosmos DB multi-region writes for active-active data layer
- APIM deployed across multiple regions with Traffic Manager

## Disaster Recovery Pattern
- Azure Site Recovery for stateful workload failover
- Cosmos DB automatic multi-region failover
- Service Bus geo-disaster recovery with namespace pairing
- Azure Front Door cross-region routing with health probes
- Blob Storage geo-redundant replication for service artifacts

## Real-World Example
**H&M Group on Azure**: Runs retail microservices on AKS with Azure Service Bus
for order event processing, Cosmos DB for product catalog, and APIM for
partner and internal API management across 74 markets.

**Siemens on Azure**: Industrial IoT microservices on AKS with Event Hubs
ingesting millions of sensor events per second, Azure Functions for event
processing, and Azure Digital Twins for asset modeling across factories.

**Stack Overflow on Azure**: Migrated to Azure with microservices on AKS,
Azure SQL for relational data, Azure Cache for Redis for Q&A caching,
and Application Insights for full-stack distributed tracing.

## Cost Profile
- Container Apps: ~$0.000024/vCPU/second + $0.000003/GB/second
- Service Bus Standard: $0.013/million operations
- Service Bus Premium: ~$677/month per messaging unit
- APIM Developer tier: ~$49/month; Production tier: ~$233/month
- Cosmos DB serverless: $0.25/million RUs consumed
- Event Grid: $0.60/million operations after first 100k free

## Strengths
- Dapr is the most developer-friendly microservice abstraction available
- Azure Service Bus is enterprise-grade with ordering and deduplication
- Managed Identities eliminate secrets for service-to-service auth
- APIM is the most feature-rich API gateway of any cloud provider
- Best choice for .NET microservices with Visual Studio integration
- Strong hybrid story with on-premises service integration via VPN/ExpressRoute

## Weaknesses
- AKS has historically lagged EKS in feature releases
- Container Apps is newer and less battle-tested than ECS/EKS at scale
- APIM can be expensive for smaller teams

## Best For
- Enterprise teams modernizing .NET monoliths into microservices
- Organizations with existing Azure AD and Microsoft licensing
- Workloads requiring enterprise messaging with ordering guarantees
- Teams wanting Dapr abstraction over service mesh complexity
- Hybrid scenarios connecting on-premises services to cloud microservices