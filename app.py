import base64

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="MAHB Pond Simulator",
    page_icon="💧",
    layout="wide",
)

AIRB_LOGO_BASE64 = "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tn89J8/Zs2pC3fEO7N69e2ho6Jprrrn88sujUIy22Pnz51966aVR/sdpHhoaUtVoBIi66fXXXz9//vwjR45kWfba1752/vz569atazQaO3fubDab11xzzXvf+96ZM2fu3r17/vz5r33ta6vV6sjISJqmV1999cDAwPDwMBFdeeWVM2bM2L179xve8IY0TTdv3hxXUZTrixYtGh8f37p1KzO/5z3veeMb32iMOX78+LnnnnvppZdG6Rvhve/u7l6xYkWz2dy2bVt3d/cHP/jBd77znWmaHj58uFKpxIdA5+kBwAWnbJYsmb94wfy+ajqzO+1KijRtllNfsqwNVxsatab6wOYnHtj0+H0bH3tww6ZHHl2/c9/QkVEdPDyybceW8fHRI4cGh48enqjVa80GE5fK1iYYGxvfumWb5LVVS2a88hUvZw2HBvdVs+SsJXPe8cYr04Qe27ypmtEl560+d+3yoYND+/dumT2z59KLz186f+bgnl3BF9O7+S2vu+SsFUu3bX187PihZQtmveKSdf09lXmzZy6cP+AbE0XRHB4+cvDIkYlGbcmyuW9+3Svfdd1VlZSIhQ0pUwjemDQ0i0pX13nnn1cplY8dGz44dOiss8760Ic+NH369AsvvHD58uV79uxZtGjRFVdcUSqVZs2atWjRon379m3evLmvr+/Xfu3X3vCGN3R3d/f29h48eHBwcHD58uUvf/nL+/v7r7322tHR0Ztuumnu3Llz5sx59NFHL7rooo9//OMrV67sZI50KPssiftsA8njeaOo7+7u7pAghNBoNEQkugQ7Xt88zycmJrq7u6N/b3x8vLe3N7I8+rTSNI3G6qNHj2ZZNn369CRJiqJoNptROlYqlUaj0Wg0osWEiOIWkJnHx8crlUpRFMePH8+ybObMmR1HzsTExPDwcFdX17Rp06y1eZ5HRaq/v7/jhOz4lr33jUZjeHi4XC739fWhrVLXarW+vr6oeHXUlVjOUUGGkecYHW+OjTcOjx4LSkXD7d+ya/DxLa++/Ip6wrXQHHf1GbNmlNKE0/7v3vrEzTf/czlt/MF/+fWXn7co0QbAWZYRJElI1OWeBg9ONBp5d4VmzZpV99h/cDiI6a5W5vRXgs8PHDleFH52f/+MGZUjI7Wjx4eJzMDMGV2V0u69+xveQvyK+TO7u7K9B48eGxvPErto/pxKakQg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"

