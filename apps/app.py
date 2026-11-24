from __future__ import annotations

import hashlib
import sys
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui_components import (  # noqa: E402
    apply_styles,
    render_brand,
    render_footer,
    render_page_header,
    render_section_heading,
)

PAGES = (
    "Dashboard",
    "Brain Tumor Classification",
    "Brain Tumor Segmentation",
    "About NeuroScan-AI",
)
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png", "bmp", "tif", "tiff"]


@st.cache_resource(show_spinner=False)
def _classification_resources():
    from src.classification.inference import (
        load_classifier,
        load_feature_extractor,
    )

    feature_extractor, transform = load_feature_extractor()
    classifier = load_classifier()
    return feature_extractor, transform, classifier


@st.cache_resource(show_spinner=False)
def _segmentation_resources():
    from src.segmentation.inference import load_segmentation_model

    return load_segmentation_model()


def _image_fingerprint(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()


def _open_uploaded_image(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def _go_to_page(page: str) -> None:
    st.session_state["navigation"] = page


def _render_dashboard() -> None:
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy">
            <div class="eyebrow"><span class="status-dot"></span> RESEARCH WORKSPACE</div>
            <h1>Clarity for every<br><span>scan.</span></h1>
            <p>Explore brain MRI images with focused AI tools for tumor
            classification and segmentation.</p>
            <div class="hero-note">A research interface for image analysis</div>
          </div>
          <div class="hero-art" aria-hidden="true">
            <div class="scan-ring ring-one"></div>
            <div class="scan-ring ring-two"></div>
            <div class="scan-core">N<span>+</span></div>
            <div class="scan-caption">NEUROSCAN / 01</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    render_section_heading(
        "Analysis workspace",
        "Choose a tool to explore an MRI image.",
        eyebrow="YOUR TOOLS",
    )
    classification, segmentation = st.columns(2, gap="large")
    with classification:
        st.markdown(
            """
            <article class="feature-card">
              <div class="feature-icon icon-classify">✳</div>
              <div class="card-kicker">01 / CLASSIFICATION</div>
              <h3>Brain Tumor<br>Classification</h3>
              <p>Generate a predicted class label for an uploaded MRI image.</p>
              <div class="feature-meta"><span>Image-level analysis</span><span>→</span></div>
            </article>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Open classification",
            key="open_classification",
            type="primary",
            use_container_width=True,
            on_click=_go_to_page,
            args=("Brain Tumor Classification",),
        )

    with segmentation:
        st.markdown(
            """
            <article class="feature-card">
              <div class="feature-icon icon-segment">◉</div>
              <div class="card-kicker">02 / SEGMENTATION</div>
              <h3>Brain Tumor<br>Segmentation</h3>
              <p>Visualize the model's predicted mask alongside the MRI input.</p>
              <div class="feature-meta"><span>Pixel-level visualization</span><span>→</span></div>
            </article>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "Open segmentation",
            key="open_segmentation",
            use_container_width=True,
            on_click=_go_to_page,
            args=("Brain Tumor Segmentation",),
        )

    st.markdown(
        """
        <div class="info-strip">
          <div class="info-mark">i</div>
          <div><strong>Designed for exploration</strong>
          <span>Outputs are model-generated research results, not a medical diagnosis.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_heading(
        "Built with established tools",
        "A focused interface connecting computer vision models with clear visual outputs.",
        eyebrow="TECHNOLOGY",
    )
    st.markdown(
        """
        <div class="tech-row">
          <span>Python</span><span>Streamlit</span><span>PyTorch</span>
          <span>EfficientNet-B0</span><span>scikit-learn</span><span>U-Net</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_classification() -> None:
    render_page_header(
        "Brain Tumor Classification",
        "Upload an MRI image to view the classifier's predicted class.",
        eyebrow="ANALYSIS / 01",
    )
    uploader_column, preview_column = st.columns([0.92, 1.08], gap="large")
    with uploader_column:
        render_section_heading(
            "Add an MRI image",
            "Select a file or drag it into the upload area.",
            eyebrow="IMAGE INPUT",
        )
        uploaded_file = st.file_uploader(
            "Upload MRI image",
            type=SUPPORTED_IMAGE_TYPES,
            key="classification_upload",
            help="Supported formats: JPG, JPEG, PNG, BMP, TIF, TIFF.",
            label_visibility="collapsed",
        )
        st.caption("Supported formats: JPG, JPEG, PNG, BMP, TIF, TIFF")

    image = None
    image_bytes = uploaded_file.getvalue() if uploaded_file is not None else None
    image_id = _image_fingerprint(image_bytes) if image_bytes is not None else None
    with preview_column:
        render_section_heading("Image preview", "Review the selected image before analysis.")
        if image_bytes is None:
            st.markdown(
                '<div class="empty-preview"><div class="empty-cross">+</div>'
                '<strong>Your image will appear here</strong>'
                '<span>Upload an MRI image to get started</span></div>',
                unsafe_allow_html=True,
            )
        else:
            try:
                image = _open_uploaded_image(image_bytes)
            except (UnidentifiedImageError, OSError, ValueError) as error:
                st.error(f"This file could not be read as an image: {error}")
            else:
                st.image(image, use_container_width=True)
                st.caption(uploaded_file.name)

    if image is None:
        st.info("Add a supported image to enable classification.")
    elif st.button(
        "Run classification",
        key="run_classification",
        type="primary",
        use_container_width=True,
    ):
        try:
            with st.spinner("Preparing the analysis..."):
                feature_extractor, transform, classifier = _classification_resources()
                from src.classification.inference import predict_classification

                result = predict_classification(
                    image,
                    feature_extractor,
                    transform,
                    classifier,
                )
            st.session_state["classification_result"] = {
                "image_id": image_id,
                "predicted_label": result["predicted_label"],
                "predicted_class": result["predicted_class"],
            }
        except (FileNotFoundError, ImportError, OSError, RuntimeError, ValueError) as error:
            st.session_state.pop("classification_result", None)
            st.error(f"Classification could not be completed: {error}")

    result = st.session_state.get("classification_result")
    if result and result["image_id"] == image_id:
        st.markdown('<div class="result-divider"></div>', unsafe_allow_html=True)
        render_section_heading(
            "Classification result",
            "The model's output for this image.",
            eyebrow="ANALYSIS COMPLETE",
        )
        result_column, detail_column = st.columns([1, 1.2], gap="large")
        with result_column:
            st.markdown(
                f"""
                <div class="result-card">
                  <div class="result-symbol">✓</div>
                  <div class="card-kicker">PREDICTED CLASS</div>
                  <div class="result-label">{result["predicted_label"].replace("_", " ").title()}</div>
                  <div class="result-subtitle">Model class index {result["predicted_class"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with detail_column:
            st.markdown(
                """
                <div class="result-note">
                  <strong>About this result</strong>
                  <p>The existing classifier returns a predicted class and raw decision
                  scores. It does not provide a calibrated confidence score, so no
                  confidence percentage is displayed.</p>
                  <span>Research output only · Not for clinical decision-making</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_segmentation() -> None:
    render_page_header(
        "Brain Tumor Segmentation",
        "View a predicted segmentation mask and its overlay on the MRI input.",
        eyebrow="ANALYSIS / 02",
    )
    upload_column, preview_column = st.columns([0.92, 1.08], gap="large")
    with upload_column:
        render_section_heading(
            "Add an MRI image",
            "Select a file or drag it into the upload area.",
            eyebrow="IMAGE INPUT",
        )
        uploaded_file = st.file_uploader(
            "Upload MRI image",
            type=SUPPORTED_IMAGE_TYPES,
            key="segmentation_upload",
            help="Supported formats: JPG, JPEG, PNG, BMP, TIF, TIFF.",
            label_visibility="collapsed",
        )
        st.caption("Supported formats: JPG, JPEG, PNG, BMP, TIF, TIFF")

    image_bytes = uploaded_file.getvalue() if uploaded_file is not None else None
    image_id = _image_fingerprint(image_bytes) if image_bytes is not None else None
    image = None
    with preview_column:
        render_section_heading("Image preview", "Original uploaded MRI image.")
        if image_bytes is None:
            st.markdown(
                '<div class="empty-preview"><div class="empty-cross">+</div>'
                '<strong>Your image will appear here</strong>'
                '<span>Upload an MRI image to get started</span></div>',
                unsafe_allow_html=True,
            )
        else:
            try:
                image = _open_uploaded_image(image_bytes)
            except (UnidentifiedImageError, OSError, ValueError) as error:
                st.error(f"This file could not be read as an image: {error}")
            else:
                st.image(image, use_container_width=True)
                st.caption(uploaded_file.name)

    if image is None:
        st.info("Add a supported image to enable segmentation.")
    elif st.button(
        "Run segmentation",
        key="run_segmentation",
        type="primary",
        use_container_width=True,
    ):
        try:
            with st.spinner("Generating the segmentation..."):
                from src.segmentation.inference import (
                    predict_segmentation,
                    preprocess_image,
                )

                model, device = _segmentation_resources()
                image_tensor = preprocess_image(BytesIO(image_bytes))
                model_image, probabilities, predicted_mask = predict_segmentation(
                    model,
                    image_tensor,
                    device,
                )
            st.session_state["segmentation_result"] = {
                "image_id": image_id,
                "image": model_image,
                "probabilities": probabilities,
                "mask": predicted_mask,
            }
        except (FileNotFoundError, ImportError, OSError, RuntimeError, ValueError) as error:
            st.session_state.pop("segmentation_result", None)
            st.error(f"Segmentation could not be completed: {error}")

    result = st.session_state.get("segmentation_result")
    if result and result["image_id"] == image_id:
        import numpy as np

        model_image = np.asarray(result["image"], dtype=np.float32)
        predicted_mask = np.asarray(result["mask"]) >= 0.5
        probabilities = np.asarray(result["probabilities"], dtype=np.float32)
        model_image = np.clip(model_image, 0.0, 1.0)
        base = np.repeat(model_image[..., np.newaxis], 3, axis=2)
        overlay = base.copy()
        overlay[predicted_mask] = (
            0.38 * overlay[predicted_mask]
            + 0.62 * np.array([0.95, 0.25, 0.30], dtype=np.float32)
        )
        tumor_pixels = int(predicted_mask.sum())
        coverage = float(predicted_mask.mean() * 100)

        st.markdown('<div class="result-divider"></div>', unsafe_allow_html=True)
        render_section_heading(
            "Segmentation result",
            "Compare the uploaded image, predicted mask, and highlighted overlay.",
            eyebrow="ANALYSIS COMPLETE",
        )
        original_column, input_column, mask_column, overlay_column = st.columns(
            4,
            gap="medium",
        )
        with original_column:
            st.markdown('<div class="image-label">ORIGINAL MRI</div>', unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        with input_column:
            st.markdown('<div class="image-label">MODEL INPUT</div>', unsafe_allow_html=True)
            st.image(model_image, clamp=True, use_container_width=True)
        with mask_column:
            st.markdown('<div class="image-label">PREDICTED MASK</div>', unsafe_allow_html=True)
            st.image(predicted_mask.astype(np.uint8) * 255, clamp=True, use_container_width=True)
        with overlay_column:
            st.markdown('<div class="image-label">MASK OVERLAY</div>', unsafe_allow_html=True)
            st.image(overlay, clamp=True, use_container_width=True)

        metric_column, note_column = st.columns([0.8, 1.2], gap="large")
        with metric_column:
            st.metric("Predicted mask pixels", f"{tumor_pixels:,}")
            st.metric("Mask coverage", f"{coverage:.2f}%")
        with note_column:
            st.markdown(
                """
                <div class="result-note">
                  <strong>Interpreting the visualization</strong>
                  <p>Coverage describes the share of pixels marked by this prediction;
                  it is not an accuracy or evaluation score. No ground-truth evaluation
                  metrics are returned by the current inference interface.</p>
                  <span>Research output only · Not for clinical decision-making</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with st.expander("View probability map"):
            st.image(
                np.clip(probabilities, 0.0, 1.0),
                clamp=True,
                use_container_width=True,
                caption="Per-pixel model probabilities before thresholding.",
            )


def _render_about() -> None:
    render_page_header(
        "About NeuroScan-AI",
        "A research-oriented interface for exploring brain MRI classification and segmentation.",
        eyebrow="PROJECT OVERVIEW",
    )
    st.markdown(
        """
        <div class="about-intro">
          <div class="about-intro-mark">N<span>+</span></div>
          <div><div class="card-kicker">NEUROSCAN-AI</div>
          <h3>Two ways to explore an image.</h3>
          <p>NeuroScan-AI brings together image-level classification and
          pixel-level segmentation workflows in one focused workspace. Upload
          an MRI image, review the model output, and use the visualizations
          as part of research or educational exploration.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    overview_columns = st.columns(2, gap="large")
    with overview_columns[0]:
        st.markdown(
            """
            <div class="about-card">
              <div class="card-kicker">01 / CLASSIFICATION</div>
              <h3>Image-level prediction</h3>
              <p>The classifier extracts image features with an EfficientNet-B0
              feature extractor and passes them to the existing SVM classifier.
              The interface displays the predicted class label. The current
              inference output does not provide calibrated confidence.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with overview_columns[1]:
        st.markdown(
            """
            <div class="about-card">
              <div class="card-kicker">02 / SEGMENTATION</div>
              <h3>Pixel-level visualization</h3>
              <p>The existing U-Net inference workflow preprocesses an image,
              predicts per-pixel probabilities, and returns a binary mask. The
              interface presents the mask and an overlay with the model input.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_heading(
        "From image to visualization",
        "A simple flow from upload to model output.",
        eyebrow="SYSTEM WORKFLOW",
    )
    steps = st.columns(4, gap="medium")
    for index, (title, description) in enumerate(
        (
            ("Upload", "Choose a supported brain MRI image."),
            ("Prepare", "Use the existing model-specific preprocessing."),
            ("Analyze", "Run classification or segmentation inference."),
            ("Review", "Inspect the label, mask, and visualization."),
        ),
        start=1,
    ):
        with steps[index - 1]:
            st.markdown(
                f"""
                <div class="workflow-step">
                  <span>0{index}</span><strong>{title}</strong><p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_heading(
        "Technology",
        "The UI connects to the project's existing model implementations.",
        eyebrow="STACK",
    )
    st.markdown(
        """
        <div class="tech-row">
          <span>Python</span><span>Streamlit</span><span>PyTorch</span>
          <span>Torchvision</span><span>EfficientNet-B0</span>
          <span>scikit-learn SVM</span><span>U-Net</span>
        </div>
        <div class="disclaimer">
          <strong>Educational and research use only</strong>
          <p>This application is not a medical device and does not provide a
          diagnosis, treatment recommendation, or substitute for professional
          medical judgment. Model outputs may be incorrect and must not be used
          to make clinical decisions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="NeuroScan-AI | MRI Analysis",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_styles()

    with st.sidebar:
        render_brand(compact=True)
        st.markdown('<div class="sidebar-label">WORKSPACE</div>', unsafe_allow_html=True)
        selected_page = st.radio(
            "Navigation",
            PAGES,
            key="navigation",
            label_visibility="collapsed",
        )
        st.markdown(
            """
            <div class="sidebar-status"><span class="status-dot"></span>
            Research interface</div>
            <div class="sidebar-disclaimer">For educational and research use.
            Not for clinical decision-making.</div>
            """,
            unsafe_allow_html=True,
        )

    render_brand()
    if selected_page == "Dashboard":
        _render_dashboard()
    elif selected_page == "Brain Tumor Classification":
        _render_classification()
    elif selected_page == "Brain Tumor Segmentation":
        _render_segmentation()
    else:
        _render_about()
    render_footer()


if __name__ == "__main__":
    main()
