import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="US College Tuition & Fees Dashboard",
    page_icon="\U0001f393",
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

# Tuition Trend Data (Public vs Private, 2000-2023)
years           = [2000, 2005, 2010, 2015, 2018, 2020, 2021, 2022, 2023]
public_tuition  = [3500, 5100, 7600, 9400, 10200, 10560, 10740, 10850, 10940]
private_tuition = [16200, 21200, 27300, 33500, 36800, 37650, 38200, 38900, 39400]

# Top 10 Most Expensive States (2023)
states = [
    "Vermont", "New Hampshire", "Pennsylvania", "Michigan", "Massachusetts",
    "Illinois", "Connecticut", "New Jersey", "Colorado", "Virginia",
]
state_tuition    = [20600, 19400, 18600, 17800, 17200, 16900, 16400, 16100, 15800, 15400]
national_average = 13200

# Waterfall Chart Data - Total Cost of Attendance Breakdown (2023)
cost_categories = ["Base Tuition", "Fees", "Room", "Board (Meals)", "Books & Supplies", "Total Cost"]
cost_values     = [10940, 1240, 7200, 4800, 1240, 25420]

# Heatmap Data - 10 States x 6 Years
heatmap_states = [
    "Vermont", "Pennsylvania", "Michigan", "New York", "California",
    "North Carolina", "Utah", "Texas", "Florida", "Wyoming",
]
heatmap_years  = [2000, 2005, 2010, 2015, 2020, 2023]
heatmap_values = [
    [7200, 10100, 14200, 17800, 19200, 20600],  # Vermont
    [5600,  8900, 12400, 15100, 17200, 18600],  # Pennsylvania
    [5100,  8200, 11800, 14200, 16100, 17800],  # Michigan
    [4100,  5900,  8800, 11200, 13100, 14800],  # New York
    [3400,  5200,  8100,  9800, 11400, 12600],  # California
    [2900,  4100,  5800,  7200,  7600,  7900],  # North Carolina
    [2600,  3800,  5100,  6800,  7400,  8100],  # Utah
    [3200,  4800,  7200,  9100, 10200, 11400],  # Texas
    [2800,  3900,  5700,  6300,  6900,  7200],  # Florida
    [2100,  2900,  3800,  4600,  5200,  5600],  # Wyoming
]

# KPI Values
kpi_public_tuition   = 10940
kpi_private_tuition  = 39400
kpi_tuition_increase = 213
kpi_total_cost       = 25420

# ─────────────────────────────────────────────
# HEATMAP DATAFRAME  (built once, reused)
# ─────────────────────────────────────────────
df_heat = pd.DataFrame(heatmap_values, index=heatmap_states, columns=heatmap_years)
df_heat = df_heat.iloc[::-1]   # reverse so Vermont is at top in Plotly

# ─────────────────────────────────────────────
# CACHED CHART BUILDERS
# ─────────────────────────────────────────────

@st.cache_data
def build_chart1():
    fig = go.Figure()

    # Invisible base for fill
    fig.add_trace(go.Scatter(
        x=years, y=public_tuition,
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip", name="_base",
    ))
    # Gap fill band
    fig.add_trace(go.Scatter(
        x=years, y=private_tuition,
        mode="lines", line=dict(width=0),
        fill="tonexty", fillcolor="rgba(46,134,171,0.08)",
        showlegend=False, hoverinfo="skip", name="_gap_fill",
    ))
    # Public line
    fig.add_trace(go.Scatter(
        x=years, y=public_tuition,
        mode="lines+markers", name="Public (In-State)",
        line=dict(color="#2E86AB", width=2.5),
        marker=dict(size=6, color="#2E86AB"),
        showlegend=False,
        hovertemplate="Year: %{x}<br>Public Tuition: $%{y:,.0f}<extra></extra>",
    ))
    # Private line
    fig.add_trace(go.Scatter(
        x=years, y=private_tuition,
        mode="lines+markers", name="Private",
        line=dict(color="#E84855", width=2.5),
        marker=dict(size=6, color="#E84855"),
        showlegend=False,
        hovertemplate="Year: %{x}<br>Private Tuition: $%{y:,.0f}<extra></extra>",
    ))

    # End-of-line labels
    fig.add_annotation(
        x=2023, y=public_tuition[-1],
        text="<b>Public</b><br>$10,940",
        xanchor="left", yanchor="middle", xshift=10,
        showarrow=False, font=dict(size=11, color="#2E86AB"),
        bgcolor="rgba(255,255,255,0)",
    )
    fig.add_annotation(
        x=2023, y=private_tuition[-1],
        text="<b>Private</b><br>$39,400",
        xanchor="left", yanchor="middle", xshift=10,
        showarrow=False, font=dict(size=11, color="#E84855"),
        bgcolor="rgba(255,255,255,0)",
    )

    # Gap callout
    gap_mid_y = (public_tuition[-1] + private_tuition[-1]) / 2
    fig.add_annotation(
        x=2023, y=gap_mid_y,
        text="Gap:<br><b>$28,460</b>",
        xanchor="left", yanchor="middle", xshift=72,
        showarrow=True, arrowhead=0,
        arrowcolor="#2D2D2D", arrowwidth=1, ax=0, ay=0,
        font=dict(size=11, color="#2D2D2D"),
        bgcolor="#FFFFFF", bordercolor="#E8E8E8", borderwidth=1, borderpad=4,
    )

    fig.update_layout(
        height=380,
        margin=dict(t=20, b=50, l=60, r=110),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        showlegend=False,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB",
                        font_size=12, font_family="Segoe UI"),
        xaxis=dict(
            title=dict(text="Year", font=dict(size=11, color="#6C757D")),
            tickvals=years, tickfont=dict(size=11, color="#6C757D"),
            showline=False, showgrid=False, zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Annual Tuition (USD)", font=dict(size=11, color="#6C757D")),
            tickformat="$,.0f", tickfont=dict(size=11, color="#6C757D"),
            showline=False, showgrid=True,
            gridcolor="#E8E8E8", gridwidth=1, nticks=5,
            zeroline=False, rangemode="tozero",
        ),
    )
    return fig


