import pickle
import streamlit as st
from PIL import Image

# Load the saved model
model = pickle.load(open('RFMmodel.sav', 'rb'))

# Load and display the image
image = Image.open("LoanDrive.jpg")
st.set_page_config(page_title="LoanDrive - Loan Default Predictor", page_icon=image, layout="wide")

# Custom CSS for toast, modal, and label styling
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .header {
        font-size: 32px;
        font-weight: bold;
        color: #003f88;
        margin-bottom: 20px;
        text-align: center;
    }
    .form-title {
        font-size: 22px;
        font-weight: bold;
        color: #007bff;
        margin-bottom: 15px;
        text-align: center;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 10px;    
    }
    .block-container {
        padding-top: 2rem;
    }
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .stImage img {
        max-width: 200px;
        height: auto;
    }
    input, select, textarea, .stTextInput, .stSelectbox, .stSlider {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    label {
        font-size: 18px !important;
        font-weight: bold;
        color: #000000 !important;
    }
    select {
        background-color: #c1c1c1 !important;
    }
    /* Custom toast message styling */
    .toast {
        visibility: visible;
        max-width: 400px;
        margin: auto;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 12px;
        padding: 15px;
        position: fixed;
        z-index: 1;
        right: 20px;
        bottom: 30px;
        font-size: 16px;
    }
    .toast-error {
        background-color: #dc3545;
    }
    .toast-close-btn {
        margin-left: 10px;
        color: white;
        cursor: pointer;
        font-weight: bold;
    }
    /* Modal styling */
    .modal {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    .modal-content {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        max-width: 600px;
        text-align: center;
        position: relative;
        font-size: 18px;
        color: #000000;
    }
    .close-btn {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 24px;
        font-weight: bold;
        color: #333;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Function to reset form inputs
def reset_form():
    for key in st.session_state.keys():
        if key.startswith("input_"):
            st.session_state[key] = ""

# Initialize session state for inputs if not already done
if "show_modal" not in st.session_state:
    st.session_state["show_modal"] = False

# Function to display custom toast messages for errors
def display_toast(message):
    st.markdown(f"""
        <div class="toast toast-error">
            {message}
            <span class="toast-close-btn">×</span>
        </div>
        <script>
            setTimeout(function() {{
                var toast = document.querySelector('.toast');
                if (toast) {{
                    toast.style.visibility = 'hidden';
                }}
            }}, 6000);
        </script>
    """, unsafe_allow_html=True)

# Function to display a success popup (modal)
def display_success_modal(client_name, loan_amount):
    st.markdown(f"""
        <div class="modal">
            <div class="modal-content">
                <button class="close-btn" onclick="document.getElementById('close-button').click()">×</button>
                <h4 style="color: green; font-size: 24px; font-weight: bold;">Success</h4>
                <p style="text-align: left; font-size: 18px;">
                    <b>Client Name:</b> {client_name}<br>
                    <b>Loan Amount:</b> {loan_amount}
                </p>
                <p style="text-align: left; font-size: 16px;">Loan request accepted.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Add a hidden button to close the modal
    if st.button("Close", key="close-modal"):
        st.session_state['show_modal'] = False
        reset_form()  # Reset form inputs when modal is closed

# Function to transform input values
def input_transformer(inputs):
    value_map = {
        "House Owned": {"Yes": 1, "No": 0},
        "Car Owned": {"Yes": 1, "No": 0},
        "Bike Owned": {"Yes": 1, "No": 0},
        "Has Active Loan": {"Yes": 1, "No": 0},
        "Client Income Type": {
            "Commercial": 1, "Service": 2, "Student": 3, "Retired": 4, "Unemployed": 5
        },
        "Client Education": {
            "Secondary": 1, "Graduation": 2
        },
        "Client Marital Status": {
            'Married': 1, 'Widow': 2, 'Single': 3, 'Divorced': 4
        },
        "Client Gender": {
            'Male': 1, 'Female': 2
        },
        "Loan Contract Type": {
            'Cash Loan': 1, 'Revolving Loan': 2
        }
    }

    transformed_inputs = []
    for input, value in inputs.items():
        if input in value_map and value in value_map[input]:
            transformed_inputs.append(value_map[input][value])
        else:
            transformed_inputs.append(value)
    return transformed_inputs

# Page Header
st.markdown('<div class="header">Welcome to LoanDrive - Loan Default Prediction</div>', unsafe_allow_html=True)

# Display and center the image
st.image(image, caption="LoanDrive", use_column_width=False)

# Main container for the form
with st.container():
    st.markdown('<div class="form-title">Enter the Following Details to Predict Loan Default Status</div>', unsafe_allow_html=True)

    with st.form(key='my_form'):
        col1, col2 = st.columns(2)

        # Store form values in session state
        fName = col1.text_input("Client full name:", key="input_fName")
        active_loan = col1.selectbox("Already has an active loan?", ("-", "Yes", "No"), key="input_active_loan")
        education = col1.selectbox("Enter client education:", ("-", 'Secondary', 'Graduation'), key="input_education")
        employed_days = col1.slider("Enter number of employed years before application:", min_value=0, max_value=80, key="input_employed_days")
        income = col1.text_input("Enter client income:", value=0, key="input_income")
        income_type = col2.selectbox("Enter income type:", ("-", 'Commercial', 'Retired', 'Service', 'Student', 'Unemployed'), key="input_income_type")
        loan_contract_type = col2.selectbox("Enter loan contract type:", ("-", 'Cash Loan', 'Revolving Loan'), key="input_loan_contract_type")
        loan_amount = col1.text_input("Enter loan amount requested:", value=0, key="input_loan_amount")
        loan_annuity = col2.text_input("Enter loan annuity amount:", value=0, key="input_loan_annuity")
        age = col1.slider("Enter age:", min_value=20, max_value=60, key="input_age")
        gender = col1.selectbox("Enter client gender:", ("-", "Female", "Male"), key="input_gender")
        child_count = col2.selectbox("Enter child count:", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key="input_child_count")
        registration = col2.slider("Years since registration:", min_value=0, max_value=50, key="input_registration")
        marital_status = col1.selectbox("Enter marital status", ("-", "Divorced", "Single", "Married", "Widow"), key="input_marital_status")
        car_owned = col1.selectbox("Car owner?", ("-", "Yes", "No"), key="input_car_owned")
        bike_owned = col1.selectbox("Bike owner?", ("-", "Yes", "No"), key="input_bike_owned")
        house_owned = col1.selectbox("House owner?", ("-", "Yes", "No"), key="input_house_owned")

        Submit = st.form_submit_button("Submit")

        if Submit:
            inputs = {
                "Loan Amount": loan_amount,
                "Income": income,
                "Loan Annuity": loan_annuity,
                "Age": age,
                "Child Count": child_count,
                "Employed Days": employed_days,
                "Years since registration": registration
            }
            inputs_to_transform = {
                "House Owned": house_owned,
                "Car Owned": car_owned,
                "Bike Owned": bike_owned,
                "Has Active Loan": active_loan,
                "Client Income Type": income_type,
                "Client Education": education,
                "Client Marital Status": marital_status,
                "Client Gender": gender,
                "Loan Contract Type": loan_contract_type
            }

            invalid_inputs = [label for label, value in inputs.items() if value in ['-', None, '']]
            invalid_inputs += [label for label, value in inputs_to_transform.items() if value in ['-', None, '']]

            if invalid_inputs:
                display_toast(f"Error: Following fields are invalid: " + ", ".join(invalid_inputs))
            else:
                transformed_inputs = input_transformer(inputs_to_transform)

                try:
                    inputs_array = [list(map(float, [inputs[key] for key in inputs])) + transformed_inputs]
                except ValueError as e:
                    display_toast(f"Error in input values: {e}")
                    inputs_array = None

                if inputs_array:
                    st.write("Client Name: " + fName)
                    st.write("Loan Amount: " + loan_amount)

                    try:
                        prediction = model.predict(inputs_array)
                        if prediction[0] == 0:
                            display_success_modal(fName, loan_amount)
                        else:
                            display_toast(f"Error: Client Name: {fName}, Loan Amount: {loan_amount}. Client prone to default. Loan request rejected.")
                    except ValueError as e:
                        display_toast(f"Error in prediction: {e}")
