# -*- coding: utf-8 -*-

import math
import streamlit as st

st.set_page_config(
page_title="ATLICE | Indoor Air Calculator",
page_icon="🌬️",
layout="wide",
initial_sidebar_state="collapsed",
)

st.markdown(
""" <style>
.stApp {
background:
radial-gradient(circle at top left, rgba(42,111,151,.14), transparent 32%),
radial-gradient(circle at bottom right, rgba(0,168,150,.12), transparent 30%),
linear-gradient(135deg, #f6fbff 0%, #eef7f8 100%);
}

```
    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        min-height: 68vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .badge {
        padding: .45rem 1rem;
        border-radius: 999px;
        color: #0b5f73;
        background: #ffffffc7;
        border: 1px solid #0b5f732e;
        font-weight: 700;
        letter-spacing: .16rem;
    }

    .hero-title {
        font-size: clamp(3.4rem, 8vw, 6.8rem);
        line-height: .95;
        font-weight: 850;
        color: #12384a;
        margin: 1.2rem 0 0;
    }

    .hero-subtitle {
        max-width: 720px;
        margin: 1.5rem auto 2.2rem;
        color: #496775;
        font-size: 1.12rem;
        line-height: 1.75;
    }

    .page-title {
        font-size: 2.25rem;
        font-weight: 800;
        color: #12384a;
    }

    .page-subtitle {
        color: #5b7480;
        margin-bottom: 1.5rem;
    }

    .card {
        background: #ffffffe8;
        border: 1px solid #19566c1f;
        border-radius: 22px;
        padding: 1.5rem 1.6rem;
        box-shadow: 0 14px 40px #1a465914;
        margin-bottom: 1rem;
    }

    .step {
        border-radius: 18px;
        padding: 1rem .8rem;
        text-align: center;
        border: 1px solid #1b4f631f;
        background: #ffffffb3;
        min-height: 104px;
    }

    .step-active {
        background: linear-gradient(135deg, #0b6680, #168f96);
        color: white;
    }

    .step-complete {
        background: #e8f7f2;
        color: #126a59;
    }

    .step-pending {
        color: #738690;
    }

    .step-number {
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .08rem;
        text-transform: uppercase;
    }

    .step-name {
        font-size: 1rem;
        font-weight: 750;
        margin-top: .45rem;
    }

    .review-label {
        color: #6b808a;
        font-size: .82rem;
        margin-bottom: .15rem;
    }

    .review-value {
        color: #173e4e;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: .9rem;
    }

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 12px;
        min-height: 3rem;
        font-weight: 750;
    }

    [data-testid="stMetric"] {
        background: #fffffff0;
        border: 1px solid #1a576d1a;
        padding: 1rem;
        border-radius: 18px;
    }
</style>
""",
unsafe_allow_html=True,
```

)

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

for key, value in {
**APP_DEFAULTS,
**INPUT_DEFAULTS,
}.items():
if key not in st.session_state:
st.session_state[key] = value

def reset_application():
for key in list(st.session_state.keys()):
del st.session_state[key]

```
st.rerun()
```

def restore_default_inputs():
for key, value in INPUT_DEFAULTS.items():
st.session_state[key] = value

```
st.session_state.step = 1
st.session_state.step1_confirmed = False
st.session_state.step2_confirmed = False
st.session_state.step3_confirmed = False
st.session_state.results_ready = False

st.rerun()
```

def calculate_results():
delta_t = (
st.session_state.target_temp
- st.session_state.supply_temp
)

```
if delta_t <= 0:
    raise ValueError(
        "Target room temperature must be higher "
        "than the supply-air temperature."
    )

if st.session_state.room_volume <= 0:
    raise ValueError(
        "Room volume must be greater than zero."
    )

if st.session_state.rho_cp <= 0:
    raise ValueError(
        "Volumetric heat capacity must be greater than zero."
    )

if st.session_state.air_velocity <= 0:
    raise ValueError(
        "Air velocity must be greater than zero."
    )

if st.session_state.ventilation_effectiveness <= 0:
    raise ValueError(
        "Ventilation effectiveness must be greater than zero."
    )

total_heat = (
    st.session_state.people
    * st.session_state.heat_per_person
)

airflow_m3s = total_heat / (
    st.session_state.rho_cp
    * delta_t
)

airflow_ls = airflow_m3s * 1000.0
airflow_m3hr = airflow_m3s * 3600.0

ach = (
    airflow_m3hr
    / st.session_state.room_volume
)

ri = (
    st.session_state.gravity
    * st.session_state.alpha
    * st.session_state.delta_t_ri
    * st.session_state.length_scale
) / (
    st.session_state.air_velocity ** 2
)

effective_airflow = (
    st.session_state.ventilation_effectiveness
    * airflow_m3hr
)

dose = (
    st.session_state.infected_people
    * st.session_state.quanta_rate
    * st.session_state.breathing_rate
    * st.session_state.exposure_time
)

if airflow_m3hr > 0:
    p_ideal = (
        1.0
        - math.exp(
            -dose / airflow_m3hr
        )
    )
else:
    p_ideal = (
        0.0
        if dose == 0
        else 1.0
    )

if effective_airflow > 0:
    p_local = (
        1.0
        - math.exp(
            -dose / effective_airflow
        )
    )
else:
    p_local = (
        0.0
        if dose == 0
        else 1.0
    )

return {
    "delta_t": delta_t,
    "total_heat": total_heat,
    "airflow_m3s": airflow_m3s,
    "airflow_ls": airflow_ls,
    "airflow_m3hr": airflow_m3hr,
    "ach": ach,
    "ri": ri,
    "effective_airflow": effective_airflow,
    "dose": dose,
    "p_ideal": p_ideal,
    "p_local": p_local,
    "p_ideal_percent": p_ideal * 100.0,
    "p_local_percent": p_local * 100.0,
}
```

def render_header_card(
title,
description,
):
st.markdown(
f""" <div class="card"> <h2 style="
             margin-top:0;
             color:#153f51;
         ">
{title} </h2>

```
        <p style="
            color:#627984;
            margin-bottom:0;
        ">
            {description}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
```

def render_review_card(items):
html = '<div class="card">'

```
for label, value in items:
    html += (
        f'<div class="review-label">'
        f'{label}'
        f'</div>'
    )

    html += (
        f'<div class="review-value">'
        f'{value}'
        f'</div>'
    )

html += "</div>"

st.markdown(
    html,
    unsafe_allow_html=True,
)
```

def render_progress():
steps = [
(
"Step 1",
"Cooling & ACH",
st.session_state.step1_confirmed,
),
(
"Step 2",
"Richardson Number",
st.session_state.step2_confirmed,
),
(
"Step 3",
"Infection Risk",
st.session_state.step3_confirmed,
),
]

```
columns = st.columns(3)

for index, (
    number,
    name,
    completed,
) in enumerate(
    steps,
    start=1,
):
    if completed:
        css_class = "step-complete"
        status = "Confirmed"

    elif st.session_state.step == index:
        css_class = "step-active"
        status = "Current section"

    else:
        css_class = "step-pending"
        status = "Not confirmed"

    with columns[index - 1]:
        st.markdown(
            f"""
            <div class="step {css_class}">
                <div class="step-number">
                    {number}
                </div>

                <div class="step-name">
                    {name}
                </div>

                <div style="
                    font-size:.78rem;
                    margin-top:.45rem;
                ">
                    {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

confirmed = sum(
    [
        st.session_state.step1_confirmed,
        st.session_state.step2_confirmed,
        st.session_state.step3_confirmed,
    ]
)

st.progress(
    confirmed / 3.0
)
```

if not st.session_state.started:
st.markdown(
""" <div class="hero"> <div class="badge">
INDOOR AIR ANALYSIS </div>

```
        <h1 class="hero-title">
            ATLICE
        </h1>

        <p class="hero-subtitle">
            A guided calculator for cooling airflow,
            air changes per hour, Richardson number,
            local ventilation effectiveness and
            Wells-Riley infection risk.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, centre, right = st.columns(
    [1.4, 1.0, 1.4]
)

with centre:
    if st.button(
        "Open ATLICE Calculator",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.started = True
        st.session_state.step = 1
        st.rerun()

st.stop()
```

header1, header2, header3 = st.columns(
[4.0, 1.25, 1.0]
)

with header1:
st.markdown(
'<div class="page-title">'
'ATLICE'
'</div>',
unsafe_allow_html=True,
)

```
st.markdown(
    '<div class="page-subtitle">'
    'Complete and confirm each section in order.'
    '</div>',
    unsafe_allow_html=True,
)
```

with header2:
if st.button(
"Restore Defaults",
use_container_width=True,
):
restore_default_inputs()

with header3:
if st.button(
"Start Again",
use_container_width=True,
):
reset_application()

render_progress()
st.write("")

if st.session_state.step == 1:
render_header_card(
"1. Cooling and ACH",
(
"The ATLICE default values are already loaded. "
"Change them only when required."
),
)

```
with st.form(
    "cooling_form"
):
    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Room volume (m³)",
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
        "Confirm Section 1 and Continue",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        if (
            st.session_state.target_temp
            <= st.session_state.supply_temp
        ):
            st.error(
                "Target room temperature must be higher "
                "than the supply-air temperature."
            )

        elif st.session_state.room_volume <= 0:
            st.error(
                "Room volume must be greater than zero."
            )

        elif st.session_state.rho_cp <= 0:
            st.error(
                "Volumetric heat capacity must be "
                "greater than zero."
            )

        else:
            st.session_state.step1_confirmed = True
            st.session_state.step2_confirmed = False
            st.session_state.step3_confirmed = False
            st.session_state.results_ready = False
            st.session_state.step = 2

            st.rerun()
```

elif st.session_state.step == 2:
render_header_card(
"2. Richardson Number",
(
"Define the buoyancy and mechanical-airflow "
"conditions used in the calculation."
),
)

```
with st.form(
    "richardson_form"
):
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
            step=0.00001,
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

        st.info(
            "Richardson number formula: "
            "Ri = gαΔTL / V²"
        )

    submitted = st.form_submit_button(
        "Confirm Section 2 and Continue",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        st.session_state.step2_confirmed = True
        st.session_state.step3_confirmed = False
        st.session_state.results_ready = False
        st.session_state.step = 3

        st.rerun()

if st.button(
    "Back to Section 1"
):
    st.session_state.step = 1
    st.rerun()
```

elif st.session_state.step == 3:
render_header_card(
"3. Ventilation and Infection Risk",
(
"Enter local ventilation effectiveness and "
"Wells-Riley exposure parameters."
),
)

```
with st.form(
    "infection_form"
):
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

        st.info(
            "Local Wells-Riley form: "
            "P = 1 - exp[-Iqpt / (εV,loc Q)]"
        )

    submitted = st.form_submit_button(
        "Confirm Section 3 and Review Inputs",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        st.session_state.step3_confirmed = True
        st.session_state.results_ready = False
        st.session_state.step = 4

        st.rerun()

if st.button(
    "Back to Section 2"
):
    st.session_state.step = 2
    st.rerun()
```

elif st.session_state.step == 4:
render_header_card(
"Review and Compile",
(
"Check the confirmed values below, then "
"compile the complete calculation."
),
)

```
review1, review2, review3 = st.columns(3)

with review1:
    st.markdown(
        "### Cooling & ACH"
    )

    render_review_card(
        [
            (
                "Room volume",
                f"{st.session_state.room_volume:.2f} m³",
            ),
            (
                "People",
                str(
                    st.session_state.people
                ),
            ),
            (
                "Heat per person",
                (
                    f"{st.session_state.heat_per_person:.2f} "
                    "W/person"
                ),
            ),
            (
                "Supply / target temperature",
                (
                    f"{st.session_state.supply_temp:.2f} / "
                    f"{st.session_state.target_temp:.2f} °C"
                ),
            ),
        ]
    )

    if st.button(
        "Edit Section 1"
    ):
        st.session_state.step = 1
        st.rerun()

with review2:
    st.markdown(
        "### Richardson Number"
    )

    render_review_card(
        [
            (
                "Gravity",
                f"{st.session_state.gravity:.2f} m/s²",
            ),
            (
                "Thermal expansion coefficient",
                f"{st.session_state.alpha:.5f} 1/K",
            ),
            (
                "Temperature difference",
                f"{st.session_state.delta_t_ri:.2f} K",
            ),
            (
                "Length / velocity",
                (
                    f"{st.session_state.length_scale:.2f} m / "
                    f"{st.session_state.air_velocity:.3f} m/s"
                ),
            ),
        ]
    )

    if st.button(
        "Edit Section 2"
    ):
        st.session_state.step = 2
        st.rerun()

with review3:
    st.markdown(
        "### Infection Risk"
    )

    render_review_card(
        [
            (
                "Ventilation effectiveness",
                (
                    f"{st.session_state."
                    f"ventilation_effectiveness:.3f}"
                ),
            ),
            (
                "Infectious people",
                str(
                    st.session_state.infected_people
                ),
            ),
            (
                "Quanta generation rate",
                (
                    f"{st.session_state.quanta_rate:.2f} "
                    "quanta/h"
                ),
            ),
            (
                "Breathing rate / exposure",
                (
                    f"{st.session_state.breathing_rate:.2f} "
                    f"m³/h / "
                    f"{st.session_state.exposure_time:.2f} h"
                ),
            ),
        ]
    )

    if st.button(
        "Edit Section 3"
    ):
        st.session_state.step = 3
        st.rerun()

st.write("")

left, centre, right = st.columns(
    [1, 2, 1]
)

with centre:
    if st.button(
        "Compile Final Results",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.results_ready = True
        st.session_state.step = 5

        st.rerun()
```

elif (
st.session_state.step == 5
and st.session_state.results_ready
):
try:
results = calculate_results()

```
except ValueError as error:
    st.error(
        str(error)
    )
    st.stop()

render_header_card(
    "Compiled Results",
    (
        "The values below combine all three confirmed "
        "calculation sections."
    ),
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "Required ACH",
        f"{results['ach']:.2f} h⁻¹",
    )

with metric2:
    st.metric(
        "Required Airflow",
        f"{results['airflow_ls']:.2f} L/s",
    )

with metric3:
    st.metric(
        "Airflow",
        f"{results['airflow_m3hr']:.2f} m³/h",
    )

with metric4:
    st.metric(
        "Richardson Number",
        f"{results['ri']:.4f}",
    )

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

with st.expander(
    "1. Cooling and ACH details",
    expanded=True,
):
    st.write(
        f"**Total sensible heat load:** "
        f"{results['total_heat']:.2f} W"
    )

    st.write(
        f"**Cooling temperature difference:** "
        f"{results['delta_t']:.2f} °C"
    )

    st.write(
        f"**Required airflow:** "
        f"{results['airflow_m3s']:.4f} m³/s"
    )

    st.write(
        f"**Required airflow:** "
        f"{results['airflow_ls']:.2f} L/s"
    )

    st.write(
        f"**Required airflow:** "
        f"{results['airflow_m3hr']:.2f} m³/h"
    )

    st.write(
        f"**Required ACH:** "
        f"{results['ach']:.2f} h⁻¹"
    )

with st.expander(
    "2. Richardson number details"
):
    st.write(
        f"**Richardson number:** "
        f"{results['ri']:.4f}"
    )

    st.latex(
        r"Ri = \frac{g\alpha\Delta T L}{V^2}"
    )

    if results["ri"] < 0.1:
        st.info(
            "Forced-air momentum is likely to "
            "dominate over buoyancy."
        )

    elif results["ri"] <= 1.0:
        st.info(
            "Both buoyancy and forced-air momentum "
            "may influence the airflow."
        )

    else:
        st.info(
            "Buoyancy effects may dominate the airflow."
        )

with st.expander(
    "3. Local ventilation details"
):
    st.write(
        f"**Local ventilation effectiveness:** "
        f"{st.session_state.ventilation_effectiveness:.3f}"
    )

    st.write(
        f"**Room airflow, Q:** "
        f"{results['airflow_m3hr']:.2f} m³/h"
    )

    st.write(
        f"**Effective local airflow:** "
        f"{results['effective_airflow']:.2f} m³/h"
    )

    st.latex(
        r"Q_{\mathrm{eff,loc}}"
        r" = "
        r"\varepsilon_{V,\mathrm{loc}}Q"
    )

with st.expander(
    "4. Wells-Riley infection-risk details"
):
    st.write(
        f"**Dose term, Iqpt:** "
        f"{results['dose']:.4f}"
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
        r" = "
        r"1 - \exp\left("
        r"-\frac{Iqpt}"
        r"{\varepsilon_{V,\mathrm{loc}}Q}"
        r"\right)"
    )

    effectiveness = (
        st.session_state.ventilation_effectiveness
    )

    if effectiveness < 1.0:
        st.warning(
            "Local ventilation effectiveness is below "
            "1.0, so local risk is higher than the "
            "well-mixed reference."
        )

    elif math.isclose(
        effectiveness,
        1.0,
        rel_tol=1e-9,
        abs_tol=1e-9,
    ):
        st.info(
            "Local ventilation effectiveness equals "
            "1.0, representing the well-mixed "
            "reference case."
        )

    else:
        st.success(
            "Local ventilation effectiveness is above "
            "1.0, so local risk is lower than the "
            "well-mixed reference."
        )

results_text = f"""ATLICE - INDOOR AIR CALCULATION RESULTS
```

Room volume: {st.session_state.room_volume:.2f} m³
Number of people: {st.session_state.people}
Heat per person: {st.session_state.heat_per_person:.2f} W/person
Supply-air temperature: {st.session_state.supply_temp:.2f} °C
Target room temperature: {st.session_state.target_temp:.2f} °C
Required airflow: {results['airflow_m3hr']:.2f} m³/h
Required ACH: {results['ach']:.2f} h⁻¹
Richardson number: {results['ri']:.4f}
Ventilation effectiveness: {st.session_state.ventilation_effectiveness:.3f}
Ideal infection probability: {results['p_ideal_percent']:.2f}%
Local infection probability: {results['p_local_percent']:.2f}%
"""

```
action1, action2, action3 = st.columns(3)

with action1:
    if st.button(
        "Review Inputs"
    ):
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
    if st.button(
        "New Calculation",
        type="primary",
    ):
        restore_default_inputs()
```
