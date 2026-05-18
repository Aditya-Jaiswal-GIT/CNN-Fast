# app.py

import streamlit as st
import requests
from PIL import Image

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Lung Disease Detection",
    page_icon="🫁",
    layout="centered"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🫁 Lung Disease Detection")
st.write("Upload a Chest X-Ray Image")

# -----------------------------------
# FILE UPLOADER
# -----------------------------------
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# PREDICT BUTTON
# -----------------------------------
if uploaded_file is not None:

    # Display Image
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    # Predict Button
    if st.button("Predict"):

        with st.spinner("Predicting..."):

            try:

                # FastAPI endpoint
                url = "http://127.0.0.1:8000/predict"

                # Send image to FastAPI
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    url,
                    files=files
                )

                # Convert response
                data = response.json()

                # Show Result
                st.success("Prediction Complete")

                st.subheader("Result")

                st.write(
                    f"### Disease: {data['message']['label']}"
                )

                # Confidence (if available)
                if "confidence" in data["message"]:

                    confidence = data["message"]["confidence"]

                    st.write(
                        f"### Confidence: {confidence:.4f}"
                    )

            except Exception as e:

                st.error(f"Error: {e}")