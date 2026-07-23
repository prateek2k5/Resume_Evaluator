# ================================
# 🤖 AI Resume Evaluator (Streamlit)
# ================================

# Streamlit UI banane ke liye
import streamlit as st

# Temporary files create karne ke liye
import tempfile

# File paths handle karne ke liye
from pathlib import Path

# Resume_Evaluator.py se required functions import kar rahe hain
from Resume_Evaluator import (
    read_resume,
    read_pdf,
    read_docx,
    parse_resume,
    final_score,
    parse_job_description
)

# ================================
# Streamlit Page Configuration
# ================================

st.set_page_config(
    page_title="AI Resume Evaluator",   # Browser tab title
    page_icon="🤖",                     # Browser tab icon
    layout="wide"                       # Full width layout
)

# ================================
# Main Heading
# ================================

st.title("🤖 AI Resume Evaluator")

st.markdown(
    """
### LLM Powered ATS Resume Screening System

Upload a Job Description and Multiple Resumes to rank candidates using AI.
"""
)

st.divider()

# ================================
# Upload Job Description
# ================================

st.subheader("📄 Upload Job Description")

job_file = st.file_uploader(
    "Upload Job Description (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"],
    key="job_file"
)

st.divider()

# ================================
# Upload Resume
# ================================

st.subheader("📂 Upload Candidate Resumes")

resume_files = st.file_uploader(
    "Upload Multiple Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    key="resume_files"
)

st.divider()

# ================================
# Evaluate Button
# ================================

