import streamlit as st
import requests
from PIL import Image

BASE_URL = "https://lung-backend-5e0fe491.fastapicloud.dev/"

st.set_page_config(
    page_title="Lung Disease Detection",
    page_icon="🫁",
    layout="centered"
)

# -------------------------
# SESSION STATE
# -------------------------

if "token" not in st.session_state:
    st.session_state.token = None

# -------------------------
# SIDEBAR
# -------------------------

menu = st.sidebar.radio(
    "Navigation",
    ["Login", "Signup", "Predict"]
)

# -------------------------
# SIGNUP
# -------------------------

if menu == "Signup":

    st.title("Create Account")

    email = st.text_input("Email")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Signup"):

        payload = {
            "email": email,
            "username": username,
            "password": password
        }

        response = requests.post(
            f"{BASE_URL}signup",
            json=payload
        )

        if response.status_code == 200:
            st.success("Account created successfully")

        else:
            st.error(response.json())

# -------------------------
# LOGIN
# -------------------------

elif menu == "Login":

    st.title("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        payload = {
            "username": username,
            "password": password
        }

        response = requests.post(
            f"{BASE_URL}signin",
            json=payload
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state.token = token

            st.success("Login successful")

        else:
            st.error(response.json())

# -------------------------
# PREDICTION
# -------------------------

elif menu == "Predict":

    if st.session_state.token is None:

        st.warning(
            "Please login first"
        )

        st.stop()

    st.title("🫁 Lung Disease Detection")

    uploaded_file = st.file_uploader(
        "Upload Chest X-Ray",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        if st.button("Predict"):

            headers = {
                "Authorization":
                f"Bearer {st.session_state.token}"
            }

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                response = requests.post(
                    f"{BASE_URL}predict",
                    files=files,
                    headers=headers
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        "Prediction Complete"
                    )

                    st.subheader("Result")

                    st.write(
                        f"### Disease: "
                        f"{data['message']['label']}"
                    )

                    if (
                        "confidence"
                        in data["message"]
                    ):

                        st.write(
                            f"### Confidence: "
                            f"{data['message']['confidence']:.4f}"
                        )

                else:

                    st.error(
                        response.json()
                    )

            except Exception as e:

                st.error(str(e))

# -------------------------
# LOGOUT
# -------------------------

if st.session_state.token:

    st.sidebar.success(
        "Logged In"
    )

    if st.sidebar.button("Logout"):

        st.session_state.token = None

        st.rerun()