import streamlit as st
import geopy.distance
import math

# ----------------------------
# Distance Calculation Class
# ----------------------------
class Maps:
    def __init__(self):
        pass

    def get_distance(self, location_1, location_2):
        try:
            distance = geopy.distance.distance(location_1, location_2).km
        except Exception as e:
            st.warning(f"Geopy error: {e}. Using fallback calculation.")
            distance = math.sqrt((location_1[0] - location_2[0])**2 + (location_1[1] - location_2[1])**2)
        return distance

# ----------------------------
# Surge Pricing Class
# ----------------------------
class SurgePricing:
    def __init__(self):
        pass

    def get_price_per_km(self, hour):
        try:
            if 8 < hour < 11:
                return 20
            elif 18 < hour < 21:
                return 15
            else:
                return 10
        except Exception as e:
            st.warning(f"Hour error: {e}. Using default price.")
            return 10

# ----------------------------
# Final Price Calculator
# ----------------------------
def get_final_price(pick_up_location, drop_location, booking_hour):
    maps = Maps()
    surge = SurgePricing()

    total_distance = maps.get_distance(pick_up_location, drop_location)
    actual_price_per_km = surge.get_price_per_km(booking_hour)

    final_price = round(total_distance * actual_price_per_km, 2)
    return final_price

# ----------------------------
# 🚀 Streamlit App Interface
# ----------------------------

st.set_page_config(page_title="🚕 Ride Fare Estimator", page_icon="🚗")
st.title("🚕 Ride Fare Estimator")

st.markdown("Calculate the ride fare based on distance and booking time (with surge pricing).")

# 📍 Coordinates Input
st.subheader("📍 Enter Coordinates")

col1, col2 = st.columns(2)
with col1:
    lat1 = st.number_input("Pick-Up Latitude", value=19.0760, format="%.6f")
    lon1 = st.number_input("Pick-Up Longitude", value=72.8777, format="%.6f")

with col2:
    lat2 = st.number_input("Drop Latitude", value=18.5204, format="%.6f")
    lon2 = st.number_input("Drop Longitude", value=73.8567, format="%.6f")

# ⏰ Time Input
booking_hour = st.slider("⏰ Booking Hour (0–23)", min_value=0, max_value=23, value=9)

# 🎯 Calculate Button
if st.button("Calculate Fare"):
    try:
        pick_up_location = (lat1, lon1)
        drop_location = (lat2, lon2)
        price = get_final_price(pick_up_location, drop_location, booking_hour)
        st.success(f"💰 Final Trip Price: ₹{price}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
