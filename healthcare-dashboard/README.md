# 📊 Interactive Clinic Executive Performance Command Center

## 🌐 Live Application
*Note: This interface was built using the Streamlit web-app framework and runs locally via terminal routing commands.*

---

## 📋 Project Executive Overview
Following up on my initial exploratory data analysis of patient attendance metrics, I built an interactive **Business Intelligence Command Center Application** using Python. This application allows clinic administrators, regional directors, and medical operations teams to dynamically stress-test historical booking records. 

Users can manipulate custom demographic sliders and gender cross-sections in real-time to observe immediate swings in attendance data, total throughput volumes, and critical operational KPIs.

---

## 🛠️ Technical Implementation Stack
* **UI Framework:** Streamlit (Dynamic component layouts, reactive stateful session handling)
* **Data Processing Pipeline:** Pandas (Automated cache implementation via `@st.cache_data` to ensure rapid page queries across 110,000+ data rows)
* **Interactive Charting Vector:** Plotly Express (Object-oriented dark-mode linear data visualization)

---

## 🎛️ Operational Dashboard Functionality
1. **Filter Command Panel:** Implemented multi-categorical cross-filtering capabilities including an item dropdown for patient biological gender and an range slider matching individual patient ages from 0 to 115.
2. **Reactive KPI Metrics Panel:** Embedded real-time performance summary metric cards calculating total systemic volume, absolute no-show integers, and live aggregate missed visit percentages.
3. **Probability Line Horizon Charting:** Generated an interactive, hover-responsive graph charting the exact historical missed appointment percentage across a 45-day operational wait horizon.

