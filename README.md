# Engine Oil Degradation Timeline

A Streamlit web application that simulates and visualises the degradation of engine lubricating oil over time using physics-based modelling. The app predicts Total Acid Number (TAN) rise and Total Base Number (TBN) depletion as a function of engine operating hours, oil temperature, and RPM — without any laboratory testing.

---

## Live Demo

Deploy on [Streamlit Cloud] ([https://oildegradationapppy-zw5a8brvvhngmbnw5kbszm.streamlit.app/](https://oildegradationapppy-zw5a8brvvhngmbnw5kbszm.streamlit.app/)) for free.

---

## What It Does

- Simulates TAN and TBN degradation curves over engine operating hours
- Supports three oil types: Mineral, Semi-Synthetic, and Synthetic
- Adjustable parameters: oil temperature, engine RPM, simulation duration, and custom thresholds
- Automatically detects the recommended oil change point
- Compares all three oil types side by side on a single chart
- Displays a change interval summary table with trigger reasons

---

## Background

**TAN (Total Acid Number)** measures the concentration of acidic compounds formed during oil oxidation. A TAN above 2.0 mg KOH/g typically indicates significant degradation.

**TBN (Total Base Number)** measures the remaining alkaline additive reserve that neutralises acids. Oil change is recommended when TBN drops below 3.0 mg KOH/g.

Conventionally, TAN and TBN are measured in a laboratory via potentiometric titration (ASTM D974, ASTM D2896). This app demonstrates that accurate TAN/TBN prediction is possible using only engine sensor data and machine learning — without any chemical testing.

This project is part of a research study on:
> *Prediction of TAN and TBN of Engine Oils Using Machine Learning Without Titration*

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| Streamlit | Web app framework |
| Plotly | Interactive charts |
| NumPy | Numerical computation |
| Pandas | Data tables |

---

## Installation

### Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run oil_degradation_app.py
```

### Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io]([https://share.streamlit.io](https://oildegradationapppy-zw5a8brvvhngmbnw5kbszm.streamlit.app/))
3. Click **New app**
4. Select your repo and set the main file path to `oil_degradation_app.py`
5. Click **Deploy**

---

## File Structure

```
your-repo/
├── oil_degradation_app.py   # Main Streamlit app
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## How the Physics Model Works

TAN and TBN are modelled using empirical degradation equations:

```
TAN(t) = base_TAN + rate_TAN × factor × t + 0.00003 × factor × t²
TBN(t) = base_TBN − rate_TBN × factor × t − 0.00002 × factor × t²

where:
  factor       = temp_factor × rpm_factor
  temp_factor  = 1 + (temp − 85) × 0.012
  rpm_factor   = 1 + (rpm − 900) × 0.0004
  t            = operating hours
```

Higher temperature and RPM accelerate both TAN rise and TBN depletion. Synthetic oil has lower degradation rates due to superior thermal stability.

---

## Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| Oil Type | Mineral / Semi-Synthetic / Synthetic | Mineral | Changes base rates |
| Oil Temperature | 60 – 130°C | 85°C | Higher temp → faster degradation |
| Engine RPM | 500 – 2000 | 900 | Higher RPM → faster degradation |
| Simulation Duration | 100 – 1000 hrs | 500 hrs | X-axis range |
| TAN Threshold | 1.0 – 4.0 mg KOH/g | 2.0 | Change trigger |
| TBN Threshold | 1.0 – 5.0 mg KOH/g | 3.0 | Change trigger |

---

## Research Context

This app is a supplementary tool for the following research project:

**Title:** Prediction of Total Acid Number (TAN) and Total Base Number (TBN) of Engine Oils Using Machine Learning Without Titration

**Models used:** XGBoost Regressor, Neural Network (TensorFlow/Keras)

**Key results:**
- XGBoost TAN prediction: R² = 0.9748, MAE = 0.128 mg KOH/g
- XGBoost TBN prediction: R² = 0.9881, MAE = 0.168 mg KOH/g

**Dataset:** Physics-based synthetic dataset of 19,535 engine oil samples generated from real engine sensor data.

---

## References

1. Wolak, A. et al. (2022). Prediction of the TBN of Engine Oil by Means of FTIR Spectroscopy. *Energies*, 15(8), 2809.
2. ASTM D974 — Standard Test Method for Acid and Base Number by Color-Indicator Titration.
3. ASTM D2896 — Standard Test Method for Base Number by Potentiometric Perchloric Acid Titration.
4. Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *KDD 2016*.

---

## License

This project is for academic and non-commercial research use only.
