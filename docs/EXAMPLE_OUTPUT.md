# Example Demo Outputs

This document shows what to expect when running the AgentCon demo.

## Text Mode Example

### Command
```powershell
python agentcon_demo.py
```

### Expected Output

```
🔌 Connecting to Microsoft Learn MCP...
📝 Text mode (default)

============================================================
🎯 INPUT ARCHITECTURE
============================================================

    We have a 3-tier e-commerce application on Azure:
    - Frontend: Virtual Machines running Node.js (public IPs)
    - Backend: Virtual Machines running .NET APIs (public IPs)
    - Database: Azure SQL Database (public endpoint enabled)
    - Storage: Azure Storage Account (no encryption at rest)

============================================================
🔍 STEP 1: Architecture Critic (MCP-grounded)
============================================================

This architecture has several critical security and scalability issues:

**Security Concerns:**
• According to Microsoft Learn, exposing VMs with public IP addresses creates an attack surface. Virtual machines should be placed behind Azure Application Gateway or Azure Front Door.
• The Azure SQL Database with a public endpoint violates the principle of least privilege. Microsoft Learn recommends using Private Link to restrict access to the database.
• Storage Account without encryption at rest is non-compliant with Azure security baselines. According to Microsoft Learn, Azure Storage should always use Microsoft-managed keys or customer-managed keys for encryption.

**Architecture Issues:**
• Using Virtual Machines for frontend and backend is an anti-pattern for cloud-native applications. According to Microsoft Learn, Azure App Service or Azure Container Apps provide better scalability, automatic patching, and reduced operational overhead.
• No mention of load balancing, auto-scaling, or availability zones indicates potential single points of failure.

**Missing Best Practices:**
• No network segmentation (VNets, subnets, NSGs) mentioned
• No mention of Azure Monitor for observability
• No disaster recovery or backup strategy
• No mention of CI/CD pipelines or deployment strategy

============================================================
🔧 STEP 2: Architecture Fixer (MCP-grounded)
============================================================

**Improved 3-Tier E-Commerce Architecture for Azure:**

**Frontend Layer:**
- Replace Node.js VMs with **Azure App Service** (Web Apps) or **Azure Container Apps**
  - According to Microsoft Learn, App Service provides automatic scaling, SSL certificates, and integrated deployment slots
  - Place behind **Azure Front Door** for global load balancing, WAF protection, and SSL offloading
  - Enable custom domains and automatic HTTPS
  - Configure auto-scaling rules based on CPU/memory metrics

**Backend Layer:**
- Replace .NET API VMs with **Azure App Service** (API Apps) or **Azure Functions** (for serverless)
  - According to Microsoft Learn, API Apps support OpenAPI/Swagger for API documentation
  - Use VNet integration to communicate privately with database
  - Enable Application Insights for monitoring and diagnostics
  - Implement authentication using Azure AD (Microsoft Entra ID)

**Database Layer:**
- Upgrade **Azure SQL Database** to use:
  - **Private Link** (no public endpoint) - According to Microsoft Learn, this ensures database is only accessible via private IP within VNet
  - Enable **Transparent Data Encryption (TDE)** (already enabled by default)
  - Configure **geo-replication** for disaster recovery
  - Use **Azure SQL Managed Instance** if advanced features needed
  - Enable **Azure Defender for SQL** for threat detection

**Storage Layer:**
- Configure **Azure Storage Account** with:
  - **Encryption at rest** using Microsoft-managed keys (according to Microsoft Learn, enabled by default for new accounts)
  - **Private endpoints** to eliminate public access
  - Enable **Azure Storage encryption in transit** (HTTPS only)
  - Use **Azure Blob Storage Cool/Archive tiers** for infrequently accessed data
  - Enable **soft delete** for blob recovery

**Network Architecture:**
- Deploy all resources within **Azure Virtual Network (VNet)**
- Use **Network Security Groups (NSGs)** to control traffic between tiers
- Implement **Application Security Groups (ASGs)** for grouping resources
- Use **Azure Bastion** for secure RDP/SSH access (eliminate public IPs)

**Security & Compliance:**
- Enable **Azure Monitor** and **Log Analytics** for centralized logging
- Configure **Azure Sentinel** for security information and event management (SIEM)
- Use **Azure Key Vault** for secrets management (connection strings, API keys)
- Enable **Azure Policy** to enforce organizational standards
- Implement **Azure Private Link** for all Azure PaaS services

**High Availability:**
- Deploy across **Availability Zones** for 99.99% SLA
- Configure **Azure Traffic Manager** or **Front Door** for global load balancing
- Enable **auto-scaling** on App Services based on demand
- Implement **Azure Site Recovery** for disaster recovery

============================================================
📊 STEP 3: Diagram Visualizer
============================================================

{
  "nodes": [
    {"id": "frontdoor", "type": "AzureFrontDoor", "label": "Azure Front Door"},
    {"id": "appservice-frontend", "type": "AzureAppService", "label": "App Service (Frontend)"},
    {"id": "appservice-backend", "type": "AzureAppService", "label": "App Service (Backend)"},
    {"id": "sql", "type": "AzureSQLDatabase", "label": "Azure SQL Database (Private)"},
    {"id": "storage", "type": "AzureBlobStorage", "label": "Azure Storage (Encrypted)"},
    {"id": "keyvault", "type": "AzureKeyVault", "label": "Key Vault"},
    {"id": "monitor", "type": "AzureMonitor", "label": "Azure Monitor"}
  ],
  "edges": [
    {"from": "frontdoor", "to": "appservice-frontend", "label": "HTTPS"},
    {"from": "appservice-frontend", "to": "appservice-backend", "label": "API calls"},
    {"from": "appservice-backend", "to": "sql", "label": "Private Link"},
    {"from": "appservice-backend", "to": "storage", "label": "Private Endpoint"},
    {"from": "appservice-frontend", "to": "keyvault", "label": "Get secrets"},
    {"from": "appservice-backend", "to": "keyvault", "label": "Get secrets"},
    {"from": "appservice-frontend", "to": "monitor", "label": "Telemetry"},
    {"from": "appservice-backend", "to": "monitor", "label": "Telemetry"}
  ]
}

============================================================
📝 STEP 4: IaC Generator (MCP-grounded)
============================================================

```bicep
// Improved Azure E-Commerce Architecture - Bicep IaC
// Resource types and API versions validated via Microsoft Learn MCP

