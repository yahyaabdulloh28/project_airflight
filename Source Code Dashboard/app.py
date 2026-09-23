import math
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_flight_price_model.pkl"
ROUTE_INFO_PATH = BASE_DIR / "models" / "route_info.pkl"

AIRLINES = ["AirAsia", "Air_India", "GO_FIRST", "Indigo", "SpiceJet", "Vistara"]
CITIES = ["Bangalore", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
TIME_OPTIONS = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]
STOP_OPTIONS = ["zero", "one", "two_or_more"]
CLASS_OPTIONS = ["Economy", "Business"]
AIRLINE_CLASSES = {
    "AirAsia": ["Economy"],
    "Air_India": ["Economy", "Business"],
    "GO_FIRST": ["Economy"],
    "Indigo": ["Economy"],
    "SpiceJet": ["Economy"],
    "Vistara": ["Economy", "Business"]
}


def build_routes() -> list[str]:
    return [f"{source} → {destination}" for source in CITIES for destination in CITIES if source != destination]


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_route_defaults() -> pd.DataFrame | None:
    if not ROUTE_INFO_PATH.exists():
        return None
    try:
        data = joblib.load(ROUTE_INFO_PATH)
    except Exception:
        return None
    return data if isinstance(data, pd.DataFrame) else None


def format_currency(value: float) -> str:
    if math.isnan(value):
        return "-"
    return f"INR {value:,.0f}"


