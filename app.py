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
    .header {
        text-align: center;
        font-size: 40px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: #4CAF50;
    }
    .form-header {
        font-size: 20px; /* Adjust the font size as needed */
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: #4CAF50;
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
        <img src="data:image/png;base64,{img_str}" alt="LoanDrive Logo" width="300">
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

    with tab.form(key='my_form'):
        st.markdown(
            """
            <style>
            .form-header {
                font-size: 20px; /* Adjust the font size as needed */
                font-family: 'Arial', sans-serif;
                font-weight: bold;
                color: #333333;
            }
            </style>
            <h2 class="form-header">Enter the Following Details to Predict Loan Default Status</h2>
            """,
            unsafe_allow_html=True
        )

    col1 , col2 = tab1.columns(2)

    fName = col1.text_input("Client full name: ")

    active_loan = col1.selectbox("Already has an active loan?" , ("-", "Yes" , "No"))
    education = col1.selectbox("Enter client education: " , ("-", 'Secondary', 'Graduation') , on_change=None)
    employed_days = col1.slider("Enter number of employed years before application: " , min_value = 0 , max_value= 80 , on_change=None)

    income = col1.text_input("Enter client income: "  , value = 0 ,on_change=None)
    income_type = col2.selectbox("Enter income type: " , ("-", 'Commercial','Retired' ,'Service', 'Student' , 'Unemployed') , on_change=None)
    loan_contract_type = col2.selectbox("Enter loan contract type: " , ("-", 'Cash Loan', 'Revolving Loan') , on_change=None)

    loan_amount = col1.text_input("Enter loan amount requested: " , value = 0 , on_change=None)
    loan_annuity = col2.text_input("Enter loan annuity amount: " , value = 0 , on_change=None)

    age = col1.slider("Enter age: " , min_value = 20 , max_value= 60 , on_change=None)

    gender = col1.selectbox("Enter client gender: " , ("-", "Female", "Male" ) , on_change=None)
    child_count = col2.selectbox("Enter child count: " , (0,1,2,3,4,5,6,7,8,9,10) , on_change=None)
    registration = col2.slider("Years since registration: " , min_value = 0 , max_value= 50 , on_change=None)

    marital_status = col1.selectbox("Enter marital status" , ("-", "Divorced", "Single", "Married", "Widow"))
    car_owned = col1.selectbox("Car owner?" , ("-", "Yes" , "No"))
    bike_owned = col1.selectbox("Bike owner?" , ("-", "Yes" , "No"))
    house_owned = col1.selectbox("House owner?" , ("-", "Yes" , "No"))


    Submit = tab1.form_submit_button("Submit")
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

        if loan_amount.strip() == "0" or loan_amount.strip() == "":
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
           st.write("Loan Amount: " + loan_amount)
           # print(inputs)
           prediction  = model.predict(inputs_array)
           if prediction[0] == 0:
               st.success("Please accept the above loan request")
           else:
               st.error("Please reject the above request as client is more prone to default on the loan")