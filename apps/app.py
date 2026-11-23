import os
import tempfile

import numpy as np
import streamlit as st
from PIL import Image

from src.classification.inference import (
    load_feature_extractor,
    load_classifier,
    predict_classification,
)

from src.segmentation.inference import (
    load_segmentation_model,
    preprocess_image,
    predict_segmentation,
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="NeuroScan AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #A0A0A0;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }

    .result-card {
        background: linear-gradient(
            135deg,
            #1E293B,
            #111827
        );
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 12px;
    }

    .result-label {
        color: #94A3B8;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }

    .result-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .small-text {
        color: #94A3B8;
        font-size: 0.85rem;
    }

    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: 600;
    }

    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="main-title">🧠 NeuroScan AI</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Brain MRI Classification & Tumor Segmentation
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    Upload a brain MRI scan to classify the tumor type
    and visualize the predicted tumor segmentation.
    """
)


# ==================================================
# MODEL LOADING
# ==================================================

@st.cache_resource
def load_classification_models():

    feature_extractor, transform = load_feature_extractor()

    classifier = load_classifier()

    return feature_extractor, transform, classifier


@st.cache_resource
def load_segmentation_models():

    model, device = load_segmentation_model()

    return model, device


# ==================================================
# IMAGE UPLOAD
# ==================================================

st.markdown("---")

upload_col, preview_col = st.columns(
    [1.1, 1],
    vertical_alignment="center",
)


with upload_col:

    st.markdown("### 📤 Upload MRI")

    uploaded_file = st.file_uploader(
        "Choose an MRI image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    st.caption(
        "Supported formats: JPG, JPEG and PNG"
    )

    st.caption(
        "For best results, upload a brain MRI image."
    )


with preview_col:

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        st.markdown("### 🖼️ Image Preview")

        st.image(
            image,
            caption=uploaded_file.name,
            width=420,
        )

    else:

        st.markdown("### 🖼️ Image Preview")

        st.info(
            "Your uploaded MRI image will appear here."
        )


# ==================================================
# ANALYSIS BUTTON
# ==================================================

st.markdown("---")

if uploaded_file is not None:

    analyze_button = st.button(
        "🔬 Analyze MRI",
        type="primary",
    )

else:

    st.info(
        "Upload an MRI image to begin analysis."
    )

    analyze_button = False


# ==================================================
# ANALYSIS
# ==================================================

if analyze_button:

    image = Image.open(uploaded_file).convert("RGB")

    with st.spinner(
        "Analyzing MRI image. Please wait..."
    ):

        temporary_path = None

        try:

            # --------------------------------------
            # CLASSIFICATION
            # --------------------------------------

            feature_extractor, transform, classifier = (
                load_classification_models()
            )

            classification_result = predict_classification(
                image,
                feature_extractor,
                transform,
                classifier,
            )

            predicted_label = classification_result[
                "predicted_label"
            ]


            # --------------------------------------
            # SEGMENTATION
            # --------------------------------------

            temporary_file = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False,
            )

            temporary_path = temporary_file.name

            temporary_file.close()

            image.save(temporary_path)

            segmentation_model, device = (
                load_segmentation_models()
            )

            image_tensor = preprocess_image(
                temporary_path
            )

            processed_image, probabilities, mask = (
                predict_segmentation(
                    segmentation_model,
                    image_tensor,
                    device,
                )
            )


        except Exception as error:

            st.error(
                f"Analysis failed: {error}"
            )

            st.stop()


        finally:

            if temporary_path is not None and os.path.exists(
                temporary_path
            ):

                os.remove(temporary_path)


    # ==================================================
    # RESULTS
    # ==================================================

    st.success(
        "Analysis completed successfully!"
    )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Analysis Results</div>',
        unsafe_allow_html=True,
    )


    # ----------------------------------------------
    # CLASSIFICATION
    # ----------------------------------------------

    class_display_names = {
        "glioma": "Glioma",
        "meningioma": "Meningioma",
        "no_tumor": "No Tumor",
        "pituitary": "Pituitary Tumor",
    }

    display_label = class_display_names.get(
        predicted_label,
        predicted_label,
    )


    st.markdown(
        """
        <div class="result-card">
            <div class="result-label">
                MRI Classification
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-value">
            🧬 {display_label}
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ==================================================
    # SEGMENTATION VISUALIZATION
    # ==================================================

    st.markdown(
        '<div class="section-title">🎯 Tumor Segmentation</div>',
        unsafe_allow_html=True,
    )


    processed_image = (
        processed_image * 255
    ).astype(np.uint8)

    processed_image = Image.fromarray(
        processed_image
    )


    mask_image = (
        mask * 255
    ).astype(np.uint8)

    mask_image = Image.fromarray(
        mask_image
    )


    # Convert MRI to RGB

    mri_rgb = np.array(
        processed_image.convert("RGB")
    )


    # Create red overlay

    overlay = mri_rgb.copy()

    tumor_pixels = mask.astype(bool)

    overlay[tumor_pixels] = [
        255,
        50,
        50,
    ]


    # Blend

    blended = (
        0.65 * mri_rgb +
        0.35 * overlay
    ).astype(np.uint8)


    overlay_image = Image.fromarray(
        blended
    )


    # ----------------------------------------------
    # IMAGE DISPLAY
    # ----------------------------------------------

    image_col1, image_col2, image_col3 = st.columns(
        3,
        gap="medium",
    )


    with image_col1:

        st.image(
            processed_image,
            caption="Preprocessed MRI",
            width=320,
        )


    with image_col2:

        st.image(
            mask_image,
            caption="Predicted Tumor Mask",
            width=320,
        )


    with image_col3:

        st.image(
            overlay_image,
            caption="Tumor Overlay",
            width=320,
        )


    # ==================================================
    # STATISTICS
    # ==================================================

    st.markdown(
        '<div class="section-title">📈 Segmentation Statistics</div>',
        unsafe_allow_html=True,
    )


    tumor_pixels = int(
        np.sum(mask)
    )

    total_pixels = int(
        mask.size
    )

    tumor_percentage = (
        tumor_pixels / total_pixels
    ) * 100


    metric_col1, metric_col2, metric_col3 = st.columns(
        3,
    )


    with metric_col1:

        st.metric(
            "Tumor Pixels",
            f"{tumor_pixels:,}",
        )


    with metric_col2:

        st.metric(
            "Total Image Pixels",
            f"{total_pixels:,}",
        )


    with metric_col3:

        st.metric(
            "Predicted Mask Area",
            f"{tumor_percentage:.2f}%",
        )


    # ==================================================
    # DISCLAIMER
    # ==================================================

    st.warning(
        """
        **Medical Disclaimer**

        NeuroScan AI is an academic machine learning project.
        It is not a medical diagnostic system and should not
        be used as a substitute for professional medical
        advice, diagnosis, or treatment.
        """
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#888888;">
        NeuroScan AI · Brain Tumor Classification
        & Segmentation Project
    </div>
    """,
    unsafe_allow_html=True,
)