if st.button("🚀 Evaluate Resumes", use_container_width=True):

    # JD upload hui ya nahi check kar rahe hain
    if job_file is None:

        st.error("❌ Please upload a Job Description.")

        st.stop()

    # Resume upload hua ya nahi check kar rahe hain
    if len(resume_files) == 0:

        st.error("❌ Please upload at least one Resume.")

        st.stop()

    # Upload successful message
    st.success(f"✅ {job_file.name} uploaded successfully.")

    st.success(f"✅ {len(resume_files)} Resume(s) uploaded successfully.")

    st.divider()

    # =====================================
    # Job Description Read Kar Rahe Hain
    # =====================================

    # Uploaded JD ko temporary file me save kar rahe hain
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=Path(job_file.name).suffix
    ) as temp_jd:

        temp_jd.write(job_file.getbuffer())

        temp_jd_path = Path(temp_jd.name)

    # File extension check kar rahe hain
    if temp_jd_path.suffix.lower() == ".pdf":

        # PDF read kar rahe hain
        job_description = read_pdf(temp_jd_path)

    elif temp_jd_path.suffix.lower() == ".docx":

        # DOCX read kar rahe hain
        job_description = read_docx(temp_jd_path)

    else:

        # TXT read kar rahe hain
        job_description = temp_jd_path.read_text(
            encoding="utf-8"
        )

    # JD ko LLM se parse kar rahe hain
    with st.spinner("🤖 Understanding Job Description..."):

        job = parse_job_description(job_description)

    st.success("✅ Job Description Parsed Successfully!")

    st.divider()

    # =====================================
    # Progress Bar
    # =====================================

    progress = st.progress(0)

    status = st.empty()

    # Sare candidate results store honge
    all_results = []

    # Total uploaded resumes
    total_files = len(resume_files)

    # =====================================
    # Resume Processing Start
    # =====================================

    for index, uploaded_file in enumerate(resume_files):

        # Current processing status
        status.info(
            f"📄 Processing {uploaded_file.name}..."
        )

        # Resume ko temporary file me save kar rahe hain
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(uploaded_file.name).suffix
        ) as temp_resume:

            temp_resume.write(
                uploaded_file.getbuffer()
            )

            temp_resume_path = Path(temp_resume.name)

        # Resume text read kar rahe hain
        resume_text = read_resume(temp_resume_path)

        # Resume parse kar rahe hain
        parsed_resume = parse_resume(resume_text)

        # Resume aur JD compare kar rahe hain
        result = final_score(
            job,
            parsed_resume
        )

        # Candidate ka complete result save kar rahe hain
        all_results.append({

            "Candidate": parsed_resume.name,

            "Score": result.score,

            "Matching Skills": ", ".join(
                result.details.get(
                    "matching_skills",
                    []
                )
            ),

            "Missing Skills": ", ".join(
                result.details.get(
                    "missing_important_skills",
                    []
                )
            ),

            "Experience": result.details.get(
                "experience_requirement_met"
            ),

            "Verdict": result.details.get(
                "final_verdict"
            ),

            # Future dashboard ke liye
            "Details": result.details,

            "Resume": parsed_resume

        })

        # Progress bar update
        progress.progress(
            (index + 1) / total_files
        )

    # Processing complete
    status.success(
        "🎉 All resumes evaluated successfully!"
    )

        # =====================================
    # Results ko Score ke basis par sort kar rahe hain
    # =====================================

    all_results.sort(
        key=lambda candidate: candidate["Score"],
        reverse=True
    )

    # =====================================
    # Dashboard Metrics
    # =====================================

    st.divider()

    st.subheader("📊 Dashboard")

    # Dashboard values calculate kar rahe hain
    total_candidates = len(all_results)

    highest_score = all_results[0]["Score"]

    lowest_score = all_results[-1]["Score"]

    average_score = round(
        sum(candidate["Score"] for candidate in all_results)
        / total_candidates,
        2
    )

    # Dashboard ke liye 4 columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Candidates",
            total_candidates
        )

    with col2:

        st.metric(
            "🏆 Highest Score",
            f"{highest_score}%"
        )

    with col3:

        st.metric(
            "📉 Lowest Score",
            f"{lowest_score}%"
        )

    with col4:

        st.metric(
            "📊 Average Score",
            f"{average_score}%"
        )

    st.divider()

    # =====================================
    # Top Candidate Card
    # =====================================

    st.subheader("🥇 Best Candidate")

    best = all_results[0]

    st.success(
        f"""
### 👤 {best['Candidate']}

🏆 Match Score : **{best['Score']}%**

📝 Verdict : **{best['Verdict']}**
"""
    )

    st.divider()

    # =====================================
    # Ranking Table Banane Ke Liye
    # =====================================

    table_data = []

    for rank, candidate in enumerate(all_results, start=1):

        table_data.append({

            "Rank": rank,

            "Candidate": candidate["Candidate"],

            "Score": f"{candidate['Score']}%",

            "Matching Skills": candidate["Matching Skills"],

            "Missing Skills": candidate["Missing Skills"],

            "Experience": candidate["Experience"],

            "Verdict": candidate["Verdict"]

        })

    # =====================================
    # Candidate Ranking Table
    # =====================================

    st.subheader("🏆 Candidate Ranking")

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================
    # Candidate Details
    # =====================================

    st.subheader("👨‍💻 Candidate Details")

    for candidate in all_results:

        with st.expander(
            f"📄 {candidate['Candidate']}  |  {candidate['Score']}%"
        ):

            st.write(
                f"### 👤 {candidate['Candidate']}"
            )

            st.write(
                f"### 📊 Match Score : {candidate['Score']}%"
            )

            st.write(
                f"### 💼 Experience Match : {candidate['Experience']}"
            )

            st.write(
                f"### 📝 Final Verdict"
            )

            st.success(
                candidate["Verdict"]
            )

            st.write(
                "### ✅ Matching Skills"
            )

            st.info(
                candidate["Matching Skills"]
            )

            st.write(
                "### ❌ Missing Skills"
            )

            st.warning(
                candidate["Missing Skills"]
            )

    st.divider()

        # =====================================
    # Plotly Libraries Import Kar Rahe Hain
    # =====================================

    import pandas as pd              # DataFrame banane ke liye
    import plotly.express as px      # Interactive charts banane ke liye

    # =====================================
    # Candidate Score Chart
    # =====================================

    st.subheader("📈 Candidate Score Analysis")

    # Table data ko DataFrame me convert kar rahe hain
    chart_df = pd.DataFrame(table_data)

    # Score se % remove karke integer bana rahe hain
    chart_df["Score"] = (
        chart_df["Score"]
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    # Interactive Bar Chart bana rahe hain
    fig = px.bar(

        chart_df,

        x="Candidate",

        y="Score",

        text="Score",

        title="Candidate Score Comparison"

    )

    # Score text bar ke bahar show hoga
    fig.update_traces(
        textposition="outside"
    )

    # Chart ki height set kar rahe hain
    fig.update_layout(
        height=500
    )

    # Streamlit me chart show kar rahe hain
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # Top 3 Candidates
    # =====================================

    st.subheader("🥇 Top 3 Candidates")

    medals = ["🥇", "🥈", "🥉"]

    for i, candidate in enumerate(all_results[:3]):

        st.success(

            f"""
{medals[i]} **{candidate['Candidate']}**

📊 Score : **{candidate['Score']}%**

📝 Verdict : **{candidate['Verdict']}**
"""

        )

    st.divider()

    # =====================================
    # Download CSV
    # =====================================

    st.subheader("📥 Export Results")

    csv = chart_df.to_csv(
        index=False
    )

    st.download_button(

        label="📥 Download CSV",

        data=csv,

        file_name="candidate_ranking.csv",

        mime="text/csv"

    )

    st.divider()

    # =====================================
    # Score Distribution
    # =====================================

    st.subheader("📊 Score Distribution")

    # Score ke hisaab se category bana rahe hain
    def score_category(score):

        if score >= 85:
            return "Highly Recommended"

        elif score >= 70:
            return "Recommended"

        elif score >= 50:
            return "Consider"

        return "Reject"

    # Har candidate ko category assign kar rahe hain
    chart_df["Category"] = chart_df["Score"].apply(
        score_category
    )

    # Pie Chart bana rahe hain
    pie = px.pie(

        chart_df,

        names="Category",

        title="Candidate Recommendation Distribution"

    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    st.divider()

    # =====================================
    # Footer
    # =====================================

    st.caption(
        "🤖 Built with Streamlit • Groq • Llama 3.3 • Pydantic"
    )

        # =====================================
    # Custom CSS (Professional UI)
    # =====================================

    st.markdown("""
    <style>

    /* Main Background */
    .stApp{
        background-color:#F8FAFC;
    }

    /* Metric Cards */
    div[data-testid="metric-container"]{
        background:white;
        border-radius:15px;
        padding:15px;
        border:1px solid #E5E7EB;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    }

    /* Buttons */
    .stButton>button{
        width:100%;
        border-radius:10px;
        font-size:18px;
        font-weight:bold;
        height:50px;
    }

    /* Download Button */
    .stDownloadButton>button{
        width:100%;
        border-radius:10px;
        height:45px;
    }

    /* Expander */
    .streamlit-expanderHeader{
        font-size:17px;
        font-weight:600;
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================
    # Top Recommendation Banner
    # =====================================

    st.subheader("🎯 Hiring Recommendation")

    best = all_results[0]

    if best["Score"] >= 85:

        st.success(
            f"✅ Strongly Recommended to Hire **{best['Candidate']}**"
        )

    elif best["Score"] >= 70:

        st.info(
            f"👍 Recommended to Interview **{best['Candidate']}**"
        )

    elif best["Score"] >= 50:

        st.warning(
            f"⚠ Consider **{best['Candidate']}** after screening."
        )

    else:

        st.error(
            "❌ No suitable candidate found."
        )

    st.divider()

    # =====================================
    # Score Badge
    # =====================================

    st.subheader("🏅 Candidate Grades")

    for candidate in all_results:

        score = candidate["Score"]

        if score >= 90:
            badge = "🟢 Excellent"

        elif score >= 80:
            badge = "🔵 Very Good"

        elif score >= 70:
            badge = "🟡 Good"

        elif score >= 50:
            badge = "🟠 Average"

        else:
            badge = "🔴 Poor"

        st.write(
            f"**{candidate['Candidate']}** → {badge} ({score}%)"
        )

    st.divider()

    # =====================================
    # AI Insights
    # =====================================

    st.subheader("🧠 AI Insights")

    st.info(f"""

• Total Candidates Evaluated : **{total_candidates}**

• Highest Match Score : **{highest_score}%**

• Average Match Score : **{average_score}%**

• Best Candidate : **{best['Candidate']}**

• Hiring Verdict : **{best['Verdict']}**

""")

    st.divider()

    # =====================================
    # Thank You Footer
    # =====================================

    st.markdown("---")

    st.markdown(
        """
### 🤖 AI Resume Evaluator

Made using

- Streamlit
- Groq API
- Llama 3.3
- Pydantic
- Plotly

Developed by **Prateek Verma**
"""
    )