st.set_page_config(page_title="Flight Price Prediction", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --primary: #1d4ed8;
        --primary-dark: #1e40af;
        --accent: #0f766e;
        --bg: #f6f8fb;
        --panel: #ffffff;
        --text: #172033;
        --muted: #5b6475;
        --border: #dfe5ef;
    }

    .stApp {
    background-image: url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }
    
    [data-testid="collapsedControl"]{
    color: #1d4ed8 !important;
    }

    [data-testid="collapsedControl"]:hover{
    background-color: #f3f4f6 !important;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dfe5ef;
        box-shadow: 4px 0 20px rgba(31,45,70,0.08);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text);
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: #f6f8fb;
        border: 0;
        box-shadow: none;
    }

   
    h1, h2, h3 {
        color: #172033 !important;
    }


    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #172033 !important;
    }


    [data-testid="stCaptionContainer"] {
        color: #172033 !important;
    }

    details summary {
        color: #172033 !important;
        font-weight: 700 !important;
    }


    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.96) !important;
        backdrop-filter: blur(8px);
    }

    .app-hero {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 22px 24px;
        margin-bottom: 22px;
        background: linear-gradient(135deg, #ffffff 0%, #eef6ff 100%);
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 14px 34px rgba(31, 45, 70, 0.08);
    }

    .plane-logo {
        width: 72px;
        height: 72px;
        display: grid;
        place-items: center;
        flex: 0 0 72px;
        border-radius: 18px;
        background: #ffffff;
        overflow: hidden;
        box-shadow: 0 14px 28px rgba(29, 78, 216, 0.18);
    }

    .plane-logo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    .app-hero h1 {
        margin: 0;
        font-size: 2.25rem;
        line-height: 1.12;
        color: var(--text);
        letter-spacing: 0;
    }

    .app-hero p {
        margin: 8px 0 0;
        color: var(--muted);
        font-size: 1rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: 0 10px 28px rgba(31, 45, 70, 0.07);
    }

    [data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stVerticalBlockBorderWrapper"] h3 {
        margin-top: 0;
        margin-bottom: 18px;
    }

    div[data-testid="stMetric"] {
        padding: 18px 18px 14px;
        background: #f8fbff;
        border: 1px solid #cfe0f8;
        border-radius: 12px;
        text-align: center;
    }

    div[data-testid="stMetricValue"] {
        color: var(--primary-dark);
        font-weight: 800;
    }

    .stButton > button {
        width: 100%;
        min-height: 46px;
        border: 0;
        border-radius: 10px;
        background: var(--primary);
        color: #ffffff;
        font-weight: 700;
        box-shadow: 0 10px 20px rgba(29, 78, 216, 0.22);
    }

    .stButton > button:hover {
        background: var(--primary-dark);
        color: #ffffff;
        border: 0;
    }

    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        color: var(--text);
        font-weight: 650;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    h2, h3 {
        color: var(--text);
        letter-spacing: 0;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
        font-weight: 800;
    }

    [data-testid="stAlert"] p {
        color: #172033 !important;
        font-size: 1rem;
        font-weight: 800;
    }

        .price-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;

        width: 260px;
        height: 45px;

        margin: 20px auto 25px;

        border-radius: 18px;

        font-size: 1.05rem;
        font-weight: 700;

        color: #172033;
        border: 1px solid transparent;

        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .prediction-title {
        margin: 0 0 18px;
        text-align: center;
        color: var(--text);
        font-size: 1.85rem;
        font-weight: 800;
    }

    .price-badge.good {
        background: #d1fae5;
        border-color: #86efac;
    }

    .price-badge.average {
        background: #fef3c7;
        border-color: #facc15;
    }

    .price-badge.expensive {
        background: #fee2e2;
        border-color: #fca5a5;
    }

    @media (max-width: 720px) {
        .app-hero {
            align-items: flex-start;
            padding: 18px;
        }

        .plane-logo {
            width: 58px;
            height: 58px;
            flex-basis: 58px;
            border-radius: 14px;
        }

        .app-hero h1 {
            font-size: 1.55rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-hero">
        <div class="plane-logo" aria-label="Flight logo">
            <img
                src="https://st2.depositphotos.com/4191945/7515/v/450/depositphotos_75158949-stock-illustration-vector-globe-and-airplane-logo.jpg"
                alt="Airplane globe logo"
            />
        </div>
        <div>
            <h1>Flight Price Prediction</h1>
            <p>Ticket price predictions based on airline, class, stops, and route.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    model = load_model()
except Exception as exc:
    st.error("Model gagal dimuat. Pastikan dependency di requirements.txt sudah ter-install.")
    st.exception(exc)
    st.stop()

routes = build_routes()

# with st.sidebar:
#     st.header("Flight Input")

#     airline = st.selectbox("Airline", AIRLINES, index=AIRLINES.index("Vistara"))
#     travel_class = st.selectbox("Class", CLASS_OPTIONS, index=CLASS_OPTIONS.index("Economy"))
#     route = st.selectbox("Route", routes, index=routes.index("Delhi → Mumbai"))

#     departure_time = st.selectbox("Departure Time", TIME_OPTIONS, index=TIME_OPTIONS.index("Evening"))
#     arrival_time = st.selectbox("Arrival Time", TIME_OPTIONS, index=TIME_OPTIONS.index("Evening"))
#     stops = st.selectbox("Stops", STOP_OPTIONS, index=STOP_OPTIONS.index("one"))

#     default_duration = 2.17
#     default_days_left = 20

#     duration = st.number_input("Duration (hours)", min_value=0.5, max_value=50.0, value=float(default_duration), step=0.25)
#     days_left = st.slider("Days Left", min_value=1, max_value=49, value=int(default_days_left))

with st.sidebar:
    st.header("Flight Input")

    airline = st.selectbox(
        "Airline",
        AIRLINES,
        index=AIRLINES.index("Air_India")
    )

    available_classes = AIRLINE_CLASSES[airline]

    if len(available_classes) == 1:
        travel_class = available_classes[0]

        st.selectbox(
            "Class",
            [travel_class],
            disabled=True
        )

    else:
        travel_class = st.selectbox(
            "Class",
            available_classes
        )

    route = st.selectbox(
        "Route",
        routes,
        index=routes.index("Delhi → Mumbai")
    )

    stops = st.selectbox(
        "Stops",
        STOP_OPTIONS,
        index=STOP_OPTIONS.index("one")
    )

    # hidden/default values
    departure_time = "Evening"
    arrival_time = "Evening"
    duration = 2.17
    days_left = 20

input_data = pd.DataFrame(
    {
        "airline": [airline],
        "departure_time": [departure_time],
        "stops": [stops],
        "arrival_time": [arrival_time],
        "class": [travel_class],
        "duration": [duration],
        "days_left": [days_left],
        "route": [route],
    }
)

display_data = pd.DataFrame(
    {
        "Airline": [airline],
        "Class": [travel_class],
        "Route": [route],
        "Stops": [stops]
    }
)

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    with st.container(border=True):
        st.subheader(" Input Details")
        # st.dataframe(input_data, use_container_width=True, hide_index=True)
        st.dataframe(display_data,use_container_width=True,hide_index=True)

with right:
    with st.container(border=True):
        st.markdown('<h3 class="prediction-title">Predict Price</h3>', unsafe_allow_html=True)
        if st.button("Predict", type="primary", use_container_width=True):
            prediction = model.predict(input_data)
            price = float(prediction[0])
            st.metric("Estimated Ticket Price", format_currency(price))
            st.caption(f"Nilai mentah model: {price:,.2f}")

            if price < 7000:
                st.markdown('<div class="price-badge good">🟢 Good Price</div>', unsafe_allow_html=True)
            elif price < 15000:
                st.markdown('<div class="price-badge average">🟡 Average Price</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="price-badge expensive">🔴 Expensive Ticket</div>', unsafe_allow_html=True)
        else:
            st.info("Click the Predict button to run the prediction.")

with st.expander("Preview payload for model"):
    st.json(input_data.iloc[0].to_dict())
