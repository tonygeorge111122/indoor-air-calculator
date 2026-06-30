import math
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ATLICE | Indoor Air Calculator",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# DESIGN / CSS
# =========================================================
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(42, 111, 151, 0.14), transparent 32%),
                radial-gradient(circle at bottom right, rgba(0, 168, 150, 0.12), transparent 30%),
                linear-gradient(135deg, #f6fbff 0%, #eef7f8 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero {
            min-height: 70vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 3rem 1rem;
        }

        .brand-badge {
            display: inline-block;
            padding: 0.45rem 1rem;
            border-radius: 999px;
            color: #0b5f73;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(11, 95, 115, 0.18);
            box-shadow: 0 8px 30px rgba(28, 79, 99, 0.08);
            font-weight: 700;
            letter-spacing: 0.16rem;
            margin-bottom: 1.2rem;
        }

        .hero-title {
            font-size: clamp(3.4rem, 8vw, 6.8rem);
            line-height: 0.95;
            font-weight: 850;
            letter-spacing: -0.25rem;
            color: #12384a;
            margin: 0;
        }

        .hero-subtitle {
            max-width: 720px;
            margin: 1.5rem auto 2.2rem auto;
            color: #496775;
            font-size: 1.12rem;
            line-height: 1.75;
        }

        .page-title {
            font-size: 2.25rem;
            font-weight: 800;
            color: #12384a;
            margin-bottom: 0.25rem;
        }

        .page-subtitle {
            color: #5b7480;
            margin-bottom: 1.5rem;
        }

        .section-card {
            background: rgba(255, 255, 255, 0.90);
            border: 1px solid rgba(25, 86, 108, 0.12);
            border-radius: 22px;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 14px 40px rgba(26, 70, 89, 0.08);
            margin-bottom: 1rem;
        }

        .step-box {
            border-radius: 18px;
            padding: 1rem 0.8rem;
            text-align: center;
            border: 1px solid rgba(27, 79, 99, 0.12);
            background: rgba(255, 255, 255, 0.70);
            min-height: 104px;
        }

        .step-active {
            background: linear-gradient(135deg, #0b6680, #168f96);
            color: white;
            box-shadow: 0 12px 28px rgba(11, 102, 128, 0.24);
        }

        .step-complete {
            background: #e8f7f2;
            color: #126a59;
            border-color: rgba(18, 106, 89, 0.18);
        }

        .step-pending {
            color: #738690;
        }

        .step-number {
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
            opacity: 0.85;
        }

        .step-name {
            font-size: 1rem;
            font-weight: 750;
            margin-top: 0.45rem;
        }

        .metric-card {
            background: white;
            border-radius: 18px;
            padding: 1rem;
            border: 1px solid rgba(22, 83, 106, 0.10);
            box-shadow: 0 10px 28px rgba(31, 74, 91, 0.07);
        }

        .review-label {
            color: #6b808a;
            font-size: 0.82rem;
            margin-bottom: 0.15rem;
        }

        .review-value {
            color: #173e4e;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.9rem;
        }

        div.stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            border-radius: 12px;
            min-height: 3rem;
            font-weight: 750;
            border: 1px solid rgba(11, 102, 128, 0.20);
        }

        div[data-testid="stFormSubmitButton"] > button[kind="primary"],
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0b6680, #15939a);
            color: white;
            border: none;
            box-shadow: 0 10px 24px rgba(11, 102, 128, 0.22);
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(26, 87, 109, 0.10);
            padding: 1rem;
            border-radius: 18px;
            box-shadow: 0 10px 25px rgba(25, 73, 91, 0.06);
        }

        [data-testid="stMetricLabel"] {
            color: #5d7480;
        }

        [data-testid="stMetricValue"] {
            color: #123f52;
        }

        .small-note {
            color: #71838c;
            font-size: 0.9rem;
        }

        @media (max-width: 700px) {
            .hero-title {
                letter-spacing: -0.12rem;
            }
            .block-container {
                padding-top: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DEFAULT VALUES AND SESSION STATE
# =========================================================

# These are the default engineering input values displayed
# automatically when the calculator is opened.
INPUT_DEFAULTS = {
    # Cooling and ACH
    "room_volume": 63.5,
    "people": 6,
    "heat_per_person": 100.0,
    "supply_temp": 12.0,
    "target_temp": 22.0,
    "rho_cp": 1200.0,

    # Richardson number
    "gravity": 9.81,
    "alpha": 0.00340,
    "delta_t_ri": 5.0,
    "length_scale": 1.0,
    "air_velocity": 0.10,

    # Wells–Riley
    "ventilation_effectiveness": 0.67,
    "infected_people": 1,
    "quanta_rate": 10.0,
    "breathing_rate": 0.5,
    "exposure_time": 2.0,
}

APP_DEFAULTS = {
    "started": False,
    "step": 1,
    "step1_confirmed": False,
    "step2_confirmed": False,
    "step3_confirmed": False,
    "results_ready": False,
}

DEFAULTS = {**APP_DEFAULTS, **INPUT_DEFAULTS}

# Change this value whenever the programmed defaults are revised.
# It ensures the updated defaults are loaded once, even when an older
# Streamlit session still contains previous values.
DEFAULTS_VERSION = "ATLICE_DEFAULTS_V2"

if st.session_state.get("_defaults_version") != DEFAULTS_VERSION:
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.session_state["_defaults_version"] = DEFAULTS_VERSION
else:
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_application():
    """Return the application to its original landing screen."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def restore_default_inputs():
    """Restore all engineering inputs without returning to the landing screen."""
    for key, value in INPUT_DEFAULTS.items():
        st.session_state[key] = value

    st.session_state.step = 1
    st.session_state.step1_confirmed = False
    st.session_state.step2_confirmed = False
    st.session_state.step3_confirmed = False
    st.session_state.results_ready = False
    st.rerun()


def calculate_results():
    """Run all engineering calculations using confirmed inputs."""
    delta_t_cooling = st.session_state.target_temp - st.session_state.supply_temp
    total_heat = st.session_state.people * st.session_state.heat_per_person

    airflow_m3s = total_heat / (
        st.session_state.rho_cp * delta_t_cooling
    )
    airflow_ls = airflow_m3s * 1000
    airflow_m3hr = airflow_m3s * 3600
    ach = airflow_m3hr / st.session_state.room_volume

    richardson_number = (
        st.session_state.gravity
        * st.session_state.alpha
        * st.session_state.delta_t_ri
        * st.session_state.length_scale
    ) / (st.session_state.air_velocity ** 2)

    q_eff_loc = (
        st.session_state.ventilation_effectiveness
        * airflow_m3hr
    )

    dose_term = (
        st.session_state.infected_people
        * st.session_state.quanta_rate
        * st.session_state.breathing_rate
        * st.session_state.exposure_time
    )

    if airflow_m3hr > 0:
        p_ideal = 1 - math.exp(-dose_term / airflow_m3hr)
    else:
        p_ideal = 0.0 if dose_term == 0 else 1.0

    if q_eff_loc > 0:
        p_local = 1 - math.exp(-dose_term / q_eff_loc)
    else:
        p_local = 0.0 if dose_term == 0 else 1.0

    return {
        "delta_t_cooling": delta_t_cooling,
        "total_heat": total_heat,
        "airflow_m3s": airflow_m3s,
        "airflow_ls": airflow_ls,
        "airflow_m3hr": airflow_m3hr,
        "ach": ach,
        "richardson_number": richardson_number,
        "q_eff_loc": q_eff_loc,
        "dose_term": dose_term,
        "p_ideal": p_ideal,
        "p_local": p_local,
        "p_ideal_percent": p_ideal * 100,
        "p_local_percent": p_local * 100,
    }


def render_progress():
    """Display the three input stages and their current status."""
    step = st.session_state.step

    steps = [
        ("Step 1", "Cooling & ACH", st.session_state.step1_confirmed),
        ("Step 2", "Richardson Number", st.session_state.step2_confirmed),
        ("Step 3", "Infection Risk", st.session_state.step3_confirmed),
    ]

    cols = st.columns(3)
    for index, (number, name, completed) in enumerate(steps, start=1):
        if completed:
            css_class = "step-complete"
            status = "✓ Confirmed"
        elif step == index:
            css_class = "step-active"
            status = "Current section"
        else:
            css_class = "step-pending"
            status = "Not confirmed"

        with cols[index - 1]:
            st.markdown(
                f"""
                <div class="step-box {css_class}">
                    <div class="step-number">{number}</div>
                    <div class="step-name">{name}</div>
                    <div style="font-size:0.78rem; margin-top:0.45rem; opacity:0.85;">
                        {status}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    confirmed_count = sum(
        [
            st.session_state.step1_confirmed,
            st.session_state.step2_confirmed,
            st.session_state.step3_confirmed,
        ]
    )
    st.progress(confirmed_count / 3)


# =========================================================
# LANDING SCREEN
# =========================================================
if not st.session_state.started:
    st.markdown(
        """
        <div class="hero">
            <div class="brand-badge">INDOOR AIR ANALYSIS</div>
            <h1 class="hero-title">ATLICE</h1>
            <p class="hero-subtitle">
                A guided calculator for cooling airflow, air changes per hour,
                Richardson number, local ventilation effectiveness and
                Wells–Riley infection risk.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, centre, right = st.columns([1.4, 1, 1.4])
    with centre:
        if st.button(
            "Open ATLICE Calculator  →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.started = True
            st.session_state.step = 1
            st.rerun()

    st.stop()


# =========================================================
# APPLICATION HEADER
# =========================================================
header_col1, header_col2, header_col3 = st.columns([4, 1.25, 1])

with header_col1:
    st.markdown('<div class="page-title">ATLICE</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Complete and confirm each section in order.</div>',
        unsafe_allow_html=True,
    )

with header_col2:
    if st.button("Restore Defaults", use_container_width=True):
        restore_default_inputs()

with header_col3:
    if st.button("Start Again", use_container_width=True):
        reset_application()

render_progress()
st.write("")


# =========================================================
# STEP 1 — COOLING AND ACH
# =========================================================
if st.session_state.step == 1:
    st.markdown(
        """
        <div class="section-card">
            <h2 style="margin-top:0; color:#153f51;">1. Cooling and ACH</h2>
            <p style="color:#627984; margin-bottom:0;">
                Enter the room, occupancy and cooling conditions. Confirm the
                section before continuing.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("cooling_ach_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.number_input(
                "Room volume (m³)",
                min_value=0.01,
                step=1.0,
                key="room_volume",
                help="Internal room volume used in the ACH calculation.",
            )
            st.number_input(
                "Number of people",
                min_value=0,
                step=1,
                key="people",
            )
            st.number_input(
                "Heat per person (W/person)",
                min_value=0.0,
                step=5.0,
                key="heat_per_person",
            )

        with col2:
            st.number_input(
                "Supply-air temperature (°C)",
                step=0.5,
                key="supply_temp",
            )
            st.number_input(
                "Target room temperature (°C)",
                step=0.5,
                key="target_temp",
            )
            st.number_input(
                "Volumetric heat capacity, ρcp (J/m³·K)",
                min_value=1.0,
                step=10.0,
                key="rho_cp",
            )

        submitted = st.form_submit_button(
            "Confirm Section 1 and Continue  →",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            errors = []

            if st.session_state.target_temp <= st.session_state.supply_temp:
                errors.append(
                    "Target room temperature must be higher than the "
                    "supply-air temperature."
                )

            if st.session_state.room_volume <= 0:
                errors.append("Room volume must be greater than zero.")

            if st.session_state.rho_cp <= 0:
                errors.append(
                    "Volumetric heat capacity must be greater than zero."
                )

            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.step1_confirmed = True
                st.session_state.results_ready = False
                st.session_state.step = 2
                st.rerun()


# =========================================================
# STEP 2 — RICHARDSON NUMBER
# =========================================================
elif st.session_state.step == 2:
    st.markdown(
        """
        <div class="section-card">
            <h2 style="margin-top:0; color:#153f51;">2. Richardson Number</h2>
            <p style="color:#627984; margin-bottom:0;">
                Define the buoyancy and momentum conditions used to calculate
                the Richardson number.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("richardson_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.number_input(
                "Gravity, g (m/s²)",
                min_value=0.01,
                step=0.01,
                key="gravity",
            )
            st.number_input(
                "Thermal expansion coefficient, α (1/K)",
                min_value=0.000001,
                format="%.5f",
                key="alpha",
            )
            st.number_input(
                "Temperature difference for Ri, ΔT (K or °C)",
                step=0.1,
                key="delta_t_ri",
            )

        with col2:
            st.number_input(
                "Characteristic length, L (m)",
                min_value=0.001,
                step=0.1,
                key="length_scale",
            )
            st.number_input(
                "Air velocity, V (m/s)",
                min_value=0.001,
                step=0.01,
                format="%.3f",
                key="air_velocity",
            )

            st.markdown(
                """
                <div style="padding:1rem; margin-top:0.5rem; border-radius:14px;
                            background:#eef7f8; color:#466873;">
                    <b>Formula</b><br>
                    Ri = gαΔTL / V²
                </div>
                """,
                unsafe_allow_html=True,
            )

        submitted = st.form_submit_button(
            "Confirm Section 2 and Continue  →",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if st.session_state.air_velocity <= 0:
                st.error("Air velocity must be greater than zero.")
            else:
                st.session_state.step2_confirmed = True
                st.session_state.results_ready = False
                st.session_state.step = 3
                st.rerun()

    back_col, _ = st.columns([1, 3])
    with back_col:
        if st.button("← Back to Section 1", use_container_width=True):
            st.session_state.step = 1
            st.rerun()


# =========================================================
# STEP 3 — VENTILATION AND INFECTION RISK
# =========================================================
elif st.session_state.step == 3:
    st.markdown(
        """
        <div class="section-card">
            <h2 style="margin-top:0; color:#153f51;">
                3. Ventilation and Infection Risk
            </h2>
            <p style="color:#627984; margin-bottom:0;">
                Enter the local ventilation effectiveness and Wells–Riley
                exposure parameters.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("infection_risk_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.number_input(
                "Local ventilation effectiveness, εV,loc",
                min_value=0.001,
                step=0.01,
                key="ventilation_effectiveness",
            )
            st.number_input(
                "Number of infectious people, I",
                min_value=0,
                step=1,
                key="infected_people",
            )
            st.number_input(
                "Quanta generation rate, q (quanta/h)",
                min_value=0.0,
                step=1.0,
                key="quanta_rate",
            )

        with col2:
            st.number_input(
                "Breathing rate, p (m³/h)",
                min_value=0.0,
                step=0.1,
                key="breathing_rate",
            )
            st.number_input(
                "Exposure time, t (h)",
                min_value=0.0,
                step=0.5,
                key="exposure_time",
            )

            st.markdown(
                """
                <div style="padding:1rem; margin-top:0.5rem; border-radius:14px;
                            background:#eef7f8; color:#466873;">
                    <b>Local Wells–Riley form</b><br>
                    P = 1 − exp[−Iqpt / (ε<sub>V,loc</sub>Q)]
                </div>
                """,
                unsafe_allow_html=True,
            )

        submitted = st.form_submit_button(
            "Confirm Section 3 and Review Inputs  →",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if st.session_state.ventilation_effectiveness <= 0:
                st.error(
                    "Local ventilation effectiveness must be greater than zero."
                )
            else:
                st.session_state.step3_confirmed = True
                st.session_state.results_ready = False
                st.session_state.step = 4
                st.rerun()

    back_col, _ = st.columns([1, 3])
    with back_col:
        if st.button("← Back to Section 2", use_container_width=True):
            st.session_state.step = 2
            st.rerun()


# =========================================================
# REVIEW AND COMPILE
# =========================================================
elif st.session_state.step == 4:
    st.markdown(
        """
        <div class="section-card">
            <h2 style="margin-top:0; color:#153f51;">Review and Compile</h2>
            <p style="color:#627984; margin-bottom:0;">
                Check the confirmed values below, then compile the complete
                calculation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    review1, review2, review3 = st.columns(3)

    with review1:
        st.markdown("### Cooling & ACH")
        st.markdown(
            f"""
            <div class="section-card">
                <div class="review-label">Room volume</div>
                <div class="review-value">{st.session_state.room_volume:.2f} m³</div>

                <div class="review-label">People</div>
                <div class="review-value">{st.session_state.people}</div>

                <div class="review-label">Heat per person</div>
                <div class="review-value">{st.session_state.heat_per_person:.2f} W/person</div>

                <div class="review-label">Supply / target temperature</div>
                <div class="review-value">
                    {st.session_state.supply_temp:.2f} / {st.session_state.target_temp:.2f} °C
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Edit Section 1", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

    with review2:
        st.markdown("### Richardson Number")
        st.markdown(
            f"""
            <div class="section-card">
                <div class="review-label">Gravity</div>
                <div class="review-value">{st.session_state.gravity:.2f} m/s²</div>

                <div class="review-label">Thermal expansion coefficient</div>
                <div class="review-value">{st.session_state.alpha:.5f} 1/K</div>

                <div class="review-label">Temperature difference</div>
                <div class="review-value">{st.session_state.delta_t_ri:.2f} K</div>

                <div class="review-label">Length / velocity</div>
                <div class="review-value">
                    {st.session_state.length_scale:.2f} m /
                    {st.session_state.air_velocity:.3f} m/s
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Edit Section 2", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

    with review3:
        st.markdown("### Infection Risk")
        st.markdown(
            f"""
            <div class="section-card">
                <div class="review-label">Ventilation effectiveness</div>
                <div class="review-value">
                    {st.session_state.ventilation_effectiveness:.3f}
                </div>

                <div class="review-label">Infectious people</div>
                <div class="review-value">{st.session_state.infected_people}</div>

                <div class="review-label">Quanta generation rate</div>
                <div class="review-value">{st.session_state.quanta_rate:.2f} quanta/h</div>

                <div class="review-label">Breathing rate / exposure</div>
                <div class="review-value">
                    {st.session_state.breathing_rate:.2f} m³/h /
                    {st.session_state.exposure_time:.2f} h
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Edit Section 3", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

    st.write("")
    left, centre, right = st.columns([1, 2, 1])
    with centre:
        if st.button(
            "Compile Final Results",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.results_ready = True
            st.session_state.step = 5
            st.rerun()


# =========================================================
# RESULTS
# =========================================================
elif st.session_state.step == 5 and st.session_state.results_ready:
    results = calculate_results()

    st.markdown(
        """
        <div class="section-card">
            <h2 style="margin-top:0; color:#153f51;">Compiled Results</h2>
            <p style="color:#627984; margin-bottom:0;">
                The values below combine all three confirmed calculation
                sections.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric("Required ACH", f"{results['ach']:.2f} h⁻¹")

    with metric2:
        st.metric("Required Airflow", f"{results['airflow_ls']:.2f} L/s")

    with metric3:
        st.metric("Airflow", f"{results['airflow_m3hr']:.2f} m³/h")

    with metric4:
        st.metric(
            "Richardson Number",
            f"{results['richardson_number']:.4f}",
        )

    st.write("")

    risk1, risk2 = st.columns(2)
    with risk1:
        st.metric(
            "Ideal Well-Mixed Probability",
            f"{results['p_ideal_percent']:.2f}%",
        )

    with risk2:
        st.metric(
            "Local Infection Probability",
            f"{results['p_local_percent']:.2f}%",
        )

    st.write("")

    with st.expander("1. Cooling and ACH details", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Total sensible heat load:** "
                f"{results['total_heat']:.2f} W"
            )
            st.write(
                f"**Cooling temperature difference:** "
                f"{results['delta_t_cooling']:.2f} °C"
            )
            st.write(
                f"**Required airflow:** "
                f"{results['airflow_m3s']:.4f} m³/s"
            )

        with col2:
            st.write(
                f"**Required airflow:** "
                f"{results['airflow_ls']:.2f} L/s"
            )
            st.write(
                f"**Required airflow:** "
                f"{results['airflow_m3hr']:.2f} m³/h"
            )
            st.write(
                f"**Required air changes per hour:** "
                f"{results['ach']:.2f} ACH"
            )

    with st.expander("2. Richardson number details"):
        st.write(
            f"**Richardson number, Ri:** "
            f"{results['richardson_number']:.4f}"
        )
        st.latex(r"Ri = \frac{g\alpha\Delta T L}{V^2}")

        ri = results["richardson_number"]
        if ri < 0.1:
            st.info(
                "Forced-air momentum is likely to dominate over buoyancy."
            )
        elif ri <= 1:
            st.info(
                "Both buoyancy and forced-air momentum may materially "
                "influence the airflow."
            )
        else:
            st.info(
                "Buoyancy effects may dominate the airflow."
            )

    with st.expander("3. Local ventilation details"):
        st.write(
            f"**Local ventilation effectiveness:** "
            f"{st.session_state.ventilation_effectiveness:.3f}"
        )
        st.write(
            f"**Room airflow, Q:** "
            f"{results['airflow_m3hr']:.2f} m³/h"
        )
        st.write(
            f"**Local effective airflow, Qeff,loc:** "
            f"{results['q_eff_loc']:.2f} m³/h"
        )
        st.latex(
            r"Q_{\mathrm{eff,loc}}"
            r"=\varepsilon_{V,\mathrm{loc}}Q"
        )

    with st.expander("4. Wells–Riley infection-risk details"):
        st.write(
            f"**Dose term, Iqpt:** "
            f"{results['dose_term']:.4f}"
        )
        st.write(
            f"**Ideal well-mixed probability:** "
            f"{results['p_ideal']:.5f}"
        )
        st.write(
            f"**Local infection probability:** "
            f"{results['p_local']:.5f}"
        )
        st.latex(
            r"P_{\mathrm{loc}}"
            r"=1-\exp\left("
            r"-\frac{Iqpt}{\varepsilon_{V,\mathrm{loc}}Q}"
            r"\right)"
        )

        effectiveness = st.session_state.ventilation_effectiveness
        if effectiveness < 1:
            st.warning(
                "Local ventilation effectiveness is below 1.0, so the "
                "effective local airflow is lower than the room-average "
                "airflow. This increases the calculated local infection risk."
            )
        elif effectiveness == 1:
            st.info(
                "Local ventilation effectiveness equals 1.0, representing "
                "the well-mixed reference case."
            )
        else:
            st.success(
                "Local ventilation effectiveness is above 1.0, so the "
                "effective local airflow is higher than the room-average "
                "airflow. This reduces the calculated local infection risk."
            )

    results_text = f"""
ATLICE — INDOOR AIR CALCULATION RESULTS

SECTION 1: COOLING AND ACH INPUTS
Room volume: {st.session_state.room_volume:.2f} m³
Number of people: {st.session_state.people}
Heat per person: {st.session_state.heat_per_person:.2f} W/person
Supply-air temperature: {st.session_state.supply_temp:.2f} °C
Target room temperature: {st.session_state.target_temp:.2f} °C
Volumetric heat capacity: {st.session_state.rho_cp:.2f} J/m³·K

COOLING AND ACH RESULTS
Total sensible heat load: {results['total_heat']:.2f} W
Cooling temperature difference: {results['delta_t_cooling']:.2f} °C
Required airflow: {results['airflow_m3s']:.4f} m³/s
Required airflow: {results['airflow_ls']:.2f} L/s
Required airflow: {results['airflow_m3hr']:.2f} m³/h
Required ACH: {results['ach']:.2f} h⁻¹

SECTION 2: RICHARDSON NUMBER INPUTS
Gravity: {st.session_state.gravity:.2f} m/s²
Thermal expansion coefficient: {st.session_state.alpha:.5f} 1/K
Temperature difference: {st.session_state.delta_t_ri:.2f} K
Characteristic length: {st.session_state.length_scale:.2f} m
Air velocity: {st.session_state.air_velocity:.3f} m/s

RICHARDSON NUMBER RESULT
Ri: {results['richardson_number']:.4f}

SECTION 3: VENTILATION AND INFECTION-RISK INPUTS
Local ventilation effectiveness: {st.session_state.ventilation_effectiveness:.3f}
Number of infectious people: {st.session_state.infected_people}
Quanta generation rate: {st.session_state.quanta_rate:.2f} quanta/h
Breathing rate: {st.session_state.breathing_rate:.2f} m³/h
Exposure time: {st.session_state.exposure_time:.2f} h

VENTILATION AND WELLS-RILEY RESULTS
Effective local airflow: {results['q_eff_loc']:.2f} m³/h
Dose term, Iqpt: {results['dose_term']:.4f}
Ideal well-mixed probability: {results['p_ideal_percent']:.2f}%
Local infection probability: {results['p_local_percent']:.2f}%
"""

    st.write("")
    action1, action2, action3 = st.columns([1, 1, 1])

    with action1:
        if st.button("← Review Inputs", use_container_width=True):
            st.session_state.step = 4
            st.rerun()

    with action2:
        st.download_button(
            label="Download Results",
            data=results_text,
            file_name="ATLICE_indoor_air_results.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with action3:
        if st.button("New Calculation", type="primary", use_container_width=True):
            reset_application()