@st.cache_data
def build_chart2():
    states_rev  = list(reversed(states))
    tuition_rev = list(reversed(state_tuition))
    bar_colors  = ["#B0C4D8"] * 7 + ["#E84855"] * 3

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tuition_rev, y=states_rev,
        orientation="h", width=0.6,
        marker_color=bar_colors,
        text=[f"${v:,}" for v in tuition_rev],
        textposition="outside",
        textfont=dict(size=11, color="#2D2D2D"),
        showlegend=False,
        hovertemplate="State: %{y}<br>Tuition: $%{x:,.0f}<extra></extra>",
    ))

    fig.add_vline(x=national_average, line_dash="dash",
                  line_color="#2D2D2D", line_width=1.5)
    fig.add_annotation(
        x=national_average, y=1.02, yref="paper",
        text="National Avg $13,200",
        showarrow=False, xanchor="center",
        font=dict(size=10, color="#2D2D2D"),
        bgcolor="#FFFFFF", borderpad=3,
    )

    fig.update_layout(
        height=380,
        margin=dict(t=20, b=30, l=120, r=80),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        showlegend=False,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB",
                        font_size=12, font_family="Segoe UI"),
        xaxis=dict(
            showticklabels=False, showline=False,
            showgrid=False, zeroline=False, title=None,
            range=[0, max(tuition_rev) * 1.22],
        ),
        yaxis=dict(
            tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, showgrid=False, zeroline=False,
        ),
    )
    return fig


@st.cache_data
def build_chart3():
    measures = ["absolute", "relative", "relative", "relative", "relative", "total"]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measures,
        x=cost_categories,
        y=cost_values,
        text=[f"${v:,}" for v in cost_values],
        textposition="outside",
        textfont=dict(size=11, color="#2D2D2D"),
        increasing=dict(marker=dict(color="#2E86AB")),
        totals=dict(marker=dict(color="#E84855")),
        connector=dict(line=dict(color="#B0C4D8", width=1), mode="between"),
        hovertemplate="Component: %{x}<br>Amount: $%{y:,.0f}<extra></extra>",
        showlegend=False,
    ))

    # "43% of total" inside Base Tuition bar (midpoint 0→10940)
    fig.add_annotation(
        x="Base Tuition", y=5470,
        text="43% of total",
        showarrow=False,
        font=dict(size=10, color="#FFFFFF"),
        xanchor="center", yanchor="middle",
    )

    # Total Cost callout
    fig.add_annotation(
        x="Total Cost", y=cost_values[-1],
        text="<b>Total: $25,420</b><br>per year",
        showarrow=True, arrowhead=2,
        arrowcolor="#E84855", arrowwidth=1.5,
        ax=50, ay=-40, xanchor="left",
        font=dict(size=12, color="#E84855"),
        bgcolor="#FFFFFF", bordercolor="#E84855", borderwidth=1, borderpad=5,
    )

    fig.update_layout(
        height=380,
        margin=dict(t=20, b=50, l=70, r=80),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        showlegend=False,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB",
                        font_size=12, font_family="Segoe UI"),
        xaxis=dict(
            tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, showgrid=False, zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Cost (USD)", font=dict(size=11, color="#6C757D")),
            tickformat="$,.0f", tickfont=dict(size=11, color="#6C757D"),
            showline=False, showgrid=True,
            gridcolor="#E8E8E8", gridwidth=1, nticks=5,
            zeroline=False, rangemode="tozero",
            range=[0, cost_values[-1] * 1.25],
        ),
    )
    return fig


