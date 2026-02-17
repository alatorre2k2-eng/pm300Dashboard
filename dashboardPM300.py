import streamlit as st

st.set_page_config(page_title="Grade Dashboard", layout="wide")

# -------- CUSTOM CSS --------
st.markdown("""
<style>

/* Remove excess padding */
.block-container {
    padding-top: 2rem;
}



/* Vertical divider */
.vertical-line {
    border-left: 3px solid #2ecc71;
    height: 90vh;
    margin: auto;
}

/* Improve metric text contrast */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("📊PM300 GRADE DASHBOARD")

col_left, col_mid, col_right = st.columns([1, 0.02, 1])

# =========================
# FIRST PARTIAL
# =========================
with col_left:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    st.markdown("## 🟢 First Partial")

    p1_class = st.number_input("Class Activities + Quick Exams (20%)", 0.0, 100.0, key="p1_class")
    p1_formative = st.number_input("Formative & Collaborative Activities (10%)", 0.0, 100.0, key="p1_formative")
    p1_inter = st.number_input("Interpartial Exam (20%)", 0.0, 100.0, key="p1_inter")
    p1_exam = st.number_input("Partial Exam (50%)", 0.0, 100.0, key="p1_exam")

    p1_total = (
        0.20 * p1_class +
        0.10 * p1_formative +
        0.20 * p1_inter +
        0.50 * p1_exam
    )

    st.divider()
    st.metric("First Partial Grade", f"{p1_total:.2f}")

    # Performance feedback
    if p1_total >= 90:
        st.success("🔥 Excellent performance! Keep it up.")
    elif p1_total >= 70:
        st.info("👍 Passing grade. Stay consistent.")
    else:
        st.warning("⚠️ At risk. You need to improve upcoming components.")

    st.markdown('</div>', unsafe_allow_html=True)

# Divider
with col_mid:
    st.markdown('<div class="vertical-line"></div>', unsafe_allow_html=True)
# =========================
# SECOND PARTIAL
# =========================
with col_right:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    st.markdown("## 🟩 Second Partial")

    # ---------- TARGET CALCULATION FIRST ----------
    target_p2 = st.number_input(
        "Desired Partial 2 Grade",
        min_value=60.0,
        max_value=100.0,
        value=70.0,
        step=1.0,
        key="target_p2"
    )

    # Get existing values safely (default 0 if not yet set)
    p2_class_val = st.session_state.get("p2_class", 0.0)
    p2_formative_val = st.session_state.get("p2_formative", 0.0)

    current_p2_contribution = 0.20 * p2_class_val + 0.10 * p2_formative_val
    remaining_p2_weight = 0.70

    required_p2_score = (target_p2 - current_p2_contribution) / remaining_p2_weight
    required_p2_score = max(0, min(100, required_p2_score))

    if required_p2_score <= 0:
        st.success("✅ You already secured this Partial 2 grade.")
    elif required_p2_score > 100:
        st.error("❗ Even scoring 100 on remaining exams will not reach this target.")
    else:
        st.info(
            f"If you perform equally on Interpartial and Partial Exam, "
            f"you need approximately **{required_p2_score:.2f}** on each."
        )

        if st.button("Autofill Partial 2 Balanced Scores"):
            st.session_state["p2_inter"] = required_p2_score
            st.session_state["p2_exam"] = required_p2_score
            st.rerun()

    st.markdown("---")

    # ---------- NOW CREATE INPUT WIDGETS ----------
    p2_class = st.number_input(
        "Class Activities + Quick Exams (20%)",
        0.0, 100.0,
        key="p2_class"
    )

    p2_formative = st.number_input(
        "Formative & Collaborative Activities (10%)",
        0.0, 100.0,
        key="p2_formative"
    )

    p2_inter = st.number_input(
        "Interpartial Exam (20%)",
        0.0, 100.0,
        key="p2_inter"
    )

    p2_exam = st.number_input(
        "Partial Exam (50%)",
        0.0, 100.0,
        key="p2_exam"
    )

    # ---------- TOTAL ----------
    p2_total = (
        0.20 * p2_class +
        0.10 * p2_formative +
        0.20 * p2_inter +
        0.50 * p2_exam
    )

    st.divider()
    st.metric("Second Partial Grade", f"{p2_total:.2f}")

    if p2_total >= 90:
        st.success("🔥 Excellent performance! Keep it up.")
    elif p2_total >= 70:
        st.info("👍 Passing grade. Stay consistent.")
    else:
        st.warning("⚠️ At risk. You need to improve upcoming components.")

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# FINAL GRADE SECTION
# ==========================================================
#-----------------------------------autofill
st.markdown("---")  # Horizontal line

st.markdown("---")
st.subheader("🎯 Balanced Target Strategy")

target_grade = st.number_input(
    "Desired Final Course Grade",
    min_value=60.0,
    max_value=100.0,
    value=70.0,
    step=1.0
)

# Current contribution from partials + fixed components
current_contribution = (
    0.28 * p1_total +
    0.26 * p2_total +
    0.08 * st.session_state.get("final_class", 0.0) +
    0.04 * st.session_state.get("final_formative", 0.0)
)

# Remaining weight ONLY exam-type components
remaining_weight = 0.34  # 4% interpartial + 30% final exam

required_score = (target_grade - current_contribution) / remaining_weight
required_score = max(0, min(100, required_score))

if remaining_weight > 0:
    if required_score <= 0:
        st.success("✅ You already secured this final grade.")
    elif required_score > 100:
        st.error("❗ Even scoring 100 on remaining exams will not reach this target.")
    else:
        st.info(
            f"If you perform equally on Final Interpartial and Final Exam, "
            f"you need approximately **{required_score:.2f}** on each."
        )

if st.button("Autofill Final Exam Targets"):
    st.session_state.final_interpartial = required_score
    st.session_state.final_exam = required_score
    st.rerun()


st.header("🎓 FINAL COURSE GRADE")

st.markdown("Enter remaining components for final calculation:")

col_final1, col_final2 = st.columns(2)

with col_final1:
    final_interpartial = st.number_input(
        "Final Interpartial Exam (4%)",
        0.0, 100.0,
        key="final_interpartial",
    )

    final_class = st.number_input(
        "Final Class Activities + Quick Exams (8%)",
        0.0, 100.0,
        key="final_class",
    )
with col_final2:
    final_formative = st.number_input(
        "Final Formative & Collaborative Activities (4%)",
        0.0, 100.0,
        key="final_formative",
    )


    final_exam = st.number_input(
        "Final Exam (30%)",
        0.0, 100.0,
        key="final_exam",
    )
# ------------------------
# FINAL GRADE CALCULATION
# ------------------------

final_grade = round(
    0.28 * p1_total +
    0.26 * p2_total +
    0.04 * final_interpartial +
    0.08 * final_class +
    0.04 * final_formative +
    0.30 * final_exam
)


#-------------------------------------



st.markdown("## 🏆 FINAL GRADE")

# Highlighted final grade box
st.markdown(
    f"""
    <div style="
        background-color:#1e5631;
        padding:30px;
        border-radius:15px;
        text-align:center;
        font-size:40px;
        font-weight:bold;
        border:3px solid #2ecc71;">
        {final_grade:.2f}
    </div>
    """,
    unsafe_allow_html=True
)

# Performance message
if final_grade >= 90:
    st.success("🔥 Outstanding final performance!")
elif final_grade >= 70:
    st.info("👍 You passed the course.")
else:
    st.error("❗ Course at risk. Final performance below passing threshold.")
