# Phase 5: Visualization & Data Governance

## 🎯 Objective

Close the circle: show the value and ensure control. Deploy visualization tools and implement data governance.

## 📊 Status: 🔴 Not Started (0%)

### Pending
- [ ] Deploy Apache Superset to Kubernetes
- [ ] Connect Superset to PostgreSQL
- [ ] Create weather dashboards
- [ ] Set up DataHub for data catalog
- [ ] Configure data lineage tracking
- [ ] Document datasets and ownership

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Apache Superset** | BI and data visualization |
| **DataHub** | Data catalog and lineage |
| **Kubernetes** | Container orchestration |

## 📁 Relevant Files

```
weather-dataops-platform/
├── infra/
│   ├── superset.tf         # Superset K8s deployment
│   └── datahub.tf          # DataHub deployment
└── docs/
    └── dashboards/
        └── weather_overview.md  # Dashboard documentation
```

## 📝 Implementation Steps

### Step 1: Deploy Superset to Kubernetes

**Option A: Helm Chart (Recommended)**
```bash
helm repo add superset https://apache.github.io/superset
helm install superset superset/superset \
  --namespace visualization \
  --create-namespace \
  --set service.type=NodePort \
  --set service.nodePort.http=30080
```

**Option B: Terraform**
```hcl
# infra/superset.tf
resource "kubernetes_namespace" "visualization" {
  metadata {
    name = "visualization"
  }
}

resource "helm_release" "superset" {
  name       = "superset"
  repository = "https://apache.github.io/superset"
  chart      = "superset"
  namespace  = kubernetes_namespace.visualization.metadata[0].name

  set {
    name  = "service.type"
    value = "NodePort"
  }

  set {
    name  = "service.nodePort.http"
    value = "30080"
  }
}
```

### Step 2: Configure Database Connection

In Superset UI:
1. Go to **Data** → **Databases** → **+ Database**
2. Select **PostgreSQL**
3. Configure connection:
   ```
   Host: postgres.database.svc.cluster.local
   Port: 5432
   Database: weather
   Username: weather_readonly
   Password: ****
   ```

### Step 3: Create Datasets

Register Gold layer tables as Superset datasets:
- `gold.fct_weather_daily`
- `gold.fct_weather_city_stats`

### Step 4: Build Dashboards

**Weather Overview Dashboard**

| Chart | Type | Data Source |
|-------|------|-------------|
| Temperature Trend | Line Chart | fct_weather_daily |
| City Comparison | Bar Chart | fct_weather_city_stats |
| Current Conditions | Big Number | Latest observations |
| Weather Map | Map | City coordinates |
| Humidity Heatmap | Heatmap | fct_weather_daily |

**Example Chart Configuration**:
```sql
-- Temperature Trend by City
SELECT
    weather_date,
    city_name,
    avg_temperature_c
FROM gold.fct_weather_daily
WHERE weather_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY weather_date, city_name
```

### Step 5: Deploy DataHub

```bash
# Using Docker Compose for local development
git clone https://github.com/datahub-project/datahub.git
cd datahub/docker
./quickstart.sh

# Access at http://localhost:9002
```

### Step 6: Configure Data Lineage

**dbt Integration with DataHub**:
```bash
pip install acryl-datahub[dbt]

# Generate metadata
datahub ingest -c dbt_recipe.yml
```

**dbt Recipe**:
```yaml
# dbt_recipe.yml
source:
  type: dbt
  config:
    manifest_path: ./transformations/target/manifest.json
    catalog_path: ./transformations/target/catalog.json
    target_platform: postgres

sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
```

### Step 7: Document Datasets

In DataHub, document each dataset:
- **Description**: What the data represents
- **Owner**: Team or person responsible
- **Tags**: Categories (e.g., "weather", "gold", "daily")
- **Glossary Terms**: Business definitions

## 📊 Dashboard Examples

### Weather Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    WEATHER OVERVIEW DASHBOARD                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  Current Temp    │  │  Avg Humidity    │  │  Wind Speed  │  │
│  │     18.5°C       │  │      65%         │  │   12 km/h    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Temperature Trend (Last 7 Days)                │ │
│  │  25°┤                                                       │ │
│  │  20°┤    ╭─╮   ╭───╮                                       │ │
│  │  15°┤───╯   ╰─╯     ╰───╮                                  │ │
│  │  10°┤                    ╰───                               │ │
│  │     └─────┬─────┬─────┬─────┬─────┬─────┬─────             │ │
│  │          Mon   Tue   Wed   Thu   Fri   Sat   Sun           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │   City Comparison       │  │   Weather Conditions        │  │
│  │   ████████ Madrid 22°   │  │   ☀️ Clear: 45%             │  │
│  │   ██████ Barcelona 19°  │  │   ☁️ Cloudy: 30%            │  │
│  │   █████ London 15°      │  │   🌧️ Rain: 25%              │  │
│  └─────────────────────────┘  └─────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔍 Data Lineage View

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LINEAGE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  OpenWeather API                                                 │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐                                                │
│  │ Python      │                                                │
│  │ Ingestor    │                                                │
│  └─────────────┘                                                │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Bronze:     │───▶│ Silver:     │───▶│ Gold:       │         │
│  │ weather_raw │    │ int_weather │    │ fct_daily   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                               │                  │
│                                               ▼                  │
│                                        ┌─────────────┐          │
│                                        │ Superset    │          │
│                                        │ Dashboard   │          │
│                                        └─────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## ✅ Completion Checklist

- [ ] Superset deployed and accessible
- [ ] PostgreSQL connection configured
- [ ] Gold tables registered as datasets
- [ ] At least one dashboard created
- [ ] DataHub deployed
- [ ] dbt lineage imported
- [ ] Datasets documented with owners
- [ ] Access controls configured

## 🔗 Related Resources

- [Apache Superset Documentation](https://superset.apache.org/docs/intro)
- [Superset Helm Chart](https://github.com/apache/superset/tree/master/helm/superset)
- [DataHub Documentation](https://datahubproject.io/docs/)
- [DataHub dbt Integration](https://datahubproject.io/docs/generated/ingestion/sources/dbt)

## 🎉 Project Complete!

Once this phase is done, you have a fully functional data platform:

```
API → Ingest → Store → Transform → Visualize → Govern
```

### Next Steps for Learning
- Add more data sources
- Implement real-time streaming
- Set up alerting and monitoring
- Explore cloud deployment (AWS, GCP, Azure)
- Add ML/AI capabilities
