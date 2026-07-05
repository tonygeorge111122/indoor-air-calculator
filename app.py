import base64
import math
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
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
            "2  🌡️  Richardson Number",
            key="nav_ri",
            use_container_width=True,
            disabled=not bool(confirmed_pattern),
        ):
            go_to("ri")

        if st.button(
            "3  🫁  Wells–Riley Risk",
            key="nav_wr",
            use_container_width=True,
            disabled=not ri_ready,
        ):
            go_to("wells_riley")

        if st.button(
            "4  📄  Final Report",
            key="nav_report",
            use_container_width=True,
            disabled=not wells_ready,
        ):
            go_to("report")

        pattern_status = f"✓ {confirmed_pattern}" if confirmed_pattern else "○ Not confirmed"
        ri_status = "✓ Confirmed" if ri_ready else "○ Pending"
        wells_status = "✓ Confirmed" if wells_ready else "○ Pending"
        report_status = "✓ Available" if wells_ready else "○ Locked"

        st.markdown(
            f"""
            <div class="workflow-status">
                <b>Progress</b><br>
                Occupancy: {pattern_status}<br>
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
                to the next stage. All model inputs remain editable.
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
    st.caption("Choose an occupancy symmetry pattern first, preview it, and confirm it before continuing to the Richardson calculation.")

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
                    Choose Pattern 1 or Pattern 2 under the Symmetry Pattern
                    group, preview the selected layout, and confirm it before
                    continuing to the Richardson calculation.
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
            "**Workflow:** Select a Symmetry Pattern → confirm the selection "
            "to display the figure → confirm the displayed pattern → continue "
            "to Richardson inputs."
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
    """Create a moderately sized occupancy figure for display inside Streamlit."""
    if pattern_name == "Pattern 1":
        positions, dimensions = get_pattern_1_positions()
        dimension_function = draw_pattern_1_dimensions
    elif pattern_name == "Pattern 2":
        positions, dimensions = get_pattern_2_positions()
        dimension_function = draw_pattern_2_dimensions
    else:
        raise ValueError(f"Unknown occupancy pattern: {pattern_name}")

    # The figure is moderately enlarged while remaining centred
    # and leaving enough white space around the layout.
    fig, ax = plt.subplots(figsize=(10.4, 6.5))
    fig.patch.set_facecolor("white")

    ax.set_xlim(-0.72, ROOM_LENGTH + 0.52)
    ax.set_ylim(-0.76, ROOM_WIDTH + 0.53)
    ax.set_aspect("equal")
    ax.set_xlabel("Room length (m)", fontsize=10)
    ax.set_ylabel("Room width (m)", fontsize=10)
    ax.set_title(
        pattern_name,
        fontsize=14,
        pad=13,
        fontweight="bold",
    )
    ax.tick_params(axis="both", labelsize=9)

    draw_ceiling_grid(ax)
    draw_room_boundary(ax)
    draw_occupants(ax, positions)
    draw_ventilation_units(ax)
    draw_room_labels(ax)
    draw_external_room_dimensions(ax)
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

    legend_items = [
        Line2D(
            [0], [0], marker="o", color="none",
            markerfacecolor=HUMAN_COLOUR, markeredgecolor="black",
            markersize=9,
            label=f"H1–H6: Human heat loads ({HUMAN_HEAT_LOAD} W each)",
        ),
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
    st.session_state.confirmed_richardson = False
    st.session_state.confirmed_wells_riley = False
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
    st.session_state.setdefault("confirmed_richardson", False)
    st.session_state.setdefault("confirmed_wells_riley", False)

    st.markdown("### Symmetry Pattern")

    selection_left, selection_centre, selection_right = st.columns([1, 2.2, 1])

    with selection_centre:
        selected_pattern = st.radio(
            "Choose a pattern",
            options=["Pattern 1", "Pattern 2"],
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
            st.session_state.confirmed_richardson = False
            st.session_state.confirmed_wells_riley = False
            st.session_state.pop("ri_result", None)
            st.session_state.pop("wr_result", None)
            st.rerun()

    preview_pattern = st.session_state.get("occupancy_preview_pattern")

    if preview_pattern != selected_pattern:
        st.info("Select Pattern 1 or Pattern 2, then confirm the selection to display its figure.")
        return

    st.markdown("---")
    st.markdown(f"### {preview_pattern}")

    # Display the figure in a wider centred column.
    figure_left, figure_centre, figure_right = st.columns([0.80, 4.10, 0.80])

    with figure_centre:
        fig, positions, dimensions = create_occupancy_figure(preview_pattern)
        png_data = figure_to_png(fig)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Occupants", "6")
    metric2.metric("Heat per occupant", "100 W")
    metric3.metric("Total occupant load", "600 W")
    metric4.metric("Room volume", "63.50 m³")

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

        if st.button(
            "Confirm pattern and continue to Richardson →",
            key="confirm_pattern_and_continue",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.confirmed_occupancy_pattern = preview_pattern
            st.session_state.confirmed_richardson = False
            st.session_state.confirmed_wells_riley = False
            st.session_state.pop("ri_result", None)
            st.session_state.pop("wr_result", None)
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
def richardson_page() -> None:
    render_page_heading(
        "🌡️",
        "Richardson Number",
        "Enter the airflow and thermal inputs, calculate the result, and confirm it before continuing.",
    )

    confirmed_pattern = st.session_state.get("confirmed_occupancy_pattern")

    if not confirmed_pattern:
        st.warning(
            "No occupancy pattern has been confirmed. Select and confirm a "
            "Symmetry Pattern before opening the Richardson inputs."
        )
        if st.button("Go to Occupancy Patterns", key="ri_go_to_occupancy", type="primary"):
            go_to("occupancy")
        return

    st.markdown(
        f"""
        <div class="result-banner">
            <b>Step 2 of 4</b><br>
            Confirmed occupancy: Symmetry Pattern — <b>{confirmed_pattern}</b>
        </div>
        """,
        unsafe_allow_html=True,
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
                    Use a characteristic length and velocity that represent the
                    airflow region being assessed. Velocity is squared, so the
                    result is highly sensitive to the selected velocity.
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

        ri = gravity * alpha * delta_t * length_scale / (air_velocity**2)

        if ri < 0:
            classification = "Opposing buoyancy direction"
            interpretation = (
                "The negative sign indicates that buoyancy acts opposite to the "
                "selected reference-flow direction."
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
        st.markdown("## Richardson result")
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
            <b>Step 3 of 4</b><br>
            Pattern: <b>{confirmed_pattern}</b> &nbsp; | &nbsp;
            Confirmed Richardson number: <b>{ri_result['ri']:.4f}</b>
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


def get_load_summary() -> dict:
    """Calculate the six-person sensible-load airflow used in the study summary."""
    occupants = 6
    heat_per_occupant = HUMAN_HEAT_LOAD
    total_heat = occupants * heat_per_occupant
    supply_temperature = 12.0
    target_temperature = 22.0
    rho_cp = 1200.0
    delta_t = target_temperature - supply_temperature
    room_volume = ROOM_LENGTH * ROOM_WIDTH * ROOM_HEIGHT
    airflow_m3s = total_heat / (rho_cp * delta_t)
    airflow_ls = airflow_m3s * 1000
    airflow_m3h = airflow_m3s * 3600
    ach = airflow_m3h / room_volume

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
    ri: dict,
    wr: dict,
) -> str:
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

2. SENSIBLE LOAD AND AIRFLOW SUMMARY
Occupants: {load['occupants']}
Heat per occupant: {load['heat_per_occupant']:.0f} W
Total sensible occupant load: {load['total_heat']:.0f} W
Supply-air temperature: {load['supply_temperature']:.1f} °C
Target room temperature: {load['target_temperature']:.1f} °C
Temperature difference: {load['delta_t']:.1f} K
Calculated airflow: {load['airflow_ls']:.2f} L/s
Calculated airflow: {load['airflow_m3h']:.2f} m³/h
Calculated total supply ACH: {load['ach']:.2f} h⁻¹

3. RICHARDSON NUMBER
Gravity: {ri['gravity']:.4f} m/s²
Thermal expansion coefficient: {ri['alpha']:.6f} 1/K
Temperature difference: {ri['delta_t']:.4f} K
Characteristic length: {ri['length_scale']:.4f} m
Air velocity: {ri['air_velocity']:.4f} m/s
Richardson number: {ri['ri']:.6f}
Classification: {ri['classification']}
Interpretation: {ri['interpretation']}

4. WELLS–RILEY SCREENING RESULT
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
The sensible-load result includes occupant heat only. The Richardson result depends on the selected representative scales. The Wells–Riley result is a steady-state screening estimate and is sensitive to quanta rate and ventilation-effectiveness assumptions.
"""


def build_complete_report_html(
    pattern_name: str,
    configuration: dict,
    load: dict,
    ri: dict,
    wr: dict,
    figure_png: bytes,
) -> str:
    encoded_figure = base64.b64encode(figure_png).decode("ascii")
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ATLiCE Complete Analysis Report</title>
<style>
    body {{ font-family: Arial, Helvetica, sans-serif; color: #18312e; margin: 0; background: #eef5f3; }}
    .page {{ max-width: 940px; margin: 28px auto; background: white; padding: 34px 40px; border-radius: 18px; box-shadow: 0 12px 35px rgba(15, 60, 56, 0.10); }}
    h1 {{ margin: 0; color: #0f766e; }}
    h2 {{ color: #115e59; border-bottom: 1px solid #dbe7e4; padding-bottom: 7px; margin-top: 30px; }}
    .meta {{ color: #64748b; margin: 6px 0 24px; }}
    .figure {{ width: 100%; max-width: 780px; display: block; margin: 15px auto 24px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
    th, td {{ text-align: left; padding: 9px 11px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    th {{ width: 42%; background: #f8fafc; color: #334155; }}
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
    <div class="meta">Generated {generated} · Selected pattern: {pattern_name}</div>

    <img class="figure" src="data:image/png;base64,{encoded_figure}" alt="Selected occupancy configuration">

    <h2>1. Room and occupancy configuration</h2>
    <table>
        <tr><th>Pattern group</th><td>{configuration['group']}</td></tr>
        <tr><th>Selected pattern</th><td>{pattern_name}</td></tr>
        <tr><th>Arrangement</th><td>{configuration['arrangement']}</td></tr>
        <tr><th>Room dimensions</th><td>{ROOM_LENGTH:.2f} m × {ROOM_WIDTH:.2f} m × {ROOM_HEIGHT:.2f} m</td></tr>
        <tr><th>Room volume</th><td>{load['room_volume']:.3f} m³</td></tr>
        <tr><th>{configuration['spacing_label']}</th><td>{configuration['spacing_value']}</td></tr>
        <tr><th>{configuration['separation_label']}</th><td>{configuration['separation_value']}</td></tr>
        <tr><th>Side-wall clearance</th><td>{configuration['side_clearance']}</td></tr>
        <tr><th>Main/opposite-wall clearance</th><td>{configuration['door_clearance']}</td></tr>
        <tr><th>Ventilation units</th><td>S1 and S2 supply units; E1 exhaust unit; each 0.60 m × 0.60 m</td></tr>
    </table>

    <h2>2. Sensible load and airflow summary</h2>
    <div class="metrics">
        <div class="metric"><b>Total occupant load</b><span>{load['total_heat']:.0f} W</span></div>
        <div class="metric"><b>Calculated airflow</b><span>{load['airflow_ls']:.1f} L/s</span></div>
        <div class="metric"><b>Total supply ACH</b><span>{load['ach']:.2f}</span></div>
    </div>
    <table>
        <tr><th>Occupants</th><td>{load['occupants']}</td></tr>
        <tr><th>Heat per occupant</th><td>{load['heat_per_occupant']:.0f} W</td></tr>
        <tr><th>Supply / target temperature</th><td>{load['supply_temperature']:.1f} °C / {load['target_temperature']:.1f} °C</td></tr>
        <tr><th>Calculated airflow</th><td>{load['airflow_m3h']:.2f} m³/h</td></tr>
    </table>

    <h2>3. Richardson number</h2>
    <div class="metrics">
        <div class="metric"><b>Richardson number</b><span>{ri['ri']:.4f}</span></div>
        <div class="metric"><b>Air velocity</b><span>{ri['air_velocity']:.3f} m/s</span></div>
        <div class="metric"><b>Classification</b><span style="font-size:15px">{ri['classification']}</span></div>
    </div>
    <table>
        <tr><th>Temperature difference</th><td>{ri['delta_t']:.3f} K</td></tr>
        <tr><th>Characteristic length</th><td>{ri['length_scale']:.3f} m</td></tr>
        <tr><th>Interpretation</th><td>{ri['interpretation']}</td></tr>
    </table>

    <h2>4. Wells–Riley screening result</h2>
    <div class="metrics">
        <div class="metric"><b>Ideal risk</b><span>{wr['p_ideal'] * 100:.2f}%</span></div>
        <div class="metric"><b>Local risk</b><span>{wr['p_local'] * 100:.2f}%</span></div>
        <div class="metric"><b>Effective local airflow</b><span>{wr['effective_local_airflow']:.1f}</span></div>
    </div>
    <table>
        <tr><th>Room airflow</th><td>{wr['room_airflow']:.2f} m³/h</td></tr>
        <tr><th>Local ventilation effectiveness</th><td>{wr['ventilation_effectiveness']:.3f}</td></tr>
        <tr><th>Infectious people / quanta rate</th><td>{wr['infected_people']} / {wr['quanta_rate']:.2f} quanta/h</td></tr>
        <tr><th>Breathing rate / exposure time</th><td>{wr['breathing_rate']:.2f} m³/h / {wr['exposure_time']:.2f} h</td></tr>
        <tr><th>Risk band</th><td>{wr['risk_band']}</td></tr>
    </table>

    <div class="note"><b>Limitations:</b> Occupant sensible heat is the only load included in the automatic load summary. Richardson number depends on representative length and velocity. Wells–Riley is a steady-state screening model and is sensitive to quanta-rate and local ventilation-effectiveness assumptions.</div>
</div>
</body>
</html>"""


def reset_complete_analysis() -> None:
    """Clear the guided workflow and return to occupancy selection."""
    keys_to_remove = [
        "occupancy_preview_pattern",
        "confirmed_occupancy_pattern",
        "ri_result",
        "wr_result",
    ]
    for key in keys_to_remove:
        st.session_state.pop(key, None)
    st.session_state.occupancy_pattern = "Pattern 1"
    st.session_state.confirmed_richardson = False
    st.session_state.confirmed_wells_riley = False
    st.session_state.current_page = "occupancy"


def complete_report_page() -> None:
    render_page_heading(
        "📄",
        "Complete Analysis Report",
        "Review and download the confirmed occupancy, load, Richardson and Wells–Riley results.",
    )

    pattern_name = st.session_state.get("confirmed_occupancy_pattern")
    ri = st.session_state.get("ri_result")
    wr = st.session_state.get("wr_result")
    ri_confirmed = bool(st.session_state.get("confirmed_richardson"))
    wr_confirmed = bool(st.session_state.get("confirmed_wells_riley"))

    if not pattern_name or not ri or not wr or not ri_confirmed or not wr_confirmed:
        st.warning(
            "The report is locked until the occupancy pattern, Richardson result "
            "and Wells–Riley result have all been confirmed."
        )
        if st.button("Return to guided workflow", key="report_return_workflow", type="primary"):
            if not pattern_name:
                go_to("occupancy")
            elif not ri_confirmed:
                go_to("ri")
            else:
                go_to("wells_riley")
        return

    configuration = get_pattern_configuration(pattern_name)
    load = get_load_summary()
    fig, _, _ = create_occupancy_figure(pattern_name)
    figure_png = figure_to_png(fig)

    st.markdown(
        f"""
        <div class="result-banner">
            <b>Step 4 of 4 — complete</b><br>
            Symmetry Pattern — <b>{pattern_name}</b> and both model results are confirmed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    figure_left, figure_centre, figure_right = st.columns([0.95, 3.7, 0.95])
    with figure_centre:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)

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

    st.markdown("### Confirmed model results")
    ri_col, wr_col = st.columns(2, gap="large")
    with ri_col:
        st.markdown('<div class="report-section"><h3>Richardson number</h3>', unsafe_allow_html=True)
        st.metric("Ri", f"{ri['ri']:.4f}")
        st.write(f"Classification: **{ri['classification']}**")
        st.write(f"Velocity: **{ri['air_velocity']:.3f} m/s**")
        st.write(f"ΔT: **{ri['delta_t']:.2f} K**")
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

    report_text = build_complete_report_text(pattern_name, configuration, load, ri, wr)
    report_html = build_complete_report_html(
        pattern_name,
        configuration,
        load,
        ri,
        wr,
        figure_png,
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
        "The HTML report includes the selected pattern figure and can be opened "
        "in a browser or printed to PDF."
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