@st.cache_data
def build_chart4():
    z_vals   = df_heat.values.tolist()
    y_labels = df_heat.index.tolist()
    x_labels = [str(yr) for yr in heatmap_years]

    fig = go.Figure(go.Heatmap(
        z=z_vals, x=x_labels, y=y_labels,
        colorscale="Blues",
        showscale=True,
        xgap=2, ygap=2,
        hovertemplate="State: %{y}<br>Year: %{x}<br>Tuition: $%{z:,.0f}<extra></extra>",
        colorbar=dict(
            title=dict(text="Tuition (USD)", font=dict(size=11), side="right"),
            tickformat="$,.0f", nticks=5,
            thickness=15, outlinewidth=0,
        ),
    ))

    # Cell value annotations
    for state in y_labels:
        for yr_str in x_labels:
            val = df_heat.loc[state, int(yr_str)]
            txt_color = "#FFFFFF" if val > 12000 else "#2D2D2D"
            fig.add_annotation(
                x=yr_str, y=state,
                text=f"${val:,}",
                showarrow=False,
                font=dict(size=9, color=txt_color),
                xanchor="center", yanchor="middle",
            )

    fig.update_layout(
        height=380,
        margin=dict(t=20, b=50, l=120, r=80),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#2E86AB",
                        font_size=12, font_family="Segoe UI"),
        xaxis=dict(
            title=dict(text="Year", font=dict(size=11, color="#2D2D2D")),
            tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, side="bottom",
        ),
        yaxis=dict(
            tickfont=dict(size=11, color="#2D2D2D"),
            showline=False, title=None,
        ),
    )
    return fig


# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
/* Thin blue top border across the full page */
body::before {
    content: "";
    display: block;
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 4px;
    background-color: #2E86AB;
    z-index: 9999;
}

/* Reset Streamlit chrome */
#root > div:first-child { background-color: #FFFFFF; }
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
    background-color: #FFFFFF;
}

/* Body font */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    color: #2D2D2D;
    background-color: #FFFFFF;
}

/* KPI card hover effect */
.kpi-card {
    background-color: #F8F9FA;
    border-left: 4px solid #2E86AB;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    transition: border-left-color 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
    box-sizing: border-box;
}
.kpi-card:hover {
    border-left-color: #E84855;
    box-shadow: 0 4px 12px rgba(0,0,0,0.14);
}

/* Section eyebrow labels */
.section-label {
    font-size: 10px;
    font-weight: 600;
    color: #9E9E9E;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
    margin-top: 0;
}

/* KPI row eyebrow */
.kpi-eyebrow {
    font-size: 11px;
    font-weight: 600;
    color: #9E9E9E;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    margin-top: 0;
}

/* Divider spacing */
hr {
    margin-top: 16px !important;
    margin-bottom: 16px !important;
    border-color: #E8E8E8 !important;
}

