import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="US College Tuition & Fees Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL COLOR PALETTE
# ─────────────────────────────────────────────
PRIMARY_BLUE = "#2E86AB"
ACCENT_CORAL = "#E84855"
NEUTRAL_GREY = "#F0F0F0"
TEXT_COLOR   = "#2D2D2D"
BACKGROUND   = "#FFFFFF"
GRID_GREY    = "#E8E8E8"

# ─────────────────────────────────────────────
# HARDCODED DATA
# ─────────────────────────────────────────────

years           = [2000, 2005, 2010, 2015, 2018, 2020, 2021, 2022, 2023]
public_tuition  = [3500, 5100, 7600, 9400, 10200, 10560, 10740, 10850, 10940]
private_tuition = [16200, 21200, 27300, 33500, 36800, 37650, 38200, 38900, 39400]

states = [
    "Vermont", "New Hampshire", "Pennsylvania", "Michigan", "Massachusetts",
    "Illinois", "Connecticut", "New Jersey", "Colorado", "Virginia",
]
state_tuition    = [20600, 19400, 18600, 17800, 17200, 16900, 16400, 16100, 15800, 15400]
national_average = 13200

cost_categories = ["Base Tuition", "Fees", "Room", "Board (Meals)", "Books & Supplies", "Total Cost"]
cost_values     = [10940, 1240, 7200, 4800, 1240, 25420]

heatmap_states = [
    "Vermont", "Pennsylvania", "Michigan", "New York", "California",
    "North Carolina", "Utah", "Texas", "Florida", "Wyoming",
]
heatmap_years  = [2000, 2005, 2010, 2015, 2020, 2023]
heatmap_values = [
    [7200, 10100, 14200, 17800, 19200, 20600],
    [5600,  8900, 12400, 15100, 17200, 18600],
    [5100,  8200, 11800, 14200, 16100, 17800],
    [4100,  5900,  8800, 11200, 13100, 14800],
    [3400,  5200,  8100,  9800, 11400, 12600],
    [2900,  4100,  5800,  7200,  7600,  7900],
    [2600,  3800,  5100,  6800,  7400,  8100],
    [3200,  4800,  7200,  9100, 10200, 11400],
    [2800,  3900,  5700,  6300,  6900,  7200],
    [2100,  2900,  3800,  4600,  5200,  5600],
]

df_heat = pd.DataFrame(heatmap_values, index=heatmap_states, columns=heatmap_years)
df_heat = df_heat.iloc[::-1]