@description('Location for all resources')
param location string = resourceGroup().location

@description('Environment name (dev, staging, prod)')
param environment string = 'prod'

// Azure App Service Plan (for both frontend and backend)
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-ecommerce-${environment}'
  location: location
  sku: {
    name: 'P1v3'  // According to Microsoft Learn: P1v3 supports VNet integration
    tier: 'PremiumV3'
    capacity: 2
  }
  properties: {
    reserved: false  // Windows
  }
}

// Frontend App Service
resource frontendApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'app-ecommerce-frontend-${environment}'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      appSettings: [
        {
          name: 'BACKEND_API_URL'
          value: backendApp.properties.defaultHostName
        }
      ]
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// Backend API App Service
resource backendApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'app-ecommerce-backend-${environment}'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    virtualNetworkSubnetId: backendSubnet.id  // VNet integration
    siteConfig: {
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// Azure SQL Server (with Private Link)
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: 'sql-ecommerce-${environment}-${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    administratorLogin: 'sqladmin'
    administratorLoginPassword: '@Microsoft.KeyVault(SecretUri=${keyVault.properties.vaultUri}secrets/sql-admin-password/)'
    publicNetworkAccess: 'Disabled'  // According to Microsoft Learn: Disable public access
  }
}

// Azure SQL Database
resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-05-01-preview' = {
  parent: sqlServer
  name: 'db-ecommerce'
  location: location
  sku: {
    name: 'S1'
    tier: 'Standard'
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
  }
}

// Storage Account (with encryption)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stecommerce${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        blob: {
          enabled: true
        }
        file: {
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'  // According to Microsoft Learn: Default encryption
    }
    publicNetworkAccess: 'Disabled'
  }
}

// Azure Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-ecommerce-${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    publicNetworkAccess: 'Disabled'
  }
}

// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: 'vnet-ecommerce-${environment}'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'snet-backend'
        properties: {
          addressPrefix: '10.0.1.0/24'
          delegations: [
            {
              name: 'delegation'
              properties: {
                serviceName: 'Microsoft.Web/serverFarms'
              }
            }
          ]
        }
      }
    ]
  }
}

// According to Microsoft Learn: Use API version 2023-01-01 or later for Web Apps
// According to Microsoft Learn: Use API version 2023-05-01 or later for SQL Server

output frontendUrl string = frontendApp.properties.defaultHostName
output backendUrl string = backendApp.properties.defaultHostName
output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
```

============================================================
✅ PIPELINE COMPLETE
============================================================
```

## Key Observations

✅ **MCP Grounding Works**: Notice citations like "According to Microsoft Learn..."

✅ **Real Issues Identified**: 
- Public IPs on VMs
- Public SQL endpoint
- No encryption at rest

✅ **Modern Improvements**:
- VMs → App Services
- Public endpoints → Private Link
- Added Key Vault, monitoring, auto-scaling

✅ **Validated IaC**:
- Correct resource types
- Valid API versions (2023-xx-xx)
- Security best practices

## Image Mode Example

### Command
```powershell
# Set in .env:
# USE_IMAGE_MODE=true
# ARCHITECTURE_IMAGE_PATH=examples/bad-architecture.png

python agentcon_demo.py
```

### Expected Output

```
🔌 Connecting to Microsoft Learn MCP...
📸 Image mode enabled

============================================================
🖼️  STEP 0: Diagram Interpreter (image → text)
============================================================

The architecture diagram shows a traditional 3-tier web application deployed on Azure with the following components:

**Frontend Tier:**
- Two Virtual Machines labeled "Web-VM-1" and "Web-VM-2"
- Each VM has a public IP address (indicated by globe icons)
- Running Node.js applications (indicated by Node.js logos)
- No load balancer shown

**Application Tier:**
- Two Virtual Machines labeled "API-VM-1" and "API-VM-2"
- Each VM has a public IP address
- Running .NET Core APIs (indicated by .NET logos)
- Direct connections to database tier

**Database Tier:**
- Azure SQL Database labeled "SQL-DB-Prod"
- Icon shows a lock is open (indicating public endpoint enabled)
- No firewall rules visible

**Storage:**
- Azure Storage Account labeled "storage-prod"
- Blob icon with warning symbol
- Connected to API tier with HTTP (not HTTPS) indicated

**Network Architecture:**
- No VNet boundaries shown
- All components appear to be in public network space
- No Network Security Groups (NSGs) visible
- No private endpoints

**Missing Components:**
- No load balancer
- No Application Gateway or Front Door
- No Key Vault
- No monitoring/logging services
- No backup or DR configuration

[... then same analysis as text mode ...]
```

## Timing Expectations

- **Initialization**: 2-5 seconds (MCP connection)
- **Step 0** (Image): 5-10 seconds (vision model)
- **Step 1** (Critic): 15-20 seconds (with MCP queries)
- **Step 2** (Fixer): 15-20 seconds (with MCP validation)
- **Step 3** (Visualizer): 10-15 seconds
- **Step 4** (IaC): 15-20 seconds (with MCP checks)

**Total**: ~1-2 minutes for complete pipeline

## What Makes It "Grounded"?

Look for these phrases in agent outputs:
- ✅ "According to Microsoft Learn..."
- ✅ "Microsoft Learn recommends..."
- ✅ "Azure documentation states..."
- ✅ Specific API versions referenced
- ✅ Resource type validation mentioned

Without MCP, you'd see:
- ❌ Generic statements
- ❌ No citations
- ❌ Potentially incorrect API versions
- ❌ Hallucinated resource types

## Conference Tips

**Live Demo Flow**:
1. Start with text mode (predictable, 1-2 min)
2. While running, explain each step
3. Point out MCP citations when they appear
4. Switch to image mode for "wow" moment
5. Show how same pipeline works with visual input

**Key Phrases to Emphasize**:
- *"This isn't hallucinating — it checked Microsoft Learn"*
- *"Every resource type is validated"*
- *"Architects start with whiteboards, not JSON"*
