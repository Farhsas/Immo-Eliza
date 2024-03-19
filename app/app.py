import requests
import streamlit as st


def make_prediction(user_inputs):
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=user_inputs)

        return response.json()

    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None


def main():
    st.title("Immo-Eliza Estimation System")

    property_id = st.number_input("Id:", min_value=1, value=1)
    postal_code = st.text_input("Postal Code:")
    region = st.selectbox("Region:", ["Wallonie", "Flandres", "Bruxelles"])
    province = st.selectbox("Province:",
        ["Anvers", "Limbourg", "Flandre Orientale", "Brabant Flamand", "Flandre Orientale",
            "Brabant Wallon", "Hainaut", "Liège", "Luxembourg", "Namur"])
    type_of_property = st.selectbox("Type of Property:", ["HOUSE", "APARTMENT"])
    subtype_of_property = st.selectbox("Subtype of Property:",
        ['APARTMENT', 'HOUSE_GROUP', 'HOUSE', 'APARTMENT_BLOCK', 'KOT',
           'MANSION', 'PENTHOUSE', 'GROUND_FLOOR', 'APARTMENT_GROUP',
           'DUPLEX', 'VILLA', 'MIXED_USE_BUILDING', 'FLAT_STUDIO',
           'TOWN_HOUSE', 'LOFT', 'BUNGALOW', 'CHALET', 'COUNTRY_COTTAGE',
           'EXCEPTIONAL_PROPERTY', 'TRIPLEX', 'FARMHOUSE', 'CASTLE',
           'OTHER_PROPERTY', 'MANOR_HOUSE', 'SERVICE_FLAT', 'PAVILION'])
    rooms = st.number_input("Number of Rooms:", min_value=1, value=1)
    bedrooms = st.number_input("Number of bedrooms:", min_value=1, value=1)
    bathrooms = st.number_input("Number of bathrooms:", min_value=1, value=1)
    living_area = st.number_input("Living Area (sq. m.):", min_value=0, value=0)
    open_fire = st.checkbox("Open Fire")
    terrace = st.checkbox("Terrace")
    garden = st.checkbox("Garden")
    heating = st.selectbox("Type of heating",
        ['GAS', 'FUELOIL', 'ELECTRIC', 'PELLET', 'WOOD', 'CARBON',
           'SOLAR'])
    kitchen = st.selectbox("Equipped Kitchen",
        ['INSTALLED', 'SEMI_EQUIPPED', 'HYPER_EQUIPPED',
           'USA_HYPER_EQUIPPED', 'NOT_INSTALLED', 'USA_SEMI_EQUIPPED',
           'USA_INSTALLED', 'USA_UNINSTALLED'])
    furnished = st.checkbox("Furnished")
    swimming_pool = st.checkbox("Swimming Pool")
    num_of_facades = st.number_input("Number of Facades:", min_value=0, value=0)
    state_of_building = st.selectbox("State of Building:",
        ['GOOD', 'TO_BE_DONE_UP', 'AS_NEW', 'TO_RENOVATE',
               'JUST_RENOVATED', 'TO_RESTORE']
    )

    user_inputs = {
        "property_id": property_id,
        "postal_code": postal_code,
        "type_of_property": type_of_property,
        "subtype_of_property": subtype_of_property,
        "bedrooms": bedrooms,
        "living_area": living_area,
        "openfire": open_fire,
        "terrace": terrace,
        "garden": garden,
        "rooms": rooms,
        "bathrooms": bathrooms,
        "region": region,
        "province": province,
        "state_of_property": state_of_building,
        "facade_count": num_of_facades,
        "heating": heating,
        "kitchen": kitchen,
        "furnished": furnished,
        "swimmingpool": swimming_pool,
    }

    if st.button("Make Estimation"):
        st.info("Making estimation...")

        prediction_result = make_prediction(user_inputs)

        # Display the prediction result
        if prediction_result is not None:
            st.subheader("Prediction Result:")
            st.write(f"Estimated Price: {prediction_result}")


if __name__ == "__main__":
    main()