st.markdown(
    f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 1.25rem;
        margin: 0.2rem 0 1.1rem 0;
    ">
        <img
            src="data:image/png;base64,{AIRB_LOGO_BASE64}"
            alt="AIRB — A Member of MMC Group"
            style="width: 155px; height: auto;"
        />
        <div>
            <h1 style="margin: 0; padding: 0;">
                MAHB Southern Balancing Pond Simulator
            </h1>
            <p style="margin: 0.25rem 0 0 0; color: #667085;">
                Preliminary water-balance and adaptive operating analysis
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

data = pd.read_excel(
    "data/historical_2000_2025.xlsx", sheet_name="Monthly Data"
)
data = data.rename(
    columns={
        "Date": "date",
        "Rainfall (mm/month)": "rainfall_mm",
        "Evaporation (mm/month)": "evaporation_mm",
        "Days": "days",
    }
)
data["date"] = pd.to_datetime(data["date"])

period_mode = st.sidebar.selectbox(
    "Analysis period",
    [
        "Full history: 2000–2025",
        "2002 drought: January–March",
        "2013 drought: April–June",
        "Custom period",
    ],
)

if period_mode == "2002 drought: January–March":
    start_date = pd.Timestamp("2002-01-01")
    end_date = pd.Timestamp("2002-03-01")
elif period_mode == "2013 drought: April–June":
    start_date = pd.Timestamp("2013-04-01")
    end_date = pd.Timestamp("2013-06-01")
elif period_mode == "Custom period":
    available_months = data["date"].dt.strftime("%b %Y").tolist()
    start_label = st.sidebar.selectbox(
        "Start month", available_months, index=0
    )
    end_label = st.sidebar.selectbox(
        "End month", available_months, index=len(available_months) - 1
    )
    start_date = pd.to_datetime(start_label, format="%b %Y")
    end_date = pd.to_datetime(end_label, format="%b %Y")
    if start_date > end_date:
        st.error("Start month must be earlier than or equal to end month.")
        st.stop()
else:
    start_date = data["date"].min()
    end_date = data["date"].max()

data = data[
    (data["date"] >= start_date) & (data["date"] <= end_date)
].copy()

period_description = (
    f"{start_date.strftime('%b %Y')} to {end_date.strftime('%b %Y')}"
)

st.caption(
    f"Monthly water-balance simulation for {period_description}. "
    "Rainfall and evaporation inputs are based on the consultant's report."
)

st.sidebar.header("Simulation Inputs")

abstraction_mld = st.sidebar.slider(
    "Total raw-water abstraction (MLD)",
    min_value=0.0,
    max_value=25.0,
    value=16.5,
    step=0.5,
)

runoff_coefficient = st.sidebar.slider(
    "Runoff coefficient",
    min_value=0.10,
    max_value=0.90,
    value=0.45,
    step=0.05,
)

initial_level = st.sidebar.slider(
    "Initial pond level (m RL)",
    min_value=6.76,
    max_value=8.35,
    value=8.35,
    step=0.01,
)

rainfall_multiplier = st.sidebar.slider(
    "Rainfall multiplier",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    step=0.05,
)

st.sidebar.subheader("Adaptive Expansion Strategy")
phase_2_reference_mld = 16.5
minimum_required_supply_mld = st.sidebar.slider(
    "Minimum required supply (MLD)",
    min_value=0.0,
    max_value=phase_2_reference_mld,
    value=11.0,
    step=0.5,
    help=(
        "The minimum monthly operating rate that the adaptive strategy "
        "must maintain. Targets that require supply below this value are "
        "excluded from the recommendation."
    ),
)
expansion_target_mld = st.sidebar.slider(
    "Normal-operation target (MLD)",
    min_value=max(11.0, minimum_required_supply_mld),
    max_value=30.0,
    value=phase_2_reference_mld,
    step=0.5,
)
curtailment_trigger_level = st.sidebar.slider(
    "Curtailment trigger level (m RL)",
    min_value=7.00,
    max_value=8.30,
    value=7.70,
    step=0.05,
)

catchment_area_km2 = 20.0
pond_area_km2 = 0.5948
maximum_level = 8.35
maximum_storage_ml = 1166.0
safe_level = 7.00
dead_zone_level = 6.76

pond_bed_level = maximum_level - (
    maximum_storage_ml / (pond_area_km2 * 1000)
)
initial_storage_ml = (
    initial_level - pond_bed_level
) * pond_area_km2 * 1000

storage = max(0.0, min(initial_storage_ml, maximum_storage_ml))
results = []

for _, row in data.iterrows():
    rainfall_mm = row["rainfall_mm"] * rainfall_multiplier
    runoff_ml = rainfall_mm * catchment_area_km2 * runoff_coefficient
    evaporation_ml = row["evaporation_mm"] * pond_area_km2
    abstraction_ml = abstraction_mld * row["days"]

    calculated_storage = (
        storage + runoff_ml - evaporation_ml - abstraction_ml
    )
    spill_ml = max(0.0, calculated_storage - maximum_storage_ml)
    storage = max(0.0, min(calculated_storage, maximum_storage_ml))
    water_level = pond_bed_level + (
        storage / (pond_area_km2 * 1000)
    )

    results.append(
        {
            "Date": row["date"],
            "Rainfall (mm)": rainfall_mm,
            "Runoff (ML)": runoff_ml,
            "Evaporation (ML)": evaporation_ml,
            "Abstraction (ML)": abstraction_ml,
            "Spill (ML)": spill_ml,
            "Storage (ML)": storage,
            "Water Level (m RL)": water_level,
        }
    )

results = pd.DataFrame(results)
minimum_level = results["Water Level (m RL)"].min()
final_storage = results["Storage (ML)"].iloc[-1]
months_below_safe = int(
    (results["Water Level (m RL)"] < safe_level).sum()
)
critical_row = results.loc[results["Water Level (m RL)"].idxmin()]
critical_month = critical_row["Date"].strftime("%b %Y")
reliability = 100.0 * (1.0 - months_below_safe / len(results))
total_spill = results["Spill (ML)"].sum()


def minimum_level_for_abstraction(test_abstraction_mld):
    test_storage = max(
        0.0, min(initial_storage_ml, maximum_storage_ml)
    )
    test_minimum_level = maximum_level

    for _, test_row in data.iterrows():
        test_runoff_ml = (
            test_row["rainfall_mm"]
            * rainfall_multiplier
            * catchment_area_km2
            * runoff_coefficient
        )
        test_evaporation_ml = (
            test_row["evaporation_mm"] * pond_area_km2
        )
        test_abstraction_ml = (
            test_abstraction_mld * test_row["days"]
        )
        test_storage = max(
            0.0,
            min(
                maximum_storage_ml,
                test_storage
                + test_runoff_ml
                - test_evaporation_ml
                - test_abstraction_ml,
            ),
        )
        test_level = pond_bed_level + (
            test_storage / (pond_area_km2 * 1000)
        )
        test_minimum_level = min(test_minimum_level, test_level)

    return test_minimum_level


def scenario_summary(test_abstraction_mld):
    test_storage = max(
        0.0, min(initial_storage_ml, maximum_storage_ml)
    )
    levels = []

    for _, test_row in data.iterrows():
        test_runoff_ml = (
            test_row["rainfall_mm"]
            * rainfall_multiplier
            * catchment_area_km2
            * runoff_coefficient
        )
        test_evaporation_ml = (
            test_row["evaporation_mm"] * pond_area_km2
        )
        test_storage = max(
            0.0,
            min(
                maximum_storage_ml,
                test_storage
                + test_runoff_ml
                - test_evaporation_ml
                - test_abstraction_mld * test_row["days"],
            ),
        )
        levels.append(
            pond_bed_level
            + test_storage / (pond_area_km2 * 1000)
        )

    minimum_index = min(range(len(levels)), key=levels.__getitem__)
    months_below = sum(level < safe_level for level in levels)
    return {
        "Minimum Level (m RL)": min(levels),
        "Critical Month": data.iloc[minimum_index]["date"].strftime(
            "%b %Y"
        ),
        "Months Below RL 7.00": months_below,
        "Reliability (%)": 100.0 * (1.0 - months_below / len(levels)),
    }


def adaptive_scenario_summary(
    normal_target_mld, trigger_level, minimum_supply_mld
):
    test_storage = max(
        0.0, min(initial_storage_ml, maximum_storage_ml)
    )
    levels = []
    adaptive_rows = []
    delivered_ml = 0.0
    curtailed_months = 0
    reduced_target_mld = minimum_supply_mld
    safe_storage_ml = (
        safe_level - pond_bed_level
    ) * pond_area_km2 * 1000

    for _, test_row in data.iterrows():
        opening_level = pond_bed_level + (
            test_storage / (pond_area_km2 * 1000)
        )
        test_runoff_ml = (
            test_row["rainfall_mm"]
            * rainfall_multiplier
            * catchment_area_km2
            * runoff_coefficient
        )
        test_evaporation_ml = (
            test_row["evaporation_mm"] * pond_area_km2
        )
        requested_rate = (
            reduced_target_mld
            if opening_level <= trigger_level
            else normal_target_mld
        )
        maximum_safe_rate = max(
            0.0,
            (
                test_storage
                + test_runoff_ml
                - test_evaporation_ml
                - safe_storage_ml
            )
            / test_row["days"],
        )
        operating_rate = min(requested_rate, maximum_safe_rate)
        if opening_level <= trigger_level:
            control_reason = "Trigger-level curtailment"
        elif operating_rate < normal_target_mld - 1e-9:
            control_reason = "RL 7.00 safeguard"
        else:
            control_reason = "Normal operation"
        if operating_rate < normal_target_mld - 1e-9:
            curtailed_months += 1

        delivered_ml += operating_rate * test_row["days"]
        test_storage = max(
            0.0,
            min(
                maximum_storage_ml,
                test_storage
                + test_runoff_ml
                - test_evaporation_ml
                - operating_rate * test_row["days"],
            ),
        )
        levels.append(
            pond_bed_level
            + test_storage / (pond_area_km2 * 1000)
        )
        adaptive_rows.append(
            {
                "Date": test_row["date"],
                "Rainfall (mm)": (
                    test_row["rainfall_mm"] * rainfall_multiplier
                ),
                "Opening Level (m RL)": opening_level,
                "Water Level (m RL)": levels[-1],
                "Normal Target (MLD)": normal_target_mld,
                "Requested Rate (MLD)": requested_rate,
                "Operating Rate (MLD)": operating_rate,
                "Reduction (MLD)": normal_target_mld - operating_rate,
                "Supply Shortfall (MLD)": max(
                    0.0, minimum_supply_mld - operating_rate
                ),
                "Control Reason": control_reason,
            }
        )

    minimum_index = min(range(len(levels)), key=levels.__getitem__)
    adaptive_results = pd.DataFrame(adaptive_rows)
    return {
        "Minimum Level (m RL)": min(levels),
        "Critical Month": data.iloc[minimum_index]["date"].strftime(
            "%b %Y"
        ),
        "Average Delivered (MLD)": delivered_ml / data["days"].sum(),
        "Minimum Operating Rate (MLD)": adaptive_results[
            "Operating Rate (MLD)"
        ].min(),
        "Months Below Minimum Supply": int(
            (
                adaptive_results["Operating Rate (MLD)"]
                < minimum_supply_mld - 1e-9
            ).sum()
        ),
        "Curtailment Months": curtailed_months,
        "Results": adaptive_results,
    }


lower_yield = 0.0
upper_yield = 100.0
for _ in range(50):
    trial_yield = (lower_yield + upper_yield) / 2
    if minimum_level_for_abstraction(trial_yield) >= safe_level:
        lower_yield = trial_yield
    else:
        upper_yield = trial_yield

sustainable_yield_mld = lower_yield
yield_margin_mld = sustainable_yield_mld - abstraction_mld

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Minimum Pond Level", f"{minimum_level:.2f} m RL")
col2.metric("Critical Month", critical_month)
col3.metric("Monthly Reliability", f"{reliability:.1f}%")
col4.metric("Months Below RL 7.00", f"{months_below_safe}")
col5.metric("Total Spill", f"{total_spill:,.0f} ML")

with st.expander("Additional simulation totals"):
    total1, total2 = st.columns(2)
    total1.metric("Final Storage", f"{final_storage:,.0f} ML")
    total2.metric(
        "Total Abstraction",
        f"{results['Abstraction (ML)'].sum():,.0f} ML",
    )

if minimum_level >= safe_level:
    st.success("PASS: The simulated pond level remains above RL 7.00 m.")
elif minimum_level >= dead_zone_level:
    st.warning(
        "WARNING: The pond falls below RL 7.00 m but remains above "
        "the dead-zone level."
    )
else:
    st.error("FAIL: The pond enters or falls below the dead zone.")

st.subheader("Historical Yield Analysis")
yield1, yield2, yield3 = st.columns(3)
yield1.metric(
    "Preliminary Sustainable Yield",
    f"{sustainable_yield_mld:.2f} MLD",
)
yield2.metric("Selected Demand", f"{abstraction_mld:.2f} MLD")
yield3.metric(
    "Yield Margin",
    f"{yield_margin_mld:+.2f} MLD",
)

if yield_margin_mld >= 0:
    st.success(
        "The selected abstraction is within the preliminary historical "
        "yield for this simulation period."
    )
else:
    st.error(
        f"The selected abstraction exceeds the preliminary historical "
        f"yield by {abs(yield_margin_mld):.2f} MLD."
    )

st.subheader("Management Scenario Comparison")
comparison_cases = [
    ("Current WTP assumption", 11.0),
    ("Phase 2 total assumption", 16.0),
    ("Consultant / selected case", 16.5),
    ("Calculated firm yield", sustainable_yield_mld),
]
comparison_rows = []
for case_name, case_rate in comparison_cases:
    case_results = scenario_summary(case_rate)
    comparison_rows.append(
        {
            "Scenario": case_name,
            "Abstraction (MLD)": case_rate,
            **case_results,
            "RL 7.00 Criterion": (
                "PASS"
                if case_results["Minimum Level (m RL)"] >= safe_level
                else "BELOW LIMIT"
            ),
        }
    )

comparison_table = pd.DataFrame(comparison_rows)
comparison_display = comparison_table.copy()
comparison_display["Abstraction (MLD)"] = comparison_display[
    "Abstraction (MLD)"
].round(2)
comparison_display["Minimum Level (m RL)"] = comparison_display[
    "Minimum Level (m RL)"
].round(2)
comparison_display["Reliability (%)"] = comparison_display[
    "Reliability (%)"
].round(1)
st.dataframe(comparison_display, width="stretch", hide_index=True)

comparison_figure = go.Figure()
comparison_figure.add_trace(
    go.Bar(
        x=comparison_table["Scenario"],
        y=comparison_table["Minimum Level (m RL)"],
        text=comparison_table["Minimum Level (m RL)"].map(
            lambda value: f"{value:.2f} m RL"
        ),
        textposition="outside",
        marker_color=[
            "#2A9D8F" if value >= safe_level else "#E76F51"
            for value in comparison_table["Minimum Level (m RL)"]
        ],
    )
)
comparison_figure.add_hline(
    y=safe_level,
    line_dash="dash",
    line_color="red",
    annotation_text="Safe Limit RL 7.00",
)
comparison_figure.update_layout(
    xaxis_title="Scenario",
    yaxis_title="Minimum Simulated Level (m RL)",
    yaxis_range=[dead_zone_level - 0.05, maximum_level + 0.15],
    showlegend=False,
)
st.plotly_chart(comparison_figure, width="stretch")

st.caption(
    "The 11.0 MLD and 16.0 MLD cases are planning assumptions. Confirm "
    "the actual current and Phase 2 abstraction rates before issuing the "
    "result for engineering or management approval."
)

st.subheader("Adaptive Expansion Strategy")
adaptive_result = adaptive_scenario_summary(
    expansion_target_mld,
    curtailment_trigger_level,
    minimum_required_supply_mld,
)

feasible_adaptive_targets = []
first_target_half = int(
    max(11.0, minimum_required_supply_mld) * 2
)
for target_halves in range(first_target_half, 61):
    candidate_target = target_halves / 2
    candidate_result = adaptive_scenario_summary(
        candidate_target,
        curtailment_trigger_level,
        minimum_required_supply_mld,
    )
    protects_safe_level = (
        candidate_result["Minimum Level (m RL)"]
        >= safe_level - 1e-9
    )
    maintains_required_supply = (
        candidate_result["Minimum Operating Rate (MLD)"]
        >= minimum_required_supply_mld - 1e-9
    )
    if protects_safe_level and maintains_required_supply:
        feasible_adaptive_targets.append(
            (candidate_target, candidate_result)
        )

adaptive1, adaptive2, adaptive3, adaptive4, adaptive5, adaptive6 = (
    st.columns(6)
)
adaptive1.metric(
    "Normal Target", f"{expansion_target_mld:.1f} MLD"
)
adaptive2.metric(
    "Average Delivered",
    f"{adaptive_result['Average Delivered (MLD)']:.2f} MLD",
)
adaptive3.metric(
    "Minimum Level",
    f"{adaptive_result['Minimum Level (m RL)']:.2f} m RL",
)
adaptive4.metric(
    "Curtailment Months",
    f"{adaptive_result['Curtailment Months']}",
)
adaptive5.metric(
    "Minimum Operating Rate",
    f"{adaptive_result['Minimum Operating Rate (MLD)']:.2f} MLD",
)
adaptive6.metric(
    "Supply-Shortfall Months",
    f"{adaptive_result['Months Below Minimum Supply']}",
)

st.caption(
    f"Phase 2 reference: {phase_2_reference_mld:.1f} MLD. The adaptive "
    "target remains open for hydrological exploration up to 30.0 MLD."
)

selected_protects_safe_level = (
    adaptive_result["Minimum Level (m RL)"] >= safe_level - 1e-9
)
selected_maintains_required_supply = (
    adaptive_result["Minimum Operating Rate (MLD)"]
    >= minimum_required_supply_mld - 1e-9
)

if selected_protects_safe_level and selected_maintains_required_supply:
    st.success(
        "This preliminary operating rule keeps all simulated month-end "
        f"levels at or above RL 7.00 and supply at or above "
        f"{minimum_required_supply_mld:.1f} MLD."
    )
elif not selected_protects_safe_level:
    st.error(
        "This operating rule still falls below RL 7.00. Increase the "
        "trigger level or reduce the normal-operation target."
    )
else:
    st.error(
        f"This operating rule protects RL 7.00 only by reducing supply "
        f"below the required {minimum_required_supply_mld:.1f} MLD. "
        "Increase the trigger level or reduce the normal-operation target."
    )

if feasible_adaptive_targets:
    highest_target, highest_adaptive_result = max(
        feasible_adaptive_targets,
        key=lambda item: item[0],
    )
    st.info(
        f"Across the tested range of 11.0–30.0 MLD and at a trigger of RL "
        f"{curtailment_trigger_level:.2f}, the highest adaptive target that "
        f"protects RL 7.00 without reducing supply below "
        f"{minimum_required_supply_mld:.1f} MLD is "
        f"{highest_target:.1f} MLD. It provides an historical average of "
        f"{highest_adaptive_result['Average Delivered (MLD)']:.2f} MLD "
        f"with {highest_adaptive_result['Curtailment Months']} curtailed "
        f"month(s)."
    )
else:
    st.warning(
        f"No adaptive target in the tested range can protect RL 7.00 while "
        f"maintaining at least {minimum_required_supply_mld:.1f} MLD at "
        f"the selected trigger. Increase the trigger level or review the "
        "minimum required supply."
    )

st.caption(
    "Operating rule: target normal abstraction while the opening monthly "
    "level is above the trigger; otherwise reduce toward the selected "
    f"minimum required supply of {minimum_required_supply_mld:.1f} MLD. A "
    "projected month-end safeguard further limits abstraction whenever "
    "required to protect RL 7.00. Daily rainfall, pond level and abstraction "
    "data are required before this rule can be adopted operationally."
)

adaptive_chart_data = adaptive_result["Results"]
adaptive_figure = go.Figure()
adaptive_figure.add_trace(
    go.Scatter(
        x=adaptive_chart_data["Date"],
        y=adaptive_chart_data["Water Level (m RL)"],
        mode="lines+markers",
        name="Adaptive Pond Level",
        line=dict(color="#2A9D8F", width=3),
    )
)
adaptive_figure.add_hline(
    y=curtailment_trigger_level,
    line_dash="dash",
    line_color="#F4A261",
    annotation_text=(
        f"Curtailment Trigger RL {curtailment_trigger_level:.2f}"
    ),
)
adaptive_figure.add_hline(
    y=safe_level,
    line_dash="dash",
    line_color="red",
    annotation_text="Safe Limit RL 7.00",
)
adaptive_figure.add_hline(
    y=dead_zone_level,
    line_dash="dot",
    line_color="black",
    annotation_text="Dead Zone RL 6.76",
)
adaptive_figure.update_layout(
    title="Adaptive-Strategy Pond Water Level",
    xaxis_title="Month",
    yaxis_title="Water Level (m RL)",
    hovermode="x unified",
)
st.plotly_chart(adaptive_figure, width="stretch")

st.subheader("Adaptive Operating Rate")
operating_figure = go.Figure()
operating_figure.add_trace(
    go.Scatter(
        x=adaptive_chart_data["Date"],
        y=adaptive_chart_data["Operating Rate (MLD)"],
        mode="lines+markers",
        name="Actual Operating Rate",
        line=dict(color="#6A4C93", width=3),
    )
)
operating_figure.add_hline(
    y=expansion_target_mld,
    line_dash="dash",
    line_color="#2A9D8F",
    annotation_text=f"Selected Target {expansion_target_mld:.1f} MLD",
)
operating_figure.add_hline(
    y=phase_2_reference_mld,
    line_dash="dot",
    line_color="#F4A261",
    annotation_text="Phase 2 Reference 16.5 MLD",
)
operating_figure.add_hline(
    y=minimum_required_supply_mld,
    line_dash="dashdot",
    line_color="red",
    annotation_text=(
        f"Minimum Required Supply {minimum_required_supply_mld:.1f} MLD"
    ),
)
operating_figure.update_layout(
    xaxis_title="Month",
    yaxis_title="Operating Rate (MLD)",
    hovermode="x unified",
)
st.plotly_chart(operating_figure, width="stretch")

curtailed_results = adaptive_chart_data[
    adaptive_chart_data["Operating Rate (MLD)"]
    < expansion_target_mld - 1e-9
].copy()

st.subheader("Curtailment Details")
if curtailed_results.empty:
    st.success("No curtailment is required for the selected target.")
else:
    curtailed_display = curtailed_results[
        [
            "Date",
            "Rainfall (mm)",
            "Opening Level (m RL)",
            "Water Level (m RL)",
            "Operating Rate (MLD)",
            "Reduction (MLD)",
            "Supply Shortfall (MLD)",
            "Control Reason",
        ]
    ].copy()
    curtailed_display["Date"] = curtailed_display["Date"].dt.strftime(
        "%b %Y"
    )
    st.dataframe(
        curtailed_display.round(2),
        width="stretch",
        hide_index=True,
    )
    st.download_button(
        "Download curtailed-month results (CSV)",
        data=curtailed_display.to_csv(index=False).encode("utf-8"),
        file_name="MAHB_adaptive_curtailment_results.csv",
        mime="text/csv",
    )

delivery_achievement = (
    adaptive_result["Average Delivered (MLD)"]
    / expansion_target_mld
    * 100
)
uplift_from_phase_2 = (
    adaptive_result["Average Delivered (MLD)"] - phase_2_reference_mld
)
st.subheader("Management Interpretation")
service_status = (
    "PASS"
    if selected_protects_safe_level and selected_maintains_required_supply
    else "FAIL"
)
management_message = (
    f"The selected {expansion_target_mld:.1f} MLD normal target delivers "
    f"an historical average of "
    f"{adaptive_result['Average Delivered (MLD)']:.2f} MLD "
    f"({delivery_achievement:.1f}% of target), while maintaining a minimum "
    f"month-end pond level of RL "
    f"{adaptive_result['Minimum Level (m RL)']:.2f}. This represents "
    f"{uplift_from_phase_2:+.2f} MLD relative to the 16.5 MLD Phase 2 "
    f"reference and requires curtailment in "
    f"{adaptive_result['Curtailment Months']} month(s). Minimum-supply "
    f"criterion: {service_status} against the required "
    f"{minimum_required_supply_mld:.1f} MLD, with "
    f"{adaptive_result['Months Below Minimum Supply']} shortfall month(s)."
)
if service_status == "PASS":
    st.info(management_message)
else:
    st.warning(management_message)

with st.expander("View abstraction sensitivity"):
    sensitivity_rates = [x / 2 for x in range(0, 51)]
    sensitivity_levels = [
        minimum_level_for_abstraction(rate)
        for rate in sensitivity_rates
    ]
    sensitivity_figure = go.Figure()
    sensitivity_figure.add_trace(
        go.Scatter(
            x=sensitivity_rates,
            y=sensitivity_levels,
            mode="lines",
            name="Minimum Pond Level",
            line=dict(color="#6A4C93", width=3),
        )
    )
    sensitivity_figure.add_hline(
        y=safe_level,
        line_dash="dash",
        line_color="red",
        annotation_text="Safe Limit RL 7.00",
    )
    sensitivity_figure.add_vline(
        x=sustainable_yield_mld,
        line_dash="dot",
        line_color="green",
        annotation_text=(
            f"Yield {sustainable_yield_mld:.2f} MLD"
        ),
    )
    sensitivity_figure.update_layout(
        xaxis_title="Constant Abstraction (MLD)",
        yaxis_title="Minimum Simulated Level (m RL)",
        hovermode="x unified",
    )
    st.plotly_chart(sensitivity_figure, width="stretch")

figure = go.Figure()
figure.add_trace(
    go.Scatter(
        x=results["Date"],
        y=results["Water Level (m RL)"],
        mode="lines+markers",
        name="Simulated Pond Level",
        line=dict(color="#0077B6", width=3),
    )
)
figure.add_hline(
    y=safe_level,
    line_dash="dash",
    line_color="red",
    annotation_text="Safe Limit RL 7.00",
)
figure.add_hline(
    y=dead_zone_level,
    line_dash="dot",
    line_color="black",
    annotation_text="Dead Zone RL 6.76",
)
figure.update_layout(
    title=(
        f"Fixed-Abstraction Pond Water Level ({abstraction_mld:.1f} MLD)"
    ),
    xaxis_title="Month",
    yaxis_title="Water Level (m RL)",
    hovermode="x unified",
)
st.plotly_chart(figure, width="stretch")

st.subheader("Monthly Water-Balance Results")
display_results = results.copy()
display_results["Date"] = display_results["Date"].dt.strftime("%b %Y")
st.dataframe(
    display_results.round(2),
    width="stretch",
    hide_index=True,
)

st.info(
    "This remains a simplified monthly model using a constant pond-area "
    "approximation. The sustainable-yield result is preliminary and based on "
    "month-end levels. Calibration against observed pond levels and a finer "
    "daily timestep are still required for engineering confirmation."
)
