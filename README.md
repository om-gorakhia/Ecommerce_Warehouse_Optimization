# 📦 E-Commerce Warehouse Optimization

**Interactive Analytics Platform for Supply Chain Optimization using Linear Programming**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Overview

A comprehensive Linear Programming solution for multi-warehouse inventory allocation that achieves **99%+ order fulfillment** and **$44.9M profit improvement** through optimal resource distribution and cost minimization.

This project optimizes inventory allocation across 6 warehouses serving 10 delivery regions with 300+ products, solving the complex problem of balancing transportation costs, holding costs, and service level targets.

---

## 🎯 Key Results

| Metric | Before Optimization | After Optimization | Improvement |
|--------|-------------------|-------------------|-------------|
| **Order Fulfillment** | 45% | 99%+ | **+54 pp** |
| **Stockout Rate** | 55% | <5% | **-50 pp** |
| **Annual Profit** | -$9.5M (loss) | +$35.4M | **$44.9M** |
| **System Cost** | $36M | Optimized | Minimized |

**Key Achievements:**
- ✅ **99% fulfillment rate** (up from 45%)
- ✅ **$44.9M profit improvement** from optimization
- ✅ **$3.7M savings opportunity** identified (20% transport cost reduction)
- ✅ **Optimal allocation** across 6-warehouse network

---

## 🛠️ Features

### Interactive Streamlit Dashboard

- **🏠 Executive Summary:** High-level KPIs and business impact metrics
- **📈 Performance Analysis:** Deep dive into fulfillment, delivery, warehouse, and transport metrics
- **🔄 Scenario Comparison:** Sensitivity analysis across 9 optimization strategies
- **🗺️ Network Visualization:** Interactive global map of warehouse-region connections
- **💡 Strategic Insights:** Data-driven recommendations with ROI projections
- **🔬 Technical Documentation:** Mathematical formulations and methodology
- **📊 Validation Logs:** Complete audit trail of calculations and assumptions

### Optimization Engine

- **Multi-Commodity Network Flow** optimization
- **Linear Programming** using PuLP/CBC solver
- **Flow Capacity Model** (12× inventory turnover)
- **Cost Minimization** (transport + holding + stockout penalties)
- **Constraint Optimization** (capacity, demand, service levels)

---

## 💻 Technology Stack

- **Python 3.10+** - Core programming language
- **PuLP** - Linear Programming and optimization
- **Pandas** - Data manipulation and analysis
- **Streamlit** - Interactive dashboard framework
- **Plotly** - Advanced data visualization
- **NumPy** - Numerical computing

---

## 📁 Project Structure

```
Ecommerce_Warehouse_Optimization/
│
├── streamlit_dashboard.py    # Main dashboard application
├── requirements.txt          # Python dependencies
├── .devcontainer/            # Development container config
│
├── results/                  # Generated optimization results
│   ├── scenario_comparison_kpis.csv
│   ├── cost_breakdown_comparison.csv
│   ├── network_nodes.csv
│   ├── network_edges.csv
│   └── Baseline/             # Baseline scenario results
│       ├── shipments.csv
│       ├── stocking.csv
│       ├── stockouts.csv
│       └── kpis.json
│
└── README.md                 # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/om-gorakhia/Ecommerce_Warehouse_Optimization.git
cd Ecommerce_Warehouse_Optimization
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
pulp>=2.7.0
json
pathlib
```

### Step 3: Run the Dashboard

```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 📊 How It Works

### Problem Statement

**Challenge:** An e-commerce company has:
- 6 warehouses with limited capacity
- 10 delivery regions with varying demand
- 300+ products to allocate
- 45% fulfillment rate (55% stockouts)
- Negative profitability

**Goal:** Maximize order fulfillment while minimizing total system costs

### Solution Approach

#### 1. **Flow Capacity Model**
Instead of static inventory, we model continuous replenishment:
```
Flow Capacity = Static Inventory × Annual Turnover Rate
              = 50,000 units × 12 turns/year
              = 600,000 units/year capacity
