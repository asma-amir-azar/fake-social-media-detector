import streamlit as st
import pickle
import base64
from pathlib import Path

# -------- PAGE CONFIG -------- #
st.set_page_config(
    page_title="Instagram Fake Account Detector",
    page_icon="📷",
    layout="wide"
)

# -------- STYLE -------- #
st.markdown("""
<style>
.stApp {
    background: linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);
}

/* Remove Streamlit padding */
.main .block-container {
    padding: 0rem;
}

            /* TOP-LEFT HEADER BELOW TITLE */
.top-left-header {
    text-align: left;
    color: white;
    font-weight: bold;
    font-size: 16px;
    line-height: 1.2;
    padding: 8px 12px;
    background-color: rgba(0,0,0,0.6);  /* dark semi-transparent */
    border-radius: 8px;
    display: inline-block;
    margin: 10px 0 10px 10px;
}
/* LEFT PANEL */
.left-panel {
    width: 100%;
    height: 1013px;              
    background-color: white; 
    padding: 20px;
    border-radius: 15px;
    color: black;
    overflow-y: auto;   
}

/* LEFT PANEL TEXT */
.left-panel h1, .left-panel h2, .left-panel h3, .left-panel h4 {
    color: black;
}

.left-panel p, .left-panel li {
    color: black;
    font-size: 14px;
}

/* RESULT BOX */
.result-box {
    background:white;
    color:black;
    padding:20px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    margin-top:20px;
}

/* Buttons style */
.stButton>button {
    background-color: white;
    color: #dc2743;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

.stNumberInput input, .stSelectbox select {
    background-color: white;  
    border: 1px solid white;  
    border-radius: 8px;
    color: black;               
}
</style>
""", unsafe_allow_html=True)

# -------- LOAD MODEL -------- #
with open("model_forest.pkl", "rb") as file:
    model = pickle.load(file)

# -------- HELPER FUNCTION -------- #
def image_to_html(path):
    file = Path(path)
    if file.exists():
        with open(file, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{data}" style="width:100%;margin-bottom:10px;">'
    else:
        return f"<p>{path} not found</p>"

# -------- TITLE FULL WIDTH -------- #
st.markdown("<h1 style='text-align:center;color:white;padding:20px 0;'>📷 Instagram Fake Account Detector</h1>", unsafe_allow_html=True)
st.write("")  # spacing
# -------- HEADER BELOW TITLE -------- #
st.markdown("""
<div class="top-left-header">
    <div>1i1w 2025-2026 </div>
    <div>Asma Amir Azar</div>
</div>
""", unsafe_allow_html=True)
# -------- LEFT + RIGHT COLUMNS BELOW TITLE -------- #
left_col, right_col = st.columns([4,6])  # left 40%, right 60%

# -------- LEFT PANEL -------- #
with left_col:
    html_content = """
    <div class="left-panel">
    <h4>About the Model</h4>
    <p>This machine Learning model detects fake Instagram accounts by some features of the account.</p>
    <p>These are the features we used in training :</p>
    <ul>
        <li>Profile picture presence</li>
        <li>Username numeric patterns</li>
        <li>Full name similarity</li>
        <li>Description length</li>
        <li>External URL presence</li>
        <li>Private account</li>
        <li>Number of posts</li>
        <li>Followers count</li>
        <li>Following count</li>
    </ul>
    <p>We have analyzied the dataset and below are some of the data visualization related to the dataset :</p>
    """
    images = [
        "profile pic.png",
        "account type.png",
        "name and username.png",
        "external url.png",
        "account verification.png",
        "number of posts.png",
        "correlation.png",
        "model_accuracy_comparison.png"  # last image
    ]

    # Insert explanation before the last image
    for i, img in enumerate(images):
        if i == len(images) - 1:
            html_content += """
            <p>These are the models that we have trained on the dataset. As it is obvious, 
            the <b>Random Forest model</b> has the highest accuracy of <b>99%</b>, 
            so we use this as the final model.</p>
            """
        html_content += image_to_html(img)

    html_content += "</div>"

    st.markdown(html_content, unsafe_allow_html=True)

# -------- RIGHT PANEL -------- #
with right_col:
    st.write("Enter account details below:")

    profile_pic_state = st.selectbox("Profile Picture", ["Yes","No"])
    profile_pic = 1 if profile_pic_state == "Yes" else 0
    nums_length_username = st.number_input("Numbers ÷ Length of Username", min_value=0.0, step=0.01)
    fullname_words = st.number_input("Fullname Words", min_value=0)
    nums_length_fullname = st.number_input("Numbers ÷ Length of Fullname", min_value=0.0, step=0.01)
    name_equals_username_state = st.selectbox("Name Equals Username", ["Yes","No"])
    name_equals_username = 1 if name_equals_username_state == "Yes" else 0
    description_length = st.number_input("Description Length", min_value=0)
    external_url_state = st.selectbox("External URL", ["Yes","No"])
    external_url = 1 if external_url_state == "Yes" else 0
    private_state = st.selectbox("Private Account", ["Yes","No"])
    private = 1 if private_state == "Yes" else 0
    posts = st.number_input("Number of Posts", min_value=0)
    followers = st.number_input("Number of Followers", min_value=0)
    follows = st.number_input("Number of Follows", min_value=0)

    if st.button("Predict"):
        features = [[
            profile_pic,
            nums_length_username,
            fullname_words,
            nums_length_fullname,
            name_equals_username,
            description_length,
            external_url,
            private,
            posts,
            followers,
            follows
        ]]
        prediction = model.predict(features)

        if prediction[0] == 1:
            st.markdown('<div class="result-box">⚠️ This account is predicted to be FAKE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box">✅ This account is predicted to be REAL</div>', unsafe_allow_html=True)