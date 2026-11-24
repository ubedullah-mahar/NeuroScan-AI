import streamlit as st


_STYLE = """
<style>
:root {
  --navy: #10233f;
  --navy-deep: #0b1b31;
  --teal: #18a99a;
  --teal-light: #e6f6f3;
  --ink: #172b45;
  --muted: #6f8093;
  --line: #e6ecf1;
  --paper: #ffffff;
  --canvas: #f4f7fa;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}

.stApp {
  background: var(--canvas);
  color: var(--ink);
}

[data-testid="stHeader"] {
  background: transparent;
}

[data-testid="stMainBlockContainer"] {
  max-width: 1330px;
  padding-top: 1.55rem;
  padding-bottom: 3.5rem;
}

[data-testid="stSidebar"] {
  background: var(--navy-deep);
  border-right: 1px solid rgba(255,255,255,.07);
}

[data-testid="stSidebar"] > div:first-child {
  padding: 1.5rem 1rem;
}

[data-testid="stSidebar"] * {
  color: #eaf2fa;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
  border-radius: 10px;
  padding: .25rem .4rem;
  font-size: .92rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,.07);
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 2px 0 25px;
}

.brand-mark {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 13px;
  color: #fff;
  font: 800 17px 'Manrope', sans-serif;
  background: linear-gradient(140deg, #24c4b1, #147d83);
  box-shadow: 0 7px 18px rgba(11, 164, 151, .24);
}

.brand-mark span {
  font-size: 13px;
  vertical-align: 5px;
  color: #b7fff2;
}

.brand-name {
  color: #fff;
  font: 800 16px 'Manrope', sans-serif;
  letter-spacing: -.5px;
}

.brand-caption {
  color: #91a6be;
  font-size: 10px;
  letter-spacing: 1.65px;
  margin-top: 2px;
}

.brand-main {
  padding-bottom: 20px;
}

.brand-main .brand-mark {
  width: 35px;
  height: 35px;
}

.brand-main .brand-name {
  color: var(--navy);
  font-size: 14px;
}

.brand-main .brand-caption {
  color: #8696a9;
}

.sidebar-label, .eyebrow, .card-kicker, .image-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
}

.sidebar-label {
  color: #7890aa;
  padding: 5px 0 10px 4px;
}

.sidebar-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 28px 4px 10px;
  padding: 12px;
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 10px;
  background: rgba(255,255,255,.035);
  font-size: 12px;
}

.status-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #35cbb2;
  box-shadow: 0 0 0 4px rgba(53,203,178,.12);
}

.sidebar-disclaimer {
  color: #91a3b8 !important;
  margin: 0 8px;
  font-size: 11px;
  line-height: 1.65;
}

.topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topline-badge {
  color: #62768c;
  font-size: 11px;
  border: 1px solid #e0e8ee;
  border-radius: 100px;
  padding: 7px 12px;
  background: rgba(255,255,255,.65);
}

.hero {
  position: relative;
  overflow: hidden;
  min-height: 355px;
  display: flex;
  align-items: center;
  margin: 8px 0 43px;
  padding: 45px 7%;
  border-radius: 22px;
  color: #fff;
  background:
    radial-gradient(ellipse at 87% 35%, rgba(35,178,164,.23), transparent 31%),
    linear-gradient(112deg, #0d2038, #143452 72%, #174e5d);
  box-shadow: 0 18px 42px rgba(17, 47, 76, .12);
}

.hero-copy {
  position: relative;
  z-index: 1;
  max-width: 575px;
}

.hero .eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #a6c4d6;
}

.hero h1 {
  margin: 22px 0 14px;
  color: #fff;
  font: 800 clamp(38px, 5vw, 58px)/1.07 'Manrope', sans-serif;
  letter-spacing: -2.3px;
}

.hero h1 span {
  color: #50d5c0;
}

.hero p {
  max-width: 465px;
  color: #c2d2df;
  font-size: 15px;
  line-height: 1.8;
}

.hero-note {
  margin-top: 24px;
  color: #a3c2d0;
  font-size: 11px;
  letter-spacing: .3px;
}

.hero-art {
  position: absolute;
  width: 330px;
  height: 330px;
  right: 7%;
  top: 50%;
  transform: translateY(-50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(28,186,171,.12), transparent 67%);
}

.scan-ring {
  position: absolute;
  inset: 34px;
  border: 1px solid rgba(126,232,218,.22);
  border-radius: 50%;
}

.ring-two {
  inset: 63px;
  border-color: rgba(126,232,218,.14);
}

.scan-core {
  position: absolute;
  inset: 94px;
  display: grid;
  place-content: center;
  border: 1px solid rgba(114,231,214,.34);
  border-radius: 50%;
  color: #e4fffa;
  font: 800 57px 'Manrope', sans-serif;
  background: radial-gradient(circle at 30% 25%, #2f8888, #123f56 76%);
  box-shadow: 0 0 50px rgba(24,194,175,.22), inset 0 0 24px rgba(101,243,216,.1);
}

.scan-core span {
  color: #66e4ce;
  font-size: 20px;
  vertical-align: 22px;
  margin-left: -13px;
}

.scan-caption {
  position: absolute;
  right: 16px;
  bottom: 60px;
  color: #a1c9d1;
  font-size: 9px;
  letter-spacing: 2px;
}

.section-heading {
  margin: 0 0 18px;
}

.section-heading .eyebrow {
  color: #179b91;
  margin-bottom: 8px;
}

.section-heading h2 {
  margin: 0;
  color: var(--navy);
  font: 750 23px 'Manrope', sans-serif;
  letter-spacing: -.7px;
}

.section-heading p {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.6;
}

.feature-card, .about-card {
  min-height: 231px;
  padding: 25px 26px 20px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--paper);
  box-shadow: 0 8px 22px rgba(25, 50, 75, .035);
}

.feature-icon {
  width: 39px;
  height: 39px;
  display: grid;
  place-items: center;
  margin-bottom: 17px;
  border-radius: 12px;
  font-size: 19px;
  font-weight: 600;
}

.icon-classify {
  color: #137f8f;
  background: #e7f4f6;
}

.icon-segment {
  color: #0a9b8c;
  background: #e6f7f2;
}

.card-kicker {
  color: #8191a2;
}

.feature-card h3, .about-card h3 {
  margin: 9px 0;
  color: var(--navy);
  font: 750 20px/1.3 'Manrope', sans-serif;
  letter-spacing: -.45px;
}

.feature-card p, .about-card p {
  margin: 0;
  color: #708197;
  font-size: 13px;
  line-height: 1.75;
}

.feature-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 18px;
  padding-top: 13px;
  border-top: 1px solid #edf1f4;
  color: #5b7788;
  font-size: 11px;
  font-weight: 600;
}

.stButton > button {
  min-height: 43px;
  border: 1px solid #dfe8ee;
  border-radius: 10px;
  color: var(--navy);
  background: #fff;
  font-weight: 650;
  transition: all .18s ease;
}

.stButton > button:hover {
  border-color: #1aa99b;
  color: #087c75;
  box-shadow: 0 5px 15px rgba(13, 135, 125, .1);
}

.stButton > button[kind="primary"] {
  border: 1px solid #118f87;
  color: #fff;
  background: linear-gradient(110deg, #118f87, #16aa9b);
}

.stButton > button[kind="primary"]:hover {
  border-color: #08796f;
  color: #fff;
  background: #087f77;
}

.info-strip {
  display: flex;
  align-items: center;
  gap: 13px;
  margin: 27px 0 43px;
  padding: 16px 19px;
  border: 1px solid #dcece9;
  border-radius: 12px;
  background: #f0faf8;
}

.info-mark {
  width: 24px;
  height: 24px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #138b80;
  background: #d7f0eb;
  font: 700 13px Georgia, serif;
}

.info-strip strong, .info-strip span {
  display: block;
}

.info-strip strong {
  color: #22504f;
  font-size: 12px;
}

.info-strip span {
  margin-top: 3px;
  color: #62817f;
  font-size: 11px;
}

.tech-row {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin: 15px 0 30px;
}

.tech-row span {
  padding: 8px 13px;
  border: 1px solid #e0e8ed;
  border-radius: 100px;
  color: #51677c;
  background: #fff;
  font-size: 11px;
  font-weight: 600;
}

.page-heading {
  padding: 13px 0 25px;
}

.page-heading .eyebrow {
  color: #169b90;
}

.page-heading h1 {
  margin: 9px 0 7px;
  color: var(--navy);
  font: 800 clamp(26px, 3.5vw, 36px) 'Manrope', sans-serif;
  letter-spacing: -1.2px;
}

.page-heading p {
  margin: 0;
  color: var(--muted);
  font-size: 14px;
}

.stFileUploader [data-testid="stFileUploaderDropzone"] {
  min-height: 175px;
  border: 1px dashed #b9cbd4;
  border-radius: 14px;
  background: #fbfdfe;
}

.stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
  border-color: #22a99b;
  background: #f4fcfa;
}

.stFileUploader [data-testid="stFileUploaderDropzone"] button {
  border-radius: 8px;
}

[data-testid="stImage"] {
  overflow: hidden;
  border: 1px solid #e4eaef;
  border-radius: 12px;
  background: #fff;
}

.empty-preview {
  min-height: 290px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px dashed #d2dce4;
  border-radius: 14px;
  color: #8191a2;
  background: linear-gradient(145deg, #fff, #f8fafc);
}

.empty-preview .empty-cross {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  margin-bottom: 13px;
  border-radius: 13px;
  color: #149b8f;
  background: #e8f7f4;
  font-size: 26px;
  font-weight: 300;
}

.empty-preview strong {
  color: #4a6074;
  font-size: 13px;
}

.empty-preview span {
  margin-top: 5px;
  font-size: 11px;
}

.result-divider {
  height: 1px;
  margin: 32px 0 27px;
  background: #e3eaf0;
}

.result-card {
  min-height: 170px;
  padding: 21px 23px;
  border: 1px solid #dcefe9;
  border-radius: 14px;
  background: linear-gradient(135deg, #fff, #f5fcfa);
}

.result-symbol {
  width: 29px;
  height: 29px;
  display: grid;
  place-items: center;
  margin-bottom: 13px;
  border-radius: 50%;
  color: #108879;
  background: #dcf4ed;
  font-weight: 700;
}

.result-label {
  margin-top: 8px;
  color: var(--navy);
  font: 800 27px 'Manrope', sans-serif;
  text-transform: capitalize;
}

.result-subtitle {
  margin-top: 4px;
  color: #77889a;
  font-size: 11px;
}

.result-note, .disclaimer {
  height: 100%;
  padding: 21px 23px;
  border: 1px solid #e3eaf0;
  border-radius: 14px;
  background: #fff;
}

.result-note strong, .disclaimer strong {
  color: var(--navy);
  font-size: 13px;
}

.result-note p, .disclaimer p {
  margin: 8px 0 14px;
  color: #667b8f;
  font-size: 12px;
  line-height: 1.75;
}

.result-note span {
  color: #8392a1;
  font-size: 10px;
}

.image-label {
  padding: 0 0 8px 2px;
  color: #697e91;
}

[data-testid="stMetric"] {
  padding: 14px 16px;
  border: 1px solid #e3eaf0;
  border-radius: 12px;
  background: #fff;
}

.about-intro {
  display: flex;
  align-items: flex-start;
  gap: 21px;
  margin: 0 0 30px;
  padding: 27px;
  border: 1px solid #e2eaf0;
  border-radius: 17px;
  background: #fff;
}

.about-intro-mark {
  flex: 0 0 53px;
  height: 53px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  color: #fff;
  background: linear-gradient(140deg, #24c4b1, #147d83);
  font: 800 23px 'Manrope', sans-serif;
}

.about-intro-mark span {
  color: #b7fff2;
  font-size: 11px;
  vertical-align: 8px;
  margin-left: -7px;
}

.about-intro h3 {
  margin: 6px 0 7px;
  color: var(--navy);
  font: 750 22px 'Manrope', sans-serif;
}

.about-intro p {
  max-width: 830px;
  margin: 0;
  color: #6f8093;
  font-size: 13px;
  line-height: 1.8;
}

.about-card {
  min-height: 215px;
  margin-bottom: 37px;
}

.about-card h3 {
  margin-top: 13px;
}

.workflow-step {
  min-height: 142px;
  padding: 17px;
  border: 1px solid #e3eaf0;
  border-radius: 13px;
  background: #fff;
}

.workflow-step span {
  display: block;
  margin-bottom: 13px;
  color: #169b90;
  font: 750 12px 'Manrope', sans-serif;
}

.workflow-step strong {
  color: var(--navy);
  font-size: 13px;
}

.workflow-step p {
  margin: 6px 0 0;
  color: #78899a;
  font-size: 11px;
  line-height: 1.6;
}

.disclaimer {
  margin-top: 22px;
  border-color: #eadfcf;
  background: #fffcf6;
}

.disclaimer strong {
  color: #765d35;
}

.disclaimer p {
  margin-bottom: 0;
  color: #806f56;
}

.app-footer {
  margin-top: 45px;
  padding-top: 16px;
  border-top: 1px solid #e3eaf0;
  color: #8a98a6;
  font-size: 10px;
}

@media (max-width: 760px) {
  .hero {
    min-height: 315px;
    padding: 34px 26px;
  }
  .hero-art {
    width: 215px;
    height: 215px;
    right: -72px;
    opacity: .46;
  }
  .scan-core {
    inset: 61px;
    font-size: 40px;
  }
  .scan-ring {
    inset: 20px;
  }
  .ring-two {
    inset: 39px;
  }
  .scan-caption {
    display: none;
  }
  .about-intro {
    padding: 20px;
  }
}
</style>
"""


def apply_styles() -> None:
    st.markdown(_STYLE, unsafe_allow_html=True)


def render_brand(compact: bool = False) -> None:
    brand_class = "brand-lockup"
    if compact:
        brand_class += " brand-sidebar"
    else:
        brand_class += " brand-main"

    st.markdown(
        f"""
        <div class="{brand_class}">
          <div class="brand-mark">N<span>+</span></div>
          <div>
            <div class="brand-name">NeuroScan-AI</div>
            <div class="brand-caption">MRI ANALYSIS WORKSPACE</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, description: str, eyebrow: str) -> None:
    st.markdown(
        f"""
        <div class="page-heading">
          <div class="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(
    title: str,
    description: str = "",
    eyebrow: str = "",
) -> None:
    eyebrow_markup = f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ""
    description_markup = f"<p>{description}</p>" if description else ""
    st.markdown(
        f"""
        <div class="section-heading">
          {eyebrow_markup}
          <h2>{title}</h2>
          {description_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        '<div class="app-footer">NeuroScan-AI · Educational and research use only · '
        'Not for clinical decision-making</div>',
        unsafe_allow_html=True,
    )
