from django import forms 

class PropertySearchForm(forms.Form):
    
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    status = forms.ChoiceField(
        choices=[('', 'Status'), ('1', 'Rent'), ('2', 'Purchase')],
        widget=forms.Select(attrs={'class': 'selectpicker', 'style': 'width: 100%'})
    )
    state_choices = [
        ('', 'Select State'),
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Kelantan', 'Kelantan'),
        ('Melaka', 'Melaka'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pahang', 'Pahang'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Perak', 'Perak'),
        ('Perlis', 'Perlis'),
        ('Selangor', 'Selangor'),
        ('Terengganu', 'Terengganu'),
        ('Sabah', 'Sabah'),
        ('Sarawak', 'Sarawak'),
        ('Kuala Lumpur', 'Kuala Lumpur'),
        ('Labuan', 'Labuan'),
        ('Putrajaya', 'Putrajaya'), 
    ]

    state = forms.ChoiceField(choices=state_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    property_type = forms.ChoiceField(
        choices=[('', 'Property Type'), ('1', 'Apartment'), ('2', 'Condominium'), ('3', 'House')],
        widget=forms.Select(attrs={'class': 'selectpicker', 'style': 'width: 100%'})
    )
    radius = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2.5 KM', 'style': 'width: 100%'})
    )
     
