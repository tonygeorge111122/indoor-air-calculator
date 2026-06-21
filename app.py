import math
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Indoor Air Calculator",
    page_icon="🌬️",
    layout="wide"
)

st.title("🌬️ ACH, Richardson Number and Wells–Riley Calculator")

st.write(
    "Enter or edit the values below, then press **Calculate Results**."
)


# ---------------------------------------------------------
# INPUT FORM
# ---------------------------------------------------------
with st.form("calculator_form"):

    col1, col2, col3 = st.columns(3)

    # -----------------------------------------------------
    # COOLING AND ACH INPUTS
    # -----------------------------------------------------
    with col1:
        st.subheader("Cooling and ACH")

        room_volume = st.number_input(
            "Room volume (m³)",
            min_value=0.01,
            value=63.0,
            step=1.0
        )

        people = st.number_input(
            "Number of people",
            min_value=0,
            value=5,
            step=1
        )

        heat_per_person = st.number_input(
            "Heat per person (W/person)",
            min_value=0.0,
            value=100.0,
            step=5.0
        )

        supply_temp = st.number_input(
            "Supply-air temperature (°C)",
            value=12.0,
            step=0.5
        )

        target_temp = st.number_input(
            "Target room temperature (°C)",
            value=22.0,
            step=0.5
        )

        rho_cp = st.number_input(
            "Volumetric heat capacity, ρcp (J/m³·K)",
            min_value=1.0,
            value=1200.0,
            step=10.0
        )

    # -----------------------------------------------------
    # RICHARDSON NUMBER INPUTS
    # -----------------------------------------------------
    with col2:
        st.subheader("Richardson Number")

        gravity = st.number_input(
            "Gravity, g (m/s²)",
            min_value=0.01,
            value=9.81,
            step=0.01
        )

        alpha = st.number_input(
            "Thermal expansion coefficient, α (1/K)",
            min_value=0.000001,
            value=0.00335,
            format="%.5f"
        )

        delta_t_ri = st.number_input(
            "Temperature difference for Ri, ΔT (K or °C)",
            value=5.0,
            step=0.1
        )

        length_scale = st.number_input(
            "Characteristic length, L (m)",
            min_value=0.001,
            value=1.0,
            step=0.1
        )

        air_velocity = st.number_input(
            "Air velocity, V (m/s)",
            min_value=0.001,
            value=0.10,
            step=0.01,
            format="%.3f"
        )

    # -----------------------------------------------------
    # WELLS–RILEY INPUTS
    # -----------------------------------------------------
    with col3:
        st.subheader("Ventilation and Infection Risk")

        ventilation_effectiveness = st.number_input(
            "Local ventilation effectiveness, εV,loc",
            min_value=0.001,
            value=0.67,
            step=0.01
        )

        infected_people = st.number_input(
            "Number of infectious people, I",
            min_value=0,
            value=1,
            step=1
        )

        quanta_rate = st.number_input(
            "Quanta generation rate, q (quanta/h)",
            min_value=0.0,
            value=10.0,
            step=1.0
        )

        breathing_rate = st.number_input(
            "Breathing rate, p (m³/h)",
            min_value=0.0,
            value=0.5,
            step=0.1
        )

        exposure_time = st.number_input(
            "Exposure time, t (h)",
            min_value=0.0,
            value=2.0,
            step=0.5
        )

    calculate_button = st.form_submit_button(
        "Calculate Results",
        use_container_width=True
    )


# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------
if calculate_button:

    errors = []

    if target_temp <= supply_temp:
        errors.append(
            "Target room temperature must be higher than "
            "the supply-air temperature."
        )

    if room_volume <= 0:
        errors.append("Room volume must be greater than zero.")

    if air_velocity <= 0:
        errors.append("Air velocity must be greater than zero.")

    if ventilation_effectiveness <= 0:
        errors.append(
            "Ventilation effectiveness must be greater than zero."
        )

    if errors:
        for error in errors:
            st.error(error)

    else:
        # Cooling and airflow
        delta_t_cooling = target_temp - supply_temp
        total_heat = people * heat_per_person

        airflow_m3s = total_heat / (
            rho_cp * delta_t_cooling
        )

        airflow_ls = airflow_m3s * 1000
        airflow_m3hr = airflow_m3s * 3600
        ach = airflow_m3hr / room_volume

        # Richardson number
        richardson_number = (
            gravity
            * alpha
            * delta_t_ri
            * length_scale
        ) / (air_velocity ** 2)

        # Local effective airflow
        q_eff_loc = (
            ventilation_effectiveness
            * airflow_m3hr
        )

        # Wells–Riley numerator
        dose_term = (
            infected_people
            * quanta_rate
            * breathing_rate
            * exposure_time
        )

        # Avoid division by zero if airflow is zero
        if airflow_m3hr > 0:
            p_ideal = 1 - math.exp(
                -dose_term / airflow_m3hr
            )
        else:
            p_ideal = 0.0 if dose_term == 0 else 1.0

        if q_eff_loc > 0:
            p_local = 1 - math.exp(
                -dose_term / q_eff_loc
            )
        else:
            p_local = 0.0 if dose_term == 0 else 1.0

        p_ideal_percent = p_ideal * 100
        p_local_percent = p_local * 100


        # -------------------------------------------------
        # RESULTS
        # -------------------------------------------------
        st.divider()
        st.header("Calculation Results")

        result_col1, result_col2, result_col3, result_col4 = st.columns(4)

        with result_col1:
            st.metric(
                "Required ACH",
                f"{ach:.2f} h⁻¹"
            )

        with result_col2:
            st.metric(
                "Airflow",
                f"{airflow_ls:.2f} L/s"
            )

        with result_col3:
            st.metric(
                "Airflow",
                f"{airflow_m3hr:.2f} m³/h"
            )

        with result_col4:
            st.metric(
                "Richardson Number",
                f"{richardson_number:.4f}"
            )


        st.subheader("1. Cooling and ACH Results")

        st.write(
            f"**Total sensible heat load:** "
            f"{total_heat:.2f} W"
        )

        st.write(
            f"**Cooling temperature difference:** "
            f"{delta_t_cooling:.2f} °C"
        )

        st.write(
            f"**Required airflow:** "
            f"{airflow_m3s:.4f} m³/s"
        )

        st.write(
            f"**Required airflow:** "
            f"{airflow_ls:.2f} L/s"
        )

        st.write(
            f"**Required airflow:** "
            f"{airflow_m3hr:.2f} m³/h"
        )

        st.write(
            f"**Required air changes per hour:** "
            f"{ach:.2f} ACH"
        )


        st.subheader("2. Richardson Number Result")

        st.write(
            f"**Richardson number, Ri:** "
            f"{richardson_number:.4f}"
        )

        st.latex(
            r"Ri = \frac{g\alpha\Delta T L}{V^2}"
        )


        st.subheader("3. Local Ventilation Effectiveness")

        st.write(
            f"**Local ventilation effectiveness:** "
            f"{ventilation_effectiveness:.3f}"
        )

        st.write(
            f"**Room airflow, Q:** "
            f"{airflow_m3hr:.2f} m^3/h"
        )

        st.write(
            f"**Local effective airflow, "
            f"Q_eff,loc:** {q_eff_loc:.2f} m³/h"
        )

        st.latex(
            r"Q_{\mathrm{eff,loc}}"
            r"=\varepsilon_{V,\mathrm{loc}}Q"
        )


        st.subheader("4. Wells–Riley Infection Risk")

        infection_col1, infection_col2 = st.columns(2)

        with infection_col1:
            st.metric(
                "Ideal well-mixed probability",
                f"{p_ideal_percent:.2f}%"
            )

        with infection_col2:
            st.metric(
                "Local infection probability",
                f"{p_local_percent:.2f}%"
            )

        st.write(
            f"**Dose term, Iqpt:** "
            f"{dose_term:.4f}"
        )

        st.write(
            f"**Ideal well-mixed probability:** "
            f"{p_ideal:.5f}"
        )

        st.write(
            f"**Local infection probability:** "
            f"{p_local:.5f}"
        )

        st.latex(
            r"P_{\mathrm{loc}}"
            r"=1-\exp\left("
            r"-\frac{Iqpt}"
            r"{Q_{\mathrm{eff,loc}}}"
            r"\right)"
        )

        st.latex(
            r"P_{\mathrm{loc}}"
            r"=1-\exp\left("
            r"-\frac{Iqpt}"
            r"{\varepsilon_{V,\mathrm{loc}}Q}"
            r"\right)"
        )


        # -------------------------------------------------
        # INTERPRETATION
        # -------------------------------------------------
        with st.expander("Show interpretation"):

            if richardson_number < 0.1:
                st.write(
                    "The Richardson number is low, indicating "
                    "that forced airflow or momentum effects are "
                    "likely to dominate over buoyancy."
                )

            elif richardson_number <= 1:
                st.write(
                    "The Richardson number indicates that both "
                    "buoyancy and forced-air momentum may influence "
                    "the airflow."
                )

            else:
                st.write(
                    "The Richardson number is relatively high, "
                    "indicating that buoyancy effects may dominate "
                    "the airflow."
                )

            if ventilation_effectiveness < 1:
                st.write(
                    "The local ventilation effectiveness is below "
                    "1.0. The effective local airflow is therefore "
                    "lower than the room-average airflow, which "
                    "increases the calculated local infection risk."
                )

            elif ventilation_effectiveness == 1:
                st.write(
                    "The local ventilation effectiveness equals "
                    "1.0, representing the well-mixed reference case."
                )

            else:
                st.write(
                    "The local ventilation effectiveness is above "
                    "1.0. The effective local airflow is therefore "
                    "higher than the room-average airflow, which "
                    "reduces the calculated local infection risk."
                )


        # -------------------------------------------------
        # DOWNLOAD RESULTS
        # -------------------------------------------------
        results_text = f"""
ACH, RICHARDSON NUMBER AND WELLS-RILEY RESULTS

INPUTS
Room volume: {room_volume:.2f} m³
Number of people: {people}
Heat per person: {heat_per_person:.2f} W/person
Supply-air temperature: {supply_temp:.2f} °C
Target room temperature: {target_temp:.2f} °C

COOLING AND ACH RESULTS
Total sensible heat load: {total_heat:.2f} W
Temperature difference: {delta_t_cooling:.2f} °C
Airflow: {airflow_m3s:.4f} m³/s
Airflow: {airflow_ls:.2f} L/s
Airflow: {airflow_m3hr:.2f} m³/h
ACH: {ach:.2f} h⁻¹

RICHARDSON NUMBER
Ri: {richardson_number:.4f}

LOCAL VENTILATION
Ventilation effectiveness: {ventilation_effectiveness:.3f}
Effective local airflow: {q_eff_loc:.2f} m³/h

WELLS-RILEY RESULTS
Ideal well-mixed probability: {p_ideal_percent:.2f}%
Local infection probability: {p_local_percent:.2f}%
"""

        st.download_button(
            label="Download Results",
            data=results_text,
            file_name="indoor_air_calculation_results.txt",
            mime="text/plain",
            use_container_width=True
        )
