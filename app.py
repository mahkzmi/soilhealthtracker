import streamlit as st
from database import SoilData, SessionLocal

# ------------------------- UI/UX Styling -------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #008CBA;
        color: white;
        font-size: 16px;
        border-radius: 5px;
    }
    .header {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="header">Soil Health Tracker</div>', unsafe_allow_html=True)
st.write("Welcome! Enter your soil data below and click 'Analyze Soil' to view advanced analysis and improvement suggestions.")

# ------------------------- Input Section -------------------------
user_name = st.text_input("User Name:", value="Ali", help="Enter your name or identifier.")
pH = st.number_input("Soil pH:", value=6.5, step=0.1, help="Typical pH range: 3.5 - 9.0")
moisture = st.number_input("Soil Moisture (%):", value=30, step=1, help="Enter soil moisture percentage.")
nitrogen = st.number_input("Nitrogen (mg/kg):", value=20, step=1)
phosphorus = st.number_input("Phosphorus (mg/kg):", value=15, step=1)
potassium = st.number_input("Potassium (mg/kg):", value=10, step=1)
soil_type = st.selectbox("Soil Type:", ["Loamy", "Sandy", "Clay", "Silty"])

# ------------------------- Advanced Analysis Function -------------------------
def advanced_soil_analysis(pH, moisture, nitrogen, phosphorus, potassium, soil_type):
    score = 0
    # تحلیل pH: بهترین مقدار بین 6.0 تا 7.5 امتیاز بالایی دارد
    if 6.0 <= pH <= 7.5:
        score += 30
    elif pH < 6.0:
        score += 15
    else:
        score += 10

    # تحلیل رطوبت: بین 40 تا 70 بهترین وضعیت است
    if 40 <= moisture <= 70:
        score += 20
    else:
        score += 10

    # تحلیل مواد مغذی (با نرمال‌سازی مقادیر)
    if 20 <= nitrogen <= 100:
        score += 15
    if 10 <= phosphorus <= 80:
        score += 15
    if 10 <= potassium <= 80:
        score += 15

    # تحلیل نوع خاک: خاک لومی امتیاز بیشتری می‌گیرد
    if soil_type == "Loamy":
        score += 10
    elif soil_type == "Sandy":
        score += 5
    else:
        score += 7

    return score

def generate_suggestions(pH, moisture, nitrogen, phosphorus, potassium):
    suggestions = []
    if pH < 6.0:
        suggestions.append("Add lime to neutralize acidity.")
    elif pH > 7.5:
        suggestions.append("Add sulfur to lower alkalinity.")
    
    if moisture < 40:
        suggestions.append("Increase irrigation to improve moisture levels.")
    elif moisture > 70:
        suggestions.append("Improve drainage to avoid waterlogging.")
    
    if nitrogen < 20:
        suggestions.append("Apply nitrogen-rich fertilizers.")
    if phosphorus < 10:
        suggestions.append("Use phosphate fertilizers.")
    if potassium < 10:
        suggestions.append("Increase potassium with appropriate fertilizers.")
    
    return suggestions

# ------------------------- Action Buttons -------------------------
# دکمه "Analyze Soil"
if st.button("Analyze Soil"):
    score = advanced_soil_analysis(pH, moisture, nitrogen, phosphorus, potassium, soil_type)
    suggestions = generate_suggestions(pH, moisture, nitrogen, phosphorus, potassium)
    
    st.success(f"Advanced Soil Health Score: {score}")
    st.write("Improvement Suggestions:")
    for suggestion in suggestions:
        st.write(f"- {suggestion}")

# دکمه "Add Record" برای ذخیره تحلیل
if st.button("Add Record"):
    score = advanced_soil_analysis(pH, moisture, nitrogen, phosphorus, potassium, soil_type)
    # تعیین وضعیت بر اساس امتیاز
    status = "Good" if score >= 70 else "Moderate" if score >= 50 else "Poor"
    
    db = SessionLocal()
    new_entry = SoilData(
        user_name=user_name,
        pH=pH,
        moisture=moisture,
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        soil_type=soil_type,
        health_score=score,
        status=status
    )
    db.add(new_entry)
    db.commit()
    db.close()
    st.success("Record added successfully!")

# دکمه "View All Records" برای مشاهده رکوردهای ذخیره شده
if st.button("View All Records"):
    db = SessionLocal()
    records = db.query(SoilData).all()
    if records:
        for record in records:
            st.write(record.__dict__)
    else:
        st.info("No records found.")
    db.close()