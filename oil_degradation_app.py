import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Oil Degradation Timeline",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Engine Oil Degradation Timeline")
st.markdown("Predict TAN rise and TBN depletion over engine operating hours using physics-based simulation.")
st.divider()

# ── Sidebar controls ──
st.sidebar.header("⚙️ Engine Parameters")

oil_type = st.sidebar.selectbox(
    "Oil Type",
    ["Mineral Oil", "Semi-Synthetic", "Synthetic Oil"]
)

avg_temp = st.sidebar.slider("Average Oil Temperature (°C)", 60, 130, 85, 1)
avg_rpm  = st.sidebar.slider("Average Engine RPM", 500, 2000, 900, 50)
max_hours = st.sidebar.slider("Simulation Duration (hours)", 100, 1000, 500, 50)

st.sidebar.divider()
st.sidebar.header("📏 Thresholds")
tan_thresh = st.sidebar.slider("TAN Change Threshold (mg KOH/g)", 1.0, 4.0, 2.0, 0.1)
tbn_thresh = st.sidebar.slider("TBN Change Threshold (mg KOH/g)", 1.0, 5.0, 3.0, 0.1)

# ── Oil parameters ──
oil_params = {
    "Mineral Oil":     {"tan_rate": 0.010, "tbn_rate": 0.020, "base_tan": 0.30, "base_tbn": 10.0},
    "Semi-Synthetic":  {"tan_rate": 0.008, "tbn_rate": 0.016, "base_tan": 0.25, "base_tbn": 11.0},
    "Synthetic Oil":   {"tan_rate": 0.006, "tbn_rate": 0.012, "base_tan": 0.20, "base_tbn": 12.0},
}

# ── Compute curves ──
def compute_curves(oil_type, temp, rpm, max_hrs):
    p = oil_params[oil_type]
    temp_factor = 1 + (temp - 85) * 0.012
    rpm_factor  = 1 + (rpm - 900) * 0.0004
    factor = temp_factor * rpm_factor

    hours = np.linspace(0, max_hrs, 500)
    tan = p["base_tan"] + p["tan_rate"] * factor * hours + 0.00003 * factor * hours**2
    tbn = np.maximum(0.1, p["base_tbn"] - p["tbn_rate"] * factor * hours - 0.00002 * factor * hours**2)
    tan = np.clip(tan, 0.05, 10.0)
    return hours, tan, tbn

def find_change_hour(hours, tan, tbn, tan_th, tbn_th):
    for i in range(len(hours)):
        if tan[i] >= tan_th or tbn[i] <= tbn_th:
            return hours[i], tan[i], tbn[i]
    return None, None, None

hours, tan, tbn = compute_curves(oil_type, avg_temp, avg_rpm, max_hours)
change_hr, tan_at_change, tbn_at_change = find_change_hour(hours, tan, tbn, tan_thresh, tbn_thresh)

# ── Metric cards ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    if change_hr:
        st.metric("Oil Change At", f"{change_hr:.0f} hrs")
    else:
        st.metric("Oil Change At", "Beyond range")

with col2:
    if tan_at_change:
        st.metric("TAN at Change", f"{tan_at_change:.3f} mg KOH/g")
    else:
        st.metric("TAN at Change", "—")

with col3:
    if tbn_at_change:
        st.metric("TBN at Change", f"{tbn_at_change:.3f} mg KOH/g")
    else:
        st.metric("TBN at Change", "—")

with col4:
    current_tan = tan[0]
    if change_hr:
        status = "🟢 Good" if hours[0] < change_hr * 0.5 else "🟡 Monitor"
    else:
        status = "🟢 Good"
    st.metric("Current Status", status)

st.divider()

# ── Main plot ──
fig = go.Figure()

# TAN curve
fig.add_trace(go.Scatter(
    x=hours, y=tan,
    name="TAN (rising)",
    line=dict(color="#E24B4A", width=2.5),
    hovertemplate="Hour: %{x:.0f}<br>TAN: %{y:.3f} mg KOH/g<extra></extra>"
))

# TBN curve
fig.add_trace(go.Scatter(
    x=hours, y=tbn,
    name="TBN (depleting)",
    line=dict(color="#2980B9", width=2.5),
    hovertemplate="Hour: %{x:.0f}<br>TBN: %{y:.3f} mg KOH/g<extra></extra>"
))