```

#### 2. **Objective Function**
Minimize total system cost:
```
Minimize: Transportation Cost + Holding Cost + Stockout Penalties
```

#### 3. **Key Constraints**
- **Demand Satisfaction:** All demand must be fulfilled or recorded as stockout
- **Capacity Limits:** Shipments cannot exceed warehouse capacity
- **Service Targets:** 95% fulfillment, 3-day delivery window
- **Non-negativity:** All quantities must be ≥ 0

#### 4. **Optimization**
Using Linear Programming (PuLP with CBC solver) to find the mathematically optimal allocation.

---

## 💼 Business Impact

### Problems Solved

| Problem | Solution | Result |
|---------|----------|--------|
| **Low Fulfillment (45%)** | Flow Capacity Model + Optimal Allocation | **99%+ fulfillment** |
| **High Stockouts (55%)** | Linear Programming optimization | **<5% stockouts** |
| **Unprofitable Operations** | Cost minimization with 10× CLV penalty | **$44.9M profit gain** |
| **Inefficient Transport** | Carrier negotiation opportunity | **$3.7M savings potential** |

### Strategic Recommendations

**🔴 Priority 1: Transportation Cost Negotiation (6 months)**
- Expected savings: $3.0-3.7M annually
- Action: Negotiate 15-20% rate reduction with carriers
- ROI: Highest sensitivity

**🟡 Priority 2: On-Time Delivery Improvement (18 months)**
- Target: 95%+ on-time rate
- Action: Add 2-3 regional distribution centers
- ROI: High

**🟢 Priority 3: Capacity Monitoring (Ongoing)**
- Current: 68% average utilization
- Headroom: 25% volume growth before expansion
- Action: Quarterly monitoring

---

## 🔬 Technical Details

### Mathematical Formulation

**Decision Variables:**
- `x[i,j,p]` = Quantity of product `p` shipped from warehouse `i` to region `j`
- `y[i,p]` = Binary indicator (1 if product `p` stocked at warehouse `i`)
- `s[j,p]` = Stockout quantity for product `p` in region `j`

**Objective Function:**
```
Minimize Z = ΣΣΣ c[i,j] × x[i,j,p]           (Transportation)
           + ΣΣ h[i] × inventory[i,p]      (Holding)
           + ΣΣ penalty[p] × s[j,p]      (Stockouts)
```

**Subject to:**
- Demand satisfaction: `Σ x[i,j,p] + s[j,p] = demand[j,p]`
- Capacity constraint: `Σ x[i,j,p] ≤ flow_capacity[i,p]`
- Service level: On-time delivery ≥ 95%

### Performance

- **Solve Time:** ~2 seconds
- **Problem Size:** ~14,000 variables, ~5,000 constraints
- **Optimization Status:** Optimal solution guaranteed
- **Algorithm:** Branch-and-Cut with CBC solver

---

## 📝 Use Cases

This solution is applicable to:

- ✅ E-commerce fulfillment network optimization
- ✅ Multi-warehouse inventory allocation
- ✅ Supply chain cost reduction initiatives
- ✅ Service level improvement projects
- ✅ Capacity planning and expansion analysis
- ✅ Warehouse network design
- ✅ Transportation optimization

---

## 📦 Scenarios Analyzed

The project evaluates **9 optimization scenarios**:

1. **Baseline** - Current optimal allocation
2-4. **Capacity Expansion** - 10%, 20%, 30% increase
5-6. **Transport Cost Reduction** - 10%, 20% decrease  
7. **Transport Cost Increase** - 10% increase
8-9. **Higher Service Targets** - 97%, 99% fulfillment

---

## 👥 Team

**DBA5103 Operations Research & Analytics**  
National University of Singapore (NUS)

- Om Gorakhia
- Prisha Shah  
- Nourah Algiffari
- Pranay Samineni
- Sanya Rajpal

---

## 📌 Next Steps

To extend this project:

1. **Real-time Integration:** Connect to live inventory systems
2. **Demand Forecasting:** Add ML-based demand prediction
3. **Dynamic Pricing:** Incorporate pricing optimization
4. **Route Optimization:** Detailed last-mile delivery routing
5. **Multi-period Planning:** Extend to monthly/quarterly planning horizon
6. **Sustainability Metrics:** Add carbon footprint optimization

---

## 📝 License

This project is part of academic coursework at NUS Business School.

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/om-gorakhia/Ecommerce_Warehouse_Optimization.git

# Navigate to directory
cd Ecommerce_Warehouse_Optimization

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
streamlit run streamlit_dashboard.py
```

**Dashboard URL:** `http://localhost:8501`

---

## ❓ FAQ

**Q: What data is required to run this optimization?**  
A: The model requires warehouse capacities, product dimensions, demand by region, transportation costs, and service level targets.

**Q: Can this work for my business?**  
A: Yes! The framework is adaptable to any multi-location inventory allocation problem. Adjust parameters in the optimization engine to match your specific requirements.

**Q: How long does optimization take?**  
A: The CBC solver finds optimal solutions in ~2 seconds for networks of this size (6 warehouses, 10 regions, 300 products).

**Q: What if I don't have optimization results?**  
A: Run the analysis engine first (check code comments for execution). Pre-generated results are included in the `/results` folder.

---

## 📞 Contact

For questions or collaboration:
- **Email:** om.gorakhia@u.nus.edu
- **LinkedIn:** [linkedin.com/in/omgorakhia](https://linkedin.com/in/omgorakhia)
- **GitHub:** [@om-gorakhia](https://github.com/om-gorakhia)

---

**⭐ If you find this project helpful, please give it a star!**

---

*Built with ❤️ for supply chain optimization | NUS Business Analytics 2025*
