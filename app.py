from pathlib import Path
import streamlit as st 
from PIL import Image

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd

css_file = current_dir/"styles"/ "main.css"
resume_file = current_dir/"assets"/"NILANJAN GHOSH.pdf"
profile_pic = current_dir/"assets"/"788.jpg"

PAGE_TITLE = "Digital CV | Nilanjan Ghosh"
PAGE_ICON = ":wave:"
NAME ="Nilanjan Ghosh"
DESCRIPTION ="""
Motivated computer science student specializing in applied machine learning, Python, and Linux, with a focus on crafting data-driven solutions."""
EMAIL ="nghosh0711@gmail.com"
SOCIAL_MEDIA={
    "LinkedIN":"https://www.linkedin.com/in/nilanjan-ghosh-a25747282/",
    "GitHub":"https://github.com/nil0711",
    "X":"https://twitter.com/csnil0711",
    

}
PROJECTS={
    ":speech_balloon: Chat Analysis with Sentiment Analyzer" :"https://miniproject-senti.streamlit.app/",
    ":file_folder: File Manager":"https://github.com/nil0711/CODE/blob/main/tkinter_test/test5.py",
    ":construction: LLM Project":"Currently under development"
}
st.set_page_config(page_title = PAGE_TITLE,page_icon=PAGE_ICON )


with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html = True)
with open(resume_file, "rb") as pdf_file:
    PDF = pdf_file.read()
profile_pic = Image.open(profile_pic)

col1 , col2 = st.columns(2,gap="small")

with col1:
    st.image(profile_pic,width = 220)
with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label="📄 Download Resume",
        data = PDF,
        file_name=resume_file.name,
        mime = "application/octet-sream"
        
    )
    st.write("📨", EMAIL)
    
st.write("#")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platforn, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platforn}]({link})")
st.write('#')

st.subheader("Experience & Qualifications")
st.write("""
        - 🏅 Qualified for JRF in Computer Science in December 2023
        - 🎓 Pursuing a Master's degree in Computer Science from Pondicherry University, expected to graduate in June 2024        
        - 🎓 Earned a Bachelor's degree in Mathematics from St. Xavier's College, Kolkata in May 2020
        - 🔎 Strong problem-solving and analytical skills
        - 💬 Good communication and teamwork skills
         """)
st.write("---")

st.subheader("Skills")
st.write(
    '''
    - 🐍 Python Programming: Numpy, Pandas, sklearn, Pytorch, Keras, Streamlit, Seaborn, Mathplotlib, google.generativeai, openai, tensorflow, nltk, Plotly
    - 🧠 Machine Learning: Decision Tree, Neural Networks, Bayesian Network, Markov Model, Hidden Markov Model, Clustering, Classification, Deep Learning, LLM, NLP
    - 🐧 Linux: Linux System Administration, Shell Scripting, Samba, LVM, Git, C/C++/Java/Python coding debugging in terminal
    - 💾 Databases: MongoDB, MySql 

    '''
)
st.write("---")
st.subheader("Projects & Accomplishments")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")

st.write("---")
