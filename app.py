       
from groq import Groq
import streamlit as st
import pandas as pd
import time
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Digital Twin Career Advisor", layout="wide")
# -----------------------------
# SIDEBAR PROFILE SELECTOR
# -----------------------------

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "start_app" not in st.session_state:
    st.session_state.start_app = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "jobs_list" not in st.session_state:
    st.session_state.jobs_list = []

if "match_scores" not in st.session_state:
    st.session_state.match_scores = {}

if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

if "match_result" not in st.session_state:
    st.session_state.match_result = ""

if "career_result" not in st.session_state:
    st.session_state.career_result = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(api_key="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")

# -----------------------------
# SAFE GENERATE
# -----------------------------
def safe_generate(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"
# -----------------------------
# -----------------------------
# LANDING PAGE WITHOUT experimental_rerun
# -----------------------------
if not st.session_state.start_app:
    st.markdown("""
    <style>

    .block-container {
        padding: 0rem;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    .hero {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;

        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;

        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                    url('https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1920&q=80');

        background-size: cover;
        background-position: center;

        color: white;
        text-align: center;
    }

    .hero h1 {
        font-size: 70px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 24px;
        margin-bottom: 20px;
    }

    /* ✅ Button styling inside hero */
    .hero-btn {
        margin-top: 10px;
    }

    .stButton > button {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        color: white;
        font-size: 22px;
        padding: 15px 40px;
        border-radius: 12px;
        border: none;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #0072ff, #00c6ff);
    }

    </style>
    """, unsafe_allow_html=True)

    # 👇 HTML content
    st.markdown("""
    <div class="hero">
        <h1>🤖 AI Digital Twin</h1>
        <p>Your Personal AI Career Advisor</p>
    </div>
    """, unsafe_allow_html=True)

    # 👇 Button ko thoda upar shift karne ke liye empty space control
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # 👇 CENTERED BUTTON (subtitle ke just neeche feel aayega)
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("🚀 Enter Website"):
            st.session_state.start_app = True
            st.rerun()

    st.stop()

# -----------------------------
# LOAD DATA
# -----------------------------
if os.path.exists("user_profiles.csv"):
    df_profiles = pd.read_csv("user_profiles.csv")
else:
    df_profiles = pd.DataFrame(columns=[
        "Name","Age","Phone","Email","Location","LinkedIn","GitHub",
        "Education","Experience","CurrentRole","Company",
        "Skills","Interests","Certifications","Projects",
        "Personality","CareerGoal","PreferredRole"
    ])

# -----------------------------
# TABS
# -----------------------------

profile_type = st.sidebar.selectbox("Choose Profile Type", ["Job", "Food"])


if profile_type == "Job":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Build Profile",
        "Compare Jobs",
        "History",
        "Skill Gap + Roadmap",
        "Chat with AI"
    ])
    # ... all your job tab code here ...

elif profile_type == "Food":
    tab1, tab2, tab3, tab4 = st.tabs([
        "Food Profile",
        "Compare Food",
        "History",
        "Chat AI"
    ])
    # ... all your food tab code here ...
