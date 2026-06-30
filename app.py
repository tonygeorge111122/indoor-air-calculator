# -*- coding: utf-8 -*-

import math
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ATLICE | Indoor Air Calculator",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# DEFAULT VALUES
# =========================================================
INPUT_DEFAULTS = {
    "room_volume": 63.5,
    "people": 6,
    "heat_per_person": 100.0,
    "supply_temp": 12.0,
    "target_temp": 22.0,
    "rho_cp": 1200.0,
    "gravity": 9.81,
    "alpha": 0.00340,
    "delta_t_ri": 5.0,
    "length_scale": 1.0,
    "air_velocity": 0.10,
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

for state_key, default_value in {**APP_DEFAULTS, **INPUT_DEFAULTS}.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def open_calculator():
    st.session_state["started"] = True
    st.session_state["step"] = 1


def start_again():
    for state_key in list(st.session_state.keys()):
        del st.session_state[state_key]

    for state_key, default_value in {**APP_DEFAULTS, **INPUT_DEFAULTS}.items():
        st.session_state[state_key] = default_value


SECTION_DEFAULT_KEYS = {
    1: [
        "room_volume",
        "people",
        "heat_per_person",
        "supply_temp",
        "target_temp",
        "rho_cp",
    ],
    2: [
        "gravity",
        "alpha",
        "delta_t_ri",
        "length_scale",
        "air_velocity",
    ],
    3: [
        "ventilation_effectiveness",
        "infected_people",
        "quanta_rate",
        "breathing_rate",
        "exposure_time",
    ],
}


def restore_section_defaults(section_number):
    """Restore defaults only for the selected section."""

    if section_number not in SECTION_DEFAULT_KEYS:
        section_number = 1

    for state_key in SECTION_DEFAULT_KEYS[section_number]:
        st.session_state[state_key] = INPUT_DEFAULTS[state_key]

    st.session_state["started"] = True
    st.session_state["step"] = section_number
    st.session_state["results_ready"] = False

    if section_number == 1:
        st.session_state["step1_confirmed"] = False
        st.session_state["step2_confirmed"] = False
        st.session_state["step3_confirmed"] = False

    elif section_number == 2:
        st.session_state["step2_confirmed"] = False
        st.session_state["step3_confirmed"] = False

    elif section_number == 3:
        st.session_state["step3_confirmed"] = False


def restore_all_defaults():
    """Restore all engineering inputs and return to Section 1."""

    for state_key, default_value in INPUT_DEFAULTS.items():
        st.session_state[state_key] = default_value

    st.session_state["started"] = True
    st.session_state["step"] = 1
    st.session_state["step1_confirmed"] = False
    st.session_state["step2_confirmed"] = False
    st.session_state["step3_confirmed"] = False
    st.session_state["results_ready"] = False


def calculate_results():
    delta_t_cooling = (
        st.session_state["target_temp"]
        - st.session_state["supply_temp"]
    )

    if delta_t_cooling <= 0:
        raise ValueError(
            "Target room temperature must be higher than "
            "the supply-air temperature."
        )

    if st.session_state["room_volume"] <= 0:
        raise ValueError("Room volume must be greater than zero.")

    if st.session_state["rho_cp"] <= 0:
        raise ValueError(
            "Volumetric heat capacity must be greater than zero."
        )

    if st.session_state["air_velocity"] <= 0:
        raise ValueError("Air velocity must be greater than zero.")

    if st.session_state["ventilation_effectiveness"] <= 0:
        raise ValueError(
            "Local ventilation effectiveness must be greater than zero."
        )

    total_heat = (
        st.session_state["people"]
        * st.session_state["heat_per_person"]
    )

    airflow_m3s = total_heat / (
        st.session_state["rho_cp"]
        * delta_t_cooling
    )

    airflow_ls = airflow_m3s * 1000.0
    airflow_m3hr = airflow_m3s * 3600.0
    ach = airflow_m3hr / st.session_state["room_volume"]

    richardson_number = (
        st.session_state["gravity"]
        * st.session_state["alpha"]
        * st.session_state["delta_t_ri"]
        * st.session_state["length_scale"]
    ) / (st.session_state["air_velocity"] ** 2)

    effective_local_airflow = (
        st.session_state["ventilation_effectiveness"]
        * airflow_m3hr
    )

    dose_term = (
        st.session_state["infected_people"]
        * st.session_state["quanta_rate"]
        * st.session_state["breathing_rate"]
        * st.session_state["exposure_time"]
    )

    if airflow_m3hr > 0:
        ideal_probability = 1.0 - math.exp(
            -dose_term / airflow_m3hr
        )
    else:
        ideal_probability = 0.0 if dose_term == 0 else 1.0

    if effective_local_airflow > 0:
        local_probability = 1.0 - math.exp(
            -dose_term / effective_local_airflow
        )
    else:
        local_probability = 0.0 if dose_term == 0 else 1.0

    return {
        "delta_t_cooling": delta_t_cooling,
        "total_heat": total_heat,
        "airflow_m3s": airflow_m3s,
        "airflow_ls": airflow_ls,
        "airflow_m3hr": airflow_m3hr,
        "ach": ach,
        "richardson_number": richardson_number,
        "effective_local_airflow": effective_local_airflow,
        "dose_term": dose_term,
        "ideal_probability": ideal_probability,
        "local_probability": local_probability,
        "ideal_probability_percent": ideal_probability * 100.0,
        "local_probability_percent": local_probability * 100.0,
    }


def render_progress():
    progress_columns = st.columns(3)

    step_information = [
        (
            "Step 1",
            "Cooling and ACH",
            st.session_state["step1_confirmed"],
        ),
        (
            "Step 2",
            "Richardson Number",
            st.session_state["step2_confirmed"],
        ),
        (
            "Step 3",
            "Infection Risk",
            st.session_state["step3_confirmed"],
        ),
    ]

    for index, step_information_item in enumerate(step_information):
        step_number, step_name, completed = step_information_item

        if completed:
            status = "Confirmed"
        elif st.session_state["step"] == index + 1:
            status = "Current section"
        else:
            status = "Not confirmed"

        with progress_columns[index]:
            st.markdown(
                f"**{step_number}: {step_name}**  \n{status}"
            )

    completed_count = sum(
        [
            st.session_state["step1_confirmed"],
            st.session_state["step2_confirmed"],
            st.session_state["step3_confirmed"],
        ]
    )

    st.progress(completed_count / 3.0)


# =========================================================
# LANDING PAGE
# =========================================================
if not st.session_state["started"]:
    st.title("ATLICE")
    st.subheader("Indoor Air Calculator")

    st.write(
        "Calculate cooling airflow, air changes per hour, "
        "Richardson number, local effective ventilation, "
        "and Wells-Riley infection probability."
    )

    st.button(
        "Open ATLICE Calculator",
        type="primary",
        on_click=open_calculator,
    )

    st.stop()


# =========================================================
# APPLICATION HEADER
# =========================================================
header_left, header_middle, header_right = st.columns([4, 1, 1])

with header_left:
    st.title("ATLICE")
    st.caption("Complete and confirm each section in order.")

current_section = st.session_state["step"]
if current_section not in (1, 2, 3):
    current_section = 1

with header_middle:
    st.button(
        "Restore This Section",
        on_click=restore_section_defaults,
        args=(current_section,),
        use_container_width=True,
    )

with header_right:
    st.button(
        "Start Again",
        on_click=start_again,
        use_container_width=True,
    )

render_progress()
st.divider()


# =========================================================
# STEP 1: COOLING AND ACH
# =========================================================
if st.session_state["step"] == 1:
    st.header("1. Cooling and ACH")
    st.write(
        "The ATLICE default values are already loaded. "
        "Change them only when required."
    )

    with st.form("cooling_ach_form"):
        left_column, right_column = st.columns(2)

        with left_column:
            st.number_input(
                "Room volume (m3)",
                min_value=0.01,
                step=0.5,
                key="room_volume",
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

        with right_column:
            st.number_input(
                "Supply-air temperature (deg C)",
                step=0.5,
                key="supply_temp",
            )

            st.number_input(
                "Target room temperature (deg C)",
                step=0.5,
                key="target_temp",
            )

            st.number_input(
                "Volumetric heat capacity, rho cp (J/m3.K)",
                min_value=1.0,
                step=10.0,
                key="rho_cp",
            )

        section_one_submitted = st.form_submit_button(
            "Confirm Section 1 and Continue",
            type="primary",
            use_container_width=True,
        )

    st.button(
        "Restore Section 1 Defaults",
        key="restore_section_1",
        on_click=restore_section_defaults,
        args=(1,),
    )

    if section_one_submitted:
        section_one_errors = []

        if (
            st.session_state["target_temp"]
            <= st.session_state["supply_temp"]
        ):
            section_one_errors.append(
                "Target room temperature must be higher than "
                "the supply-air temperature."
            )

        if st.session_state["room_volume"] <= 0:
            section_one_errors.append(
                "Room volume must be greater than zero."
            )

        if st.session_state["rho_cp"] <= 0:
            section_one_errors.append(
                "Volumetric heat capacity must be greater than zero."
            )

        if section_one_errors:
            for error_message in section_one_errors:
                st.error(error_message)
        else:
            st.session_state["step1_confirmed"] = True
            st.session_state["step2_confirmed"] = False
            st.session_state["step3_confirmed"] = False
            st.session_state["results_ready"] = False
            st.session_state["step"] = 2
            st.rerun()


# =========================================================
# STEP 2: RICHARDSON NUMBER
# =========================================================
elif st.session_state["step"] == 2:
    st.header("2. Richardson Number")
    st.write(
        "Enter the buoyancy and mechanical-airflow conditions."
    )

    with st.form("richardson_form"):
        left_column, right_column = st.columns(2)

        with left_column:
            st.number_input(
                "Gravity, g (m/s2)",
                min_value=0.01,
                step=0.01,
                key="gravity",
            )

            st.number_input(
                "Thermal expansion coefficient, alpha (1/K)",
                min_value=0.000001,
                step=0.00001,
                format="%.5f",
                key="alpha",
            )

            st.number_input(
                "Temperature difference for Ri, delta T (K)",
                step=0.1,
                key="delta_t_ri",
            )

        with right_column:
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

            st.info("Richardson number: Ri = g alpha deltaT L / V^2")

        section_two_submitted = st.form_submit_button(
            "Confirm Section 2 and Continue",
            type="primary",
            use_container_width=True,
        )

    st.button(
        "Restore Section 2 Defaults",
        key="restore_section_2",
        on_click=restore_section_defaults,
        args=(2,),
    )

    if section_two_submitted:
        if st.session_state["air_velocity"] <= 0:
            st.error("Air velocity must be greater than zero.")
        else:
            st.session_state["step2_confirmed"] = True
            st.session_state["step3_confirmed"] = False
            st.session_state["results_ready"] = False
            st.session_state["step"] = 3
            st.rerun()

    if st.button("Back to Section 1"):
        st.session_state["step"] = 1
        st.rerun()


# =========================================================
# STEP 3: VENTILATION AND INFECTION RISK
# =========================================================
elif st.session_state["step"] == 3:
    st.header("3. Ventilation and Infection Risk")
    st.write(
        "Enter the local ventilation effectiveness and "
        "Wells-Riley exposure parameters."
    )

    with st.form("infection_risk_form"):
        left_column, right_column = st.columns(2)

        with left_column:
            st.number_input(
                "Local ventilation effectiveness",
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

        with right_column:
            st.number_input(
                "Breathing rate, p (m3/h)",
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

            st.info(
                "Local Wells-Riley equation: "
                "P = 1 - exp[-Iqpt / (ventilation effectiveness x Q)]"
            )

        section_three_submitted = st.form_submit_button(
            "Confirm Section 3 and Review Inputs",
            type="primary",
            use_container_width=True,
        )

    st.button(
        "Restore Section 3 Defaults",
        key="restore_section_3",
        on_click=restore_section_defaults,
        args=(3,),
    )

    if section_three_submitted:
        if st.session_state["ventilation_effectiveness"] <= 0:
            st.error(
                "Local ventilation effectiveness must be greater than zero."
            )
        else:
            st.session_state["step3_confirmed"] = True
            st.session_state["results_ready"] = False
            st.session_state["step"] = 4
            st.rerun()

    if st.button("Back to Section 2"):
        st.session_state["step"] = 2
        st.rerun()


# =========================================================
# STEP 4: REVIEW
# =========================================================
elif st.session_state["step"] == 4:
    st.header("Review and Compile")
    st.write("Check all inputs before compiling the results.")

    review_one, review_two, review_three = st.columns(3)

    with review_one:
        st.subheader("Cooling and ACH")
        st.write(f"Room volume: {st.session_state['room_volume']:.2f} m3")
        st.write(f"People: {st.session_state['people']}")
        st.write(
            "Heat per person: "
            f"{st.session_state['heat_per_person']:.2f} W/person"
        )
        st.write(
            "Supply / target temperature: "
            f"{st.session_state['supply_temp']:.2f} / "
            f"{st.session_state['target_temp']:.2f} deg C"
        )

        if st.button("Edit Section 1"):
            st.session_state["step"] = 1
            st.rerun()

    with review_two:
        st.subheader("Richardson Number")
        st.write(f"Gravity: {st.session_state['gravity']:.2f} m/s2")
        st.write(
            "Thermal expansion coefficient: "
            f"{st.session_state['alpha']:.5f} 1/K"
        )
        st.write(
            "Temperature difference: "
            f"{st.session_state['delta_t_ri']:.2f} K"
        )
        st.write(
            "Length / velocity: "
            f"{st.session_state['length_scale']:.2f} m / "
            f"{st.session_state['air_velocity']:.3f} m/s"
        )

        if st.button("Edit Section 2"):
            st.session_state["step"] = 2
            st.rerun()

    with review_three:
        st.subheader("Infection Risk")
        st.write(
            "Ventilation effectiveness: "
            f"{st.session_state['ventilation_effectiveness']:.3f}"
        )
        st.write(
            "Infectious people: "
            f"{st.session_state['infected_people']}"
        )
        st.write(
            "Quanta generation rate: "
            f"{st.session_state['quanta_rate']:.2f} quanta/h"
        )
        st.write(
            "Breathing rate / exposure: "
            f"{st.session_state['breathing_rate']:.2f} m3/h / "
            f"{st.session_state['exposure_time']:.2f} h"
        )

        if st.button("Edit Section 3"):
            st.session_state["step"] = 3
            st.rerun()

    st.divider()

    if st.button(
        "Compile Final Results",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["results_ready"] = True
        st.session_state["step"] = 5
        st.rerun()


# =========================================================
# STEP 5: RESULTS
# =========================================================
elif (
    st.session_state["step"] == 5
    and st.session_state["results_ready"]
):
    try:
        results = calculate_results()
    except ValueError as calculation_error:
        st.error(str(calculation_error))
        st.stop()

    st.header("Compiled Results")

    metric_one, metric_two, metric_three, metric_four = st.columns(4)

    with metric_one:
        st.metric(
            "Required ACH",
            f"{results['ach']:.2f} h-1",
        )

    with metric_two:
        st.metric(
            "Required Airflow",
            f"{results['airflow_ls']:.2f} L/s",
        )

    with metric_three:
        st.metric(
            "Airflow",
            f"{results['airflow_m3hr']:.2f} m3/h",
        )

    with metric_four:
        st.metric(
            "Richardson Number",
            f"{results['richardson_number']:.4f}",
        )

    risk_one, risk_two = st.columns(2)

    with risk_one:
        st.metric(
            "Ideal Well-Mixed Probability",
            f"{results['ideal_probability_percent']:.2f}%",
        )

    with risk_two:
        st.metric(
            "Local Infection Probability",
            f"{results['local_probability_percent']:.2f}%",
        )

    with st.expander("Cooling and ACH details", expanded=True):
        st.write(
            f"Total sensible heat load: "
            f"{results['total_heat']:.2f} W"
        )
        st.write(
            f"Cooling temperature difference: "
            f"{results['delta_t_cooling']:.2f} deg C"
        )
        st.write(
            f"Required airflow: "
            f"{results['airflow_m3s']:.4f} m3/s"
        )
        st.write(
            f"Required airflow: "
            f"{results['airflow_ls']:.2f} L/s"
        )
        st.write(
            f"Required airflow: "
            f"{results['airflow_m3hr']:.2f} m3/h"
        )
        st.write(f"Required ACH: {results['ach']:.2f} h-1")

    with st.expander("Richardson number details"):
        st.write(
            f"Richardson number: "
            f"{results['richardson_number']:.4f}"
        )
        st.latex(r"Ri = \frac{g\alpha\Delta T L}{V^2}")

        if results["richardson_number"] < 0.1:
            st.info(
                "Forced-air momentum is likely to dominate over buoyancy."
            )
        elif results["richardson_number"] <= 1.0:
            st.info(
                "Both buoyancy and forced-air momentum may influence airflow."
            )
        else:
            st.info("Buoyancy effects may dominate the airflow.")

    with st.expander("Local ventilation details"):
        st.write(
            "Local ventilation effectiveness: "
            f"{st.session_state['ventilation_effectiveness']:.3f}"
        )
        st.write(
            f"Room airflow, Q: "
            f"{results['airflow_m3hr']:.2f} m3/h"
        )
        st.write(
            f"Effective local airflow: "
            f"{results['effective_local_airflow']:.2f} m3/h"
        )

    with st.expander("Wells-Riley infection-risk details"):
        st.write(f"Dose term, Iqpt: {results['dose_term']:.4f}")
        st.write(
            "Ideal well-mixed probability: "
            f"{results['ideal_probability']:.5f}"
        )
        st.write(
            "Local infection probability: "
            f"{results['local_probability']:.5f}"
        )
        st.latex(
            r"P_{\mathrm{loc}}"
            r"=1-\exp\left("
            r"-\frac{Iqpt}"
            r"{\varepsilon_{V,\mathrm{loc}}Q}"
            r"\right)"
        )

    results_text = f"""ATLICE - INDOOR AIR CALCULATION RESULTS

Room volume: {st.session_state['room_volume']:.2f} m3
Number of people: {st.session_state['people']}
Heat per person: {st.session_state['heat_per_person']:.2f} W/person
Supply-air temperature: {st.session_state['supply_temp']:.2f} deg C
Target room temperature: {st.session_state['target_temp']:.2f} deg C
Required airflow: {results['airflow_m3hr']:.2f} m3/h
Required ACH: {results['ach']:.2f} h-1
Richardson number: {results['richardson_number']:.4f}
Ventilation effectiveness: {st.session_state['ventilation_effectiveness']:.3f}
Ideal infection probability: {results['ideal_probability_percent']:.2f}%
Local infection probability: {results['local_probability_percent']:.2f}%
"""

    action_one, action_two, action_three = st.columns(3)

    with action_one:
        if st.button("Review Inputs"):
            st.session_state["step"] = 4
            st.rerun()

    with action_two:
        st.download_button(
            label="Download Results",
            data=results_text,
            file_name="ATLICE_indoor_air_results.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with action_three:
        st.button(
            "New Calculation",
            type="primary",
            on_click=restore_all_defaults,
            use_container_width=True,
        )
