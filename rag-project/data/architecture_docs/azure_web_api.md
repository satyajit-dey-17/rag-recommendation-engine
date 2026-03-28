# Azure Web API and Containerized Application Architecture

## Source References
- Azure Well-Architected Framework: https://learn.microsoft.com/en-us/azure/well-architected/
- Azure Container Apps Best Practices: https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-container-apps
- Azure Architecture Center: https://learn.microsoft.com/en-us/azure/architecture/

## Use Cases
- Enterprise-grade REST APIs and microservices
- Microsoft-stack integrated applications (.NET, SQL Server)
- Hybrid cloud workloads connecting on-premises to cloud
- Government and regulated industry workloads

## Recommended Core Services

### Compute
- **Azure Container Apps**: Fully managed serverless containers with Dapr support
- **Azure Kubernetes Service (AKS)**: Managed Kubernetes for complex orchestration
- **Azure Functions**: Serverless event-driven compute
- **Azure API Management (APIM)**: Enterprise API gateway with policies, auth, throttling

### Database
- **Azure Database for PostgreSQL Flexible Server**: Managed PostgreSQL with zone-redundant HA
- **Azure SQL Database**: Fully managed SQL Server, hyperscale option available
- **Azure Cosmos DB**: Globally distributed NoSQL, multi-model
- **Azure Cache for Redis**: Managed Redis for caching and session storage

### Storage
- **Azure Blob Storage**: Object storage for assets, backups, logs
- **Azure Files**: Managed SMB/NFS file shares
- **Azure Container Registry (ACR)**: Private container image registry

### Networking
- **Virtual Network (VNet)**: Isolated private network with subnets
- **Application Gateway**: Layer 7 load balancer with WAF integration
- **Azure Front Door**: Global CDN and load balancer with WAF
- **Azure DNS**: Managed DNS with traffic routing
- **Azure DDoS Protection**: Network-level DDoS mitigation

### Security
- **Azure Active Directory (Entra ID)**: Identity and access management
- **Azure Key Vault**: Secrets, keys, and certificate management
- **Microsoft Defender for Cloud**: Security posture management
- **Azure Policy**: Governance and compliance enforcement
- **NSGs + Azure Firewall**: Network-level access control

### Observability
- **Azure Monitor**: Centralized metrics, logs, and alerts
- **Application Insights**: APM and distributed tracing for applications
- **Log Analytics Workspace**: Centralized log aggregation and querying
- **Azure Activity Log**: Audit trail for all Azure operations

### CI/CD
- **Azure DevOps Pipelines**: End-to-end CI/CD with native Azure integration
- **GitHub Actions with Azure**: OIDC-based deployment to Azure resources
- **ACR Tasks**: Automated container image builds

## High Availability Pattern
- Deploy Container Apps across multiple zones with zone redundancy enabled
- PostgreSQL Flexible Server zone-redundant HA with standby in separate AZ
- Application Gateway with multi-instance deployment across AZs
- Azure Front Door for global failover and traffic distribution
- Cosmos DB multi-region writes for globally distributed workloads

## Disaster Recovery Pattern
- PostgreSQL geo-redundant backups with cross-region restore
- Azure Site Recovery for VM-based workloads
- Blob Storage geo-redundant (GRS) or geo-zone-redundant (GZRS) replication
- Azure Front Door for cross-region traffic failover
- Azure Backup for centralized backup management

## Real-World Deployed Example
**LinkedIn on Azure**: Uses Azure for enterprise data workloads, Azure SQL for
relational data at scale, and Azure Active Directory for identity federation
across Microsoft properties.

**BMW Group on Azure**: Runs connected vehicle platform on AKS with Azure
Service Bus for event-driven messaging, Azure Cosmos DB for global vehicle
telemetry, and Azure API Management for partner integrations.

**Maersk on Azure**: Global logistics platform on Azure Container Apps with
Azure PostgreSQL for operational data, Azure Service Bus for shipment event
processing, and Application Insights for distributed tracing across microservices.

## Cost Profile
- Container Apps: ~$0.000024/vCPU/second + $0.000003/GB/second
- PostgreSQL Flexible Server General Purpose 2vCores: ~$90-110/month
- Application Gateway WAF v2: ~$0.0125/capacity unit/hour + $0.246/hour base
- Blob Storage: $0.018/GB/month for LRS hot tier
- Azure Hybrid Benefit can reduce costs 40%+ for existing Microsoft license holders
- Azure Hybrid Benefit reduces costs 40%+ for existing Microsoft license holders
- Azure Reserved Instances save up to 72% vs pay-as-you-go
- Azure Dev/Test pricing significantly reduces non-production environment costs
- Azure Cost Management provides detailed spending analysis and budgets

## Compliance Certifications
HIPAA, SOC 1/2/3, PCI DSS, FedRAMP, ISO 27001, GDPR, UK G-Cloud,
DoD IL2/IL4, ITAR, Australia IRAP

## Strengths
- Best Microsoft and enterprise ecosystem integration
- Strong hybrid cloud story with Azure Arc
- Azure AD / Entra ID is industry-leading identity platform
- Competitive pricing for Microsoft-stack workloads with Hybrid Benefit
- Strong government and regulated industry presence
- Dapr integration in Container Apps simplifies microservices

## Weaknesses
- Smaller global footprint than AWS
- Some managed services lag AWS in maturity
- Console and portal can be complex for non-Microsoft teams

## Best For
- Enterprises running Microsoft-stack workloads (.NET, SQL Server)
- Organizations with existing Microsoft licensing (EA, CSP)
- Hybrid cloud scenarios connecting on-premises Windows/AD environments
- Government and 