# -----------------------------
# TAB 1: PROFILE
# -----------------------------
if profile_type == "Job":
    with tab1:
        st.header("👤 Create Your Professional Profile")

        name = st.text_input("Full Name")

        # ✅ AUTO FIX: Ensure all columns exist (VERY IMPORTANT)
        required_cols = [
            "Name","Age","Phone","Email","Location","LinkedIn","GitHub",
            "Education","Experience","CurrentRole","Company",
            "Skills","Interests","Certifications","Projects",
            "Personality","CareerGoal","PreferredRole"
        ]

        for col in required_cols:
            if col not in df_profiles.columns:
                df_profiles[col] = ""

        user_data = None
        if name and name in df_profiles["Name"].values:
            user_data = df_profiles[df_profiles["Name"] == name].iloc[0]

        st.markdown("### 📌 Personal Details")
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input("Age", 10, 100, int(user_data["Age"]) if user_data is not None else 20)
            phone = st.text_input("Phone Number", user_data["Phone"] if user_data is not None else "")
        
        with col2:
            email = st.text_input("Email", user_data["Email"] if user_data is not None else "")
            location = st.text_input("Location", user_data["Location"] if user_data is not None else "")

        with col3:
            linkedin = st.text_input("LinkedIn Profile", user_data["LinkedIn"] if user_data is not None else "")
            github = st.text_input("GitHub Profile", user_data["GitHub"] if user_data is not None else "")

        st.markdown("---")

        st.markdown("### 🎓 Education & Experience")
        col4, col5 = st.columns(2)

        with col4:
            education_list = ["High School", "Diploma", "Bachelors", "Masters", "PhD"]
            education = st.selectbox(
                "Education",
                education_list,
                index=education_list.index(user_data["Education"]) if user_data is not None and user_data["Education"] in education_list else 2
            )

            experience = st.slider(
                "Experience (Years)",
                0, 20,
                int(user_data["Experience"]) if user_data is not None else 0
            )

        with col5:
            current_role = st.text_input("Current Role", user_data["CurrentRole"] if user_data is not None else "")
            company = st.text_input("Current Company", user_data["Company"] if user_data is not None else "")

        st.markdown("---")

        st.markdown("### 💡 Skills & Interests")

        skills = st.text_area("Technical Skills (comma separated)", user_data["Skills"] if user_data is not None else "")
        interests = st.text_area("Interests / Domains", user_data["Interests"] if user_data is not None else "")

        certifications = st.text_area("Certifications", user_data["Certifications"] if user_data is not None else "")
        projects = st.text_area("Projects", user_data["Projects"] if user_data is not None else "")

        st.markdown("---")

        st.markdown("### 🧠 Personality & Goals")
        col6, col7 = st.columns(2)

        with col6:
            personality_list = ["Introvert", "Extrovert", "Creative", "Analytical"]
            personality = st.selectbox(
                "Personality",
                personality_list,
                index=personality_list.index(user_data["Personality"]) if user_data is not None and user_data["Personality"] in personality_list else 0
            )

        with col7:
            career_goal = st.text_input("Career Goal", user_data["CareerGoal"] if user_data is not None else "")
            preferred_role = st.text_input("Preferred Job Role", user_data["PreferredRole"] if user_data is not None else "")

        st.markdown("---")

        if st.button("💾 Save Profile"):

            new_data = {
                "Name": name,
                "Age": age,
                "Phone": phone,
                "Email": email,
                "Location": location,
                "LinkedIn": linkedin,
                "GitHub": github,
                "Education": education,
                "Experience": experience,
                "CurrentRole": current_role,
                "Company": company,
                "Skills": skills,
                "Interests": interests,
                "Certifications": certifications,
                "Projects": projects,
                "Personality": personality,
                "CareerGoal": career_goal,
                "PreferredRole": preferred_role
            }

            if name in df_profiles["Name"].values:
                for col in new_data:
                    df_profiles.loc[df_profiles["Name"] == name, col] = new_data[col]
                st.success("✅ Profile Updated Successfully!")
            else:
                df_profiles = pd.concat([df_profiles, pd.DataFrame([new_data])], ignore_index=True)
                st.success("✅ Profile Created Successfully!")

            df_profiles.to_csv("user_profiles.csv", index=False)
            st.session_state.current_user = name

            time.sleep(1)
            st.rerun()


    # -----------------------------
    # CURRENT USER
    # -----------------------------
    user_profile = None
    if st.session_state.current_user:
        if st.session_state.current_user in df_profiles["Name"].values:
            user_profile = df_profiles[df_profiles["Name"] == st.session_state.current_user].iloc[0]
    # -----------------------------
    # TAB 2: JOB COMPARISON + ADVANCED (FIXED)
    # -----------------------------
    # -----------------------------
    # TAB 2: JOB COMPARISON + ADVANCED (UPDATED)
    # -----------------------------
    with tab2:
        st.header("⚡ Compare Jobs & Smart AI Analysis")

        if user_profile is None:
            st.warning("⚠️ Please create/select profile in Tab 1")
            st.stop()

        st.success(f"👤 Current User: {st.session_state.current_user}")

        # -----------------------------
        # SESSION STATE INIT
        # -----------------------------
        if "jobs_list" not in st.session_state:
            st.session_state.jobs_list = []

        if "match_scores" not in st.session_state:
            st.session_state.match_scores = {}

        if "ai_result" not in st.session_state:
            st.session_state.ai_result = ""

        if "match_result" not in st.session_state:
            st.session_state.match_result = ""

        if "career_result" not in st.session_state:
            st.session_state.career_result = ""

        # -----------------------------
        # JOB INPUT SECTION
        # -----------------------------
        st.markdown("### 📝 Enter Jobs to Compare")
        num_jobs = st.number_input("How many jobs?", 2, 10, 2)
        jobs = [st.text_input(f"Job {i+1}", key=f"job_{i}") for i in range(int(num_jobs))]

        # -----------------------------
        # SAFE PROFILE ACCESS
        # -----------------------------
        def get_val(key):
            return user_profile.get(key, "Not Provided")

        # -----------------------------
        # AI RECOMMENDATION
        # -----------------------------
        st.markdown("---")
        if st.button("🚀 Get AI Recommendation"):
            if any(j.strip() == "" for j in jobs):
                st.warning("⚠️ Please enter all job fields")
            else:
                st.session_state.jobs_list = jobs
                jobs_str = "\n".join([f"{i+1}. {j}" for i, j in enumerate(jobs)])

                prompt = f"""
    You are an expert AI career advisor.

    User Full Profile:
    - Name: {get_val('Name')}
    - Skills: {get_val('Skills')}
    - Interests: {get_val('Interests')}
    - Experience: {get_val('Experience')}
    - Education: {get_val('Education')}
    - Personality: {get_val('Personality')}
    - Career Goal: {get_val('CareerGoal')}
    - LinkedIn: {get_val('LinkedIn')}
    - Github: {get_val('GitHub')}
    - Current Role: {get_val('CurrentRole')}
    - Projects: {get_val('Projects')}
    - Certifications: {get_val('Certifications')}

    Jobs:
    {jobs_str}

    Task:
    1. Analyze deeply user personality + skills + goals
    2. Compare all jobs
    3. Give best job with strong reasoning
    4. Explain WHY it fits this specific user
    5. Also recommend best company for that particular job according to my profile
    """

                with st.spinner("🤖 AI is analyzing deeply..."):
                    st.session_state.ai_result = safe_generate(prompt)

        if st.session_state.ai_result:
            st.success("🎯 Recommendation Ready")
            st.info(st.session_state.ai_result)

        # -----------------------------
        # JOB MATCH SCORE (AI BASED)
        # -----------------------------
        st.markdown("---")
        st.subheader("🎯 AI Smart Job Match Score")
        if st.button("Calculate AI Match Score"):
            valid_jobs = [j for j in jobs if j.strip() != ""]
            if len(valid_jobs) == 0:
                st.warning("⚠️ Please enter jobs in above section")
            else:
                jobs_str = "\n".join([f"{i+1}. {j}" for i, j in enumerate(valid_jobs)])
                prompt = f"""
    User Profile:
    Name: {get_val('Name')}
    Skills: {get_val('Skills')}
    Interests: {get_val('Interests')}
    Experience: {get_val('Experience')}
    Personality: {get_val('Personality')}

    Jobs:
    {jobs_str}

    Task:
    - Give each job a match percentage (0-100%)
    - Give short reason
    - Rank jobs from best to worst

    Output STRICT FORMAT:

    Job: <name>
    Match: <percentage>%
    Reason: <short>

    Best Job: <name>
    """
                with st.spinner("🤖 AI calculating match score..."):
                    st.session_state.match_result = safe_generate(prompt)

        if st.session_state.match_result:
            st.success("✅ AI Match Score Ready")
            st.write(st.session_state.match_result)

        # -----------------------------
        # PERFECT CAREER
        # -----------------------------
        if st.button("🤖 Find My Perfect Career"):
            prompt = f"""
    User Profile:
    {user_profile.to_dict()}

    Suggest:
    - Best career (not from given jobs)
    - Why perfect fit
    - Future growth
    - Skills to improve
    """
            st.session_state.career_result = safe_generate(prompt)

        if st.session_state.career_result:
            st.success(st.session_state.career_result)

        # -----------------------------
        # SKILL VISUALIZATION
        # -----------------------------
        st.markdown("---")
        st.subheader("📈 Skill Strength Visualization")
        skills_list = [s.strip() for s in get_val("Skills").split(",") if s.strip() != ""]
        if skills_list:
            skill_df = pd.DataFrame({
                "Skill": skills_list,
                "Strength": [10 + int(get_val("Experience"))] * len(skills_list)
            })
            st.bar_chart(skill_df.set_index("Skill"))

            # ✅ Advanced: Radar Chart
            import plotly.express as px
            fig = px.line_polar(skill_df, r="Strength", theta="Skill", line_close=True, title="Skill Radar")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)

        # -----------------------------
        # ADVANCED AI INSIGHTS (UNCHANGED UI)
        # -----------------------------
        st.markdown("---")
        st.header("🚀 Advanced AI Insights")

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🧠 Explain Job Match"):
                if st.button("Run Job Match Analysis"):
                    jobs_text = ", ".join(st.session_state.jobs_list)
                    prompt = f"""
    User Profile:
    Skills: {get_val('Skills')}
    Jobs: {jobs_text}

    Give score and reason for each job.
    """
                    st.success(safe_generate(prompt))

        with col2:
            with st.expander("📊 Career Timeline"):
                if st.button("Show Career Growth"):
                    prompt = f"""
    Skills: {get_val('Skills')}
    Experience: {get_val('Experience')}

    Show career growth for 1, 3, 5 years.
    """
                    st.info(safe_generate(prompt))

        # -----------------------------
        # CAREER RISK GRAPH
        # -----------------------------
        import matplotlib.pyplot as plt
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("⚠️ Career Risk"):
                if st.button("Analyze Risk"):
                    prompt = f"""
    User Profile: {get_val('Name')}
    Skills: {get_val('Skills')}
    Interests: {get_val('Interests')}
    """
                    st.warning(safe_generate(prompt))

                    # Advanced: Risk bar chart (dummy logic based on number of skills)
                    risk_levels = [len(skills_list) * 2, len(skills_list) * 3, len(skills_list) * 1.5]
                    labels = ["Skill Fit", "Market Demand", "Experience"]
                    plt.bar(labels, risk_levels, color=['red', 'orange', 'green'])
                    plt.title("Career Risk Analysis")
                    st.pyplot(plt.gcf())
        
        with col2:
            with st.expander("💰 Salary Prediction"):
                if st.button("Predict Salary"):
                    prompt = f"""
    Skills: {get_val('Skills')}
    Experience: {get_val('Experience')}
    """
                    st.success(safe_generate(prompt))
        
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("🎯 Skill Priority"):
                if st.button("Find Important Skills"):
                    prompt = f"""
    User Skills: {get_val('Skills')}
    """
                    st.success(safe_generate(prompt))

        with col2:
            with st.expander("🧠 Personality Advice"):
                if st.button("Get Advice"):
                    prompt = f"""
    Personality: {get_val('Personality')}
    """
                    st.success(safe_generate(prompt))

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("🧭 Career Switch Predictor"):
                if st.button("Should I Switch Career?"):
                    prompt = f"""
    User Profile:{get_val('Name')}
    Skills: {get_val('Skills')}
    Interests: {get_val('Interests')}
    Experience: {get_val('Experience')}
    """
                    st.warning(safe_generate(prompt))

        with col2:
            with st.expander("🏆 Job Readiness Score"):
                if st.button("Check Readiness"):
                    prompt = f"""
    User Profile: {get_val('Name')}
    Skills: {get_val('Skills')}
    Experience: {get_val('Experience')}
    """
                    st.success(safe_generate(prompt))

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("🎤 Interview Preparation"):
                if st.button("Generate Questions"):
                    jobs_text = ", ".join(jobs)
                    prompt = f"""
    User Skills: {get_val('Skills')}
    Target Jobs: {jobs_text}
    """
                    st.info(safe_generate(prompt))

        with col2:
            with st.expander("📚 Learning Roadmap"):
                if st.button("Create Plan"):
                    prompt = f"""
    User Skills: {get_val('Skills')}
    Experience: {get_val('Experience')}
    """
                    st.success(safe_generate(prompt))
        
        # -----------------------------
        # RESUME
        # -----------------------------
        st.markdown("---")
        st.subheader("⬇️ Download Resume")

        if "resume_text" not in st.session_state:
            st.session_state.resume_text = ""

        with st.expander("📄 Resume Generator"):
            if st.button("Generate & Download Resume"):
                prompt = f"""
    Create a professional resume:

    Name: {st.session_state.current_user}
    Skills: {get_val('Skills')}
    Experience: {get_val('Experience')}
    Education: {get_val('Education')}
    """
                resume = safe_generate(prompt)
                st.session_state.resume_text = resume

                st.download_button(
                    label="📥 Download Resume",
                    data=resume,
                    file_name="resume.txt",
                    mime="text/plain"
                )

    # -----------------------------
    # TAB 3: HISTORY
    # -----------------------------
    with tab3:
        st.header("📂 History")

        if os.path.exists("user_profiles.csv"):
            st.dataframe(pd.read_csv("user_profiles.csv"))
        else:
            st.info("No data")

    # -----------------------------
    # TAB 4: SKILL GAP
    # -----------------------------
    with tab4:
        st.header("📈 Skill Gap")

        if user_profile is None:
            st.warning("Create profile first")
            st.stop()

        target_job = st.text_input("Target Job")

        if st.button("Analyze"):
            prompt = f"""
    You are an expert AI career mentor.

    User Profile:
    - Skills: {user_profile['Skills']}
    - Experience: {user_profile['Experience']}
    - Education: {user_profile['Education']}
    - Personality: {user_profile['Personality']}

    Target Job: {target_job}

    Task:

    1. Identify SKILL GAP:
    - List missing technical skills
    - List missing soft skills

    2. Categorize skills:
    - Beginner level
    - Intermediate level
    - Advanced level

    3. PRIORITY:
    - High priority skills (must learn first)
    - Medium priority
    - Low priority

    4. ROADMAP:
    - Step-by-step plan (Week-wise or Month-wise)

    5. PROJECT SUGGESTIONS:
    - Suggest 2-3 projects to gain these skills

    6. RESOURCES:
    - Recommend platforms (YouTube, Coursera, etc.)

    7. COMPANY READINESS:
    - Is user ready for this job? (Yes/No)
    - If not, what is missing?

    8. FINAL SUMMARY:
    - Clear action plan to achieve this job
    """

            with st.spinner("Analyzing..."):
                result = safe_generate(prompt)

            st.success("✅ Analysis Ready")
            st.write(result)

    # -----------------------------
    # TAB 5: CHAT
    # -----------------------------
    # -----------------------------
    # TAB 5: CHAT WITH AI (ADVANCED)
    # -----------------------------
    with tab5:
        st.header("💬 Chat AI - Personalized Guidance")

        if user_profile is None:
            st.warning("⚠️ Create profile first in Tab 1")
            st.stop()

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        query = st.text_input("Ask something", key="chat_query")

        if st.button("Ask AI") and query.strip() != "":

            # Context-aware prompt
            prompt_chat = f"""
    User Profile:
    Name: {get_val('Name')}
    Skills: {get_val('Skills')}
    Experience: {get_val('Experience')}
    Education: {get_val('Education')}
    Personality: {get_val('Personality')}
    Career Goal: {get_val('CareerGoal')}
    Target Job: {query}

    Respond like a professional career mentor.
    Provide:
    - Clear actionable advice
    - Learning resources or roadmap
    - Interview preparation tips if relevant
    - Keep it concise
    """

            with st.spinner("AI is thinking..."):
                response = safe_generate(prompt_chat)

            # Save chat history
            st.session_state.chat_history.append({"query": query, "response": response})

        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 💬 Chat History")
            for chat in st.session_state.chat_history[::-1]:  # newest first
                st.markdown(f"**You:** {chat['query']}")
                st.markdown(f"**AI:** {chat['response']}")
                st.markdown("---")
                


# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "food_profiles" not in st.session_state:
    st.session_state.food_profiles = []

if "current_food_user" not in st.session_state:
    st.session_state.current_food_user = None

if "food_history" not in st.session_state:
    st.session_state.food_history = []


# -----------------------------
# FOOD TABS
# -----------------------------
elif profile_type == "Food":
    file_path = "food_profiles.csv"

    if os.path.exists(file_path):
        df_food_profiles = pd.read_csv(file_path)
    else:
        df_food_profiles = pd.DataFrame()

    # EXTRA FOOD COLUMNS
    extra_cols = ["WeightGoal", "DailyCalories", "MealHistory"]

    for col in extra_cols:
        if col not in df_food_profiles.columns:
            df_food_profiles[col] = ""
        # Ensure required columns
        
    required_cols = [
        "Name","Age","TastePreferences","FavoriteFoods","DietType","Allergies"
    ]

    for col in required_cols:
        if col not in df_food_profiles.columns:
            df_food_profiles[col] = ""


    # -----------------------------
    # TAB 1: Food Profile
    # -----------------------------
    with tab1:
        st.header("🍔 Create Your Food Profile")

        name = st.text_input("Full Name")

        # ✅ Ensure required columns exist
        required_cols = [
            "Name","Age","TastePreferences","FavoriteFoods",
            "DietType","Allergies","Mood","SpiceLevel","SweetLevel",
            "WeightGoal","DailyCalories"
        ]

        for col in required_cols:
            if col not in df_food_profiles.columns:
                df_food_profiles[col] = ""

        # -----------------------------
        # AUTO-FILL EXISTING USER
        # -----------------------------
        user_data = None
        if name and name in df_food_profiles["Name"].values:
            user_data = df_food_profiles[df_food_profiles["Name"] == name].iloc[0]

        # -----------------------------
        # BASIC DETAILS
        # -----------------------------
        st.markdown("### 👤 Basic Details")
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age", 10, 100,
                int(user_data["Age"]) if user_data is not None and str(user_data["Age"]).isdigit() else 20
            )

            # 🔥 NEW: Taste Preferences (Selectable + Custom)
            taste_options = ["Spicy 🌶️", "Sweet 🍫", "Salty 🧂", "Sour 🍋", "Bitter ☕", "Umami 🍜"]

            # Fix default issue: Only keep default tastes that exist in options
            default_taste = []
            if user_data is not None and user_data["TastePreferences"]:
                for t in user_data["TastePreferences"].split(","):
                    t = t.strip()
                    if t in taste_options:
                        default_taste.append(t)

            selected_taste = st.multiselect(
                "Taste Preferences",
                taste_options,
                default=default_taste
            )

            custom_taste = st.text_input("Add Custom Taste (optional)")

            taste = ", ".join(selected_taste + ([custom_taste] if custom_taste else []))

        with col2:
            favorite_foods = st.text_area(
                "Favorite Foods (comma separated)",
                user_data["FavoriteFoods"] if user_data is not None else ""
            )

            diet_list = ["Vegetarian", "Non-Vegetarian", "Vegan"]
            diet_type = st.selectbox(
                "Diet Type",
                diet_list,
                index=diet_list.index(user_data["DietType"]) if user_data is not None and user_data["DietType"] in diet_list else 0
            )

        # -----------------------------
        # ADVANCED PREFERENCES
        # -----------------------------
        st.markdown("### ⚙️ Advanced Preferences")

        col3, col4 = st.columns(2)

        with col3:
            spice_level = st.slider(
                "Spice Level 🌶️",
                1, 10,
                int(user_data["SpiceLevel"]) if user_data is not None and str(user_data["SpiceLevel"]).isdigit() else 5
            )

            sweet_level = st.slider(
                "Sweet Preference 🍫",
                1, 10,
                int(user_data["SweetLevel"]) if user_data is not None and str(user_data["SweetLevel"]).isdigit() else 5
            )

        with col4:
            # 🔥 NEW: Mood Selector
            mood_list = ["Happy 😊", "Sad 😔", "Stressed 😩", "Normal 😐", "Excited 🤩"]
            mood = st.selectbox(
                "Current Mood",
                mood_list,
                index=mood_list.index(user_data["Mood"]) if user_data is not None and user_data["Mood"] in mood_list else 3
            )

        # -----------------------------
        # HEALTH INFO
        # -----------------------------
        st.markdown("### 🏥 Health Preferences")

        allergies = st.text_area(
            "Allergies (if any)",
            user_data["Allergies"] if user_data is not None else ""
        )

        st.markdown("---")
        st.markdown("### 🎯 Health Goals")

        col5, col6 = st.columns(2)

        with col5:
            goal_list = ["Weight Loss", "Weight Gain", "Maintain"]
            weight_goal = st.selectbox(
                "Weight Goal",
                goal_list,
                index=goal_list.index(user_data["WeightGoal"]) if user_data is not None and user_data["WeightGoal"] in goal_list else 0
            )

        with col6:
            daily_calories = st.number_input(
                "Target Daily Calories",
                1000, 4000,
                int(user_data["DailyCalories"]) if user_data is not None and str(user_data["DailyCalories"]).isdigit() else 2000
            )

        # -----------------------------
        # SAVE BUTTON (UPDATE + CREATE)
        # -----------------------------
        if st.button("💾 Save Food Profile"):

            new_data = {
                "Name": name,
                "Age": age,
                "TastePreferences": taste,
                "FavoriteFoods": favorite_foods,
                "DietType": diet_type,
                "Allergies": allergies,
                "Mood": mood,
                "SpiceLevel": spice_level,
                "SweetLevel": sweet_level,
                "WeightGoal": weight_goal,
                "DailyCalories": daily_calories
            }

            if name in df_food_profiles["Name"].values:
                for col in new_data:
                    df_food_profiles.loc[df_food_profiles["Name"] == name, col] = new_data[col]
                st.success("✅ Food Profile Updated Successfully!")
            else:
                df_food_profiles = pd.concat([df_food_profiles, pd.DataFrame([new_data])], ignore_index=True)
                st.success("✅ Food Profile Created Successfully!")

            df_food_profiles.to_csv("food_profiles.csv", index=False)
            st.session_state.current_food_user = name

            time.sleep(1)
            st.rerun()