class StateSelectionForm(forms.Form):
    state_choices = [
        ('', 'Select State'),
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Kelantan', 'Kelantan'),
        ('Melaka', 'Melaka'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pahang', 'Pahang'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Perak', 'Perak'),
        ('Perlis', 'Perlis'),
        ('Selangor', 'Selangor'),
        ('Terengganu', 'Terengganu'),
        ('Sabah', 'Sabah'),
        ('Sarawak', 'Sarawak'),
        ('Kuala Lumpur', 'Kuala Lumpur'),
        ('Labuan', 'Labuan'),
        ('Putrajaya', 'Putrajaya'),
    ]
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(choices=state_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

class LoanCalculatorForm(forms.Form):



    age = forms.IntegerField(
        min_value=18, max_value=65,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    family_member = forms.DecimalField(
        min_value=0, max_value=25,
    )


    
    down_payment = forms.IntegerField(
        min_value=0, max_value=99999999,
    )
    property_price = forms.IntegerField(
        min_value=20000, max_value=99999999,
    )
    interest_rate = forms.DecimalField(
        max_digits=4, decimal_places=2, min_value=0, max_value=10
    )


    monthly_income = forms.IntegerField(
        min_value=1500, max_value=55000,
        widget=forms.NumberInput(attrs={'type': 'number'}, )
          
    )
    gross_monthly = forms.IntegerField(
        min_value=1500, max_value=55000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    average_commision_monthly = forms.IntegerField(
        min_value=0, max_value=55000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    other_income_monthly = forms.IntegerField(
        min_value=0, max_value=100000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    income_yearly = forms.IntegerField(
        min_value=0, max_value=100000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    EPF_Choice = [
        ('', 'Select EPF'),
        ('0', '0'),
        ('9', '9'),
        ('11', '11'),
    ]

    EPF = forms.ChoiceField(choices=EPF_Choice, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    PCB = forms.IntegerField(
        min_value=0, max_value=55000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    


    car_loan = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    house_loan = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    personal_loan = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    education_loan = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    other_loan = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    credit_card_outstanding = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    existing_debts = forms.IntegerField(
        min_value=0, max_value=55000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )


    

    current_rental = forms.IntegerField(
        min_value=0, max_value=100000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )   
    electric_bil = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    water_bil = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    internet = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    other_bil = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )
    insurance = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    ) 





    insurance = forms.IntegerField(
        min_value=0, max_value=100000000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )



     




    household_member = forms.DecimalField(
        min_value=0, max_value=25,
    )
    parent_allowance = forms.IntegerField(
        min_value=20000, max_value=99999999,
    )



 
    loan_term = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={'type': 'number'}),
        required=False  # This field is not required initially
    )

    def clean_loan_term(self):
        age = self.cleaned_data.get('age')
        requested_loan_term = self.cleaned_data.get('loan_term')

        if age is None:
            raise forms.ValidationError("Please enter your age first.")

        if requested_loan_term is None:
            return None  # Return None if loan term is not provided yet

        # Calculate the maximum allowed loan term based on age, capped at 35
        max_loan_term = min(65 - age, 35)

        if requested_loan_term <= max_loan_term:
            return requested_loan_term
        else:
            raise forms.ValidationError(
                f"The maximum loan term allowed for your age is {max_loan_term} years."
            )

class AI_Buyer_Advisor_Form(forms.Form):
    age = forms.IntegerField(
    min_value=18, max_value=65,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    total_family_member = forms.IntegerField(
    min_value=0, max_value=20,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    total_kid = forms.IntegerField(
    min_value=0, max_value=15,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    monthly_income = forms.IntegerField(
    min_value=1500, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    additional_monthly_income = forms.IntegerField(
    min_value=1500, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    personal_tax = forms.IntegerField(
        min_value=0, max_value=50000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    ) 

    phone_bill_monthly = forms.IntegerField(
        min_value=0, max_value=1000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    internet_bill_monthly = forms.IntegerField(
        min_value=0, max_value=1000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    utility_bill_monthly = forms.IntegerField(
        min_value=0, max_value=1000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    insurance_monthly = forms.IntegerField(
        min_value=0, max_value=10000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    car_motorcycle_monthly = forms.IntegerField(
    min_value=0, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    child_allowance = forms.IntegerField(
    min_value=0, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    current_rental_commitment = forms.IntegerField(
    min_value=0, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    housing_loan = forms.IntegerField(
    min_value=0, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    pa_loan_monthly = forms.IntegerField(
    min_value=0, max_value=55000,
    widget=forms.NumberInput(attrs={'type': 'number'})
    )

    other_monthly_commitment = forms.IntegerField(
        min_value=0, max_value=10000,
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    down_payment = forms.IntegerField(
        min_value=0, max_value=99999999,
    )
    property_price = forms.IntegerField(
        min_value=20000, max_value=99999999,
    )
    interest_rate = forms.DecimalField(
        max_digits=4, decimal_places=2, min_value=0, max_value=10
    )
    loan_term = forms.IntegerField(
        min_value=0, widget=forms.NumberInput(attrs={'type': 'number'}),
        required=False  # This field is not required initially
    )

    def clean_loan_term(self):
        age = self.cleaned_data.get('age')
        requested_loan_term = self.cleaned_data.get('loan_term')

        if age is None:
            raise forms.ValidationError("Please enter your age first.")

        if requested_loan_term is None:
            return None  # Return None if loan term is not provided yet

        # Calculate the maximum allowed loan term based on age, capped at 35
        max_loan_term = min(65 - age, 35)

        if requested_loan_term <= max_loan_term:
            return requested_loan_term
        else:
            raise forms.ValidationError(
                f"The maximum loan term allowed for your age is {max_loan_term} years."
            )

  
class AnalyticForm(forms.Form):
    
    
    name = forms.CharField(
        #max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
    )
    phone_number = forms.CharField(
        #max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
         
    )
    email = forms.EmailField(
        #max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    state_choices = [
        ('', 'Select State'),
        ('Johor', 'Johor'),
        ('Kedah', 'Kedah'),
        ('Kelantan', 'Kelantan'),
        ('Melaka', 'Melaka'),
        ('Negeri Sembilan', 'Negeri Sembilan'),
        ('Pahang', 'Pahang'),
        ('Pulau Pinang', 'Pulau Pinang'),
        ('Perak', 'Perak'),
        ('Perlis', 'Perlis'),
        ('Selangor', 'Selangor'),
        ('Terengganu', 'Terengganu'),
        ('Sabah', 'Sabah'),
        ('Sarawak', 'Sarawak'),
        ('Kuala Lumpur', 'Kuala Lumpur'),
        ('Labuan', 'Labuan'),
        ('Putrajaya', 'Putrajaya'),
    ]
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(choices=state_choices, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    HOUSE_TYPES = [
        ('', 'Select House Types'),
        ('Detached', 'Detached'),
        ('Semi-Detached', 'Semi-Detached'),
        ('Terraced', 'Terraced'),
        ('Bungalow', 'Bungalow'),
        ('Flat', 'Flat'),
        ('Appartment', 'Appartment'),
        ('Studio', 'Studio')
    ]

    house_type = forms.ChoiceField(choices=HOUSE_TYPES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    year_built = forms.IntegerField(
        min_value=1850,max_value=3000, widget=forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Year Built'}), 
    ) 
     
class housing_analytic_report_form(forms.Form):
   
    number_of_floors = forms.IntegerField(
        min_value=0,max_value=200, widget=forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Number of Floors'}), 
    )
    number_of_rooms = forms.IntegerField(
        min_value=0,max_value=20, widget=forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Number of Rooms'}), 
    )
    number_of_bathrooms = forms.IntegerField(
        min_value=0,max_value=15, widget=forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Number of Bathrooms'}), 
    )
    built_up_area = forms.FloatField(
        min_value=0,max_value=15000, widget=forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Built-up Area (sq ft/m²)'}), 
    )

    expenditure = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Expenditure'}))
    income = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Income'}))
    number_of_family_members = forms.IntegerField(min_value=0, max_value=20, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Family Members'}))

  
