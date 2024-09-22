import pickle
import streamlit as st

# Load the saved model
model = pickle.load(open('RFMmodel.sav', 'rb'))

def input_transformer(inputs):
    value_map = {
        "House Owned": {"Yes": 1, "No": 0},
        "Car Owned": {"Yes": 1, "No": 0},
        "Bike Owned": {"Yes": 1, "No": 0},
        "Has Active Loan": {"Yes": 1, "No": 0},
        "Client Income Type": {"Commercial": 1, "Service": 2, "Student": 3, "Retired": 4, "Unemployed": 5},
        "Client Education": {"Secondary": 1, "Graduation": 2},
        "Client Marital Status": {'Married': 1, 'Widow': 2, 'Single': 3, 'Divorced': 4},
        "Client Gender": {'Male': 1, 'Female': 2},
        "Loan Contract Type": {'Cash Loan': 1, 'Revolving Loan': 2}
    }

    transformed_inputs = []
    for input, value in inputs.items():
        if value in value_map[input]:
            transformed_inputs.append(value_map[input][value])
        else:
            transformed_inputs.append(None)  # Handle invalid values gracefully

    return transformed_inputs

mainContainer = st.container()

with mainContainer:
    tab = st.table()
    tab1 = tab.form(key='my_form')
    tab1.header("Enter Following Details to predict Loan Default status")

    col1, col2 = tab1.columns(2)

    fName = col1.text_input("Client full name: ")
    active_loan = col1.selectbox("Already has an active loan?", ("-", "Yes", "No"))
    education = col1.selectbox("Enter client education:", ("-", 'Secondary', 'Graduation'))
    employed_days = col1.slider("Enter number of employed years before application:", min_value=0, max_value=80)
    income = col1.text_input("Enter client income:", value="0")
    income_type = col2.selectbox("Enter income type:", ("-", 'Commercial', 'Retired', 'Service', 'Student', 'Unemployed'))
    loan_contract_type = col2.selectbox("Enter loan contract type:", ("-", 'Cash Loan', 'Revolving Loan'))
    loan_amount = col1.text_input("Enter loan amount requested:", value="0")
    loan_annuity = col2.text_input("Enter loan annuity amount:", value="0")
    age = col1.slider("Enter age:", min_value=20, max_value=60)
    gender = col1.selectbox("Enter client gender:", ("-", "Female", "Male"))
    child_count = col2.selectbox("Enter child count:", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    registration = col2.slider("Years since registration:", min_value=0, max_value=50)
    marital_status = col1.selectbox("Enter marital status:", ("-", "Divorced", "Single", "Married", "Widow"))
    car_owned = col1.selectbox("Car owner?", ("-", "Yes", "No"))
    bike_owned = col1.selectbox("Bike owner?", ("-", "Yes", "No"))
    house_owned = col1.selectbox("House owner?", ("-", "Yes", "No"))

    Submit = tab1.form_submit_button("Submit")
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

        invalid_inputs = []

        if fName.strip() == "":
            invalid_inputs.append("Client Name")

        for label, value in inputs.items():
            if value in ['-', None, '']:
                invalid_inputs.append(label)

        for label, value in inputs_to_transform.items():
            if value in ['-', None, '']:
                invalid_inputs.append(label)

        if len(invalid_inputs) > 0:
            invalid_inputs_str = "Following fields are invalid: \n"
            st.error(invalid_inputs_str + ", ".join(invalid_inputs))
        else:
            tab.empty()
            transformed_inputs = input_transformer(inputs_to_transform)

            try:
                inputs_array = [list(map(float, [inputs[key] for key in inputs])) + transformed_inputs]
            except ValueError as e:
                st.error(f"Error in input values: {e}")
                inputs_array = None

            if inputs_array:
                st.write("Client Name: " + fName)
                st.write("Loan Amount: " + loan_amount)

                try:
                    prediction = model.predict(inputs_array)
                    if prediction[0] == 0:
                        st.success("Please accept the above loan request")
                    else:
                        st.error("Please reject the above request as client is more prone to default on the loan")
                except ValueError as e:
                    st.error(f"Error in prediction: {e}")