# -----------------------------
# CURRENT FOOD USER
user_profile = None
if st.session_state.current_food_user:
    if st.session_state.current_food_user in df_food_profiles["Name"].values:
        user_profile = df_food_profiles[df_food_profiles["Name"] == st.session_state.current_food_user].iloc[0]
        
    # TAB 2: COMPARE FOOD
    # -----------------------------
    with tab2:
        st.header("🍽️ Compare Foods & Smart AI Analysis")

        if user_profile is None:
            st.warning("⚠️ Please create/select food profile in Tab 1")
            st.stop()

        st.success(f"👤 Current User: {st.session_state.current_food_user}")

        # -----------------------------
        # SESSION STATE INIT
        # -----------------------------
        if "foods_list" not in st.session_state:
            st.session_state.foods_list = []

        if "food_ai_result" not in st.session_state:
            st.session_state.food_ai_result = ""

        if "food_match_result" not in st.session_state:
            st.session_state.food_match_result = ""

        if "diet_result" not in st.session_state:
            st.session_state.diet_result = ""

        # -----------------------------
        # FOOD INPUT
        # -----------------------------
        st.markdown("### 📝 Enter Foods to Compare")
        num_foods = st.number_input("How many foods?", 2, 10, 2)
        foods = [st.text_input(f"Food {i+1}", key=f"food_{i}") for i in range(int(num_foods))]

        # -----------------------------
        # SAFE ACCESS
        # -----------------------------
        def get_val(key):
            return user_profile.get(key, "Not Provided")

        # -----------------------------
        # AI FOOD RECOMMENDATION (UPGRADED 🔥)
        # -----------------------------
        st.markdown("---")
        if st.button("🍔 Get AI Food Recommendation"):
            if any(f.strip() == "" for f in foods):
                st.warning("⚠️ Please enter all food fields")
            else:
                st.session_state.foods_list = foods
                foods_str = "\n".join([f"{i+1}. {f}" for i, f in enumerate(foods)])

                prompt = f"""
    You are an expert AI nutritionist.

    User Profile:
    - Name: {get_val('Name')}
    - Age: {get_val('Age')}
    - Taste Preferences: {get_val('TastePreferences')}
    - Favorite Foods: {get_val('FavoriteFoods')}
    - Diet Type: {get_val('DietType')}
    - Allergies: {get_val('Allergies')}
    - Mood: {get_val('Mood')}
    - Spice Level: {get_val('SpiceLevel')}
    - Sweet Preference: {get_val('SweetLevel')}

    Foods:
    {foods_str}

    Task:
    1. Analyze taste + health + mood
    2. If user is:
    - Happy → suggest fun/dessert foods
    - Sad → suggest comfort foods
    - Stressed → suggest light/healthy foods
    - Excited → suggest spicy/fast foods
    3. Compare all foods
    4. Suggest best option
    5. Explain WHY it fits this specific user
    """

                with st.spinner("🤖 AI is analyzing food..."):
                    st.session_state.food_ai_result = safe_generate(prompt)

        if st.session_state.food_ai_result:
            st.success("🍽️ Recommendation Ready")
            st.info(st.session_state.food_ai_result)

        # -----------------------------
        # FOOD MATCH SCORE (UPGRADED)
        # -----------------------------
        st.markdown("---")
        st.subheader("🎯 AI Food Match Score")

        if st.button("Calculate Food Match Score"):
            valid_foods = [f for f in foods if f.strip() != ""]
            if len(valid_foods) == 0:
                st.warning("⚠️ Enter foods first")
            else:
                foods_str = "\n".join([f"{i+1}. {f}" for i, f in enumerate(valid_foods)])

                prompt = f"""
    User Profile:
    Taste: {get_val('TastePreferences')}
    Diet: {get_val('DietType')}
    Allergies: {get_val('Allergies')}
    Mood: {get_val('Mood')}
    Spice Level: {get_val('SpiceLevel')}
    Sweet Preference: {get_val('SweetLevel')}

    Foods:
    {foods_str}

    Task:
    - Give each food a match % (0-100)
    - Consider mood + taste + health
    - Short reason
    - Rank best to worst

    Format:

    Food: <name>
    Match: <percentage>%
    Reason: <short>

    Best Food: <name>
    """

                with st.spinner("🤖 Calculating food score..."):
                    st.session_state.food_match_result = safe_generate(prompt)

        if st.session_state.food_match_result:
            st.success("✅ Food Match Ready")
            st.write(st.session_state.food_match_result)

        # -----------------------------
        # PERFECT DIET PLAN (UPGRADED)
        # -----------------------------
        if st.button("🥗 Generate Perfect Diet Plan"):
            prompt = f"""
    User Profile:
    {user_profile.to_dict()}

    Also consider mood: {get_val('Mood')}

    Suggest:
    - Daily diet plan
    - Mood-based food suggestions
    - Healthy food suggestions
    - Avoid foods
    - Nutrition tips
    """
            st.session_state.diet_result = safe_generate(prompt)

        if st.session_state.diet_result:
            st.success(st.session_state.diet_result)

        # -----------------------------
        # TASTE VISUALIZATION
        # -----------------------------
        st.markdown("---")
        st.subheader("📊 Taste Preference Visualization")

        taste_list = [t.strip() for t in get_val("TastePreferences").split(",") if t.strip() != ""]

        if taste_list:
            taste_df = pd.DataFrame({
                "Taste": taste_list,
                "Preference": [int(get_val("SpiceLevel")) if str(get_val("SpiceLevel")).isdigit() else 5] * len(taste_list)
            })
            st.bar_chart(taste_df.set_index("Taste"))

            import plotly.express as px
            fig = px.line_polar(taste_df, r="Preference", theta="Taste", line_close=True, title="Taste Radar")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)

        # -----------------------------
        # ADVANCED AI INSIGHTS
        # -----------------------------
        st.markdown("---")
        st.header("🚀 Advanced Food Insights")

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("🧠 Food Analysis"):
                if st.button("Analyze Food Choices"):
                    foods_text = ", ".join(st.session_state.foods_list)
                    prompt = f"""
    Taste: {get_val('TastePreferences')}
    Mood: {get_val('Mood')}
    Foods: {foods_text}

    Analyze health + mood suitability.
    """
                    st.success(safe_generate(prompt))

        with col2:
            with st.expander("📅 Weekly Diet Plan"):
                if st.button("Generate Weekly Plan"):
                    prompt = f"""
    User Taste: {get_val('TastePreferences')}
    Diet Type: {get_val('DietType')}
    Mood: {get_val('Mood')}
    """
                    st.info(safe_generate(prompt))

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("⚠️ Food Risk"):
                if st.button("Analyze Food Risk"):
                    prompt = f"""
    Allergies: {get_val('Allergies')}
    Foods: {", ".join(foods)}
    """
                    st.warning(safe_generate(prompt))

        with col2:
            with st.expander("💪 Nutrition Tips"):
                if st.button("Get Tips"):
                    prompt = f"""
    User Profile:
    {user_profile.to_dict()}
    """
                    st.success(safe_generate(prompt))

        # -----------------------------
        # DOWNLOAD DIET PLAN
        # -----------------------------
        st.markdown("---")
        st.subheader("⬇️ Download Diet Plan")

        if "diet_text" not in st.session_state:
            st.session_state.diet_text = ""

        with st.expander("📄 Diet Generator"):
            if st.button("Generate & Download Diet"):
                prompt = f"""
    Create a diet plan:

    Name: {st.session_state.current_food_user}
    Taste: {get_val('TastePreferences')}
    Diet: {get_val('DietType')}
    Mood: {get_val('Mood')}
    """
                diet = safe_generate(prompt)
                st.session_state.diet_text = diet

                st.download_button(
                    label="📥 Download Diet Plan",
                    data=diet,
                    file_name="diet_plan.txt",
                    mime="text/plain"
                )
                
        # -----------------------------