# ─────────────────────────────────────────────
# CSS  — minimal, no fixed/absolute positioning
# ─────────────────────────────────────────────
st.markdown("""
<style>
.block-container {
    padding-top: 4rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}
.kpi-card {
    background-color: #F8F9FA;
    border-left: 4px solid #2E86AB;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    box-sizing: border-box;
}
.kpi-card:hover {
    border-left-color: #E84855;
    box-shadow: 0 4px 12px rgba(0,0,0,0.14);
}
.section-label {
    font-size: 10px;
    font-weight: 600;
    color: #9E9E9E;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.footer-text {
    font-size: 12px;
    color: #6C757D;
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TITLE  — use st.title() so Streamlit controls placement
# ─────────────────────────────────────────────
st.markdown(
    '<div style="height:4px;background:#2E86AB;border-radius:2px;margin-bottom:12px;"></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="font-size:20px;font-weight:700;color:#2D2D2D;margin-bottom:2px;">'
    "US College Tuition &amp; Fees Dashboard"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="font-size:15px;color:#6C757D;margin-bottom:8px;">'
    "Analyzing tuition trends, state comparisons, and total cost of attendance across US institutions (2000–2023)"
    "</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
st.markdown(
    '<p style="font-size:11px;font-weight:600;color:#9E9E9E;letter-spacing:1.5px;margin-bottom:8px;">'
    "KEY METRICS AT A GLANCE</p>",
    unsafe_allow_html=True,
)

def kpi_card(icon, label, value, delta, delta_color):
    return (
        f'<div class="kpi-card">'
        f'<div style="font-size:20px;margin-bottom:6px;">{icon}</div>'
        f'<div style="font-size:13px;color:#6C757D;margin-bottom:6px;">{label}</div>'
        f'<div style="font-size:26px;color:#2D2D2D;font-weight:700;margin-bottom:6px;line-height:1.1;">{value}</div>'
        f'<div style="font-size:12px;color:{delta_color};">{delta}</div>'
        f'</div>'
    )

k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    st.markdown(kpi_card("🏛️", "Avg Public Tuition (2023)", "$10,940", "+213% since 2000", "#E84855"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card("🎓", "Avg Private Tuition (2023)", "$39,400", "+143% since 2000", "#E84855"), unsafe_allow_html=True)
with k3:
    st.markdown(kpi_card("📈", "Public Tuition Growth", "+213%", "Over 23 years (2000–2023)", "#6C757D"), unsafe_allow_html=True)
with k4:
    st.markdown(kpi_card("💰", "Avg Total Cost of Attendance", "$25,420", "Tuition is only 43% of total cost", "#6C757D"), unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
# CACHED CHART BUILDERS
# ─────────────────────────────────────────────

@st.cache_data
def build_chart1():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=public_tuition, mode="lines",
        line=dict(width=0), showlegend=False, hoverinfo="skip", name="_base"))
    fig.add_trace(go.Scatter(x=years, y=private_tuition, mode="lines",
        line=dict(width=0), fill="tonexty", fillcolor="rgba(46,134,171,0.08)",
        showlegend=False, hoverinfo="skip", name="_fill"))
    fig.add_trace(go.Scatter(x=years, y=public_tuition, mode="lines+markers",
        line=dict(color="#2E86AB", width=2.5), marker=dict(size=6, color="#2E86AB"),
        showlegend=False, hovertemplate="Year: %{x}<br>Public: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=years, y=private_tuition, mode="lines+markers",
        line=dict(color="#E84855", width=2.5), marker=dict(size=6, color="#E84855"),
        showlegend=False, hovertemplate="Year: %{x}<br>Private: $%{y:,.0f}<extra></extra>"))
    fig.add_annotation(x=2023, y=public_tuition[-1], text="<b>Public</b><br>$10,940",
        xanchor="left", yanchor="middle", xshift=10, showarrow=False,
        font=dict(size=11, color="#2E86AB"), bgcolor="rgba(0,0,0,0)")
    fig.add_annotation(x=2023, y=private_tuition[-1], text="<b>Private</b><br>$39,400",
        xanchor="left", yanchor="middle", xshift=10, showarrow=False,
        font=dict(size=11, color="#E84855"), bgcolor="rgba(0,0,0,0)")
    gap_mid = (public_tuition[-1] + private_tuition[-1]) / 2
    fig.add_annotation(x=2023, y=gap_mid, text="Gap:<br><b>$28,460</b>",
        xanchor="left", yanchor="middle", xshift=72,
        showarrow=True, arrowhead=0, arrowcolor="#2D2D2D", arrowwidth=1, ax=0, ay=0,
        font=dict(size=11, color="#2D2D2D"),
        bgcolor="#FFFFFF", bordercolor="#E8E8E8", borderwidth=1, borderpad=4)
    fig.update_layout(height=380, margin=dict(t=20, b=50, l=60, r=110),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", showlegend=False,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB"),
        xaxis=dict(title="Year", tickvals=years, tickfont=dict(size=11, color="#6C757D"),
            showline=False, showgrid=False, zeroline=False),
        yaxis=dict(title="Annual Tuition (USD)", tickformat="$,.0f",
            tickfont=dict(size=11, color="#6C757D"), showline=False,
            showgrid=True, gridcolor="#E8E8E8", nticks=5, zeroline=False, rangemode="tozero"))
    return fig


@st.cache_data
def build_chart2():
    states_rev  = list(reversed(states))
    tuition_rev = list(reversed(state_tuition))
    colors      = ["#B0C4D8"] * 7 + ["#E84855"] * 3
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tuition_rev, y=states_rev, orientation="h", width=0.6,
        marker_color=colors, text=[f"${v:,}" for v in tuition_rev],
        textposition="outside", textfont=dict(size=11, color="#2D2D2D"),
        showlegend=False, hovertemplate="State: %{y}<br>Tuition: $%{x:,.0f}<extra></extra>"))
    fig.add_vline(x=national_average, line_dash="dash", line_color="#2D2D2D", line_width=1.5)
    fig.add_annotation(x=national_average, y=1.02, yref="paper",
        text="National Avg $13,200", showarrow=False, xanchor="center",
        font=dict(size=10, color="#2D2D2D"), bgcolor="#FFFFFF", borderpad=3)
    fig.update_layout(height=380, margin=dict(t=20, b=30, l=120, r=80),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", showlegend=False,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB"),
        xaxis=dict(showticklabels=False, showline=False, showgrid=False,
            zeroline=False, range=[0, max(tuition_rev) * 1.22]),
        yaxis=dict(tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, showgrid=False, zeroline=False))
    return fig


@st.cache_data
def build_chart3():
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=cost_categories, y=cost_values,
        text=[f"${v:,}" for v in cost_values], textposition="outside",
        textfont=dict(size=11, color="#2D2D2D"),
        increasing=dict(marker=dict(color="#2E86AB")),
        totals=dict(marker=dict(color="#E84855")),
        connector=dict(line=dict(color="#B0C4D8", width=1), mode="between"),
        hovertemplate="Component: %{x}<br>Amount: $%{y:,.0f}<extra></extra>",
        showlegend=False))
    fig.add_annotation(x="Base Tuition", y=5470, text="43% of total",
        showarrow=False, font=dict(size=10, color="#FFFFFF"),
        xanchor="center", yanchor="middle")
    fig.add_annotation(x="Total Cost", y=cost_values[-1],
        text="<b>Total: $25,420</b><br>per year",
        showarrow=True, arrowhead=2, arrowcolor="#E84855", arrowwidth=1.5,
        ax=50, ay=-40, xanchor="left", font=dict(size=12, color="#E84855"),
        bgcolor="#FFFFFF", bordercolor="#E84855", borderwidth=1, borderpad=5)
    fig.update_layout(height=380, margin=dict(t=20, b=50, l=70, r=80),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", showlegend=False,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB"),
        xaxis=dict(tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, showgrid=False, zeroline=False),
        yaxis=dict(title="Cost (USD)", tickformat="$,.0f",
            tickfont=dict(size=11, color="#6C757D"), showline=False,
            showgrid=True, gridcolor="#E8E8E8", nticks=5,
            zeroline=False, rangemode="tozero", range=[0, cost_values[-1] * 1.25]))
    return fig


@st.cache_data
def build_chart4():
    z_vals   = df_heat.values.tolist()
    y_labels = df_heat.index.tolist()
    x_labels = [str(yr) for yr in heatmap_years]
    fig = go.Figure(go.Heatmap(
        z=z_vals, x=x_labels, y=y_labels,
        colorscale="Blues", showscale=True, xgap=2, ygap=2,
        hovertemplate="State: %{y}<br>Year: %{x}<br>Tuition: $%{z:,.0f}<extra></extra>",
        colorbar=dict(title=dict(text="Tuition (USD)", font=dict(size=11), side="right"),
            tickformat="$,.0f", nticks=5, thickness=15, outlinewidth=0)))
    for state in y_labels:
        for yr_str in x_labels:
            val = df_heat.loc[state, int(yr_str)]
            fig.add_annotation(x=yr_str, y=state, text=f"${val:,}",
                showarrow=False, font=dict(size=9, color="#FFFFFF" if val > 12000 else "#2D2D2D"),
                xanchor="center", yanchor="middle")
    fig.update_layout(height=380, margin=dict(t=20, b=50, l=120, r=80),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB"),
        xaxis=dict(title="Year", tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, side="bottom"),
        yaxis=dict(tickfont=dict(size=11, color="#2D2D2D"), showline=False, title=None))
    return fig


# ─────────────────────────────────────────────
# CHART ROW 1
# ─────────────────────────────────────────────
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-label">TREND OVER TIME</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">The gap between public and private tuition has tripled since 2000</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">Average annual tuition for 4-year institutions | 2000–2023</p>', unsafe_allow_html=True)
        st.plotly_chart(build_chart1(), use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<p class="section-label">GEOGRAPHIC COMPARISON</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">Vermont, New Hampshire and Pennsylvania lead as the most expensive states</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">Average annual in-state tuition by state | 2023 | Sorted highest to lowest</p>', unsafe_allow_html=True)
        st.plotly_chart(build_chart2(), use_container_width=True, config={"displayModeBar": False})

st.write("")

# ─────────────────────────────────────────────
# CHART ROW 2
# ─────────────────────────────────────────────
with st.container():
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<p class="section-label">COST COMPOSITION</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">Tuition is only 43% of what students actually pay to attend college</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">Average annual cost of attendance breakdown for 4-year public institutions | 2023</p>', unsafe_allow_html=True)
        st.plotly_chart(build_chart3(), use_container_width=True, config={"displayModeBar": False})

    with col4:
        st.markdown('<p class="section-label">STATE TRENDS OVER TIME</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">Northeastern states have seen the steepest tuition increases over two decades</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">Average in-state tuition by state and year | States sorted by 2023 tuition</p>', unsafe_allow_html=True)
        st.plotly_chart(build_chart4(), use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
_, fc, _ = st.columns([1, 2, 1])
with fc:
    st.markdown('<p class="footer-text" style="text-align:center;">Data Source: National Center for Education Statistics (NCES)</p>', unsafe_allow_html=True)
