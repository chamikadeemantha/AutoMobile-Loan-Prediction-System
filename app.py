import pickle
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# loading the saved models
model = pickle.load(open('RFModel.sav', 'rb'))

# Load the image
image = Image.open("LoanDrive.png")

# Convert the image to a base64 string
buffered = BytesIO()
image.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Set page configuration
st.set_page_config(page_title="LoanDrive - Loan Default Predictor", page_icon=image, layout="wide")

# Create centered header
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rampart+One&display=swap');
    .header {
        text-align: center;
        font-size: 40px;
        font-family: 'Rampart One', sans-serif;
        font-weight: bold;
        color: #FAF7F0;
    }
    </style>
    <h1 class="header">Welcome to LoanDrive - Loan Default Prediction</h1>
    """,
    unsafe_allow_html=True
)

# Centering the image using HTML
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{img_str}" alt="LoanDrive Logo" width="400">
    </div>
    """,
    unsafe_allow_html=True
)


def input_transformer(inputs):
    value_map = {
        "House Owned": {
            "Yes": 1,
            "No": 0
        },
        "Car Owned": {
            "Yes": 1,
            "No": 0
        },
        "Bike Owned": {
            "Yes": 1,
            "No": 0
        },
        "Has Active Loan": {
            "Yes": 1,
            "No": 0
        },
        "Client Income Type": {
            "Commercial": 1,
            "Service": 2,
            "Student": 3,
            "Retired": 4,
            "Unemployed": 5
        },
        "Client Education": {
            "Secondary": 1,
            "Graduation": 2
        },
        "Client Marital Status": {
            'Married': 1,
            'Widow': 2,
            'Single': 3,
            'Divorced':4
        },
        "Client Gender": {
            'Male': 1,
            'Female': 2
        },
        "Loan Contract Type": {
            'Cash Loan': 1,
            'Revolving Loan': 2
        }
    }

    transformed_inputs = []
    for input, value in inputs.items():
        if (value_map[input] != None and value_map[input][value] != None):
            transformed_inputs.append(value_map[input][value])

    return transformed_inputs


mainContainer = st.container()

with mainContainer:
    
    tab = st.table()

    tab1 = tab.form(key='my_form')
    tab1.header("Enter the Following Details to Predict Loan Default Status")

    col1 , col2 = tab1.columns(2)

    fName = col1.text_input("Client full name: ")

    active_loan = col1.selectbox("Already has an active loan?" , ("-", "Yes" , "No"))
    education = col1.selectbox("Enter client education: " , ("-", 'Secondary', 'Graduation') , on_change=None)
    employed_days = col1.slider("Enter number of employed years before application: " , min_value = 0 , max_value= 80 , on_change=None)

    
    income = col2.number_input("Enter client income: ", min_value=0.0, step=10000.00)
    income_type = col2.selectbox("Enter income type: " , ("-", 'Commercial','Retired' ,'Service', 'Student' , 'Unemployed') , on_change=None)
    loan_contract_type = col2.selectbox("Enter loan contract type: " , ("-", 'Cash Loan', 'Revolving Loan') , on_change=None)

    
    loan_amount = col2.number_input("Enter loan amount requested: ", min_value=0.0, step=10000.00)

    loan_annuity = col2.number_input("Enter loan annuity amount: ", min_value=0.0, step=10000.00)

    age = col2.slider("Enter age: " , min_value = 20 , max_value= 60 , on_change=None)

    gender = col1.selectbox("Enter client gender: " , ("-", "Female", "Male" ) , on_change=None)
    child_count = col2.selectbox("Enter child count: " , (0,1,2,3,4,5,6,7,8,9,10) , on_change=None)
    registration = col2.slider("Years since registration: " , min_value = 0 , max_value= 50 , on_change=None)

    marital_status = col1.selectbox("Enter marital status" , ("-", "Divorced", "Single", "Married", "Widow"))
    car_owned = col1.selectbox("Car owner?" , ("-", "Yes" , "No"))
    bike_owned = col1.selectbox("Bike owner?" , ("-", "Yes" , "No"))
    house_owned = col1.selectbox("House owner?" , ("-", "Yes" , "No"))

    # Centering the submit button using columns
    col_center = tab1.columns([1, 1, 1])
    with col_center[1]:
        Submit = st.form_submit_button("Submit", help="Click to submit the form")

    if Submit:
        inputs = { "Loan Amount":loan_amount , "Income": income , "Loan Annuity":loan_annuity , "Age": age, "Child Count": child_count, "Employed Days": employed_days, "Years since registration": registration }
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


        invalid_inputs = []

        if fName.strip() == "":
            invalid_inputs.append("Client Name")

        # Updated validation logic
        if loan_amount == 0:
            invalid_inputs.append("Loan Amount")

        for label, value in inputs.items():
            if value == '-' or value == "-" or value == None:
                invalid_inputs.append(label)

        for label, value in inputs_to_transform.items():
            if value == '-' or value == "-" or value == None:
                invalid_inputs.append(label)


        if len(invalid_inputs) > 0:
            invalid_inputs_str = "Following fields are invalid: \n"
            st.error(invalid_inputs_str + ", ".join(invalid_inputs))
        else:
            tab.empty()
            transformed_inputs = input_transformer(inputs_to_transform)
            inputs_array = [list(inputs.values()) + transformed_inputs]
            st.write("Client Name: " + fName)
            st.write("Loan Amount: " + str(loan_amount))
            # print(inputs)
            if inputs.get('Loan Annuity') >= 50000:
                st.error("Please reject the above request as client is more prone to default on the loan")
            else:
                prediction = model.predict(inputs_array)
                if prediction[0] == 0:
                    st.success("Please accept the above loan request")
                else:
                    st.error("Please reject the above request as client is more prone to default on the loan")