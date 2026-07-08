import base64
import html
import math
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle


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

        .workflow-status {
            padding: 0.8rem 0.9rem;
            border-radius: 12px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.14);
            margin: 0.45rem 0 0.8rem 0;
            font-size: 0.82rem;
            line-height: 1.65;
        }

        .report-section {
            padding: 1.2rem 1.3rem;
            margin: 0.9rem 0;
            border-radius: 16px;
            background: rgba(255,255,255,0.94);
            border: 1px solid var(--atlice-border);
            box-shadow: 0 8px 22px rgba(15,23,42,0.04);
        }

        .report-section h3 {
            margin-top: 0;
            color: var(--atlice-primary-dark);
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
    "Occupancy Patterns": "occupancy",
    "Measurement ΔT Upload": "measurement",
    "Cooling & ACH": "ach",
    "Richardson Number": "ri",
    "Wells–Riley Risk": "wells_riley",
    "Final Report": "report",
}


if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


def go_to(page_name: str) -> None:
    st.session_state.current_page = page_name
    st.rerun()


def render_sidebar() -> None:
    confirmed_pattern = st.session_state.get("confirmed_occupancy_pattern")
    measurement_ready = bool(st.session_state.get("confirmed_measurement_delta_t"))
    ri_ready = bool(st.session_state.get("confirmed_richardson"))
    wells_ready = bool(st.session_state.get("confirmed_wells_riley"))

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

        st.markdown("### Guided workflow")

        if st.button("1  👥  Occupancy Pattern", key="nav_occupancy", use_container_width=True):
            go_to("occupancy")

        if st.button(
            "2  📊  Measurement ΔT Upload",
            key="nav_measurement",
            use_container_width=True,
            disabled=not bool(confirmed_pattern),
        ):
            go_to("measurement")

        if st.button(
            "3  🌡️  Richardson Number",
            key="nav_ri",
            use_container_width=True,
            disabled=not measurement_ready,
        ):
            go_to("ri")

        if st.button(
            "4  🫁  Wells–Riley Risk",
            key="nav_wr",
            use_container_width=True,
            disabled=not ri_ready,
        ):
            go_to("wells_riley")

        if st.button(
            "5  📄  Final Report",
            key="nav_report",
            use_container_width=True,
            disabled=not wells_ready,
        ):
            go_to("report")

        pattern_status = f"✓ {confirmed_pattern}" if confirmed_pattern else "○ Not confirmed"
        measurement_status = "✓ Confirmed" if measurement_ready else "○ Pending"
        ri_status = "✓ Confirmed" if ri_ready else "○ Pending"
        wells_status = "✓ Confirmed" if wells_ready else "○ Pending"
        report_status = "✓ Available" if wells_ready else "○ Locked"

        st.markdown(
            f"""
            <div class="workflow-status">
                <b>Progress</b><br>
                Occupancy: {pattern_status}<br>
                Measurement ΔT: {measurement_status}<br>
                Richardson: {ri_status}<br>
                Wells–Riley: {wells_status}<br>
                Report: {report_status}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Standalone calculator")
        if st.button("❄️  Cooling & ACH", key="nav_ach", use_container_width=True):
            go_to("ach")

        st.markdown("---")
        st.markdown(
            """
            <div class="small-note" style="color:rgba(255,255,255,0.72);">
                Complete each guided stage and confirm its result before moving
                to the next stage. Excel uploads are read only from the third column
                to calculate ΔT for uploaded locations.
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
                A focused toolkit for configuring occupant arrangements, estimating
                cooling airflow and air changes, evaluating buoyancy-to-momentum effects,
                and screening airborne infection risk using the Wells–Riley model.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Choose a tool")
    st.caption("Choose an occupancy symmetry pattern first, preview it, upload uploaded locations measurement files, and then continue to the Richardson calculation.")

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

    st.markdown("### Occupancy configuration")
    occupancy_card, occupancy_note = st.columns([1.45, 1], gap="large")

    with occupancy_card:
        st.markdown(
            """
            <div class="tool-card" style="min-height:210px;">
                <div class="tool-icon">👥</div>
                <h3>Occupancy Patterns</h3>
                <p>
                    Choose Pattern 1, Pattern 2, or Null Pattern under the Symmetry Pattern
                    group, preview the selected layout, and confirm it before
                    continuing to the measurement ΔT upload stage.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Open Occupancy Patterns →",
            key="home_occupancy",
            type="primary",
            use_container_width=True,
        ):
            go_to("occupancy")

    with occupancy_note:
        st.info(
            "**Workflow:** Select a Symmetry Pattern → confirm the displayed pattern "
            "→ upload uploaded locations Excel files → calculate and confirm ΔT "
            "→ continue to Richardson inputs."
        )

    st.markdown("### Model scope")
    info1, info2, info3 = st.columns(3)
    info1.info("**Cooling model:** sensible heat only; latent and envelope loads are not included.")
    info2.info("**Richardson model:** uses the specified characteristic length and representative velocity.")
    info3.info("**Wells–Riley model:** assumes steady conditions and does not replace detailed exposure assessment.")



# =========================================================
# OCCUPANCY PATTERN DRAWING ENGINE
# =========================================================
ROOM_LENGTH = 5.6
ROOM_WIDTH = 4.2
ROOM_HEIGHT = 2.7

HUMAN_DIAMETER = 0.30
HUMAN_RADIUS = HUMAN_DIAMETER / 2
HUMAN_HEAT_LOAD = 100

UNIT_SIZE = 0.60
S1_X = 1.8 + UNIT_SIZE / 2
S1_Y = ROOM_WIDTH / 2
S2_X = ROOM_LENGTH - 1.4 - UNIT_SIZE / 2
S2_Y = ROOM_WIDTH / 2
E1_X = 0.90
E1_Y = 0.90

MEASUREMENT_X_COORDS = [1.12, 2.24, 3.36, 4.48]
MEASUREMENT_Y_COORDS = [1.05, 2.10, 3.15]
MEASUREMENT_COLOUR = "crimson"

HUMAN_COLOUR = "tab:orange"
SUPPLY_COLOUR = "tab:blue"
EXHAUST_COLOUR = "tab:green"
CEILING_GRID_COLOUR = "lightgray"
DIMENSION_COLOUR = "#475569"


def get_pattern_1_positions():
    """Pattern 1: the existing two-column arrangement."""
    vertical_clear_distance = 0.70
    top_bottom_clearance = 0.95
    left_right_clearance = 1.20
    column_clear_distance = 2.60

    y1 = top_bottom_clearance + HUMAN_RADIUS
    y2 = y1 + HUMAN_DIAMETER + vertical_clear_distance
    y3 = y2 + HUMAN_DIAMETER + vertical_clear_distance

    left_x = left_right_clearance + HUMAN_RADIUS
    right_x = left_x + HUMAN_DIAMETER + column_clear_distance

    positions = {
        "H1": (left_x, y1),
        "H2": (left_x, y2),
        "H3": (left_x, y3),
        "H4": (right_x, y1),
        "H5": (right_x, y2),
        "H6": (right_x, y3),
    }
    dimensions = {
        "adjacent_clear": vertical_clear_distance,
        "wall_clear_x": left_right_clearance,
        "wall_clear_y": top_bottom_clearance,
        "between_columns": column_clear_distance,
    }
    return positions, dimensions


def get_pattern_2_positions():
    """Pattern 2: two rows of three occupants."""
    adjacent_clear_distance = 0.70
    main_opposite_wall_clearance = 0.90

    occupied_row_length = 3 * HUMAN_DIAMETER + 2 * adjacent_clear_distance
    left_right_clearance = (ROOM_LENGTH - occupied_row_length) / 2

    row_clear_distance = (
        ROOM_WIDTH
        - 2 * main_opposite_wall_clearance
        - 2 * HUMAN_DIAMETER
    )
    if row_clear_distance <= 0:
        raise ValueError("Pattern 2 does not fit inside the room.")

    x1 = left_right_clearance + HUMAN_RADIUS
    x2 = x1 + HUMAN_DIAMETER + adjacent_clear_distance
    x3 = x2 + HUMAN_DIAMETER + adjacent_clear_distance

    bottom_row_y = main_opposite_wall_clearance + HUMAN_RADIUS
    top_row_y = bottom_row_y + HUMAN_DIAMETER + row_clear_distance

    positions = {
        "H1": (x1, bottom_row_y),
        "H2": (x2, bottom_row_y),
        "H3": (x3, bottom_row_y),
        "H4": (x1, top_row_y),
        "H5": (x2, top_row_y),
        "H6": (x3, top_row_y),
    }
    dimensions = {
        "adjacent_clear": adjacent_clear_distance,
        "wall_clear_x": left_right_clearance,
        "wall_clear_y": main_opposite_wall_clearance,
        "between_rows": row_clear_distance,
    }
    return positions, dimensions


def draw_double_arrow(
    ax,
    start,
    end,
    label,
    label_position=None,
    rotation=0,
    fontsize=8.0,
    linewidth=0.75,
):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="<->",
            linewidth=linewidth,
            color=DIMENSION_COLOUR,
            mutation_scale=8,
            shrinkA=0,
            shrinkB=0,
        ),
        zorder=8,
    )

    if label_position is None:
        label_position = (
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2,
        )

    ax.text(
        label_position[0],
        label_position[1],
        label,
        ha="center",
        va="center",
        rotation=rotation,
        fontsize=fontsize,
        fontweight="normal",
        color=DIMENSION_COLOUR,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.68, pad=0.7),
        zorder=9,
    )


def draw_extension_line(ax, x_values, y_values):
    ax.plot(
        x_values,
        y_values,
        color=DIMENSION_COLOUR,
        linewidth=0.50,
        zorder=7,
    )


def draw_ceiling_grid(ax):
    vertical_lines = [0.60, 1.20, 1.80, 2.40, 3.00, 3.60, 4.20, 4.80, 5.40]
    horizontal_lines = [0.60, 1.20, 1.80, 2.40, 3.00, 3.60]
    ax.vlines(
        vertical_lines,
        ymin=0,
        ymax=ROOM_WIDTH,
        colors=CEILING_GRID_COLOUR,
        linewidth=1.0,
        zorder=1,
    )
    ax.hlines(
        horizontal_lines,
        xmin=0,
        xmax=ROOM_LENGTH,
        colors=CEILING_GRID_COLOUR,
        linewidth=1.0,
        zorder=1,
    )


def draw_room_boundary(ax):
    ax.add_patch(
        Rectangle(
            (0, 0),
            ROOM_LENGTH,
            ROOM_WIDTH,
            fill=False,
            edgecolor="black",
            linewidth=3,
            zorder=6,
        )
    )


def draw_occupants(ax, positions):
    for label, (x_value, y_value) in positions.items():
        ax.add_patch(
            Circle(
                (x_value, y_value),
                HUMAN_RADIUS,
                facecolor=HUMAN_COLOUR,
                edgecolor="black",
                linewidth=1.1,
                alpha=0.92,
                zorder=4,
            )
        )
        ax.text(
            x_value,
            y_value,
            label,
            ha="center",
            va="center",
            fontsize=7.8,
            fontweight="bold",
            zorder=5,
        )


def draw_ventilation_units(ax):
    units = [
        (S1_X, S1_Y, "S1", SUPPLY_COLOUR),
        (S2_X, S2_Y, "S2", SUPPLY_COLOUR),
        (E1_X, E1_Y, "E1", EXHAUST_COLOUR),
    ]
    for x_value, y_value, label, colour in units:
        ax.add_patch(
            Rectangle(
                (x_value - UNIT_SIZE / 2, y_value - UNIT_SIZE / 2),
                UNIT_SIZE,
                UNIT_SIZE,
                facecolor=colour,
                edgecolor="black",
                linewidth=2,
                alpha=0.78,
                zorder=4,
            )
        )
        ax.text(
            x_value,
            y_value,
            label,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            zorder=5,
        )


def get_measurement_locations():
    """Return the 12 measurement locations using split-system-side snake numbering.

    Numbering starts from the top-right point near the split system,
    moves left across the top row, comes down, moves right across
    the middle row, comes down again, and moves left across the bottom row.

    Final order:
        M1  = (4.48, 3.15), M2  = (3.36, 3.15), M3  = (2.24, 3.15), M4  = (1.12, 3.15)
        M5  = (1.12, 2.10), M6  = (2.24, 2.10), M7  = (3.36, 2.10), M8  = (4.48, 2.10)
        M9  = (4.48, 1.05), M10 = (3.36, 1.05), M11 = (2.24, 1.05), M12 = (1.12, 1.05)
    """
    locations = {}
    index = 1

    # Start at the top row and move downward.
    y_values_top_to_bottom = sorted(MEASUREMENT_Y_COORDS, reverse=True)

    for row_index, y_value in enumerate(y_values_top_to_bottom):
        # Row 1: right to left, Row 2: left to right, Row 3: right to left.
        if row_index % 2 == 0:
            x_values = sorted(MEASUREMENT_X_COORDS, reverse=True)
        else:
            x_values = sorted(MEASUREMENT_X_COORDS)

        for x_value in x_values:
            locations[f"M{index}"] = (x_value, y_value)
            index += 1

    return locations


def draw_measurement_locations(ax):
    """Draw the 12 measurement locations as labelled markers."""
    for label, (x_value, y_value) in get_measurement_locations().items():
        ax.scatter(
            x_value,
            y_value,
            s=60,
            marker="D",
            facecolor=MEASUREMENT_COLOUR,
            edgecolor="white",
            linewidth=0.9,
            zorder=6,
        )
        ax.text(
            x_value + 0.08,
            y_value + 0.08,
            label,
            fontsize=7.8,
            color=MEASUREMENT_COLOUR,
            fontweight="normal",
            zorder=7,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.72, pad=0.5),
        )


def draw_external_room_dimensions(ax):
    draw_double_arrow(
        ax,
        (0, -0.38),
        (ROOM_LENGTH, -0.38),
        "5.6 m",
        (ROOM_LENGTH / 2, -0.55),
        fontsize=8.4,
    )
    draw_double_arrow(
        ax,
        (-0.34, 0),
        (-0.34, ROOM_WIDTH),
        "4.2 m",
        (-0.53, ROOM_WIDTH / 2),
        rotation=90,
        fontsize=8.4,
    )


def draw_room_labels(ax):
    ax.text(
        ROOM_LENGTH / 2,
        -0.08,
        "Main Door",
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
    )
    ax.text(
        ROOM_LENGTH / 2,
        ROOM_WIDTH + 0.08,
        "Wall opposite to Main Door",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
    ax.text(
        ROOM_LENGTH + 0.18,
        ROOM_WIDTH / 2,
        "Split system",
        ha="center",
        va="center",
        rotation=90,
        fontsize=10,
        fontweight="bold",
    )


def draw_pattern_1_dimensions(ax, positions, dimensions):
    h1_x, h1_y = positions["H1"]
    h2_x, h2_y = positions["H2"]
    h3_x, h3_y = positions["H3"]
    h6_x, h6_y = positions["H6"]

    h2_top = h2_y + HUMAN_RADIUS
    h3_bottom = h3_y - HUMAN_RADIUS
    arrow_x = h2_x + 0.34
    draw_double_arrow(
        ax,
        (arrow_x, h2_top),
        (arrow_x, h3_bottom),
        f"{dimensions['adjacent_clear']:.2f} m",
        (arrow_x + 0.20, (h2_top + h3_bottom) / 2),
        fontsize=7.8,
    )
    draw_extension_line(ax, [h2_x + HUMAN_RADIUS, arrow_x], [h2_top, h2_top])
    draw_extension_line(ax, [h3_x + HUMAN_RADIUS, arrow_x], [h3_bottom, h3_bottom])

    h3_left = h3_x - HUMAN_RADIUS
    left_arrow_y = h3_y - 0.40
    draw_double_arrow(
        ax,
        (0, left_arrow_y),
        (h3_left, left_arrow_y),
        f"{dimensions['wall_clear_x']:.2f} m",
        (h3_left / 2, left_arrow_y - 0.13),
        fontsize=7.8,
    )
    draw_extension_line(ax, [h3_left, h3_left], [left_arrow_y, h3_y])

    h6_right = h6_x + HUMAN_RADIUS
    right_arrow_y = h6_y - 0.40
    draw_double_arrow(
        ax,
        (h6_right, right_arrow_y),
        (ROOM_LENGTH, right_arrow_y),
        f"{dimensions['wall_clear_x']:.2f} m",
        ((h6_right + ROOM_LENGTH) / 2, right_arrow_y - 0.13),
        fontsize=7.8,
    )
    draw_extension_line(ax, [h6_right, h6_right], [right_arrow_y, h6_y])

    h3_top = h3_y + HUMAN_RADIUS
    top_arrow_x = h3_x - 0.43
    draw_double_arrow(
        ax,
        (top_arrow_x, h3_top),
        (top_arrow_x, ROOM_WIDTH),
        f"{dimensions['wall_clear_y']:.2f} m",
        (top_arrow_x - 0.14, (h3_top + ROOM_WIDTH) / 2),
        rotation=90,
        fontsize=7.8,
    )
    draw_extension_line(ax, [top_arrow_x, h3_x], [h3_top, h3_top])

    h1_bottom = h1_y - HUMAN_RADIUS
    bottom_arrow_x = h1_x - 0.43
    draw_double_arrow(
        ax,
        (bottom_arrow_x, 0),
        (bottom_arrow_x, h1_bottom),
        f"{dimensions['wall_clear_y']:.2f} m",
        (bottom_arrow_x - 0.14, h1_bottom / 2),
        rotation=90,
        fontsize=7.8,
    )
    draw_extension_line(ax, [bottom_arrow_x, h1_x], [h1_bottom, h1_bottom])

    left_column_right_edge = h3_x + HUMAN_RADIUS
    right_column_left_edge = h6_x - HUMAN_RADIUS
    arrow_y = h3_y + HUMAN_RADIUS + 0.26
    draw_double_arrow(
        ax,
        (left_column_right_edge, arrow_y),
        (right_column_left_edge, arrow_y),
        f"{dimensions['between_columns']:.2f} m",
        ((left_column_right_edge + right_column_left_edge) / 2, arrow_y + 0.12),
        fontsize=7.8,
    )
    draw_extension_line(
        ax,
        [left_column_right_edge, left_column_right_edge],
        [h3_y, arrow_y],
    )
    draw_extension_line(
        ax,
        [right_column_left_edge, right_column_left_edge],
        [h6_y, arrow_y],
    )


def draw_pattern_2_dimensions(ax, positions, dimensions):
    """Pattern 2 dimensions, with most dimensions referenced to the H4 row."""
    h1_x, h1_y = positions["H1"]
    h2_x, h2_y = positions["H2"]
    h4_x, h4_y = positions["H4"]
    h5_x, h5_y = positions["H5"]
    h6_x, h6_y = positions["H6"]

    h4_right = h4_x + HUMAN_RADIUS
    h5_left = h5_x - HUMAN_RADIUS
    adjacent_arrow_y = h4_y + 0.36
    draw_double_arrow(
        ax,
        (h4_right, adjacent_arrow_y),
        (h5_left, adjacent_arrow_y),
        f"{dimensions['adjacent_clear']:.2f} m",
        ((h4_right + h5_left) / 2, adjacent_arrow_y + 0.13),
        fontsize=7.8,
    )
    draw_extension_line(ax, [h4_right, h4_right], [h4_y, adjacent_arrow_y])
    draw_extension_line(ax, [h5_left, h5_left], [h5_y, adjacent_arrow_y])

    h4_left = h4_x - HUMAN_RADIUS
    left_arrow_y = h4_y - 0.35
    draw_double_arrow(
        ax,
        (0, left_arrow_y),
        (h4_left, left_arrow_y),
        f"{dimensions['wall_clear_x']:.2f} m",
        (h4_left / 2, left_arrow_y - 0.13),
        fontsize=7.8,
    )
    draw_extension_line(ax, [h4_left, h4_left], [left_arrow_y, h4_y])

    h6_right = h6_x + HUMAN_RADIUS
    right_arrow_y = h6_y - 0.35
    draw_double_arrow(
        ax,
        (h6_right, right_arrow_y),
        (ROOM_LENGTH, right_arrow_y),
        f"{dimensions['wall_clear_x']:.2f} m",
        ((h6_right + ROOM_LENGTH) / 2, right_arrow_y - 0.13),
        fontsize=7.8,
    )
    draw_extension_line(ax, [h6_right, h6_right], [right_arrow_y, h6_y])

    bottom_row_top = h1_y + HUMAN_RADIUS
    top_row_bottom = h4_y - HUMAN_RADIUS
    row_arrow_x = h4_x - 0.43
    draw_double_arrow(
        ax,
        (row_arrow_x, bottom_row_top),
        (row_arrow_x, top_row_bottom),
        f"{dimensions['between_rows']:.2f} m",
        (row_arrow_x - 0.17, (bottom_row_top + top_row_bottom) / 2),
        rotation=90,
        fontsize=7.8,
    )
    draw_extension_line(ax, [row_arrow_x, h1_x], [bottom_row_top, bottom_row_top])
    draw_extension_line(ax, [row_arrow_x, h4_x], [top_row_bottom, top_row_bottom])

    h2_bottom = h2_y - HUMAN_RADIUS
    main_door_arrow_x = h2_x + 0.43
    draw_double_arrow(
        ax,
        (main_door_arrow_x, 0),
        (main_door_arrow_x, h2_bottom),
        f"{dimensions['wall_clear_y']:.2f} m",
        (main_door_arrow_x + 0.16, h2_bottom / 2),
        rotation=90,
        fontsize=7.8,
    )
    draw_extension_line(ax, [h2_x, main_door_arrow_x], [h2_bottom, h2_bottom])

    h6_top = h6_y + HUMAN_RADIUS
    opposite_arrow_x = h6_x + 0.43
    draw_double_arrow(
        ax,
        (opposite_arrow_x, h6_top),
        (opposite_arrow_x, ROOM_WIDTH),
        f"{dimensions['wall_clear_y']:.2f} m",
        (opposite_arrow_x + 0.16, (h6_top + ROOM_WIDTH) / 2),
        rotation=90,
        fontsize=7.8,
    )
    draw_extension_line(ax, [h6_x, opposite_arrow_x], [h6_top, h6_top])



def create_occupancy_figure(pattern_name: str):
    """Create a moderately sized occupancy figure for display inside Streamlit.

    Pattern 1 and Pattern 2 include six human heat loads. Null Pattern shows
    the room, split-system supply units and exhaust only, without occupants.
    """
    if pattern_name == "Pattern 1":
        positions, dimensions = get_pattern_1_positions()
        dimension_function = draw_pattern_1_dimensions
        show_occupants = True
    elif pattern_name == "Pattern 2":
        positions, dimensions = get_pattern_2_positions()
        dimension_function = draw_pattern_2_dimensions
        show_occupants = True
    elif pattern_name == "Null Pattern":
        positions, dimensions = {}, {}
        dimension_function = None
        show_occupants = False
    else:
        raise ValueError(f"Unknown occupancy pattern: {pattern_name}")

    fig, ax = plt.subplots(figsize=(10.4, 6.5))
    fig.patch.set_facecolor("white")

    ax.set_xlim(-0.72, ROOM_LENGTH + 0.52)
    ax.set_ylim(-0.76, ROOM_WIDTH + 0.53)
    ax.set_aspect("equal")
    ax.set_xlabel("Room length (m)", fontsize=10)
    ax.set_ylabel("Room width (m)", fontsize=10)
    ax.set_title(pattern_name, fontsize=14, pad=13, fontweight="bold")
    ax.tick_params(axis="both", labelsize=9)

    draw_ceiling_grid(ax)
    draw_room_boundary(ax)
    if show_occupants:
        draw_occupants(ax, positions)
    draw_ventilation_units(ax)
    draw_room_labels(ax)
    draw_external_room_dimensions(ax)
    if dimension_function is not None:
        dimension_function(ax, positions, dimensions)

    ax.text(
        ROOM_LENGTH / 2,
        ROOM_WIDTH + 0.34,
        f"Room: {ROOM_LENGTH:.1f} m × {ROOM_WIDTH:.1f} m × {ROOM_HEIGHT:.1f} m",
        ha="center",
        va="bottom",
        fontsize=9,
    )
    ax.grid(False)

    legend_items = []
    if show_occupants:
        legend_items.append(
            Line2D(
                [0], [0], marker="o", color="none",
                markerfacecolor=HUMAN_COLOUR, markeredgecolor="black",
                markersize=9,
                label=f"H1–H6: Human heat loads ({HUMAN_HEAT_LOAD} W each)",
            )
        )
    legend_items.extend(
        [
            Line2D(
                [0], [0], marker="s", color="none",
                markerfacecolor=SUPPLY_COLOUR, markeredgecolor="black",
                markersize=9, label="S1 and S2: Supply units",
            ),
            Line2D(
                [0], [0], marker="s", color="none",
                markerfacecolor=EXHAUST_COLOUR, markeredgecolor="black",
                markersize=9, label="E1: Exhaust unit",
            ),
            Line2D(
                [0], [0], color=CEILING_GRID_COLOUR,
                linewidth=2, label="Ceiling grid: 0.60 m × 0.60 m",
            ),
        ]
    )

    fig.legend(
        handles=legend_items,
        title="Layout Labels",
        loc="lower center",
        bbox_to_anchor=(0.5, 0.015),
        ncol=2,
        frameon=True,
        fontsize=9,
        title_fontsize=10,
    )
    fig.tight_layout(rect=[0.02, 0.13, 0.98, 0.95])
    return fig, positions, dimensions



def create_measurement_locations_figure(pattern_name: str):
    """Create a second figure showing the 12 measurement locations."""
    if pattern_name == "Pattern 1":
        positions, dimensions = get_pattern_1_positions()
        dimension_function = draw_pattern_1_dimensions
        show_occupants = True
    elif pattern_name == "Pattern 2":
        positions, dimensions = get_pattern_2_positions()
        dimension_function = draw_pattern_2_dimensions
        show_occupants = True
    elif pattern_name == "Null Pattern":
        positions, dimensions = {}, {}
        dimension_function = None
        show_occupants = False
    else:
        raise ValueError(f"Unknown occupancy pattern: {pattern_name}")

    fig, ax = plt.subplots(figsize=(10.4, 6.5))
    fig.patch.set_facecolor("white")

    ax.set_xlim(-0.72, ROOM_LENGTH + 0.52)
    ax.set_ylim(-0.76, ROOM_WIDTH + 0.53)
    ax.set_aspect("equal")
    ax.set_xlabel("Room length (m)", fontsize=10)
    ax.set_ylabel("Room width (m)", fontsize=10)
    ax.set_title(f"{pattern_name} — Measurement Locations", fontsize=14, pad=13, fontweight="bold")
    ax.tick_params(axis="both", labelsize=9)

    draw_ceiling_grid(ax)
    draw_room_boundary(ax)
    if show_occupants:
        draw_occupants(ax, positions)
    draw_ventilation_units(ax)
    draw_room_labels(ax)
    draw_external_room_dimensions(ax)
    if dimension_function is not None:
        dimension_function(ax, positions, dimensions)
    draw_measurement_locations(ax)

    ax.text(
        ROOM_LENGTH / 2,
        ROOM_WIDTH + 0.34,
        "Measurement numbering starts at top-right near the split system and follows a snake path downward",
        ha="center",
        va="bottom",
        fontsize=8.6,
    )
    ax.grid(False)

    legend_items = []
    if show_occupants:
        legend_items.append(
            Line2D(
                [0], [0], marker="o", color="none",
                markerfacecolor=HUMAN_COLOUR, markeredgecolor="black",
                markersize=9,
                label=f"H1–H6: Human heat loads ({HUMAN_HEAT_LOAD} W each)",
            )
        )
    legend_items.extend(
        [
            Line2D(
                [0], [0], marker="s", color="none",
                markerfacecolor=SUPPLY_COLOUR, markeredgecolor="black",
                markersize=9, label="S1 and S2: Supply units",
            ),
            Line2D(
                [0], [0], marker="s", color="none",
                markerfacecolor=EXHAUST_COLOUR, markeredgecolor="black",
                markersize=9, label="E1: Exhaust unit",
            ),
            Line2D(
                [0], [0], marker="D", color="none",
                markerfacecolor=MEASUREMENT_COLOUR, markeredgecolor="white",
                markersize=8, label="uploaded locations: Measurement locations",
            ),
        ]
    )

    fig.legend(
        handles=legend_items,
        title="Layout Labels",
        loc="lower center",
        bbox_to_anchor=(0.5, 0.015),
        ncol=2,
        frameon=True,
        fontsize=9,
        title_fontsize=10,
    )
    fig.tight_layout(rect=[0.02, 0.13, 0.98, 0.95])
    return fig


def figure_to_png(fig) -> bytes:
    """Convert a Matplotlib figure to downloadable PNG bytes."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    buffer.seek(0)
    return buffer.getvalue()


# =========================================================
# OCCUPANCY PAGE
# =========================================================
def reset_occupancy_workflow() -> None:
    """Clear the preview and every downstream result after a pattern change."""
    st.session_state.occupancy_preview_pattern = None
    st.session_state.confirmed_occupancy_pattern = None
    st.session_state.confirmed_measurement_delta_t = False
    st.session_state.confirmed_richardson = False
    st.session_state.confirmed_wells_riley = False
    st.session_state.pop("measurement_delta_t_result", None)
    st.session_state.pop("ri_result", None)
    st.session_state.pop("wr_result", None)







def occupancy_page() -> None:
    render_page_heading(
        "👥",
        "Occupancy Patterns",
        "Choose a symmetry pattern, preview its layout, and confirm it before continuing.",
    )

    st.session_state.setdefault("occupancy_pattern", "Pattern 1")
    st.session_state.setdefault("occupancy_preview_pattern", None)
    st.session_state.setdefault("confirmed_occupancy_pattern", None)
    st.session_state.setdefault("confirmed_measurement_delta_t", False)
    st.session_state.setdefault("confirmed_richardson", False)
    st.session_state.setdefault("confirmed_wells_riley", False)

    st.markdown("### Symmetry Pattern")

    selection_left, selection_centre, selection_right = st.columns([1, 2.2, 1])

    with selection_centre:
        selected_pattern = st.radio(
            "Choose a pattern",
            options=["Pattern 1", "Pattern 2", "Null Pattern"],
            key="occupancy_pattern",
            horizontal=True,
            on_change=reset_occupancy_workflow,
        )

        if st.button(
            "Confirm selection and show figure",
            key="preview_selected_pattern",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.occupancy_preview_pattern = selected_pattern
            st.session_state.confirmed_occupancy_pattern = None
            st.session_state.confirmed_measurement_delta_t = False
            st.session_state.confirmed_richardson = False
            st.session_state.confirmed_wells_riley = False
            st.session_state.pop("measurement_delta_t_result", None)
            st.session_state.pop("ri_result", None)
            st.session_state.pop("wr_result", None)
            st.rerun()

    preview_pattern = st.session_state.get("occupancy_preview_pattern")

    if preview_pattern != selected_pattern:
        st.info("Select Pattern 1, Pattern 2 or Null Pattern, then confirm the selection to display its figure.")
        return

    st.markdown("---")
    st.markdown(f"### {preview_pattern}")

    figure_left, figure_centre, figure_right = st.columns([0.80, 4.10, 0.80])

    with figure_centre:
        fig, positions, dimensions = create_occupancy_figure(preview_pattern)
        png_data = figure_to_png(fig)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    if preview_pattern == "Null Pattern":
        occupant_count = 0
        heat_per_occupant = 0
        total_occupant_load = 0
    else:
        occupant_count = 6
        heat_per_occupant = HUMAN_HEAT_LOAD
        total_occupant_load = occupant_count * heat_per_occupant

    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Occupants", f"{occupant_count}")
    metric2.metric("Heat per occupant", f"{heat_per_occupant} W")
    metric3.metric("Total occupant load", f"{total_occupant_load} W")
    metric4.metric("Room volume", "63.50 m³")

    if preview_pattern == "Null Pattern":
        st.info("Null Pattern contains no human heat loads. Only S1, S2 and E1 are shown in the room layout.")

    st.markdown("### Measurement locations")
    measure_left, measure_centre, measure_right = st.columns([0.80, 4.10, 0.80])
    with measure_centre:
        measurement_fig = create_measurement_locations_figure(preview_pattern)
        measurement_png_data = figure_to_png(measurement_fig)
        st.pyplot(measurement_fig, use_container_width=True)
        plt.close(measurement_fig)

    st.caption(
        "Measurement grid numbering: M1 starts at the top-right location near the split system, "
        "then M1–M4 move right-to-left across the top row, M5–M8 move left-to-right across the middle row, "
        "and M9–M12 move right-to-left across the bottom row."
    )

    action_left, action_centre, action_right = st.columns([1, 2.2, 1])

    with action_centre:
        st.download_button(
            label=f"⬇ Download {preview_pattern} figure",
            data=png_data,
            file_name=f"atlice_{preview_pattern.lower().replace(' ', '_')}.png",
            mime="image/png",
            key=f"download_preview_{preview_pattern}",
            use_container_width=True,
        )
        st.download_button(
            label=f"⬇ Download {preview_pattern} measurement-locations figure",
            data=measurement_png_data,
            file_name=f"atlice_{preview_pattern.lower().replace(' ', '_')}_measurement_locations.png",
            mime="image/png",
            key=f"download_measurement_{preview_pattern}",
            use_container_width=True,
        )

        if st.button(
            "Confirm pattern and continue to Measurement ΔT Upload →",
            key="confirm_pattern_and_continue",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.confirmed_occupancy_pattern = preview_pattern
            st.session_state.confirmed_measurement_delta_t = False
            st.session_state.confirmed_richardson = False
            st.session_state.confirmed_wells_riley = False
            st.session_state.pop("measurement_delta_t_result", None)
            st.session_state.pop("ri_result", None)
            st.session_state.pop("wr_result", None)
            st.session_state.current_page = "measurement"
            st.rerun()


# =========================================================
# MEASUREMENT ΔT UPLOAD PAGE
# =========================================================
MEASUREMENT_HEIGHT_START = 0.20
MEASUREMENT_HEIGHT_STEP = 0.10
MEASUREMENT_EXPECTED_HEIGHT_END = 2.40
MEASUREMENT_EXPECTED_COUNT = int(round((MEASUREMENT_EXPECTED_HEIGHT_END - MEASUREMENT_HEIGHT_START) / MEASUREMENT_HEIGHT_STEP)) + 1
RICHARDSON_TOTAL_HEIGHT = 2.70



def read_delta_t_from_excel(uploaded_file) -> dict:
    """Read only the third column of an uploaded Excel file and calculate ΔT.

    The first and second columns are ignored. Non-numeric values in the third
    column, including a header such as Temperature_C, are automatically skipped.
    The retained numeric values are assigned heights beginning at 0.2 m and
    increasing by 0.1 m for each subsequent reading.
    """
    uploaded_file.seek(0)
    dataframe = pd.read_excel(uploaded_file, header=None)

    if dataframe.shape[1] < 3:
        raise ValueError("The uploaded Excel file must contain at least three columns.")

    temperature_values = pd.to_numeric(dataframe.iloc[:, 2], errors="coerce").dropna().reset_index(drop=True)

    if temperature_values.empty:
        raise ValueError("No numeric temperature values were found in the third column.")

    heights = [MEASUREMENT_HEIGHT_START + MEASUREMENT_HEIGHT_STEP * index for index in range(len(temperature_values))]
    profile = [
        {"height": float(height), "temperature": float(temperature)}
        for height, temperature in zip(heights, temperature_values)
    ]

    minimum_temperature = float(temperature_values.min())
    maximum_temperature = float(temperature_values.max())
    mean_temperature = float(temperature_values.mean())
    delta_t = maximum_temperature - minimum_temperature
    number_of_readings = int(temperature_values.shape[0])
    assumed_last_height = MEASUREMENT_HEIGHT_START + MEASUREMENT_HEIGHT_STEP * (number_of_readings - 1)

    return {
        "file_name": uploaded_file.name,
        "minimum_temperature": minimum_temperature,
        "maximum_temperature": maximum_temperature,
        "mean_temperature": mean_temperature,
        "delta_t": delta_t,
        "number_of_readings": number_of_readings,
        "assumed_first_height": MEASUREMENT_HEIGHT_START,
        "assumed_last_height": assumed_last_height,
        "profile": profile,
    }



def get_measurement_delta_t_dataframe(delta_t_result: dict) -> pd.DataFrame:
    """Convert measurement ΔT results into a display table.

    Only uploaded and successfully processed measurement locations are included.
    """
    measurement_locations = get_measurement_locations()
    rows = []

    result_items = sorted(
        delta_t_result.get("results", {}).items(),
        key=lambda item: int(item[0].replace("M", "")),
    )

    for measurement_label, result in result_items:
        x_value, y_value = measurement_locations[measurement_label]

        rows.append(
            {
                "Measurement": measurement_label,
                "x (m)": x_value,
                "y (m)": y_value,
                "File": result["file_name"],
                "Readings": result["number_of_readings"],
                "Min T (°C)": result["minimum_temperature"],
                "Max T (°C)": result["maximum_temperature"],
                "Mean T (°C)": result.get("mean_temperature", float("nan")),
                "ΔT = Max − Min (K or °C)": result["delta_t"],
            }
        )

    return pd.DataFrame(rows)


def get_measurement_profile_dataframe(delta_t_result: dict) -> pd.DataFrame:
    """Return a long-form dataframe containing height-temperature profiles."""
    rows = []
    for measurement_label, result in sorted(
        delta_t_result.get("results", {}).items(),
        key=lambda item: int(item[0].replace("M", "")),
    ):
        for point in result.get("profile", []):
            rows.append(
                {
                    "Measurement": measurement_label,
                    "Height (m)": float(point["height"]),
                    "Temperature (°C)": float(point["temperature"]),
                }
            )
    return pd.DataFrame(rows)


def get_room_average_profile_dataframe(delta_t_result: dict) -> pd.DataFrame:
    """Average temperature across uploaded locations at each measured height."""
    profile_dataframe = get_measurement_profile_dataframe(delta_t_result)
    if profile_dataframe.empty:
        return pd.DataFrame(columns=["Height (m)", "Average Temperature (°C)"])

    average_dataframe = (
        profile_dataframe.groupby("Height (m)", as_index=False)["Temperature (°C)"]
        .mean()
        .rename(columns={"Temperature (°C)": "Average Temperature (°C)"})
        .sort_values("Height (m)")
    )
    return average_dataframe


def get_room_temperature_statistics(delta_t_result: dict) -> dict:
    """Return global high, low and mean temperature across all uploaded files."""
    profile_dataframe = get_measurement_profile_dataframe(delta_t_result)
    if profile_dataframe.empty:
        return {"highest_temperature": float("nan"), "lowest_temperature": float("nan"), "room_mean_temperature": float("nan")}

    return {
        "highest_temperature": float(profile_dataframe["Temperature (°C)"].max()),
        "lowest_temperature": float(profile_dataframe["Temperature (°C)"].min()),
        "room_mean_temperature": float(profile_dataframe["Temperature (°C)"].mean()),
    }


def draw_measurement_delta_t_locations(ax, delta_t_result: dict):
    """Draw measurement markers labelled as M# (ΔT value) for uploaded files."""
    measurement_locations = get_measurement_locations()
    results = delta_t_result.get("results", {})

    for label, (x_value, y_value) in measurement_locations.items():
        has_result = label in results
        marker_size = 72 if has_result else 46
        marker_alpha = 0.95 if has_result else 0.35
        ax.scatter(
            x_value,
            y_value,
            s=marker_size,
            marker="D",
            facecolor=MEASUREMENT_COLOUR,
            edgecolor="white",
            linewidth=0.9,
            alpha=marker_alpha,
            zorder=6,
        )

        if has_result:
            delta_text = f"{results[label]['delta_t']:.2f}"
            text_label = f"{label} ({delta_text})"
        else:
            text_label = label

        ax.text(
            x_value + 0.08,
            y_value + 0.08,
            text_label,
            fontsize=7.5,
            color=MEASUREMENT_COLOUR,
            fontweight="normal",
            zorder=7,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.76, pad=0.5),
        )


def create_measurement_delta_t_map_figure(pattern_name: str, delta_t_result: dict):
    """Create room measurement-location map with ΔT shown in brackets."""
    if pattern_name == "Pattern 1":
        positions, dimensions = get_pattern_1_positions()
        dimension_function = draw_pattern_1_dimensions
        show_occupants = True
    elif pattern_name == "Pattern 2":
        positions, dimensions = get_pattern_2_positions()
        dimension_function = draw_pattern_2_dimensions
        show_occupants = True
    elif pattern_name == "Null Pattern":
        positions, dimensions = {}, {}
        dimension_function = None
        show_occupants = False
    else:
        raise ValueError(f"Unknown occupancy pattern: {pattern_name}")

    fig, ax = plt.subplots(figsize=(10.4, 6.5))
    fig.patch.set_facecolor("white")
    ax.set_xlim(-0.72, ROOM_LENGTH + 0.52)
    ax.set_ylim(-0.76, ROOM_WIDTH + 0.53)
    ax.set_aspect("equal")
    ax.set_xlabel("Room length (m)", fontsize=10)
    ax.set_ylabel("Room width (m)", fontsize=10)
    ax.set_title(f"{pattern_name} — Measurement ΔT Map", fontsize=14, pad=13, fontweight="bold")
    ax.tick_params(axis="both", labelsize=9)

    draw_ceiling_grid(ax)
    draw_room_boundary(ax)
    if show_occupants:
        draw_occupants(ax, positions)
    draw_ventilation_units(ax)
    draw_room_labels(ax)
    draw_external_room_dimensions(ax)
    if dimension_function is not None:
        dimension_function(ax, positions, dimensions)
    draw_measurement_delta_t_locations(ax, delta_t_result)

    ax.text(
        ROOM_LENGTH / 2,
        ROOM_WIDTH + 0.34,
        "Uploaded locations are labelled as M# (ΔT). Non-uploaded locations are shown faintly.",
        ha="center",
        va="bottom",
        fontsize=8.6,
    )
    ax.grid(False)
    fig.tight_layout(rect=[0.02, 0.05, 0.98, 0.95])
    return fig


def create_temperature_profile_figure(measurement_label: str, result: dict):
    """Create a height-temperature plot for one measurement location."""
    profile_dataframe = pd.DataFrame(result.get("profile", []))
    if profile_dataframe.empty:
        raise ValueError(f"No profile data found for {measurement_label}.")

    fig, ax = plt.subplots(figsize=(6.8, 6.0))
    ax.plot(profile_dataframe["temperature"], profile_dataframe["height"], marker="o", linewidth=1.8)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Height (m)")
    ax.set_title(f"{measurement_label} height vs temperature")
    ax.grid(True, alpha=0.28)

    annotation = (
        f"ΔT = {result['delta_t']:.3f} K\n"
        f"Min T = {result['minimum_temperature']:.3f} °C\n"
        f"Max T = {result['maximum_temperature']:.3f} °C\n"
        f"Mean T = {result.get('mean_temperature', float('nan')):.3f} °C"
    )
    ax.text(
        0.03,
        0.97,
        annotation,
        transform=ax.transAxes,
        ha="left",
        va="top",
        bbox=dict(facecolor="white", edgecolor="#dbe7e4", alpha=0.90, boxstyle="round,pad=0.4"),
    )
    fig.tight_layout()
    return fig


def create_room_average_profile_figure(delta_t_result: dict):
    """Create room-average height-temperature plot."""
    average_dataframe = get_room_average_profile_dataframe(delta_t_result)
    if average_dataframe.empty:
        raise ValueError("No profile data available to build room-average plot.")

    fig, ax = plt.subplots(figsize=(6.8, 6.0))
    ax.plot(average_dataframe["Average Temperature (°C)"], average_dataframe["Height (m)"], marker="o", linewidth=2.2)
    ax.set_xlabel("Room average temperature (°C)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Room average height vs temperature")
    ax.grid(True, alpha=0.28)
    fig.tight_layout()
    return fig


def create_combined_profiles_figure(delta_t_result: dict):
    """Create one comparison plot with every uploaded location and the room-average profile."""
    profile_dataframe = get_measurement_profile_dataframe(delta_t_result)
    average_dataframe = get_room_average_profile_dataframe(delta_t_result)

    if profile_dataframe.empty:
        raise ValueError("No profile data available to build comparison plot.")

    fig, ax = plt.subplots(figsize=(8.2, 6.2))

    for measurement_label, group in profile_dataframe.groupby("Measurement"):
        group = group.sort_values("Height (m)")
        ax.plot(
            group["Temperature (°C)"],
            group["Height (m)"],
            marker="o",
            linewidth=1.1,
            alpha=0.65,
            label=measurement_label,
        )

    if not average_dataframe.empty:
        ax.plot(
            average_dataframe["Average Temperature (°C)"],
            average_dataframe["Height (m)"],
            marker="s",
            linewidth=2.8,
            color="black",
            label="Room average",
        )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Height (m)")
    ax.set_title("All uploaded locations with room-average profile")
    ax.grid(True, alpha=0.28)
    ax.legend(loc="best", fontsize=8, ncol=2)
    fig.tight_layout()
    return fig



def measurement_delta_t_page() -> None:
    render_page_heading(
        "📊",
        "Measurement ΔT Upload",
        "Upload Excel files for any measurement locations and calculate ΔT from the third column only.",
    )

    confirmed_pattern = st.session_state.get("confirmed_occupancy_pattern")

    if not confirmed_pattern:
        st.warning(
            "No occupancy pattern has been confirmed. Select and confirm a "
            "Symmetry Pattern before uploading measurement files."
        )
        if st.button("Go to Occupancy Patterns", key="measurement_go_to_occupancy", type="primary"):
            go_to("occupancy")
        return

    st.session_state.setdefault("confirmed_measurement_delta_t", False)

    st.markdown(
        f"""
        <div class="result-banner">
            <b>Step 2 of 5</b><br>
            Confirmed occupancy: Symmetry Pattern — <b>{confirmed_pattern}</b><br>
            Upload Excel files for any available locations uploaded locations. The app reads only
            column 3 and calculates ΔT = maximum temperature − minimum temperature.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Measurement-location reference")
    measurement_left, measurement_centre, measurement_right = st.columns([0.80, 4.10, 0.80])
    with measurement_centre:
        measurement_fig = create_measurement_locations_figure(confirmed_pattern)
        st.pyplot(measurement_fig, use_container_width=True)
        plt.close(measurement_fig)

    st.caption(
        "Height assumption for each uploaded file: first numeric reading in the third column is at 0.2 m, "
        "then 0.3 m, 0.4 m, and so on. Expected final reading is at 2.4 m. "
        "The Richardson characteristic height is kept as 2.7 m by default. "
        "You may upload only the locations you have; all 12 files are not mandatory."
    )

    st.markdown("### Upload available Excel files")
    st.info(
        "Upload one file per available measurement location. The first and second columns are ignored. "
        "Only the third column is used for the temperature range and profile plots."
    )

    uploaded_files = {}
    upload_columns = st.columns(3)

    for index in range(1, 13):
        measurement_label = f"M{index}"
        with upload_columns[(index - 1) % 3]:
            uploaded_files[measurement_label] = st.file_uploader(
                f"{measurement_label} Excel file",
                type=["xlsx", "xls"],
                key=f"upload_{measurement_label.lower()}_excel",
            )

    calculate_left, calculate_centre, calculate_right = st.columns([1, 2.4, 1])
    with calculate_centre:
        calculate_delta_t = st.button(
            "Calculate ΔT for uploaded files",
            key="calculate_measurement_delta_t",
            type="primary",
            use_container_width=True,
        )

    if calculate_delta_t:
        uploaded_only = {
            measurement_label: uploaded_file
            for measurement_label, uploaded_file in uploaded_files.items()
            if uploaded_file is not None
        }

        if not uploaded_only:
            st.error("Please upload at least one Excel file before calculating ΔT.")
        else:
            results = {}
            errors = []

            for measurement_label, uploaded_file in uploaded_only.items():
                try:
                    results[measurement_label] = read_delta_t_from_excel(uploaded_file)
                except Exception as error:
                    errors.append(f"{measurement_label}: {error}")

            if errors:
                st.session_state.confirmed_measurement_delta_t = False
                st.session_state.pop("measurement_delta_t_result", None)
                for error in errors:
                    st.error(error)
            else:
                st.session_state.measurement_delta_t_result = {
                    "pattern_name": confirmed_pattern,
                    "height_start": MEASUREMENT_HEIGHT_START,
                    "height_step": MEASUREMENT_HEIGHT_STEP,
                    "expected_height_end": MEASUREMENT_EXPECTED_HEIGHT_END,
                    "expected_count": MEASUREMENT_EXPECTED_COUNT,
                    "richardson_total_height": RICHARDSON_TOTAL_HEIGHT,
                    "results": results,
                }
                st.session_state.confirmed_measurement_delta_t = False
                st.session_state.confirmed_richardson = False
                st.session_state.confirmed_wells_riley = False
                st.session_state.pop("ri_result", None)
                st.session_state.pop("wr_result", None)
                st.success(
                    f"ΔT values calculated for {len(results)} uploaded location(s). "
                    "Review the table and plots below, then confirm to continue."
                )

    delta_t_result = st.session_state.get("measurement_delta_t_result")

    if delta_t_result:
        st.markdown("---")
        st.markdown("## Calculated ΔT values")

        result_dataframe = get_measurement_delta_t_dataframe(delta_t_result)
        display_dataframe = result_dataframe.copy()
        for column_name in [
            "x (m)",
            "y (m)",
            "Min T (°C)",
            "Max T (°C)",
            "Mean T (°C)",
            "ΔT = Max − Min (K or °C)",
        ]:
            display_dataframe[column_name] = display_dataframe[column_name].map(lambda value: f"{value:.4f}")

        st.dataframe(display_dataframe, use_container_width=True, hide_index=True)

        processed_count = len(result_dataframe)
        average_delta_t = result_dataframe["ΔT = Max − Min (K or °C)"].mean()
        maximum_delta_t = result_dataframe["ΔT = Max − Min (K or °C)"].max()
        minimum_delta_t = result_dataframe["ΔT = Max − Min (K or °C)"].min()
        room_stats = get_room_temperature_statistics(delta_t_result)

        metric1, metric2, metric3, metric4 = st.columns(4)
        metric1.metric("Files processed", f"{processed_count}")
        metric2.metric("Average ΔT", f"{average_delta_t:.3f} K")
        metric3.metric("Minimum ΔT", f"{minimum_delta_t:.3f} K")
        metric4.metric("Maximum ΔT", f"{maximum_delta_t:.3f} K")

        stat1, stat2, stat3 = st.columns(3)
        stat1.metric("Higher-end T", f"{room_stats['highest_temperature']:.3f} °C")
        stat2.metric("Lower-end T", f"{room_stats['lowest_temperature']:.3f} °C")
        stat3.metric("Room mean T", f"{room_stats['room_mean_temperature']:.3f} °C")

        unexpected_counts = result_dataframe[result_dataframe["Readings"] != MEASUREMENT_EXPECTED_COUNT]
        if not unexpected_counts.empty:
            st.warning(
                f"Expected {MEASUREMENT_EXPECTED_COUNT} numeric readings per file for 0.2 m to 2.4 m at 0.1 m spacing. "
                "Some uploaded files have a different count. ΔT and plots are still calculated using all numeric values in the third column."
            )

        st.markdown("### Plots after ΔT")
        plot_mode = st.radio(
            "Choose plot option",
            options=[
                "ΔT map",
                "Individual height vs temperature plot",
                "Compare plots",
            ],
            horizontal=True,
            key="measurement_plot_mode",
        )

        if plot_mode == "ΔT map":
            st.caption("Each uploaded location is marked as M# (ΔT). Locations without uploaded files are shown faintly.")
            delta_map_fig = create_measurement_delta_t_map_figure(confirmed_pattern, delta_t_result)
            st.pyplot(delta_map_fig, use_container_width=True)
            delta_map_png = figure_to_png(delta_map_fig)
            plt.close(delta_map_fig)
            st.download_button(
                label="⬇ Download ΔT map",
                data=delta_map_png,
                file_name="atlice_measurement_delta_t_map.png",
                mime="image/png",
                key="download_delta_t_map",
                use_container_width=True,
            )

        elif plot_mode == "Individual height vs temperature plot":
            uploaded_labels = sorted(
                delta_t_result["results"].keys(),
                key=lambda label: int(label.replace("M", "")),
            )
            selected_label = st.selectbox(
                "Select measurement location",
                options=uploaded_labels,
                key="selected_individual_measurement_plot",
            )
            selected_result = delta_t_result["results"][selected_label]
            profile_fig = create_temperature_profile_figure(selected_label, selected_result)
            st.pyplot(profile_fig, use_container_width=True)
            profile_png = figure_to_png(profile_fig)
            plt.close(profile_fig)
            st.download_button(
                label=f"⬇ Download {selected_label} height-temperature plot",
                data=profile_png,
                file_name=f"atlice_{selected_label.lower()}_height_temperature_plot.png",
                mime="image/png",
                key=f"download_{selected_label.lower()}_profile_plot",
                use_container_width=True,
            )

        else:
            compare_col1, compare_col2 = st.columns(2, gap="large")
            with compare_col1:
                st.markdown("#### Room average height vs temperature")
                average_fig = create_room_average_profile_figure(delta_t_result)
                st.pyplot(average_fig, use_container_width=True)
                average_png = figure_to_png(average_fig)
                plt.close(average_fig)
                st.download_button(
                    label="⬇ Download room-average plot",
                    data=average_png,
                    file_name="atlice_room_average_height_temperature_plot.png",
                    mime="image/png",
                    key="download_room_average_plot",
                    use_container_width=True,
                )

            with compare_col2:
                st.markdown("#### Uploaded locations with room average")
                combined_fig = create_combined_profiles_figure(delta_t_result)
                st.pyplot(combined_fig, use_container_width=True)
                combined_png = figure_to_png(combined_fig)
                plt.close(combined_fig)
                st.download_button(
                    label="⬇ Download comparison plot",
                    data=combined_png,
                    file_name="atlice_all_locations_with_room_average_plot.png",
                    mime="image/png",
                    key="download_combined_profile_plot",
                    use_container_width=True,
                )

            st.markdown(
                f"""
                <div class="result-banner">
                    <b>Temperature summary from uploaded locations</b><br>
                    Higher-end T: <b>{room_stats['highest_temperature']:.3f} °C</b> &nbsp; | &nbsp;
                    Lower-end T: <b>{room_stats['lowest_temperature']:.3f} °C</b> &nbsp; | &nbsp;
                    Room mean T: <b>{room_stats['room_mean_temperature']:.3f} °C</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        results_text_lines = [
            "ATLiCE — MEASUREMENT DELTA T RESULTS",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "Reading rule: third Excel column only; first and second columns ignored.",
            "Height assumption: first numeric reading = 0.2 m; subsequent readings increase by 0.1 m; expected final height = 2.4 m.",
            f"Richardson characteristic height used later: {RICHARDSON_TOTAL_HEIGHT:.2f} m.",
            f"Processed locations: {processed_count}",
            f"Higher-end T: {room_stats['highest_temperature']:.6f} °C",
            f"Lower-end T: {room_stats['lowest_temperature']:.6f} °C",
            f"Room mean T: {room_stats['room_mean_temperature']:.6f} °C",
            "",
            "Measurement, x (m), y (m), File, Readings, Min T (°C), Max T (°C), Mean T (°C), ΔT (K or °C)",
        ]

        for _, row in result_dataframe.iterrows():
            results_text_lines.append(
                f"{row['Measurement']}, {row['x (m)']:.2f}, {row['y (m)']:.2f}, {row['File']}, "
                f"{int(row['Readings'])}, {row['Min T (°C)']:.6f}, {row['Max T (°C)']:.6f}, "
                f"{row['Mean T (°C)']:.6f}, {row['ΔT = Max − Min (K or °C)']:.6f}"
            )

        results_text = "\n".join(results_text_lines) + "\n"

        action_left, action_centre, action_right = st.columns([1, 2.4, 1])
        with action_centre:
            download_text_button(
                results_text,
                "atlice_measurement_delta_t_results.txt",
                "download_measurement_delta_t",
            )

            if not st.session_state.get("confirmed_measurement_delta_t"):
                if st.button(
                    "Confirm ΔT values and continue to Richardson →",
                    key="confirm_delta_t_continue",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.confirmed_measurement_delta_t = True
                    st.session_state.confirmed_richardson = False
                    st.session_state.confirmed_wells_riley = False
                    st.session_state.current_page = "ri"
                    st.rerun()
            else:
                st.success("Measurement ΔT values confirmed. The Richardson stage is ready.")
                if st.button(
                    "Open Richardson Number →",
                    key="open_ri_from_measurement",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.current_page = "ri"
                    st.rerun()


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
                value=63.5,
                step=0.5,
                key="ach_room_volume",
            )
            people = row1b.number_input(
                "Number of people",
                min_value=0,
                value=6,
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
                    The default values represent a 63.5 m³ room with six occupants,
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
def classify_richardson_number(ri_value: float) -> tuple[str, str]:
    """Classify one Richardson number value."""
    if ri_value < 0:
        return (
            "Opposing buoyancy direction",
            "The negative sign indicates that buoyancy acts opposite to the selected reference-flow direction.",
        )
    if ri_value < 0.1:
        return (
            "Momentum-dominated flow",
            "Forced-air momentum is likely to dominate over buoyancy for the selected scales.",
        )
    if ri_value <= 1:
        return (
            "Mixed convection",
            "Both buoyancy and forced-air momentum are likely to influence the airflow.",
        )
    return (
        "Buoyancy-dominated flow",
        "Thermal buoyancy is likely to dominate over forced-air momentum for the selected scales.",
    )


def get_richardson_dataframe(ri_result: dict) -> pd.DataFrame:
    """Convert Richardson result rows into a display table."""
    return pd.DataFrame(ri_result["ri_table"])



def richardson_page() -> None:
    render_page_heading(
        "🌡️",
        "Richardson Number",
        "Review the imported ΔT values, edit the common Richardson inputs, calculate, and confirm.",
    )

    confirmed_pattern = st.session_state.get("confirmed_occupancy_pattern")
    delta_t_result = st.session_state.get("measurement_delta_t_result")
    delta_t_confirmed = bool(st.session_state.get("confirmed_measurement_delta_t"))

    if not confirmed_pattern:
        st.warning(
            "No occupancy pattern has been confirmed. Select and confirm a "
            "Symmetry Pattern before opening the Richardson inputs."
        )
        if st.button("Go to Occupancy Patterns", key="ri_go_to_occupancy", type="primary"):
            go_to("occupancy")
        return

    if not delta_t_result or not delta_t_confirmed:
        st.warning(
            "Measurement ΔT values have not been confirmed. Upload at least one Excel file, "
            "calculate ΔT, and confirm the table before opening Richardson inputs."
        )
        if st.button("Go to Measurement ΔT Upload", key="ri_go_to_measurement", type="primary"):
            go_to("measurement")
        return

    measurement_dataframe = get_measurement_delta_t_dataframe(delta_t_result)
    processed_count = len(measurement_dataframe)

    st.markdown(
        f"""
        <div class="result-banner">
            <b>Step 3 of 5</b><br>
            Confirmed occupancy: Symmetry Pattern — <b>{confirmed_pattern}</b><br>
            Confirmed measurement ΔT values: <b>{processed_count} uploaded location(s)</b>. Characteristic height default:
            <b>{RICHARDSON_TOTAL_HEIGHT:.2f} m</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Confirmed ΔT values from uploaded Excel files")
    delta_display = measurement_dataframe[
        ["Measurement", "x (m)", "y (m)", "Min T (°C)", "Max T (°C)", "Mean T (°C)", "ΔT = Max − Min (K or °C)"]
    ].copy()

    for column_name in ["x (m)", "y (m)", "Min T (°C)", "Max T (°C)", "Mean T (°C)", "ΔT = Max − Min (K or °C)"]:
        delta_display[column_name] = delta_display[column_name].map(lambda value: f"{value:.4f}")

    st.dataframe(delta_display, use_container_width=True, hide_index=True)

    input_col, guide_col = st.columns([1.45, 1], gap="large")

    with input_col:
        with st.form("ri_form"):
            st.markdown("### Editable common Richardson inputs")
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
            length_scale = row2a.number_input(
                "Characteristic height / length, L (m)",
                min_value=0.001,
                value=RICHARDSON_TOTAL_HEIGHT,
                step=0.1,
                key="ri_length",
                help="Default is the total room height of 2.7 m.",
            )
            air_velocity = row2b.number_input(
                "Representative air velocity, V (m/s)",
                min_value=0.001,
                value=0.10,
                step=0.01,
                format="%.3f",
                key="ri_velocity",
            )

            calculate = st.form_submit_button(
                "Calculate Richardson Number for uploaded locations",
                type="primary",
                use_container_width=True,
            )

    with guide_col:
        st.markdown(
            """
            <div class="section-card">
                <h3>Equation used for each measurement location</h3>
                <div class="formula-box"><b>Ri = g α ΔT L / V²</b></div>
                <p class="small-note">
                    The ΔT values are taken from the uploaded Excel files.
                    Gravity, thermal expansion coefficient, characteristic height and
                    velocity are editable common inputs.
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
        st.session_state.confirmed_richardson = False
        st.session_state.confirmed_wells_riley = False
        st.session_state.pop("wr_result", None)

        ri_rows = []
        for _, row in measurement_dataframe.iterrows():
            delta_t = float(row["ΔT = Max − Min (K or °C)"])
            ri_value = gravity * alpha * delta_t * length_scale / (air_velocity**2)
            classification, interpretation = classify_richardson_number(ri_value)

            ri_rows.append(
                {
                    "Measurement": row["Measurement"],
                    "x (m)": float(row["x (m)"]),
                    "y (m)": float(row["y (m)"]),
                    "ΔT (K or °C)": delta_t,
                    "Ri": ri_value,
                    "Classification": classification,
                    "Interpretation": interpretation,
                }
            )

        ri_values = [row["Ri"] for row in ri_rows]
        delta_values = [row["ΔT (K or °C)"] for row in ri_rows]

        maximum_ri_row = max(ri_rows, key=lambda row: row["Ri"])
        minimum_ri_row = min(ri_rows, key=lambda row: row["Ri"])
        average_ri = sum(ri_values) / len(ri_values)
        average_delta_t = sum(delta_values) / len(delta_values)
        summary_classification, summary_interpretation = classify_richardson_number(average_ri)

        st.session_state.ri_result = {
            "gravity": gravity,
            "alpha": alpha,
            "length_scale": length_scale,
            "air_velocity": air_velocity,
            "ri_table": ri_rows,
            "ri_average": average_ri,
            "ri_min": minimum_ri_row["Ri"],
            "ri_max": maximum_ri_row["Ri"],
            "delta_t_average": average_delta_t,
            "delta_t_min": min(delta_values),
            "delta_t_max": max(delta_values),
            "processed_count": len(ri_rows),
            "max_ri_measurement": maximum_ri_row["Measurement"],
            "min_ri_measurement": minimum_ri_row["Measurement"],
            "classification": summary_classification,
            "interpretation": summary_interpretation,
        }

    result = st.session_state.get("ri_result")
    if result:
        st.markdown("---")
        st.markdown("## Richardson result for uploaded locations")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Average Ri", f"{result['ri_average']:.4f}")
        m2.metric("Minimum Ri", f"{result['ri_min']:.4f}", result["min_ri_measurement"])
        m3.metric("Maximum Ri", f"{result['ri_max']:.4f}", result["max_ri_measurement"])
        m4.metric("Average ΔT", f"{result['delta_t_average']:.3f} K")

        st.markdown(
            f"""
            <div class="result-banner">
                <b>Average classification: {result['classification']}</b><br>
                {result['interpretation']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        ri_dataframe = get_richardson_dataframe(result)
        ri_display = ri_dataframe.copy()
        for column_name in ["x (m)", "y (m)", "ΔT (K or °C)", "Ri"]:
            ri_display[column_name] = ri_display[column_name].map(lambda value: f"{value:.5f}")
        st.dataframe(
            ri_display[
                ["Measurement", "x (m)", "y (m)", "ΔT (K or °C)", "Ri", "Classification"]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.latex(r"Ri = \frac{g\alpha\Delta T L}{V^2}")
        st.write(
            f"Common inputs used: **g = {result['gravity']:.2f} m/s²**, "
            f"**α = {result['alpha']:.5f} 1/K**, "
            f"**L = {result['length_scale']:.2f} m**, "
            f"**V = {result['air_velocity']:.3f} m/s**."
        )

        results_text_lines = [
            "ATLiCE — RICHARDSON NUMBER RESULTS",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "COMMON INPUTS",
            f"Gravity: {result['gravity']:.4f} m/s²",
            f"Thermal expansion coefficient: {result['alpha']:.6f} 1/K",
            f"Characteristic height / length: {result['length_scale']:.4f} m",
            f"Air velocity: {result['air_velocity']:.4f} m/s",
            "",
            "SUMMARY",
            f"Processed measurement locations: {result.get('processed_count', len(result['ri_table']))}",
            f"Average ΔT: {result['delta_t_average']:.6f} K or °C",
            f"Average Richardson number: {result['ri_average']:.6f}",
            f"Minimum Richardson number: {result['ri_min']:.6f} at {result['min_ri_measurement']}",
            f"Maximum Richardson number: {result['ri_max']:.6f} at {result['max_ri_measurement']}",
            f"Average classification: {result['classification']}",
            "",
            "Measurement, x (m), y (m), ΔT (K or °C), Ri, Classification",
        ]

        for row in result["ri_table"]:
            results_text_lines.append(
                f"{row['Measurement']}, {row['x (m)']:.2f}, {row['y (m)']:.2f}, "
                f"{row['ΔT (K or °C)']:.6f}, {row['Ri']:.6f}, {row['Classification']}"
            )

        results_text = "\n".join(results_text_lines) + "\n"

        action_left, action_centre, action_right = st.columns([1, 2.4, 1])
        with action_centre:
            download_text_button(
                results_text,
                "atlice_richardson_results.txt",
                "download_ri",
            )
            if st.button(
                "Confirm Richardson result and continue to Wells–Riley →",
                key="confirm_ri_continue",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.confirmed_richardson = True
                st.session_state.confirmed_wells_riley = False
                st.session_state.current_page = "wells_riley"
                st.rerun()


# =========================================================
# WELLS–RILEY PAGE
# =========================================================
def wells_riley_page() -> None:
    render_page_heading(
        "🫁",
        "Wells–Riley Infection Risk",
        "Calculate the ideal and local modelled infection probabilities, then confirm the result.",
    )

    confirmed_pattern = st.session_state.get("confirmed_occupancy_pattern")
    ri_result = st.session_state.get("ri_result")
    ri_confirmed = bool(st.session_state.get("confirmed_richardson"))

    if not confirmed_pattern or not ri_result or not ri_confirmed:
        st.warning(
            "The Richardson result has not been confirmed. Complete and confirm "
            "the Richardson stage before opening Wells–Riley inputs."
        )
        if st.button("Go to Richardson Number", key="wr_go_to_ri", type="primary"):
            go_to("ri")
        return

    st.markdown(
        f"""
        <div class="result-banner">
            <b>Step 4 of 5</b><br>
            Pattern: <b>{confirmed_pattern}</b> &nbsp; | &nbsp;
            Confirmed Richardson results: <b>{ri_result.get('processed_count', len(ri_result['ri_table']))} measurement location(s)</b> &nbsp; | &nbsp;
            Average Ri: <b>{ri_result['ri_average']:.4f}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_col, guide_col = st.columns([1.55, 1], gap="large")

    with input_col:
        with st.form("wr_form"):
            st.markdown("### Input values")
            row1a, row1b = st.columns(2)
            room_airflow = row1a.number_input(
                "Room airflow, Q (m³/h)",
                min_value=0.0,
                value=180.0,
                step=10.0,
                help=(
                    "Default: 180 m³/h, corresponding to six 100 W sensible "
                    "heat sources with 12 °C supply air and a 22 °C room target."
                ),
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
            "Quanta generation rates are scenario-dependent. This is a screening "
            "model and not a clinical prediction."
        )

    if calculate:
        st.session_state.confirmed_wells_riley = False

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
        st.markdown("## Wells–Riley result")
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
                <b>{result['ventilation_effectiveness']:.2f}</b>, the local modelled
                risk is <b>{direction_text}</b> the ideal well-mixed result.
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
            st.latex(
                r"P_{\mathrm{loc}} = 1-\exp\left(-\frac{Iqpt}{\varepsilon_{V,\mathrm{loc}}Q}\right)"
            )

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

        action_left, action_centre, action_right = st.columns([1, 2.4, 1])
        with action_centre:
            download_text_button(
                results_text,
                "atlice_wells_riley_results.txt",
                "download_wr",
            )

            if not st.session_state.get("confirmed_wells_riley"):
                if st.button(
                    "Confirm Wells–Riley result",
                    key="confirm_wells_result",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.confirmed_wells_riley = True
                    st.rerun()
            else:
                st.success("Wells–Riley result confirmed. The complete report is ready.")
                if st.button(
                    "View complete analysis report →",
                    key="open_final_report",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.current_page = "report"
                    st.rerun()


# =========================================================
# COMPLETE REPORT
# =========================================================

def get_pattern_configuration(pattern_name: str) -> dict:
    """Return the selected arrangement and its clear-distance summary."""
    if pattern_name == "Pattern 1":
        return {
            "group": "Symmetry Pattern",
            "arrangement": "Two columns of three occupants",
            "spacing_label": "Clear spacing within each column",
            "spacing_value": "0.70 m",
            "separation_label": "Clear distance between columns",
            "separation_value": "2.60 m",
            "side_clearance": "1.20 m at each side wall",
            "door_clearance": "0.95 m at the Main Door and opposite wall",
        }

    if pattern_name == "Pattern 2":
        return {
            "group": "Symmetry Pattern",
            "arrangement": "Two rows of three occupants",
            "spacing_label": "Clear spacing within each row",
            "spacing_value": "0.70 m",
            "separation_label": "Clear distance between rows",
            "separation_value": "1.80 m",
            "side_clearance": "1.65 m at each side wall",
            "door_clearance": "0.90 m at the Main Door and opposite wall",
        }

    return {
        "group": "Null Pattern",
        "arrangement": "No human loads; supply and exhaust units only",
        "spacing_label": "Occupant spacing",
        "spacing_value": "Not applicable",
        "separation_label": "Occupant separation",
        "separation_value": "Not applicable",
        "side_clearance": "Not applicable because no occupants are present",
        "door_clearance": "Not applicable because no occupants are present",
    }



def get_load_summary(pattern_name=None) -> dict:
    """Calculate the sensible-load airflow used in the study summary.

    Null Pattern contains no human heat loads, so the automatic occupant-load
    airflow summary is zero.
    """
    if pattern_name == "Null Pattern":
        occupants = 0
        heat_per_occupant = 0
    else:
        occupants = 6
        heat_per_occupant = HUMAN_HEAT_LOAD

    total_heat = occupants * heat_per_occupant
    supply_temperature = 12.0
    target_temperature = 22.0
    rho_cp = 1200.0
    delta_t = target_temperature - supply_temperature
    room_volume = ROOM_LENGTH * ROOM_WIDTH * ROOM_HEIGHT

    if total_heat > 0 and delta_t > 0 and rho_cp > 0:
        airflow_m3s = total_heat / (rho_cp * delta_t)
    else:
        airflow_m3s = 0.0

    airflow_ls = airflow_m3s * 1000
    airflow_m3h = airflow_m3s * 3600
    ach = airflow_m3h / room_volume if room_volume > 0 else 0.0

    return {
        "occupants": occupants,
        "heat_per_occupant": heat_per_occupant,
        "total_heat": total_heat,
        "supply_temperature": supply_temperature,
        "target_temperature": target_temperature,
        "rho_cp": rho_cp,
        "delta_t": delta_t,
        "room_volume": room_volume,
        "airflow_m3s": airflow_m3s,
        "airflow_ls": airflow_ls,
        "airflow_m3h": airflow_m3h,
        "ach": ach,
    }


def build_complete_report_text(
    pattern_name: str,
    configuration: dict,
    load: dict,
    measurement_delta_t: dict,
    ri: dict,
    wr: dict,
    measurement_locations: dict,
) -> str:
    measurement_dataframe = get_measurement_delta_t_dataframe(measurement_delta_t)
    ri_dataframe = get_richardson_dataframe(ri)

    measurement_lines = []
    for _, row in measurement_dataframe.iterrows():
        measurement_lines.append(
            f"{row['Measurement']}: x={row['x (m)']:.2f} m, y={row['y (m)']:.2f} m, "
            f"file={row['File']}, readings={int(row['Readings'])}, "
            f"min={row['Min T (°C)']:.4f} °C, max={row['Max T (°C)']:.4f} °C, "
            f"ΔT={row['ΔT = Max − Min (K or °C)']:.4f} K or °C"
        )

    ri_lines = []
    for _, row in ri_dataframe.iterrows():
        ri_lines.append(
            f"{row['Measurement']}: ΔT={row['ΔT (K or °C)']:.4f} K or °C, "
            f"Ri={row['Ri']:.6f}, classification={row['Classification']}"
        )

    return f"""ATLiCE — COMPLETE INDOOR AIR ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

1. ROOM AND OCCUPANCY CONFIGURATION
Pattern group: {configuration['group']}
Selected pattern: {pattern_name}
Arrangement: {configuration['arrangement']}
Room dimensions: {ROOM_LENGTH:.2f} m × {ROOM_WIDTH:.2f} m × {ROOM_HEIGHT:.2f} m
Room volume: {load['room_volume']:.3f} m³
Supply units: S1 and S2, each {UNIT_SIZE:.2f} m × {UNIT_SIZE:.2f} m
Exhaust unit: E1, {UNIT_SIZE:.2f} m × {UNIT_SIZE:.2f} m
{configuration['spacing_label']}: {configuration['spacing_value']}
{configuration['separation_label']}: {configuration['separation_value']}
Side-wall clearance: {configuration['side_clearance']}
Main/opposite-wall clearance: {configuration['door_clearance']}
Measurement grid numbering: M1 starts at the top-right location near the split system; M1-M4 move right-to-left across the top row, M5-M8 move left-to-right across the middle row, and M9-M12 move right-to-left across the bottom row.

2. MEASUREMENT ΔT FROM UPLOADED EXCEL FILES
Reading rule: only the third Excel column was used. The first and second columns were ignored.
Height assumption: first numeric reading = 0.2 m; subsequent readings increase by 0.1 m; expected final height = 2.4 m.
Richardson characteristic height used: {measurement_delta_t['richardson_total_height']:.2f} m.

{chr(10).join(measurement_lines)}

3. SENSIBLE LOAD AND AIRFLOW SUMMARY
Occupants: {load['occupants']}
Heat per occupant: {load['heat_per_occupant']:.0f} W
Total sensible occupant load: {load['total_heat']:.0f} W
Supply-air temperature: {load['supply_temperature']:.1f} °C
Target room temperature: {load['target_temperature']:.1f} °C
Temperature difference: {load['delta_t']:.1f} K
Calculated airflow: {load['airflow_ls']:.2f} L/s
Calculated airflow: {load['airflow_m3h']:.2f} m³/h
Calculated total supply ACH: {load['ach']:.2f} h⁻¹

4. RICHARDSON NUMBER FOR UPLOADED MEASUREMENT LOCATIONS
Gravity: {ri['gravity']:.4f} m/s²
Thermal expansion coefficient: {ri['alpha']:.6f} 1/K
Characteristic height / length: {ri['length_scale']:.4f} m
Air velocity: {ri['air_velocity']:.4f} m/s
Average ΔT: {ri['delta_t_average']:.6f} K or °C
Average Richardson number: {ri['ri_average']:.6f}
Minimum Richardson number: {ri['ri_min']:.6f} at {ri['min_ri_measurement']}
Maximum Richardson number: {ri['ri_max']:.6f} at {ri['max_ri_measurement']}
Average classification: {ri['classification']}
Average interpretation: {ri['interpretation']}

{chr(10).join(ri_lines)}

5. WELLS–RILEY SCREENING RESULT
Room airflow: {wr['room_airflow']:.2f} m³/h
Local ventilation effectiveness: {wr['ventilation_effectiveness']:.4f}
Infectious people: {wr['infected_people']}
Quanta generation rate: {wr['quanta_rate']:.4f} quanta/h
Breathing rate: {wr['breathing_rate']:.4f} m³/h
Exposure time: {wr['exposure_time']:.4f} h
Effective local airflow: {wr['effective_local_airflow']:.4f} m³/h
Ideal well-mixed probability: {wr['p_ideal'] * 100:.4f}%
Local infection probability: {wr['p_local'] * 100:.4f}%
Risk band: {wr['risk_band']}

MODEL LIMITATIONS
The sensible-load result includes occupant heat only. Measurement ΔT is calculated from the uploaded Excel third column only. The Richardson result depends on the selected representative height and velocity. The Wells–Riley result is a steady-state screening estimate and is sensitive to quanta rate and ventilation-effectiveness assumptions.
"""




def build_complete_report_html(
    pattern_name: str,
    configuration: dict,
    load: dict,
    measurement_delta_t: dict,
    ri: dict,
    wr: dict,
    figure_png: bytes,
    measurement_figure_png: bytes,
    measurement_locations: dict,
) -> str:
    encoded_figure = base64.b64encode(figure_png).decode("ascii")
    encoded_measurement_figure = base64.b64encode(measurement_figure_png).decode("ascii")
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    measurement_dataframe = get_measurement_delta_t_dataframe(measurement_delta_t)
    ri_dataframe = get_richardson_dataframe(ri)

    measurement_rows = []
    for _, row in measurement_dataframe.iterrows():
        measurement_rows.append(
            "<tr>"
            f"<td>{html.escape(str(row['Measurement']))}</td>"
            f"<td>{row['x (m)']:.2f}</td>"
            f"<td>{row['y (m)']:.2f}</td>"
            f"<td>{html.escape(str(row['File']))}</td>"
            f"<td>{int(row['Readings'])}</td>"
            f"<td>{row['Min T (°C)']:.3f}</td>"
            f"<td>{row['Max T (°C)']:.3f}</td>"
            f"<td>{row['ΔT = Max − Min (K or °C)']:.3f}</td>"
            "</tr>"
        )

    ri_rows = []
    for _, row in ri_dataframe.iterrows():
        ri_rows.append(
            "<tr>"
            f"<td>{html.escape(str(row['Measurement']))}</td>"
            f"<td>{row['ΔT (K or °C)']:.3f}</td>"
            f"<td>{row['Ri']:.5f}</td>"
            f"<td>{html.escape(str(row['Classification']))}</td>"
            "</tr>"
        )

    measurement_rows_html = "\n".join(measurement_rows)
    ri_rows_html = "\n".join(ri_rows)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ATLiCE Complete Analysis Report</title>
<style>
    body {{ font-family: Arial, Helvetica, sans-serif; color: #18312e; margin: 0; background: #eef5f3; }}
    .page {{ max-width: 980px; margin: 28px auto; background: white; padding: 34px 40px; border-radius: 18px; box-shadow: 0 12px 35px rgba(15, 60, 56, 0.10); }}
    h1 {{ margin: 0; color: #0f766e; }}
    h2 {{ color: #115e59; border-bottom: 1px solid #dbe7e4; padding-bottom: 7px; margin-top: 30px; }}
    .meta {{ color: #64748b; margin: 6px 0 24px; }}
    .figure {{ width: 100%; max-width: 780px; display: block; margin: 15px auto 24px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px; }}
    th, td {{ text-align: left; padding: 8px 9px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    th {{ background: #f8fafc; color: #334155; }}
    .info-table th {{ width: 42%; }}
    .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 14px 0; }}
    .metric {{ border: 1px solid #dbe7e4; border-radius: 12px; padding: 12px; background: #f8fbfa; }}
    .metric b {{ display: block; color: #64748b; font-size: 12px; margin-bottom: 5px; }}
    .metric span {{ color: #115e59; font-size: 20px; font-weight: 700; }}
    .note {{ margin-top: 26px; padding: 13px 15px; background: #f8fafc; border-left: 4px solid #14b8a6; color: #475569; font-size: 13px; line-height: 1.5; }}
    @media print {{ body {{ background: white; }} .page {{ box-shadow: none; margin: 0; max-width: none; }} }}
</style>
</head>
<body>
<div class="page">
    <h1>ATLiCE Complete Indoor Air Analysis</h1>
    <div class="meta">Generated {generated} · Selected pattern: {html.escape(pattern_name)}</div>

    <img class="figure" src="data:image/png;base64,{encoded_figure}" alt="Selected occupancy configuration">
    <img class="figure" src="data:image/png;base64,{encoded_measurement_figure}" alt="Measurement locations">

    <h2>1. Room and occupancy configuration</h2>
    <table class="info-table">
        <tr><th>Pattern group</th><td>{html.escape(configuration['group'])}</td></tr>
        <tr><th>Selected pattern</th><td>{html.escape(pattern_name)}</td></tr>
        <tr><th>Arrangement</th><td>{html.escape(configuration['arrangement'])}</td></tr>
        <tr><th>Room dimensions</th><td>{ROOM_LENGTH:.2f} m × {ROOM_WIDTH:.2f} m × {ROOM_HEIGHT:.2f} m</td></tr>
        <tr><th>Room volume</th><td>{load['room_volume']:.3f} m³</td></tr>
        <tr><th>{html.escape(configuration['spacing_label'])}</th><td>{html.escape(configuration['spacing_value'])}</td></tr>
        <tr><th>{html.escape(configuration['separation_label'])}</th><td>{html.escape(configuration['separation_value'])}</td></tr>
        <tr><th>Side-wall clearance</th><td>{html.escape(configuration['side_clearance'])}</td></tr>
        <tr><th>Main/opposite-wall clearance</th><td>{html.escape(configuration['door_clearance'])}</td></tr>
        <tr><th>Ventilation units</th><td>S1 and S2 supply units; E1 exhaust unit; each 0.60 m × 0.60 m</td></tr>
        <tr><th>Measurement grid</th><td>M1 starts at the top-right location near the split system; M1-M4 move right-to-left across the top row, M5-M8 move left-to-right across the middle row, and M9-M12 move right-to-left across the bottom row.</td></tr>
        <tr><th>Total measurement locations</th><td>{len(measurement_locations)}</td></tr>
    </table>

    <h2>2. Measurement ΔT from uploaded Excel files</h2>
    <div class="metrics">
        <div class="metric"><b>Average ΔT</b><span>{ri['delta_t_average']:.3f}</span></div>
        <div class="metric"><b>Minimum ΔT</b><span>{ri['delta_t_min']:.3f}</span></div>
        <div class="metric"><b>Maximum ΔT</b><span>{ri['delta_t_max']:.3f}</span></div>
    </div>
    <p>Only the third Excel column was used. The first and second columns were ignored. Height assumption: 0.2 m to 2.4 m at 0.1 m intervals. Richardson characteristic height: {measurement_delta_t['richardson_total_height']:.2f} m.</p>
    <table>
        <tr><th>Measurement</th><th>x (m)</th><th>y (m)</th><th>File</th><th>Readings</th><th>Min T</th><th>Max T</th><th>ΔT</th></tr>
        {measurement_rows_html}
    </table>

    <h2>3. Sensible load and airflow summary</h2>
    <div class="metrics">
        <div class="metric"><b>Total occupant load</b><span>{load['total_heat']:.0f} W</span></div>
        <div class="metric"><b>Calculated airflow</b><span>{load['airflow_ls']:.1f} L/s</span></div>
        <div class="metric"><b>Total supply ACH</b><span>{load['ach']:.2f}</span></div>
    </div>
    <table class="info-table">
        <tr><th>Occupants</th><td>{load['occupants']}</td></tr>
        <tr><th>Heat per occupant</th><td>{load['heat_per_occupant']:.0f} W</td></tr>
        <tr><th>Supply / target temperature</th><td>{load['supply_temperature']:.1f} °C / {load['target_temperature']:.1f} °C</td></tr>
        <tr><th>Calculated airflow</th><td>{load['airflow_m3h']:.2f} m³/h</td></tr>
    </table>

    <h2>4. Richardson number for uploaded measurement locations</h2>
    <div class="metrics">
        <div class="metric"><b>Average Ri</b><span>{ri['ri_average']:.4f}</span></div>
        <div class="metric"><b>Minimum Ri</b><span>{ri['ri_min']:.4f}</span></div>
        <div class="metric"><b>Maximum Ri</b><span>{ri['ri_max']:.4f}</span></div>
    </div>
    <table class="info-table">
        <tr><th>Gravity</th><td>{ri['gravity']:.4f} m/s²</td></tr>
        <tr><th>Thermal expansion coefficient</th><td>{ri['alpha']:.6f} 1/K</td></tr>
        <tr><th>Characteristic height / length</th><td>{ri['length_scale']:.3f} m</td></tr>
        <tr><th>Air velocity</th><td>{ri['air_velocity']:.3f} m/s</td></tr>
        <tr><th>Average classification</th><td>{html.escape(ri['classification'])}</td></tr>
    </table>
    <table>
        <tr><th>Measurement</th><th>ΔT</th><th>Ri</th><th>Classification</th></tr>
        {ri_rows_html}
    </table>

    <h2>5. Wells–Riley screening result</h2>
    <div class="metrics">
        <div class="metric"><b>Ideal risk</b><span>{wr['p_ideal'] * 100:.2f}%</span></div>
        <div class="metric"><b>Local risk</b><span>{wr['p_local'] * 100:.2f}%</span></div>
        <div class="metric"><b>Effective local airflow</b><span>{wr['effective_local_airflow']:.1f}</span></div>
    </div>
    <table class="info-table">
        <tr><th>Room airflow</th><td>{wr['room_airflow']:.2f} m³/h</td></tr>
        <tr><th>Local ventilation effectiveness</th><td>{wr['ventilation_effectiveness']:.3f}</td></tr>
        <tr><th>Infectious people / quanta rate</th><td>{wr['infected_people']} / {wr['quanta_rate']:.2f} quanta/h</td></tr>
        <tr><th>Breathing rate / exposure time</th><td>{wr['breathing_rate']:.2f} m³/h / {wr['exposure_time']:.2f} h</td></tr>
        <tr><th>Risk band</th><td>{html.escape(wr['risk_band'])}</td></tr>
    </table>

    <div class="note"><b>Limitations:</b> Occupant sensible heat is the only load included in the automatic load summary. Measurement ΔT is calculated from the uploaded Excel third column only. Richardson number depends on representative height and velocity. Wells–Riley is a steady-state screening model and is sensitive to quanta-rate and local ventilation-effectiveness assumptions.</div>
</div>
</body>
</html>"""




def reset_complete_analysis() -> None:
    """Clear the guided workflow and return to occupancy selection."""
    keys_to_remove = [
        "occupancy_preview_pattern",
        "confirmed_occupancy_pattern",
        "measurement_delta_t_result",
        "ri_result",
        "wr_result",
    ]
    for key in keys_to_remove:
        st.session_state.pop(key, None)
    st.session_state.occupancy_pattern = "Pattern 1"
    st.session_state.confirmed_measurement_delta_t = False
    st.session_state.confirmed_richardson = False
    st.session_state.confirmed_wells_riley = False
    st.session_state.current_page = "occupancy"


def complete_report_page() -> None:
    render_page_heading(
        "📄",
        "Complete Analysis Report",
        "Review and download the confirmed occupancy, measurement ΔT, Richardson and Wells–Riley results.",
    )

    pattern_name = st.session_state.get("confirmed_occupancy_pattern")
    measurement_delta_t = st.session_state.get("measurement_delta_t_result")
    ri = st.session_state.get("ri_result")
    wr = st.session_state.get("wr_result")
    measurement_confirmed = bool(st.session_state.get("confirmed_measurement_delta_t"))
    ri_confirmed = bool(st.session_state.get("confirmed_richardson"))
    wr_confirmed = bool(st.session_state.get("confirmed_wells_riley"))

    if (
        not pattern_name
        or not measurement_delta_t
        or not ri
        or not wr
        or not measurement_confirmed
        or not ri_confirmed
        or not wr_confirmed
    ):
        st.warning(
            "The report is locked until the occupancy pattern, measurement ΔT values, "
            "Richardson result and Wells–Riley result have all been confirmed."
        )
        if st.button("Return to guided workflow", key="report_return_workflow", type="primary"):
            if not pattern_name:
                go_to("occupancy")
            elif not measurement_confirmed:
                go_to("measurement")
            elif not ri_confirmed:
                go_to("ri")
            else:
                go_to("wells_riley")
        return

    configuration = get_pattern_configuration(pattern_name)
    load = get_load_summary(pattern_name)
    measurement_locations = get_measurement_locations()
    fig, _, _ = create_occupancy_figure(pattern_name)
    figure_png = figure_to_png(fig)
    measurement_fig = create_measurement_locations_figure(pattern_name)
    measurement_figure_png = figure_to_png(measurement_fig)

    st.markdown(
        f"""
        <div class="result-banner">
            <b>Step 5 of 5 — complete</b><br>
            Symmetry Pattern — <b>{pattern_name}</b>, measurement ΔT, Richardson and Wells–Riley results are confirmed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    figure_left, figure_centre, figure_right = st.columns([0.95, 3.7, 0.95])
    with figure_centre:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    measurement_left, measurement_centre, measurement_right = st.columns([0.95, 3.7, 0.95])
    with measurement_centre:
        st.pyplot(measurement_fig, use_container_width=True)
    plt.close(measurement_fig)

    st.markdown("### Configuration and sensible load")
    config_col, load_col = st.columns(2, gap="large")
    with config_col:
        st.markdown('<div class="report-section"><h3>Selected configuration</h3>', unsafe_allow_html=True)
        st.write(f"Pattern group: **{configuration['group']}**")
        st.write(f"Selected layout: **{pattern_name}**")
        st.write(f"Arrangement: **{configuration['arrangement']}**")
        st.write(f"Room: **{ROOM_LENGTH:.1f} × {ROOM_WIDTH:.1f} × {ROOM_HEIGHT:.1f} m**")
        st.write(f"{configuration['spacing_label']}: **{configuration['spacing_value']}**")
        st.write(f"{configuration['separation_label']}: **{configuration['separation_value']}**")
        st.write(f"Side-wall clearance: **{configuration['side_clearance']}**")
        st.write(f"Door-wall clearance: **{configuration['door_clearance']}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with load_col:
        st.markdown('<div class="report-section"><h3>Load and airflow</h3>', unsafe_allow_html=True)
        st.write(f"Occupants: **{load['occupants']}**")
        st.write(f"Heat per occupant: **{load['heat_per_occupant']:.0f} W**")
        st.write(f"Total sensible occupant load: **{load['total_heat']:.0f} W**")
        st.write(f"Supply / target temperature: **{load['supply_temperature']:.1f} / {load['target_temperature']:.1f} °C**")
        st.write(f"Calculated airflow: **{load['airflow_ls']:.2f} L/s ({load['airflow_m3h']:.2f} m³/h)**")
        st.write(f"Calculated total supply ACH: **{load['ach']:.2f} h⁻¹**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Measurement ΔT results")
    measurement_dataframe = get_measurement_delta_t_dataframe(measurement_delta_t)
    measurement_display = measurement_dataframe[
        ["Measurement", "x (m)", "y (m)", "File", "Readings", "Min T (°C)", "Max T (°C)", "Mean T (°C)", "ΔT = Max − Min (K or °C)"]
    ].copy()
    for column_name in ["x (m)", "y (m)", "Min T (°C)", "Max T (°C)", "Mean T (°C)", "ΔT = Max − Min (K or °C)"]:
        measurement_display[column_name] = measurement_display[column_name].map(lambda value: f"{value:.4f}")
    st.dataframe(measurement_display, use_container_width=True, hide_index=True)

    st.markdown("### Confirmed model results")
    ri_col, wr_col = st.columns(2, gap="large")
    with ri_col:
        st.markdown('<div class="report-section"><h3>Richardson number</h3>', unsafe_allow_html=True)
        st.metric("Average Ri", f"{ri['ri_average']:.4f}")
        st.write(f"Average classification: **{ri['classification']}**")
        st.write(f"Velocity: **{ri['air_velocity']:.3f} m/s**")
        st.write(f"Characteristic height: **{ri['length_scale']:.2f} m**")
        st.write(f"Minimum Ri: **{ri['ri_min']:.4f}** at **{ri['min_ri_measurement']}**")
        st.write(f"Maximum Ri: **{ri['ri_max']:.4f}** at **{ri['max_ri_measurement']}**")
        st.write(ri["interpretation"])
        st.markdown('</div>', unsafe_allow_html=True)

    with wr_col:
        st.markdown('<div class="report-section"><h3>Wells–Riley</h3>', unsafe_allow_html=True)
        st.metric("Local modelled risk", f"{wr['p_local'] * 100:.2f}%")
        st.write(f"Ideal well-mixed risk: **{wr['p_ideal'] * 100:.2f}%**")
        st.write(f"Effective local airflow: **{wr['effective_local_airflow']:.2f} m³/h**")
        st.write(f"Ventilation effectiveness: **{wr['ventilation_effectiveness']:.3f}**")
        st.write(f"Risk band: **{wr['risk_band']}**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### Richardson table")
    ri_dataframe = get_richardson_dataframe(ri)
    ri_display = ri_dataframe[["Measurement", "x (m)", "y (m)", "ΔT (K or °C)", "Ri", "Classification"]].copy()
    for column_name in ["x (m)", "y (m)", "ΔT (K or °C)", "Ri"]:
        ri_display[column_name] = ri_display[column_name].map(lambda value: f"{value:.5f}")
    st.dataframe(ri_display, use_container_width=True, hide_index=True)

    report_text = build_complete_report_text(
        pattern_name,
        configuration,
        load,
        measurement_delta_t,
        ri,
        wr,
        measurement_locations,
    )
    report_html = build_complete_report_html(
        pattern_name,
        configuration,
        load,
        measurement_delta_t,
        ri,
        wr,
        figure_png,
        measurement_figure_png,
        measurement_locations,
    )

    st.markdown("### Download report")
    download_col1, download_col2 = st.columns(2)
    with download_col1:
        st.download_button(
            label="⬇ Download formatted HTML report",
            data=report_html.encode("utf-8"),
            file_name=f"ATLiCE_{pattern_name.replace(' ', '_')}_complete_report.html",
            mime="text/html",
            key="download_complete_html_report",
            use_container_width=True,
        )
    with download_col2:
        st.download_button(
            label="⬇ Download text report",
            data=report_text,
            file_name=f"ATLiCE_{pattern_name.replace(' ', '_')}_complete_report.txt",
            mime="text/plain",
            key="download_complete_text_report",
            use_container_width=True,
        )

    st.caption(
        "The HTML report includes the selected pattern figure, measurement-locations figure, "
        "measurement ΔT table, Richardson table and Wells–Riley result."
    )

    restart_left, restart_centre, restart_right = st.columns([1, 2, 1])
    with restart_centre:
        if st.button(
            "Start a new analysis",
            key="restart_complete_analysis",
            use_container_width=True,
        ):
            reset_complete_analysis()
            st.rerun()




# =========================================================
# PAGE ROUTER
# =========================================================
page = st.session_state.current_page

if page == "home":
    home_page()
elif page == "occupancy":
    occupancy_page()
elif page == "measurement":
    measurement_delta_t_page()
elif page == "ach":
    cooling_ach_page()
elif page == "ri":
    richardson_page()
elif page == "wells_riley":
    wells_riley_page()
elif page == "report":
    complete_report_page()
else:
    st.session_state.current_page = "home"
    st.rerun()