# 🍽️ CALORIE TRACKER
# -----------------------------
        st.markdown("---")
        st.subheader("🔥 Daily Calorie Tracker")

        if "calories_today" not in st.session_state:
            st.session_state.calories_today = 0

        food_item = st.text_input("What did you eat?")
        calories = st.number_input("Calories", 0, 2000, 100)

        if st.button("Add Meal"):
            st.session_state.calories_today += calories
            st.success(f"Added! Total today: {st.session_state.calories_today} kcal")

        st.info(f"🔥 Total Calories Today: {st.session_state.calories_today}")

        target = int(get_val("DailyCalories")) if str(get_val("DailyCalories")).isdigit() else 2000

        if st.session_state.calories_today > target:
            st.warning("⚠️ You exceeded your calorie goal!")
        else:
            st.success("✅ You are within your calorie goal!")
            
            
        # -----------------------------

            
    
# 🛒 GROCERY LIST
# -----------------------------
        st.markdown("---")

        if st.button("🛒 Generate Grocery List"):
            prompt = f"""
        User Diet: {get_val('DietType')}
        Taste: {get_val('TastePreferences')}
        Goal: {get_val('WeightGoal')}

        Generate weekly grocery list.
        """
            st.success(safe_generate(prompt))
            
            # -----------------------------
