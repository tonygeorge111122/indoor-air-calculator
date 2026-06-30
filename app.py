import math
from datetime import datetime

import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ATLiCE | Indoor Air Toolkit",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# APP STYLING
# =========================================================
def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --atlice-primary: #0f766e;
            --atlice-primary-dark: #115e59;
            --atlice-secondary: #14b8a6;
            --atlice-accent: #f59e0b;
            --atlice-bg: #f4f8f7;
            --atlice-card: #ffffff;
            --atlice-text: #15302d;
            --atlice-muted: #64748b;
            --atlice-border: #dbe7e4;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(20,184,166,0.10), transparent 30%),
                linear-gradient(180deg, #f8fbfa 0%, var(--atlice-bg) 100%);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f3d3a 0%, #115e59 100%);
            border-right: 1px solid rgba(255,255,255,0.12);
        }

        [data-testid="stSidebar"] * {
            color: #ffffff;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 46px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.08);
            color: #ffffff;
            font-weight: 650;
            transition: all 0.2s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: rgba(255,255,255,0.45);
            background: rgba(255,255,255,0.18);
            transform: translateY(-1px);
        }

        .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 2.2rem 2.4rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 55%, #14b8a6 100%);
            box-shadow: 0 18px 45px rgba(15,118,110,0.18);
            color: white;
            margin-bottom: 1.4rem;
            position: relative;
            overflow: hidden;
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: rgba(255,255,255,0.10);
            right: -90px;
            top: -110px;
        }

        .hero h1 {
            color: white;
            font-size: clamp(2rem, 4vw, 3.35rem);
            margin: 0 0 0.45rem 0;
            letter-spacing: -0.04em;
        }

        .hero p {
            color: rgba(255,255,255,0.88);
            font-size: 1.08rem;
            max-width: 760px;
            margin: 0;
            line-height: 1.65;
        }

        .eyebrow {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-weight: 800;
            opacity: 0.78;
            margin-bottom: 0.55rem;
        }

        .tool-card {
            min-height: 245px;
            padding: 1.55rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.88);
            border: 1px solid var(--atlice-border);
            box-shadow: 0 12px 28px rgba(15,23,42,0.06);
            backdrop-filter: blur(6px);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .tool-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 18px 36px rgba(15,23,42,0.10);
        }

        .tool-icon {
            width: 54px;
            height: 54px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            background: #dff7f3;
            font-size: 1.7rem;
            margin-bottom: 1rem;
        }

        .tool-card h3 {
            color: var(--atlice-text);
            margin: 0 0 0.55rem 0;
            font-size: 1.28rem;
        }

        .tool-card p {
            color: var(--atlice-muted);
            line-height: 1.58;
            margin: 0;
        }

        .section-card {
            padding: 1.35rem 1.45rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--atlice-border);
            box-shadow: 0 10px 25px rgba(15,23,42,0.045);
            margin-bottom: 1rem;
        }

        .page-title {
            margin-bottom: 1rem;
        }

        .page-title h1 {
            color: var(--atlice-text);
            letter-spacing: -0.035em;
            margin-bottom: 0.3rem;
        }

        .page-title p {
            color: var(--atlice-muted);
            font-size: 1.02rem;
            margin-top: 0;
        }

        .result-banner {
            padding: 1.2rem 1.35rem;
            border-radius: 16px;
            border-left: 5px solid var(--atlice-secondary);
            background: #ecfdf8;
            color: #134e4a;
            margin: 0.8rem 0 1.1rem 0;
        }

        .formula-box {
            padding: 1rem 1.2rem;
            border-radius: 15px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            margin-top: 0.8rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.94);
            border: 1px solid var(--atlice-border);
            padding: 1rem 1.1rem;
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(15,23,42,0.045);
        }

        div[data-testid="stMetricLabel"] p {
            color: var(--atlice-muted);
            font-weight: 650;
        }

        div[data-testid="stMetricValue"] {
            color: var(--atlice-primary-dark);
        }

        .stButton > button,
        .stDownloadButton > button,
        button[kind="primary"] {
            border-radius: 12px;
            min-height: 44px;
            font-weight: 700;
        }

        .stButton > button[kind="primary"],
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--atlice-primary) 0%, var(--atlice-secondary) 100%);
            border: none;
            color: white;
        }

        .stNumberInput input {
            border-radius: 10px;
        }

        [data-testid="stForm"] {
            background: rgba(255,255,255,0.70);
            border: 1px solid var(--atlice-border);
            border-radius: 18px;
            padding: 1.2rem;
        }

        .small-note {
            color: var(--atlice-muted);
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .sidebar-brand {
            text-align: center;
            padding: 0.5rem 0 1rem 0;
        }

        .sidebar-brand .mark {
            font-size: 2rem;
            line-height: 1;
        }

        .sidebar-brand .name {
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            margin-top: 0.35rem;
        }

        .sidebar-brand .tagline {
            color: rgba(255,255,255,0.68) !important;
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_custom_css()


# =========================================================
# NAVIGATION HELPERS
# =========================================================
PAGES = {
    "Home": "home",
    "Cooling & ACH": "ach",
    "Richardson Number": "ri",
    "Wells–Riley Risk": "wells_riley",
}

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


def go_to(page_name: str) -> None:
    st.session_state.current_page = page_name
    st.rerun()


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="mark">🌿</div>
                <div class="name">ATLiCE</div>
                <div class="tagline">Indoor Air Analysis Toolkit</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("⌂  ATLiCE Home", key="nav_home", use_container_width=True):
            go_to("home")

        st.markdown("### Calculators")

        if st.button("❄️  Cooling & ACH", key="nav_ach", use_container_width=True):
            go_to("ach")

        if st.button("🌡️  Richardson Number", key="nav_ri", use_container_width=True):
            go_to("ri")

        if st.button("🫁  Wells–Riley Risk", key="nav_wr", use_container_width=True):
            go_to("wells_riley")

        st.markdown("---")
        st.markdown(
            """
            <div class="small-note" style="color:rgba(255,255,255,0.72);">
                All values are editable. Results are intended for preliminary
                analysis and should be checked against the assumptions of each model.
            </div>
            """,
            unsafe_allow_html=True,
        )


render_sidebar()


# =========================================================
# SHARED UI COMPONENTS
# =========================================================
def render_page_heading(icon: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="page-title">
            <div class="eyebrow">ATLiCE Calculator</div>
            <h1>{icon} {title}</h1>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def download_text_button(text: str, file_name: str, key: str) -> None:
    st.download_button(
        label="⬇ Download results",
        data=text,
        file_name=file_name,
        mime="text/plain",
        key=key,
        use_container_width=True,
    )


# =========================================================
# HOME PAGE
# =========================================================
def home_page() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Indoor Air Analysis Platform</div>
            <h1>ATLiCE</h1>
            <p>
                A focused toolkit for estimating cooling airflow and air changes,
                evaluating buoyancy-to-momentum effects, and screening airborne
                infection risk using the Wells–Riley model.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Choose a calculator")
    st.caption("Open any tool below. The supplied values are defaults and can be changed at any time.")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            """
            <div class="tool-card">
                <div class="tool-icon">❄️</div>
                <h3>Cooling & ACH</h3>
                <p>
                    Calculate sensible cooling airflow, airflow in three common
                    units, and the corresponding air changes per hour.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Cooling & ACH →", key="home_ach", type="primary", use_container_width=True):
            go_to("ach")

    with col2:
        st.markdown(
            """
            <div class="tool-card">
                <div class="tool-icon">🌡️</div>
                <h3>Richardson Number</h3>
                <p>
                    Compare thermal buoyancy with forced-air momentum and classify
                    the likely dominant airflow mechanism.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Richardson Tool →", key="home_ri", type="primary", use_container_width=True):
            go_to("ri")

    with col3:
        st.markdown(
            """
            <div class="tool-card">
                <div class="tool-icon">🫁</div>
                <h3>Wells–Riley Risk</h3>
                <p>
                    Estimate ideal well-mixed and local infection probabilities
                    using airflow and local ventilation effectiveness.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Wells–Riley Tool →", key="home_wr", type="primary", use_container_width=True):
            go_to("wells_riley")

    st.markdown("### Model scope")
    info1, info2, info3 = st.columns(3)
    info1.info("**Cooling model:** sensible heat only; latent and envelope loads are not included.")
    info2.info("**Richardson model:** uses the specified characteristic length and representative velocity.")
    info3.info("**Wells–Riley model:** assumes steady conditions and does not replace detailed exposure assessment.")


# =========================================================
# COOLING AND ACH PAGE
# =========================================================
def cooling_ach_page() -> None:
    render_page_heading(
        "❄️",
        "Cooling Airflow & ACH",
        "Estimate the airflow needed to remove a specified sensible internal heat load.",
    )

    input_col, guide_col = st.columns([1.55, 1], gap="large")

    with input_col:
        with st.form("ach_form"):
            st.markdown("### Input values")
            row1a, row1b = st.columns(2)
            room_volume = row1a.number_input(
                "Room volume (m³)",
                min_value=0.01,
                value=63.0,
                step=1.0,
                key="ach_room_volume",
            )
            people = row1b.number_input(
                "Number of people",
                min_value=0,
                value=5,
                step=1,
                key="ach_people",
            )

            row2a, row2b = st.columns(2)
            heat_per_person = row2a.number_input(
                "Heat per person (W/person)",
                min_value=0.0,
                value=100.0,
                step=5.0,
                key="ach_heat_person",
            )
            additional_heat = row2b.number_input(
                "Additional sensible heat (W)",
                min_value=0.0,
                value=0.0,
                step=50.0,
                help="Optional load from lighting, equipment, heaters or other sources.",
                key="ach_additional_heat",
            )

            row3a, row3b = st.columns(2)
            supply_temp = row3a.number_input(
                "Supply-air temperature (°C)",
                value=12.0,
                step=0.5,
                key="ach_supply_temp",
            )
            target_temp = row3b.number_input(
                "Target room temperature (°C)",
                value=22.0,
                step=0.5,
                key="ach_target_temp",
            )

            rho_cp = st.number_input(
                "Volumetric heat capacity, ρcp (J/m³·K)",
                min_value=1.0,
                value=1200.0,
                step=10.0,
                key="ach_rho_cp",
            )

            calculate = st.form_submit_button(
                "Calculate Cooling & ACH",
                type="primary",
                use_container_width=True,
            )

    with guide_col:
        st.markdown(
            """
            <div class="section-card">
                <h3>Calculation basis</h3>
                <p>The sensible cooling airflow is calculated from:</p>
                <div class="formula-box"><b>Q = H / [ρcp × (Troom − Tsupply)]</b></div>
                <p class="small-note">
                    The default values represent a 63 m³ room with five occupants,
                    100 W sensible heat per person, 12 °C supply air and a 22 °C target.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning(
            "This is not a complete HVAC load calculation. Solar gain, fabric heat transfer, "
            "infiltration, latent load and equipment diversity are excluded unless entered as additional sensible heat."
        )

    if calculate:
        errors = []
        if target_temp <= supply_temp:
            errors.append("Target room temperature must be higher than the supply-air temperature.")
        if room_volume <= 0:
            errors.append("Room volume must be greater than zero.")
        if rho_cp <= 0:
            errors.append("Volumetric heat capacity must be greater than zero.")

        if errors:
            for error in errors:
                st.error(error)
            st.session_state.pop("ach_result", None)
        else:
            delta_t = target_temp - supply_temp
            people_heat = people * heat_per_person
            total_heat = people_heat + additional_heat
            airflow_m3s = total_heat / (rho_cp * delta_t)
            airflow_ls = airflow_m3s * 1000
            airflow_m3h = airflow_m3s * 3600
            ach = airflow_m3h / room_volume

            st.session_state.ach_result = {
                "room_volume": room_volume,
                "people": people,
                "heat_per_person": heat_per_person,
                "additional_heat": additional_heat,
                "people_heat": people_heat,
                "total_heat": total_heat,
                "supply_temp": supply_temp,
                "target_temp": target_temp,
                "delta_t": delta_t,
                "rho_cp": rho_cp,
                "airflow_m3s": airflow_m3s,
                "airflow_ls": airflow_ls,
                "airflow_m3h": airflow_m3h,
                "ach": ach,
            }

    result = st.session_state.get("ach_result")
    if result:
        st.markdown("---")
        st.markdown("## Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Required ACH", f"{result['ach']:.2f} h⁻¹")
        m2.metric("Airflow", f"{result['airflow_ls']:.2f} L/s")
        m3.metric("Airflow", f"{result['airflow_m3h']:.2f} m³/h")
        m4.metric("Total heat load", f"{result['total_heat']:.0f} W")

        st.markdown(
            f"""
            <div class="result-banner">
                To offset a sensible load of <b>{result['total_heat']:.0f} W</b> with a
                <b>{result['delta_t']:.1f} °C</b> supply-to-room temperature difference,
                the calculated airflow is <b>{result['airflow_m3h']:.1f} m³/h</b>,
                equivalent to <b>{result['ach']:.2f} ACH</b> for this room volume.
            </div>
            """,
            unsafe_allow_html=True,
        )

        detail1, detail2 = st.columns(2)
        with detail1:
            st.markdown("### Heat-load breakdown")
            st.write(f"Occupant sensible heat: **{result['people_heat']:.2f} W**")
            st.write(f"Additional sensible heat: **{result['additional_heat']:.2f} W**")
            st.write(f"Total sensible heat: **{result['total_heat']:.2f} W**")
        with detail2:
            st.markdown("### Airflow conversion")
            st.write(f"Airflow: **{result['airflow_m3s']:.5f} m³/s**")
            st.write(f"Airflow: **{result['airflow_ls']:.2f} L/s**")
            st.write(f"Airflow: **{result['airflow_m3h']:.2f} m³/h**")

        results_text = f"""ATLiCE — COOLING AIRFLOW AND ACH RESULTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

INPUTS
Room volume: {result['room_volume']:.2f} m³
Number of people: {result['people']}
Heat per person: {result['heat_per_person']:.2f} W/person
Additional sensible heat: {result['additional_heat']:.2f} W
Supply-air temperature: {result['supply_temp']:.2f} °C
Target room temperature: {result['target_temp']:.2f} °C
Volumetric heat capacity: {result['rho_cp']:.2f} J/m³·K

RESULTS
Occupant sensible heat: {result['people_heat']:.2f} W
Total sensible heat: {result['total_heat']:.2f} W
Temperature difference: {result['delta_t']:.2f} °C
Airflow: {result['airflow_m3s']:.5f} m³/s
Airflow: {result['airflow_ls']:.2f} L/s
Airflow: {result['airflow_m3h']:.2f} m³/h
ACH: {result['ach']:.2f} h⁻¹
"""
        download_text_button(results_text, "atlice_cooling_ach_results.txt", "download_ach")


# =========================================================
# RICHARDSON NUMBER PAGE
# =========================================================
def richardson_page() -> None:
    render_page_heading(
        "🌡️",
        "Richardson Number",
        "Assess the relative importance of thermal buoyancy and forced-air momentum.",
    )

    input_col, guide_col = st.columns([1.45, 1], gap="large")

    with input_col:
        with st.form("ri_form"):
            st.markdown("### Input values")
            row1a, row1b = st.columns(2)
            gravity = row1a.number_input(
                "Gravity, g (m/s²)",
                min_value=0.01,
                value=9.81,
                step=0.01,
                key="ri_gravity",
            )
            alpha = row1b.number_input(
                "Thermal expansion coefficient, α (1/K)",
                min_value=0.000001,
                value=0.00335,
                step=0.00001,
                format="%.5f",
                key="ri_alpha",
            )

            row2a, row2b = st.columns(2)
            delta_t = row2a.number_input(
                "Temperature difference, ΔT (K or °C)",
                value=5.0,
                step=0.1,
                key="ri_delta_t",
            )
            length_scale = row2b.number_input(
                "Characteristic length, L (m)",
                min_value=0.001,
                value=1.0,
                step=0.1,
                key="ri_length",
            )

            air_velocity = st.number_input(
                "Representative air velocity, V (m/s)",
                min_value=0.001,
                value=0.10,
                step=0.01,
                format="%.3f",
                key="ri_velocity",
            )

            calculate = st.form_submit_button(
                "Calculate Richardson Number",
                type="primary",
                use_container_width=True,
            )

    with guide_col:
        st.markdown(
            """
            <div class="section-card">
                <h3>Equation</h3>
                <div class="formula-box"><b>Ri = g α ΔT L / V²</b></div>
                <p class="small-note">
                    Use a length and velocity that represent the actual flow region being assessed.
                    The result can change substantially because velocity appears as a squared term.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info(
            "Indicative interpretation: Ri < 0.1 suggests momentum dominance; "
            "0.1–1 indicates mixed influence; Ri > 1 suggests buoyancy dominance."
        )

    if calculate:
        if air_velocity <= 0:
            st.error("Air velocity must be greater than zero.")
            st.session_state.pop("ri_result", None)
        else:
            ri = gravity * alpha * delta_t * length_scale / (air_velocity**2)

            if ri < 0:
                classification = "Opposing buoyancy direction"
                interpretation = (
                    "The negative sign indicates that the specified temperature difference produces "
                    "buoyancy in the opposite direction to the reference flow convention."
                )
            elif ri < 0.1:
                classification = "Momentum-dominated flow"
                interpretation = (
                    "Forced-air momentum is likely to dominate over buoyancy for the selected scales."
                )
            elif ri <= 1:
                classification = "Mixed convection"
                interpretation = (
                    "Both buoyancy and forced-air momentum are likely to influence the airflow."
                )
            else:
                classification = "Buoyancy-dominated flow"
                interpretation = (
                    "Thermal buoyancy is likely to dominate over forced-air momentum for the selected scales."
                )

            st.session_state.ri_result = {
                "gravity": gravity,
                "alpha": alpha,
                "delta_t": delta_t,
                "length_scale": length_scale,
                "air_velocity": air_velocity,
                "ri": ri,
                "classification": classification,
                "interpretation": interpretation,
            }

    result = st.session_state.get("ri_result")
    if result:
        st.markdown("---")
        st.markdown("## Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Richardson number", f"{result['ri']:.4f}")
        m2.metric("Air velocity", f"{result['air_velocity']:.3f} m/s")
        m3.metric("Temperature difference", f"{result['delta_t']:.2f} K")

        st.markdown(
            f"""
            <div class="result-banner">
                <b>{result['classification']}</b><br>
                {result['interpretation']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.latex(r"Ri = \frac{g\alpha\Delta T L}{V^2}")
        st.write(
            f"Substitution: **({result['gravity']:.2f} × {result['alpha']:.5f} × "
            f"{result['delta_t']:.2f} × {result['length_scale']:.2f}) / "
            f"({result['air_velocity']:.3f})² = {result['ri']:.4f}**"
        )

        results_text = f"""ATLiCE — RICHARDSON NUMBER RESULTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

INPUTS
Gravity: {result['gravity']:.4f} m/s²
Thermal expansion coefficient: {result['alpha']:.6f} 1/K
Temperature difference: {result['delta_t']:.4f} K
Characteristic length: {result['length_scale']:.4f} m
Air velocity: {result['air_velocity']:.4f} m/s

RESULT
Richardson number: {result['ri']:.6f}
Classification: {result['classification']}
Interpretation: {result['interpretation']}
"""
        download_text_button(results_text, "atlice_richardson_results.txt", "download_ri")


# =========================================================
# WELLS–RILEY PAGE
# =========================================================
def wells_riley_page() -> None:
    render_page_heading(
        "🫁",
        "Wells–Riley Infection Risk",
        "Estimate ideal well-mixed and local airborne infection probabilities for a steady exposure scenario.",
    )

    input_col, guide_col = st.columns([1.55, 1], gap="large")

    with input_col:
        with st.form("wr_form"):
            st.markdown("### Input values")
            row1a, row1b = st.columns(2)
            room_airflow = row1a.number_input(
                "Room airflow, Q (m³/h)",
                min_value=0.0,
                value=150.0,
                step=10.0,
                help="The original defaults produce 150 m³/h from the cooling calculation.",
                key="wr_airflow",
            )
            ventilation_effectiveness = row1b.number_input(
                "Local ventilation effectiveness, εV,loc",
                min_value=0.001,
                value=0.67,
                step=0.01,
                format="%.3f",
                key="wr_effectiveness",
            )

            row2a, row2b = st.columns(2)
            infected_people = row2a.number_input(
                "Number of infectious people, I",
                min_value=0,
                value=1,
                step=1,
                key="wr_infected",
            )
            quanta_rate = row2b.number_input(
                "Quanta generation rate, q (quanta/h)",
                min_value=0.0,
                value=10.0,
                step=1.0,
                key="wr_quanta",
            )

            row3a, row3b = st.columns(2)
            breathing_rate = row3a.number_input(
                "Breathing rate, p (m³/h)",
                min_value=0.0,
                value=0.5,
                step=0.1,
                key="wr_breathing",
            )
            exposure_time = row3b.number_input(
                "Exposure time, t (h)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                key="wr_exposure",
            )

            calculate = st.form_submit_button(
                "Calculate Infection Risk",
                type="primary",
                use_container_width=True,
            )

    with guide_col:
        st.markdown(
            """
            <div class="section-card">
                <h3>Calculation basis</h3>
                <div class="formula-box"><b>P = 1 − exp[−Iqpt / Q]</b></div>
                <p class="small-note">
                    The local case replaces Q with εV,loc × Q. A value below 1.0
                    represents lower effective ventilation at the assessed location.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning(
            "Quanta generation rates are highly scenario-dependent. This output is a model estimate, "
            "not a clinical prediction or a substitute for public-health guidance."
        )

    if calculate:
        dose_term = infected_people * quanta_rate * breathing_rate * exposure_time
        effective_local_airflow = ventilation_effectiveness * room_airflow

        if room_airflow > 0:
            p_ideal = 1 - math.exp(-dose_term / room_airflow)
        else:
            p_ideal = 0.0 if dose_term == 0 else 1.0

        if effective_local_airflow > 0:
            p_local = 1 - math.exp(-dose_term / effective_local_airflow)
        else:
            p_local = 0.0 if dose_term == 0 else 1.0

        if p_local < 0.01:
            risk_band = "Below 1% for this modelled scenario"
        elif p_local < 0.05:
            risk_band = "Between 1% and 5% for this modelled scenario"
        elif p_local < 0.10:
            risk_band = "Between 5% and 10% for this modelled scenario"
        else:
            risk_band = "Above 10% for this modelled scenario"

        st.session_state.wr_result = {
            "room_airflow": room_airflow,
            "ventilation_effectiveness": ventilation_effectiveness,
            "infected_people": infected_people,
            "quanta_rate": quanta_rate,
            "breathing_rate": breathing_rate,
            "exposure_time": exposure_time,
            "dose_term": dose_term,
            "effective_local_airflow": effective_local_airflow,
            "p_ideal": p_ideal,
            "p_local": p_local,
            "risk_band": risk_band,
        }

    result = st.session_state.get("wr_result")
    if result:
        st.markdown("---")
        st.markdown("## Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Ideal well-mixed risk", f"{result['p_ideal'] * 100:.2f}%")
        m2.metric("Local infection risk", f"{result['p_local'] * 100:.2f}%")
        m3.metric("Effective local airflow", f"{result['effective_local_airflow']:.1f} m³/h")
        m4.metric("Dose term, Iqpt", f"{result['dose_term']:.2f}")

        direction_text = (
            "higher than" if result["p_local"] > result["p_ideal"]
            else "equal to" if math.isclose(result["p_local"], result["p_ideal"], rel_tol=1e-12)
            else "lower than"
        )

        st.markdown(
            f"""
            <div class="result-banner">
                <b>{result['risk_band']}.</b><br>
                With a local ventilation effectiveness of
                <b>{result['ventilation_effectiveness']:.2f}</b>, the local modelled risk is
                <b>{direction_text}</b> the ideal well-mixed result.
            </div>
            """,
            unsafe_allow_html=True,
        )

        detail1, detail2 = st.columns(2)
        with detail1:
            st.markdown("### Airflow relationship")
            st.write(f"Room airflow, Q: **{result['room_airflow']:.2f} m³/h**")
            st.write(
                f"Local effective airflow, εV,loc × Q: "
                f"**{result['effective_local_airflow']:.2f} m³/h**"
            )
            st.latex(r"Q_{\mathrm{eff,loc}} = \varepsilon_{V,\mathrm{loc}}Q")
        with detail2:
            st.markdown("### Probability values")
            st.write(f"Ideal probability: **{result['p_ideal']:.6f}**")
            st.write(f"Local probability: **{result['p_local']:.6f}**")
            st.latex(r"P_{\mathrm{loc}} = 1-\exp\left(-\frac{Iqpt}{\varepsilon_{V,\mathrm{loc}}Q}\right)")

        results_text = f"""ATLiCE — WELLS–RILEY RESULTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

INPUTS
Room airflow: {result['room_airflow']:.2f} m³/h
Local ventilation effectiveness: {result['ventilation_effectiveness']:.4f}
Infectious people: {result['infected_people']}
Quanta generation rate: {result['quanta_rate']:.4f} quanta/h
Breathing rate: {result['breathing_rate']:.4f} m³/h
Exposure time: {result['exposure_time']:.4f} h

RESULTS
Dose term, Iqpt: {result['dose_term']:.6f}
Effective local airflow: {result['effective_local_airflow']:.4f} m³/h
Ideal well-mixed probability: {result['p_ideal']:.8f}
Ideal well-mixed probability: {result['p_ideal'] * 100:.4f}%
Local infection probability: {result['p_local']:.8f}
Local infection probability: {result['p_local'] * 100:.4f}%
"""
        download_text_button(results_text, "atlice_wells_riley_results.txt", "download_wr")


# =========================================================
# PAGE ROUTER
# =========================================================
page = st.session_state.current_page

if page == "home":
    home_page()
elif page == "ach":
    cooling_ach_page()
elif page == "ri":
    richardson_page()
elif page == "wells_riley":
    wells_riley_page()
else:
    st.session_state.current_page = "home"
    st.rerun()
