import pickle
import streamlit as st
from PIL import Image

# Load the saved model
model = pickle.load(open('RFMmodel.sav', 'rb'))

# Load and display the image
image = Image.open("LoanDrive.jpg")
st.set_page_config(page_title="LoanDrive - Loan Default Predictor", page_icon=image, layout="wide")

# Custom CSS for styling
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
        max-width: 200px; /* Resize the image */
        height: auto;
    }
    input, select, textarea, .stTextInput, .stSelectbox, .stSlider {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    label {
        color: #000000 !important; /* Ensure label visibility */
    }
    select {
        background-color: #e6e6e6 !important; /* Lighter color for select boxes */
    }
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
        color: #000000; /* Ensure message text is visible */
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

# Function for displaying modal (popup)
def show_modal(message, success=True):
    st.markdown(f"""
        <div class="modal">
            <div class="modal-content">
                <button class="close-btn" onclick="document.getElementById('close-button').click()">×</button>
                <h4 style="color: {'green' if success else 'red'};">{'Success' if success else 'Error'}</h4>
                <p>{message}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Add a hidden Streamlit button to close the modal
    if st.button("Close", key="close-modal"):
        st.session_state['show_modal'] = False

# Initialize modal visibility in session state
if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

# Function to toggle modal state
def toggle_modal():
    st.session_state['show_modal'] = not st.session_state['show_modal']

# Page Header
st.markdown('<div class="header">Welcome to LoanDrive - Loan Default Prediction</div>', unsafe_allow_html=True)

# Display and center the image
st.image(image, caption="LoanDrive", use_column_width=False)

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

# Main container for the form
with st.container():
    st.markdown('<div class="form-title">Enter the Following Details to Predict Loan Default Status</div>', unsafe_allow_html=True)

    with st.form(key='my_form'):
        col1, col2 = st.columns(2)

        fName = col1.text_input("Client full name: ")

        active_loan = col1.selectbox("Already has an active loan?", ("-", "Yes", "No"))
        education = col1.selectbox("Enter client education:", ("-", 'Secondary', 'Graduation'))
        employed_days = col1.slider("Enter number of employed years before application:", min_value=0, max_value=80)

        income = col1.text_input("Enter client income:", value=0)
        income_type = col2.selectbox("Enter income type:", ("-", 'Commercial', 'Retired', 'Service', 'Student', 'Unemployed'))
        loan_contract_type = col2.selectbox("Enter loan contract type:", ("-", 'Cash Loan', 'Revolving Loan'))

        loan_amount = col1.text_input("Enter loan amount requested:", value=0)
        loan_annuity = col2.text_input("Enter loan annuity amount:", value=0)

        age = col1.slider("Enter age:", min_value=20, max_value=60)

        gender = col1.selectbox("Enter client gender:", ("-", "Female", "Male"))
        child_count = col2.selectbox("Enter child count:", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
        registration = col2.slider("Years since registration:", min_value=0, max_value=50)

        marital_status = col1.selectbox("Enter marital status", ("-", "Divorced", "Single", "Married", "Widow"))
        car_owned = col1.selectbox("Car owner?", ("-", "Yes", "No"))
        bike_owned = col1.selectbox("Bike owner?", ("-", "Yes", "No"))
        house_owned = col1.selectbox("House owner?", ("-", "Yes", "No"))

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
                st.session_state['show_modal'] = True
                show_modal("Following fields are invalid: " + ", ".join(invalid_inputs), success=False)
            else:
                transformed_inputs = input_transformer(inputs_to_transform)

                try:
                    inputs_array = [list(map(float, [inputs[key] for key in inputs])) + transformed_inputs]
                except ValueError as e:
                    st.session_state['show_modal'] = True
                    show_modal(f"Error in input values: {e}", success=False)
                    inputs_array = None

                if inputs_array:
                    st.write("Client Name: " + fName)
                    st.write("Loan Amount: " + loan_amount)

                    try:
                        prediction = model.predict(inputs_array)
                        if prediction[0] == 0:
                            st.session_state['show_modal'] = True
                            show_modal(f"Success: Client Name: {fName}, Loan Amount: {loan_amount}. Please accept the above loan request", success=True)
                        else:
                            st.session_state['show_modal'] = True
                            show_modal(f"Error: Client Name: {fName}, Loan Amount: {loan_amount}. Please reject the above request as client is prone to default on the loan", success=False)
                    except ValueError as e:
                        st.session_state['show_modal'] = True
                        show_modal(f"Error in prediction: {e}", success=False)

# Function to close the modal and clear the form
if st.session_state['show_modal']:
    if st.button("Close"):
        st.session_state['show_modal'] = False
        st.experimental_rerun()