# ⚖️ BMI CALCULATOR
# -----------------------------
        st.markdown("---")
        st.subheader("⚖️ BMI Calculator")

        height = st.number_input("Height (cm)", 100, 220, 170)
        weight = st.number_input("Weight (kg)", 30, 150, 65)

        if st.button("Calculate BMI"):
            bmi = weight / ((height/100) ** 2)
            st.info(f"Your BMI: {round(bmi,2)}")

            if bmi < 18.5:
                st.warning("Underweight")
            elif bmi < 25:
                st.success("Normal weight")
            else:
                st.error("Overweight")
                
   # -----------------------------
# TAB 3: Food History (Fixed)
# -----------------------------
    with tab3:
        st.header("📂 Food Profiles & History")

        if os.path.exists("food_profiles.csv"):
            st.dataframe(pd.read_csv("food_profiles.csv"))
        else:
            st.info("No food profiles found.")
            
    with tab4:
        st.header("💬 Chat AI - Personalized Food Guidance")

        if user_profile is None:
            st.warning("⚠️ Create food profile first in Tab 1")
            st.stop()

        if "food_chat_history" not in st.session_state:
            st.session_state.food_chat_history = []

        query = st.text_input("Ask something about food/diet", key="food_chat_query")

        if st.button("Ask AI") and query.strip() != "":

            # ✅ CLEAN BUT ADVANCED PROMPT
            prompt_chat = f"""
    You are an expert AI nutritionist.

    User Profile:
    Name: {get_val('Name')}
    Age: {get_val('Age')}
    Taste Preferences: {get_val('TastePreferences')}
    Favorite Foods: {get_val('FavoriteFoods')}
    Diet Type: {get_val('DietType')}
    Allergies: {get_val('Allergies')}
    Mood: {get_val('Mood')}
    Spice Level: {get_val('SpiceLevel')}
    Sweet Preference: {get_val('SweetLevel')}

    User Question: {query}

    Instructions:
    - Understand user's mood
    - Give personalized food suggestions
    - Suggest healthy alternatives
    - Mention foods to avoid if needed
    - Keep answer simple and practical
    - If user exceeds calories → warn
    - If unhealthy pattern → suggest improvement
    """

            with st.spinner("🍽️ AI is thinking..."):
                response = safe_generate(prompt_chat)

            # Save chat history
            st.session_state.food_chat_history.append({
                "query": query,
                "response": response
            })

        # -----------------------------
        # DISPLAY CHAT HISTORY
        # -----------------------------
        if st.session_state.food_chat_history:
            st.markdown("### 💬 Chat History")

            for chat in st.session_state.food_chat_history[::-1]:
                st.markdown(f"**You:** {chat['query']}")
                st.markdown(f"**AI:** {chat['response']}")
                st.markdown("---")