/* Footer */
.footer-bar {
    background-color: #F8F9FA;
    border-top: 1px solid #E8E8E8;
    padding: 16px 0 8px 0;
    margin-top: 8px;
}
.footer-text {
    font-size: 12px;
    color: #6C757D;
    font-family: 'Segoe UI', sans-serif;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# DASHBOARD TITLE SECTION
# ─────────────────────────────────────────────
st.markdown(
    '<p style="font-size:22px;font-weight:700;color:#2D2D2D;margin-bottom:2px;'
    'font-family:Segoe UI,sans-serif;white-space:nowrap;">'
    "US College Tuition &amp; Fees Dashboard"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="font-size:14px;color:#6C757D;margin-bottom:4px;'
    'font-family:Segoe UI,sans-serif;">'
    "Analyzing tuition trends, state comparisons, and total cost of attendance "
    "across US institutions (2000 - 2023)"
    "</p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<p style="font-size:11px;color:#9E9E9E;font-style:italic;margin-bottom:20px;'
    'font-family:Segoe UI,sans-serif;">'
    "Source: National Center for Education Statistics (NCES)"
    "</p>",
    unsafe_allow_html=True,
)



# ─────────────────────────────────────────────
# KPI CARDS ROW
# ─────────────────────────────────────────────
st.markdown('<p class="kpi-eyebrow">KEY METRICS AT A GLANCE</p>', unsafe_allow_html=True)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")

def kpi_card(icon, label, value, delta, delta_color):
    return (
        f'<div class="kpi-card">'
        f'<div style="font-size:22px;margin-bottom:6px;">{icon}</div>'
        f'<div style="font-size:13px;color:#6C757D;font-weight:normal;'
        f'font-family:Segoe UI,sans-serif;margin-bottom:6px;">{label}</div>'
        f'<div style="font-size:28px;color:#2D2D2D;font-weight:700;'
        f'font-family:Segoe UI,sans-serif;margin-bottom:8px;line-height:1.1;">{value}</div>'
        f'<div style="font-size:12px;color:{delta_color};'
        f'font-family:Segoe UI,sans-serif;">{delta}</div>'
        f"</div>"
    )

with kpi_col1:
    st.markdown(kpi_card(
        icon="\U0001f3db\ufe0f",
        label="Avg Public Tuition (2023)",
        value="$10,940",
        delta="+213% since 2000",
        delta_color="#E84855",
    ), unsafe_allow_html=True)

with kpi_col2:
    st.markdown(kpi_card(
        icon="\U0001f393",
        label="Avg Private Tuition (2023)",
        value="$39,400",
        delta="+143% since 2000",
        delta_color="#E84855",
    ), unsafe_allow_html=True)

with kpi_col3:
    st.markdown(kpi_card(
        icon="\U0001f4c8",
        label="Public Tuition Growth",
        value="+213%",
        delta="Over 23 years (2000-2023)",
        delta_color="#6C757D",
    ), unsafe_allow_html=True)

with kpi_col4:
    st.markdown(kpi_card(
        icon="\U0001f4b0",
        label="Avg Total Cost of Attendance",
        value="$25,420",
        delta="Tuition is only 43% of total cost",
        delta_color="#6C757D",
    ), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DIVIDER
# ─────────────────────────────────────────────
st.divider()

# ─────────────────────────────────────────────
# CHART ROW 1  (Chart 1 left | Chart 2 right)
# ─────────────────────────────────────────────
with st.container():
    chart_row1_left, chart_row1_right = st.columns(2)

    with chart_row1_left:
        st.markdown('<p class="section-label">TREND OVER TIME</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">'
            "The gap between public and private tuition has tripled since 2000"
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">'
            "Average annual tuition for 4-year institutions | 2000 - 2023"
            "</p>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(build_chart1(), use_container_width=True,
                        config={"displayModeBar": False})

    with chart_row1_right:
        st.markdown('<p class="section-label">GEOGRAPHIC COMPARISON</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">'
            "Vermont, New Hampshire and Pennsylvania lead as the most expensive states for college tuition"
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">'
            "Average annual in-state tuition by state | 2023 | Sorted by tuition (highest to lowest)"
            "</p>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(build_chart2(), use_container_width=True,
                        config={"displayModeBar": False})

st.write("")  # row spacer

# ─────────────────────────────────────────────
# CHART ROW 2  (Chart 3 left | Chart 4 right)
# ─────────────────────────────────────────────
with st.container():
    chart_row2_left, chart_row2_right = st.columns(2)

    with chart_row2_left:
        st.markdown('<p class="section-label">COST COMPOSITION</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">'
            "Tuition is only 43% of what students actually pay to attend college"
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">'
            "Average annual cost of attendance breakdown for 4-year public institutions | 2023"
            "</p>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(build_chart3(), use_container_width=True,
                        config={"displayModeBar": False})

    with chart_row2_right:
        st.markdown('<p class="section-label">STATE TRENDS OVER TIME</p>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:15px;font-weight:600;color:#2D2D2D;margin-bottom:2px;">'
            "Northeastern states have seen the steepest and most sustained tuition increases over two decades"
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="font-size:12px;color:#6C757D;margin-top:0;margin-bottom:8px;">'
            "Average in-state tuition by state and year (USD) | States sorted by 2023 tuition (highest to lowest)"
            "</p>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(build_chart4(), use_container_width=True,
                        config={"displayModeBar": False})

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()

foot_left, foot_center, foot_right = st.columns([1, 2, 1])

with foot_center:
    st.markdown(
        '<p class="footer-text" style="text-align:center;">'
        "Data Source: National Center for Education Statistics (NCES)"
        "</p>",
        unsafe_allow_html=True,
    )