# TAN threshold
fig.add_hline(y=tan_thresh, line_dash="dash", line_color="#C0392B", line_width=1.5,
              annotation_text=f"TAN threshold ({tan_thresh})", annotation_position="top right")

# TBN threshold
fig.add_hline(y=tbn_thresh, line_dash="dash", line_color="#E67E22", line_width=1.5,
              annotation_text=f"TBN threshold ({tbn_thresh})", annotation_position="bottom right")

# Change point marker
if change_hr:
    fig.add_vline(x=change_hr, line_dash="dot", line_color="#27AE60", line_width=2,
                  annotation_text=f"Change at {change_hr:.0f} hrs", annotation_position="top left")
    fig.add_trace(go.Scatter(
        x=[change_hr], y=[tan_at_change],
        mode="markers", name="Change point (TAN)",
        marker=dict(color="#E24B4A", size=12, symbol="circle"),
        showlegend=True,
        hovertemplate=f"Change at {change_hr:.0f} hrs<br>TAN: {tan_at_change:.3f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[change_hr], y=[tbn_at_change],
        mode="markers", name="Change point (TBN)",
        marker=dict(color="#2980B9", size=12, symbol="circle"),
        showlegend=True,
        hovertemplate=f"Change at {change_hr:.0f} hrs<br>TBN: {tbn_at_change:.3f}<extra></extra>"
    ))

fig.update_layout(
    title=dict(
        text=f"Oil Degradation Timeline — {oil_type} @ {avg_temp}°C, {avg_rpm} RPM",
        font=dict(size=16)
    ),
    xaxis_title="Operating Hours",
    yaxis_title="mg KOH/g",
    yaxis=dict(range=[0, 13]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    height=480,
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    yaxis_showgrid=True,
)
fig.update_xaxes(gridcolor="#f0f0f0")
fig.update_yaxes(gridcolor="#f0f0f0")

st.plotly_chart(fig, use_container_width=True)

# ── Compare all oil types ──
st.divider()
st.subheader("📊 Compare All Oil Types")

fig2 = go.Figure()
colors = {"Mineral Oil": ("#E24B4A", "#2980B9"),
          "Semi-Synthetic": ("#E67E22", "#27AE60"),
          "Synthetic Oil": ("#9B59B6", "#1ABC9C")}

for ot, (tc, tnc) in colors.items():
    h, t, tn = compute_curves(ot, avg_temp, avg_rpm, max_hours)
    fig2.add_trace(go.Scatter(x=h, y=t,  name=f"TAN — {ot}", line=dict(color=tc, width=2), hovertemplate=f"{ot} TAN: %{{y:.3f}}<extra></extra>"))
    fig2.add_trace(go.Scatter(x=h, y=tn, name=f"TBN — {ot}", line=dict(color=tnc, width=2, dash="dash"), hovertemplate=f"{ot} TBN: %{{y:.3f}}<extra></extra>"))

fig2.add_hline(y=tan_thresh, line_dash="dot", line_color="gray", line_width=1)
fig2.add_hline(y=tbn_thresh, line_dash="dot", line_color="gray", line_width=1)

fig2.update_layout(
    title="All Oil Types — TAN & TBN Comparison",
    xaxis_title="Operating Hours",
    yaxis_title="mg KOH/g",
    yaxis=dict(range=[0, 13]),
    height=420,
    hovermode="x unified",
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10))
)
fig2.update_xaxes(gridcolor="#f0f0f0")
fig2.update_yaxes(gridcolor="#f0f0f0")

st.plotly_chart(fig2, use_container_width=True)

# ── Change interval table ──
st.divider()
st.subheader("🔁 Recommended Change Intervals")

table_data = []
for ot in ["Mineral Oil", "Semi-Synthetic", "Synthetic Oil"]:
    h, t, tn = compute_curves(ot, avg_temp, avg_rpm, max_hours)
    ch, tac, tnac = find_change_hour(h, t, tn, tan_thresh, tbn_thresh)
    table_data.append({
        "Oil Type": ot,
        "Change Interval (hrs)": f"{ch:.0f}" if ch else ">"+str(max_hours),
        "TAN at Change": f"{tac:.3f}" if tac else "—",
        "TBN at Change": f"{tnac:.3f}" if tnac else "—",
        "Triggered By": "TAN" if (tac and tac >= tan_thresh) else ("TBN" if tnac else "—")
    })

import pandas as pd
st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

st.divider()
st.caption("Physics-based simulation | TAN/TBN Prediction Project | March 2026")
