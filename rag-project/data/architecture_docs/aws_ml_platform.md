# AWS Machine Learning Platform Architecture Pattern

## Source References
- Amazon SageMaker: https://aws.amazon.com/sagemaker/
- AWS ML Infrastructure: https://aws.amazon.com/machine-learning/infrastructure/
- AWS Well-Architected ML Lens: https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/
- AWS AI Services: https://aws.amazon.com/machine-learning/ai-services/

## Use Cases
- End-to-end ML model training, evaluation, and deployment
- MLOps pipelines with automated retraining and model versioning
- Real-time and batch model inference at scale
- Large language model fine-tuning and deployment
- Computer vision, NLP, and forecasting workloads

## Recommended Core Services

### Data Preparation
- **Amazon SageMaker Data Wrangler**: Visual data preparation and feature engineering
- **Amazon SageMaker Feature Store**: Centralized feature storage for training and serving
- **AWS Glue**: Serverless ETL for preparing training datasets
- **Amazon S3**: Central storage for raw and processed training data
- **Amazon SageMaker Ground Truth**: Managed data labeling with human reviewers

### Model Training
- **Amazon SageMaker Training Jobs**: Managed distributed training on EC2 instances
- **Amazon SageMaker Studio**: Integrated IDE for ML development
- **Amazon SageMaker Experiments**: Track and compare training runs
- **Amazon EC2 P4d/P5 instances**: NVIDIA A100/H100 GPU instances for deep learning
- **AWS Trainium**: Custom AWS chip for cost-efficient deep learning training
- **Amazon SageMaker HyperParameter Tuning**: Automated hyperparameter optimization

### Model Registry and Versioning
- **Amazon SageMaker Model Registry**: Centralized model versioning and approval workflow
- **Amazon ECR**: Container image registry for custom training and inference containers
- **Amazon S3**: Model artifact storage with versioning enabled

### Model Deployment
- **Amazon SageMaker Real-Time Endpoints**: Low-latency online inference endpoints
- **Amazon SageMaker Serverless Inference**: Scale-to-zero inference for intermittent workloads
- **Amazon SageMaker Batch Transform**: Large-scale batch inference jobs
- **Amazon SageMaker Multi-Model Endpoints**: Host multiple models on a single endpoint
- **AWS Inferentia**: Custom AWS chip for cost-efficient inference (up to 70% savings)
- **Amazon SageMaker Async Inference**: Queue-based inference for large payloads

### MLOps and Pipelines
- **Amazon SageMaker Pipelines**: Native ML pipeline orchestration with DAG support
- **Amazon SageMaker Model Monitor**: Detect data drift and model degradation in production
- **Amazon SageMaker Clarify**: Bias detection and model explainability
- **AWS Step Functions**: Workflow orchestration for cross-service ML pipelines
- **Amazon EventBridge**: Trigger retraining pipelines on data or schedule events

### Serving and APIs
- **Amazon API Gateway + Lambda**: REST API wrapper over SageMaker endpoints
- **Amazon SageMaker Real-Time Endpoints**: Direct HTTPS inference endpoints
- **Amazon CloudFront**: CDN caching layer for inference results
- **AWS AppSync**: GraphQL API for ML-powered applications

### Observability
- **CloudWatch Model Monitor**: Metrics and alerts for endpoint performance
- **SageMaker Experiments**: Training job comparison and metric tracking
- **SageMaker Clarify**: Ongoing fairness and explainability monitoring
- **AWS X-Ray**: Distributed tracing for inference API calls

## High Availability Pattern
- SageMaker endpoints deployed across multiple AZs automatically
- Auto scaling on SageMaker endpoints based on invocation count
- Multi-model endpoints reduce cold start risk across model variants
- S3 training data with cross-region replication for DR
- Feature Store online store backed by DynamoDB (multi-AZ by default)

## Disaster Recovery Pattern
- Model artifacts in S3 with versioning and cross-region replication
- SageMaker Model Registry approval workflow with rollback capability
- Retrain pipelines triggered automatically via EventBridge on data drift alerts
- Multi-region endpoint deployment with Route 53 latency-based routing

## Real-World Example
**Intuit on AWS SageMaker**: Runs ML platform for TurboTax and QuickBooks
on SageMaker, training hundreds of models for fraud detection, document
understanding, and financial forecasting. Uses SageMaker Pipelines for
automated retraining, Feature Store for shared features across teams,
and SageMaker Model Monitor for production drift detection.

**Verizon on AWS**: Deploys network anomaly detection and customer churn
models on SageMaker endpoints, uses Trainium for cost-efficient training
of large telecom models, and SageMaker Clarify for regulatory bias
reporting across customer-facing ML decisions.

## Cost Profile
- SageMaker Studio: Free IDE, pay for underlying compute
- SageMaker Training ml.p3.2xlarge (1x V100): ~$3.825/hour
- SageMaker Training ml.p4d.24xlarge (8x A100): ~$32.77/hour
- AWS Trainium trn1.2xlarge: ~$1.343/hour (60% cheaper than GPU for training)
- SageMaker Real-Time Endpoint ml.m5.xlarge: ~$0.269/hour
- AWS Inferentia inf2.xlarge: ~$0.227/hour (70% cheaper than GPU for inference)
- SageMaker Serverless Inference: $0.20/million invocations + $0.0000002/GB-second
- Feature Store Online: $0.25/million read/write units

## Strengths
- Most complete end-to-end MLOps platform of any cloud provider
- SageMaker Studio provides best-in-class integrated ML IDE
- AWS Trainium and Inferentia offer significant cost savings over GPU
- SageMaker Pipelines native integration with all AWS data services
- Model Monitor and Clarify are best-in-class for production ML governance
- Largest selection of GPU instance types for training workloads
- Deep integration with S3, Glue, and Redshift for data pipelines

## Weaknesses
- SageMaker has a steep learning curve compared to Vertex AI
- Pricing can be complex across many SageMaker components
- Custom container management adds operational overhead
- Cold starts on serverless inference can be significant

## Best For
- Enterprise ML teams needing full MLOps lifecycle management
- Organizations requiring model governance, bias detection, and explainability
- Teams training large deep learning models needing GPU variety
- Cost-conscious teams leveraging Trainium and Inferentia custom chips
- ML platforms requiring tight integration with AWS data lake and analytics