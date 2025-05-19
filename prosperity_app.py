
import streamlit as st

st.set_page_config(page_title="Cost per Prosperity Unit (CPPG) Calculator", page_icon="📈", layout="centered")

st.title("📈 Cost per Prosperity Unit (CPPG) Calculator")
st.write(
    """
    Estimate the **cost per prosperity unit (CPPG)** for an education or workforce intervention.
    A *prosperity unit* here is defined as **one dollar of present‑value lifetime earnings gained**.
    Lower CPPG values = better cost‑effectiveness.
    """
)

# ==== BASIC PROGRAM INPUTS ====
st.header("1️⃣ Intervention Inputs")

col1, col2 = st.columns(2)
with col1:
    cost_per_person = st.number_input(
        "Cost per participant ($)", min_value=0.0, value=1000.0, step=100.0
    )
    population = st.number_input(
        "Number of participants served (within 2 years)", min_value=1, value=1000, step=100
    )
    target_age = st.slider("Target age of participants", 0, 65, value=16)
with col2:
    avg_motivation = st.slider("Average motivation (1=low, 5=high)", 1, 5, value=3)
    engagement = st.slider("Average engagement (hrs/week)", 0.0, 40.0, value=5.0, step=0.5)
    persistence_months = st.slider("Average months of persistence", 0, 48, value=6)

st.subheader("Proximate Impact Metrics")
st.write("Enter effect sizes **per participant** (in absolute terms):")

col3, col4, col5 = st.columns(3)
with col3:
    math_sd = st.number_input("Δ Math score (SD)", value=0.1, step=0.05)
with col4:
    grad_rate_pp = st.number_input("Δ HS graduation rate (pct points)", value=5.0, step=1.0)
with col5:
    college_enroll_pp = st.number_input("Δ College enrollment (pct points)", value=3.0, step=1.0)

# ==== ASSUMPTION PANEL ====
with st.expander("⚙️ Assumptions for Converting Proximate Metrics to Lifetime Prosperity"):
    st.write("Adjust the conversion factors and discounting assumptions as new research becomes available.")
    discount_rate = st.number_input("Real discount rate (%, annual)", value=3.0, step=0.5) / 100

    st.subheader("Conversion Factors (per participant, present-value dollars)")
    math_gain_per_sd = st.number_input(
        "Lifetime earnings gain per 1 SD math improvement ($)", value=80000.0, step=10000.0
    )
    earnings_gain_hs_vs_dropout = st.number_input(
        "Lifetime earnings gap: HS grad vs dropout ($)", value=300000.0, step=50000.0
    )
    earnings_gain_college_vs_hs = st.number_input(
        "Lifetime earnings gap: Bachelor's degree vs HS ($)", value=600000.0, step=50000.0
    )
    fadeout_factor = st.slider(
        "Fade‑out factor for test‑score impacts (0=no fade, 1=full fade)",
        0.0,
        1.0,
        value=0.3,
        step=0.05,
    )
    st.caption(
        "Fade‑out reduces the earnings gain from test‑score improvements. "
        "A value of 0.3 means 30% of the initial gain fades over time."
    )

# ==== CALCULATIONS ====
# Convert proximate metrics to dollar gains
gain_from_math = math_sd * math_gain_per_sd * (1 - fadeout_factor)
gain_from_grad_rate = (grad_rate_pp / 100) * earnings_gain_hs_vs_dropout
gain_from_college = (college_enroll_pp / 100) * earnings_gain_college_vs_hs

total_gain_per_person = gain_from_math + gain_from_grad_rate + gain_from_college

# cost per prosperity unit
cppg = cost_per_person / total_gain_per_person if total_gain_per_person > 0 else None

# ==== OUTPUT ====
st.header("📊 Results")

if total_gain_per_person <= 0:
    st.error("Total prosperity gain per participant is zero or negative. Adjust inputs.")
else:
    st.metric(
        "Cost per $1 of lifetime prosperity gained (CPPG)",
        f"${cppg:,.2f}",
        help="Lower is better. CPPG < $1 means the intervention is expected to yield net positive lifetime earnings."
    )
    roi = 1 / cppg
    st.metric("Return on Investment (ROI)", f"{roi:,.1f}×", help="How many dollars of gain per dollar spent.")
    
    total_cost = cost_per_person * population
    total_gain = total_gain_per_person * population
    net_gain = total_gain - total_cost

    st.subheader("Cohort Totals (2‑year implementation)")
    st.write(f"**Total program cost:** ${total_cost:,.0f}")
    st.write(f"**Total lifetime prosperity gain:** ${total_gain:,.0f}")
    st.write(f"**Net lifetime prosperity gain:** ${net_gain:,.0f}")

    # Scenario analysis: optimistic / pessimistic toggles
    st.subheader("Scenario Analysis")
    scenario_multiplier = st.slider(
        "Effect size multiplier for scenario analysis",
        0.5,
        1.5,
        value=1.0,
        step=0.1
    )
    adj_gain = total_gain_per_person * scenario_multiplier
    adj_cppg = cost_per_person / adj_gain if adj_gain > 0 else None
    st.write(
        f"With a multiplier of **{scenario_multiplier:.1f}×** on effect sizes, "
        f"adjusted CPPG = **${adj_cppg:,.2f}**."
    )

st.markdown("---")
st.caption(
    "Prototype created for illustrative purposes. Update assumptions with the latest meta‑analyses to improve accuracy."
)
