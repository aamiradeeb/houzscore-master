from django.shortcuts import render
from .forms import LoanCalculatorForm  
import plotly.graph_objs as go 
from decimal import Decimal
import requests
from django.shortcuts import render 
import requests
import requests 
import overpy
from geopy.distance import great_circle
from .forms import StateSelectionForm
from .forms import PropertySearchForm 
from .forms import AnalyticForm

def calculate_distance(lat1, lon1, lat2, lon2):
 
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    distance = great_circle(point1, point2).kilometers
    return round(distance, 2)


    # Convert latitude and longitude from degrees to radians
    #lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    #dlat = lat2 - lat1
    #dlon = lon2 - lon1
    #a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    #c = 2 * math.asin(math.sqrt(a))
    #radius = 6371  # Earth's radius in kilometers
    #distance = radius * c 
    #distance = round(distance, 2)
    #return distance
  
def ai_home_advisor(request): 
    form = LoanCalculatorForm(initial={
        'property_price': 300000,
        'down_payment': 30000,
        'interest_rate': 4.00,
        #'age': 31,
        #'loan_term': 35,
    })

    context = {
        'form': form,  # Add the form to the initial context
    }

    if request.method == 'POST':
        form = LoanCalculatorForm(request.POST)
        if form.is_valid():
            monthly_income = form.cleaned_data['monthly_income']
            existing_debts = form.cleaned_data['existing_debts']
            age = form.cleaned_data['age']

            # Calculate Debt-to-Income Ratio (DSR)
            dsr = (existing_debts / monthly_income) * 100

            dsr_ceiling = 70.1

            eligible = ''
            
            property_price = form.cleaned_data['property_price']
            down_payment = form.cleaned_data['down_payment']
            loan_term = form.cleaned_data['loan_term']
            interest_rate = form.cleaned_data['interest_rate'] / 100
            property_price_round = round(property_price, 2)
            interest_rate_round = round((interest_rate * 100), 2)

            loan_amount = property_price - down_payment
            monthly_interest_rate = (interest_rate / 12)  # Convert to decimal

            num_payments = loan_term * 12

            monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)

            afford_text=''
            afford_property_text=''
            max_loan_term = min(65 - age, 35)

            if loan_term <= max_loan_term:
                num_payments_afford_year=loan_term
                num_payments_afford = loan_term*12
            else:
                num_payments_afford_year=max_loan_term
                num_payments_afford = max_loan_term*12


            monthly_income_decimal = Decimal(monthly_income)
            dsr_decimal = Decimal(dsr)
            monthly_interest_rate_decimal = Decimal(monthly_interest_rate)

            afford=(((100-dsr)/100)*monthly_income)
            afford_decimal=Decimal(afford)
            
            # Perform calculations using Decimal types
            afford_property = (monthly_income_decimal * (1 - dsr_decimal/100) * (1 - (1 + monthly_interest_rate_decimal) ** -num_payments_afford)) / monthly_interest_rate_decimal
            afford_property_dp = afford_property/10

            monthly_payment_not_eligible = ((afford_property- afford_property_dp ) * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments_afford)

            monthly_payment_not_eligible_decimal=Decimal(monthly_payment_not_eligible)

            remain= round(afford_decimal - monthly_payment_not_eligible_decimal)

            different_afford_monthly = round(afford_decimal-monthly_payment)
            afford_property_round=round(afford_property+remain)


            # Determine loan eligibility based on DSR and lender's criteria
            if dsr < dsr_ceiling and different_afford_monthly > 0:
                eligible = 'You are eligible'
            else:
                eligible = 'You are not eligible'
                afford_text = f'Currently, you only remain RM {afford:.2f} after debt and will be left with RM {different_afford_monthly:.2f} if you bought this house'
                afford_property_text = f'You can only afford a property up to RM {afford_property_round:.2f} with a maximum loan period of {num_payments_afford_year} years and {interest_rate*100:.2f}% interest rate'
           
            # Generate payment schedule data
            payment_schedule = []
            remaining_balance = loan_amount
            total_interest_paid = 0  # Initialize total interest paid
            year_counter = 0
            principal_0 = 0

            for i in range(1, num_payments + 1):
                interest_payment = remaining_balance * monthly_interest_rate
                principal_payment = monthly_payment - interest_payment
                remaining_balance -= principal_payment
                principal_0 += principal_payment
                total_interest_paid += interest_payment

                if i % 12 == 0:
                    year_counter += 1
                    payment_schedule.append({
                        'x': year_counter,
                        'principal': principal_0,
                        'interest': total_interest_paid,
                        'balance': remaining_balance,
                    })

            # Create a bar chart using Plotly for annual data
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=[entry['x'] for entry in payment_schedule], y=[entry['principal'] for entry in payment_schedule], mode='lines+markers', name='Principal'))
            fig.add_trace(go.Scatter(x=[entry['x'] for entry in payment_schedule], y=[entry['interest'] for entry in payment_schedule], mode='lines+markers', name='Interest'))
            fig.add_trace(go.Scatter(x=[entry['x'] for entry in payment_schedule], y=[entry['balance'] for entry in payment_schedule], mode='lines+markers', name='Balance'))

            # Format y-axis labels with symbols and 2 decimal places
            fig.update_layout(yaxis_tickprefix='RM ', yaxis_tickformat=".2f")

            fig.update_layout(title='Payment Schedule by Year', xaxis_title='Year', yaxis_title='Amount')
            plot_div = fig.to_html(full_html=False)

            context.update({
                'form': form,
                'plot_div': plot_div,
                'property_price': property_price_round,
                'down_payment': down_payment,
                'loan_term': loan_term,
                'interest_rate': interest_rate_round,
                'monthly_payment': float(monthly_payment),
                'payment_schedule': payment_schedule,
                'dsr': dsr,
                'eligible': eligible,
                'monthly_income': monthly_income,
                'existing_debts': existing_debts,
                'afford':afford,
                'afford_property':afford_property,
                'afford_text': afford_text,
                'afford_property_text': afford_property_text,
                'num_payments_afford_year': num_payments_afford_year,
                'remain':remain,
            })

            return render(request, 'ai_home_advisor.html', context)
        else:
            context['form'] = form  # Include the form with errors in the context

    return render(request, 'ai_home_advisor.html', context)

def home(request):
    form = PropertySearchForm(request.POST)
    context = {'form': form}

    return render(request, 'home.html',context)
 
def property_cma(request):
 
    if request.method == 'POST':
        form = StateSelectionForm(request.POST)

        if form.is_valid():
            selected_state = form.cleaned_data['state']
            location_name = form.cleaned_data['address']
            
            location_data = None
            nearby_residential = []  # Changed variable names to reflect 'residential'
            no_of_residential = []    # Changed variable names to reflect 'residential'

            if request.method == 'POST':
                selected_state = form.cleaned_data['state']
                location_name = form.cleaned_data['address']
                response = requests.get(f'https://nominatim.openstreetmap.org/search?q={location_name}&format=json')
                location_results = response.json()

                if location_results:
                    location_result = location_results[0]
                    latitude = location_result.get('lat')
                    longitude = location_result.get('lon')

                    latitude = float(latitude)
                    longitude = float(longitude)

                    residential_tags = {
                        'apartments': 'building=apartments', #  <tag k="building:levels" v="15"/> future can see lvl
                        'residential': 'landuse=residential', 
                        #'house': 'building=house',(already get from residential but necessary to count number of house)
                        #'bungalow': 'building=bungalow', 
                        #'detached': 'building=detached',
                        #'semidetached_house': 'building=semidetached_house',
                        #'terrace': 'building=terrace',
                        #'dormitory': 'building=dormitory',
                        #'hotel': 'building=hotel', 
                        #'commercial': 'building=commercial',
                        #'industrial': 'building=industrial',
                        #'kiosk': 'building=kiosk',
                        #'office': 'building=office',
                        #'retail': 'building=retail',
                        #'supermarket': 'building=supermarket',
                        #'warehouse': 'building=warehouse'
                    }

                    api = overpy.Overpass()

                    nearby_residential = []  
                    no_of_residential = []    

                    for residential_name, residential_tag in residential_tags.items(): 
                        query = f"""
                        area[name="{selected_state}"]->.searchArea;
                        (
                        node(around:2500, {latitude}, {longitude})[{residential_tag}](area.searchArea);
                        way(around:2500, {latitude}, {longitude})[{residential_tag}](area.searchArea);
                        relation(around:2500, {latitude}, {longitude})[{residential_tag}](area.searchArea);
                        );

                        out center;
                        """

                        result = api.query(query)

                        residential_count = len(result.nodes) + len(result.ways) + len(result.relations)
                        no_of_residential.append({'residential_name': residential_name, 'count': residential_count})

                        for element in result.nodes + result.ways + result.relations:
                            if isinstance(element, overpy.Node):
                                lat = element.lat
                                lon = element.lon
                            elif isinstance(element, overpy.Way):
                                lat = element.center_lat
                                lon = element.center_lon
                            else:
                                continue

                            name = element.tags.get('name')
                            if name is not None and len(name) > 2 and 'kedutaan' not in name.lower() and 'malaysia' not in name.lower() and 'commission' not in name.lower() and 'embassy' not in name.lower() and 'asrama' not in name.lower() and 'awam' not in name.lower() and 'kuarters' not in name.lower()  and 'istana' not in name.lower() and 'guest' not in name.lower() and 'campus' not in name.lower() and 'kolej' not in name.lower():
                                address = element.tags.get('addr:street') 
                                distance = calculate_distance(latitude, longitude, lat, lon)
                                levels=element.tags.get('building:levels')
                                #if distance <= 2500:
                                nearby_residential.append({
                                'name': name,
                                'address': address,
                                'levels': levels,
                                'distance': distance,
                                'residential_type': residential_name,
                                'latitude': lat, 
                                'longitude': lon

                                })

                        location_data = {
                            'name': location_name,
                            'latitude': latitude,
                            'longitude': longitude
                        }

                        sorted_residential = sorted(nearby_residential, key=lambda x: x['residential_type'])
                        sorted_residential = sorted(nearby_residential, key=lambda x: x['distance'])
                        nearby_residential = sorted_residential

                        seen_names = set()
                        unique_residential = []

                        for item in nearby_residential:
                            if item['name'] not in seen_names:
                                unique_residential.append(item)
                                seen_names.add(item['name'])
                        # Update nearby_residential with the list containing unique items
                        nearby_residential = unique_residential

                        # Define tags for different educational facilities
                        educational_tags = {
                            'school': 'amenity=school', 
                            'kindergarten': 'amenity=kindergarten', 
                            'university': 'amenity=university'#,
                            #'library': 'amenity=library',  
                        }

                        # Initialize a list to store nearby educational facilities
                        nearby_educational_facilities = []

                        # Iterate over each educational facility type and perform queries
                        for facility_name, facility_tag in educational_tags.items():
                            facility_query = f"""
                            area[name="{selected_state}"]->.searchArea;
                            (
                            node(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            way(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            relation(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            );
                            out center;
                            """

                            # Execute the query
                            facility_result = api.query(facility_query)

                            # Process the results
                            for element in facility_result.nodes + facility_result.ways + facility_result.relations:
                                if isinstance(element, overpy.Node):
                                    lat = element.lat
                                    lon = element.lon
                                elif isinstance(element, overpy.Way):
                                    lat = element.center_lat
                                    lon = element.center_lon
                                else:
                                    continue

                                name = element.tags.get('name')
                                if name:
                                    address = element.tags.get('addr:street', 'No Address')
                                    distance = calculate_distance(latitude, longitude, lat, lon)

                                    # Adding the facility to the list
                                    nearby_educational_facilities.append({
                                        'name': name,
                                        'address': address,
                                        'distance': distance,
                                        'facility_type': facility_name,
                                        'latitude': lat, 
                                        'longitude': lon
                                    })

                        # Sorting the results by facility type and then by distance
                        nearby_educational_facilities.sort(key=lambda x: (x['facility_type'], x['distance']))

                        # Define tags for hospitals, clinics, and doctor's offices
                        healthcare_tags = {
                            'hospital': 'amenity=hospital',
                            'clinic': 'amenity=clinic',
                            'doctor': 'amenity=doctor',
                        }

                        # Initialize a list to store nearby healthcare facilities
                        nearby_healthcare_facilities = []

                        # Iterate over each healthcare facility type and perform queries
                        for facility_name, facility_tag in healthcare_tags.items():
                            facility_query = f"""
                            area[name="{selected_state}"]->.searchArea;
                            (
                            node(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            way(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            relation(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            );
                            out center;
                            """

                            # Execute the query
                            facility_result = api.query(facility_query)

                            # Process the results
                            for element in facility_result.nodes + facility_result.ways + facility_result.relations:
                                if isinstance(element, overpy.Node):
                                    lat = element.lat
                                    lon = element.lon
                                elif isinstance(element, overpy.Way):
                                    lat = element.center_lat
                                    lon = element.center_lon
                                else:
                                    continue

                                name = element.tags.get('name')
                                if name:
                                    address = element.tags.get('addr:street', 'No Address')
                                    distance = calculate_distance(latitude, longitude, lat, lon)

                                    # Adding the facility to the list
                                    nearby_healthcare_facilities.append({
                                        'name': name,
                                        'address': address,
                                        'distance': distance,
                                        'facility_type': facility_name,
                                        'latitude': lat, 
                                        'longitude': lon
                                    })

                        # Sorting the results by facility type and then by distance
                        nearby_healthcare_facilities.sort(key=lambda x: (x['facility_type'], x['distance']))


                        # Define tags for banks and ATMs
                        #financial_tags = {
                        #    'bank': 'amenity=bank', 
                        #    'atm': 'amenity=atm',
                        #}

                        # Initialize a list to store nearby banks and ATMs
                        #nearby_financial_facilities = []

                        # Iterate over each financial facility type and perform queries
                        #for facility_name, facility_tag in financial_tags.items():
                        #    facility_query = f"""
                        #    area[name="{selected_state}"]->.searchArea;
                        #    (
                        #    node(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                        #    way(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                        #    relation(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                        #    );
                        #    out center;
                        #    """

                            # Execute the query
                        #    facility_result = api.query(facility_query)

                            # Process the results
                        #    for element in facility_result.nodes + facility_result.ways + facility_result.relations:
                        #        if isinstance(element, overpy.Node):
                        #            lat = element.lat
                        #            lon = element.lon
                        #        elif isinstance(element, overpy.Way):
                        #            lat = element.center_lat
                        #            lon = element.center_lon
                        #        else:
                        #            continue
                        #
                        #        name = element.tags.get('name')
                        #        if name:
                        #            address = element.tags.get('addr:street', 'No Address')
                        #            distance = calculate_distance(latitude, longitude, lat, lon)

                                    # Adding the facility to the list
                        #            nearby_financial_facilities.append({
                        #                'name': name,
                        #                'address': address,
                        #                'distance': distance,
                        #                'facility_type': facility_name,
                        #                'latitude': lat, 
                        #                'longitude': lon
                        #            })

                        # Sorting the results by facility type and then by distance
                        #nearby_financial_facilities.sort(key=lambda x: (x['facility_type'], x['distance']))
                        ## context - 'nearby_financial_facilities': nearby_financial_facilities, 

            context = {'form': form,'location_data': location_data,'nearby_healthcare_facilities': nearby_healthcare_facilities, 'nearby_educational_facilities' : nearby_educational_facilities, 'nearby_residential': nearby_residential, 'no_of_residential': no_of_residential}
            return render(request, 'property_cma.html', context) 
            
    else:
        form = StateSelectionForm()
        context = {'form': form}
    return render(request, 'property_cma.html', context)


def housing_analytic_report(request):
 
    if request.method == 'POST':
        form = AnalyticForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['name']
            selected_state = form.cleaned_data['state']
            location_name = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email'] 
            house_type= form.cleaned_data['house_type'] 
            year_built= form.cleaned_data['year_built']  

            location_data = None
            nearby_residential = []  # Changed variable names to reflect 'residential'
            no_of_residential = []    # Changed variable names to reflect 'residential'

            if request.method == 'POST':
                username = form.cleaned_data['name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email'] 
                house_type= form.cleaned_data['house_type'] 
                year_built= form.cleaned_data['year_built'] 
 
                selected_state = form.cleaned_data['state']
                location_name = form.cleaned_data['address']
                response = requests.get(f'https://nominatim.openstreetmap.org/search?q={location_name}&format=json')
                location_results = response.json()

                if location_results:
                    location_result = location_results[0]
                    latitude = location_result.get('lat')
                    longitude = location_result.get('lon')

                    latitude = float(latitude)
                    longitude = float(longitude)

                    residential_tags = {
                        'apartments': 'building=apartments', #  <tag k="building:levels" v="15"/> future can see lvl
                        'residential': 'landuse=residential', 
                        #'house': 'building=house',(already get from residential but necessary to count number of house)
                        #'bungalow': 'building=bungalow', 
                        #'detached': 'building=detached',
                        #'semidetached_house': 'building=semidetached_house',
                        #'terrace': 'building=terrace',
                        #'dormitory': 'building=dormitory',
                        #'hotel': 'building=hotel', 
                        #'commercial': 'building=commercial',
                        #'industrial': 'building=industrial',
                        #'kiosk': 'building=kiosk',
                        #'office': 'building=office',
                        #'retail': 'building=retail',
                        #'supermarket': 'building=supermarket',
                        #'warehouse': 'building=warehouse'
                    }

                    api = overpy.Overpass()

                    nearby_residential = []  
                    no_of_residential = []    

                    for residential_name, residential_tag in residential_tags.items(): 
                        query = f"""
                        area[name="{selected_state}"]->.searchArea;
                        (
                        node(around:2500, {latitude}, {longitude})[{residential_tag}](area.searchArea);
                        way(around:2500, {latitude}, {longitude})[{residential_tag}](area.searchArea);
                        relation(around:2500, {latitude}, {longitude})[{residential_tag}](area.searchArea);
                        );

                        out center;
                        """

                        result = api.query(query)

                        residential_count = len(result.nodes) + len(result.ways) + len(result.relations)
                        no_of_residential.append({'residential_name': residential_name, 'count': residential_count})

                        for element in result.nodes + result.ways + result.relations:
                            if isinstance(element, overpy.Node):
                                lat = element.lat
                                lon = element.lon
                            elif isinstance(element, overpy.Way):
                                lat = element.center_lat
                                lon = element.center_lon
                            else:
                                continue

                            name = element.tags.get('name')
                            if name is not None and len(name) > 2 and 'kedutaan' not in name.lower() and 'malaysia' not in name.lower() and 'commission' not in name.lower() and 'embassy' not in name.lower() and 'asrama' not in name.lower() and 'awam' not in name.lower() and 'kuarters' not in name.lower()  and 'istana' not in name.lower() and 'guest' not in name.lower() and 'campus' not in name.lower() and 'kolej' not in name.lower():
                                address = element.tags.get('addr:street') 
                                distance = calculate_distance(latitude, longitude, lat, lon)
                                levels=element.tags.get('building:levels')
                                #if distance <= 2500:
                                nearby_residential.append({
                                'name': name,
                                'address': address,
                                'levels': levels,
                                'distance': distance,
                                'residential_type': residential_name,
                                'latitude': lat, 
                                'longitude': lon

                                })

                        location_data = {
                            'name': location_name,
                            'latitude': latitude,
                            'longitude': longitude
                        }

                        sorted_residential = sorted(nearby_residential, key=lambda x: x['residential_type'])
                        sorted_residential = sorted(nearby_residential, key=lambda x: x['distance'])
                        nearby_residential = sorted_residential

                        seen_names = set()
                        unique_residential = []

                        for item in nearby_residential:
                            if item['name'] not in seen_names:
                                unique_residential.append(item)
                                seen_names.add(item['name'])
                        # Update nearby_residential with the list containing unique items
                        nearby_residential = unique_residential

                        # Define tags for different educational facilities
                        educational_tags = {
                            'school': 'amenity=school', 
                            'kindergarten': 'amenity=kindergarten', 
                            'university': 'amenity=university'#,
                            #'library': 'amenity=library',  
                        }

                        # Initialize a list to store nearby educational facilities
                        nearby_educational_facilities = []

                        # Iterate over each educational facility type and perform queries
                        for facility_name, facility_tag in educational_tags.items():
                            facility_query = f"""
                            area[name="{selected_state}"]->.searchArea;
                            (
                            node(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            way(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            relation(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            );
                            out center;
                            """

                            # Execute the query
                            facility_result = api.query(facility_query)

                            # Process the results
                            for element in facility_result.nodes + facility_result.ways + facility_result.relations:
                                if isinstance(element, overpy.Node):
                                    lat = element.lat
                                    lon = element.lon
                                elif isinstance(element, overpy.Way):
                                    lat = element.center_lat
                                    lon = element.center_lon
                                else:
                                    continue

                                name = element.tags.get('name')
                                if name:
                                    address = element.tags.get('addr:street', 'No Address')
                                    distance = calculate_distance(latitude, longitude, lat, lon)

                                    # Adding the facility to the list
                                    nearby_educational_facilities.append({
                                        'name': name,
                                        'address': address,
                                        'distance': distance,
                                        'facility_type': facility_name,
                                        'latitude': lat, 
                                        'longitude': lon
                                    })

                        # Sorting the results by facility type and then by distance
                        nearby_educational_facilities.sort(key=lambda x: (x['facility_type'], x['distance']))

                        # Define tags for hospitals, clinics, and doctor's offices
                        healthcare_tags = {
                            'hospital': 'amenity=hospital',
                            'clinic': 'amenity=clinic',
                            'doctor': 'amenity=doctor',
                        }

                        # Initialize a list to store nearby healthcare facilities
                        nearby_healthcare_facilities = []

                        # Iterate over each healthcare facility type and perform queries
                        for facility_name, facility_tag in healthcare_tags.items():
                            facility_query = f"""
                            area[name="{selected_state}"]->.searchArea;
                            (
                            node(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            way(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            relation(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                            );
                            out center;
                            """

                            # Execute the query
                            facility_result = api.query(facility_query)

                            # Process the results
                            for element in facility_result.nodes + facility_result.ways + facility_result.relations:
                                if isinstance(element, overpy.Node):
                                    lat = element.lat
                                    lon = element.lon
                                elif isinstance(element, overpy.Way):
                                    lat = element.center_lat
                                    lon = element.center_lon
                                else:
                                    continue

                                name = element.tags.get('name')
                                if name:
                                    address = element.tags.get('addr:street', 'No Address')
                                    distance = calculate_distance(latitude, longitude, lat, lon)

                                    # Adding the facility to the list
                                    nearby_healthcare_facilities.append({
                                        'name': name,
                                        'address': address,
                                        'distance': distance,
                                        'facility_type': facility_name,
                                        'latitude': lat, 
                                        'longitude': lon
                                    })

                        # Sorting the results by facility type and then by distance
                        nearby_healthcare_facilities.sort(key=lambda x: (x['facility_type'], x['distance']))


                        # Define tags for banks and ATMs
                        #financial_tags = {
                        #    'bank': 'amenity=bank', 
                        #    'atm': 'amenity=atm',
                        #}

                        # Initialize a list to store nearby banks and ATMs
                        #nearby_financial_facilities = []

                        # Iterate over each financial facility type and perform queries
                        #for facility_name, facility_tag in financial_tags.items():
                        #    facility_query = f"""
                        #    area[name="{selected_state}"]->.searchArea;
                        #    (
                        #    node(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                        #    way(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                        #    relation(around:2500, {latitude}, {longitude})[{facility_tag}](area.searchArea);
                        #    );
                        #    out center;
                        #    """

                            # Execute the query
                        #    facility_result = api.query(facility_query)

                            # Process the results
                        #    for element in facility_result.nodes + facility_result.ways + facility_result.relations:
                        #        if isinstance(element, overpy.Node):
                        #            lat = element.lat
                        #            lon = element.lon
                        #        elif isinstance(element, overpy.Way):
                        #            lat = element.center_lat
                        #            lon = element.center_lon
                        #        else:
                        #            continue
                        #
                        #        name = element.tags.get('name')
                        #        if name:
                        #            address = element.tags.get('addr:street', 'No Address')
                        #            distance = calculate_distance(latitude, longitude, lat, lon)

                                    # Adding the facility to the list
                        #            nearby_financial_facilities.append({
                        #                'name': name,
                        #                'address': address,
                        #                'distance': distance,
                        #                'facility_type': facility_name,
                        #                'latitude': lat, 
                        #                'longitude': lon
                        #            })

                        # Sorting the results by facility type and then by distance
                        #nearby_financial_facilities.sort(key=lambda x: (x['facility_type'], x['distance']))
                        ## context - 'nearby_financial_facilities': nearby_financial_facilities, 

            context = {'form': form, 
                       'username':username,
                       'phone_number':phone_number,
                       'email':email,
                       'selected_state':selected_state,
                       'house_type':house_type,
                       'year_built':year_built,
                        
                       'location_data': location_data,
                       'nearby_healthcare_facilities': nearby_healthcare_facilities, 'nearby_educational_facilities' : nearby_educational_facilities, 'nearby_residential': nearby_residential, 'no_of_residential': no_of_residential}
            return render(request, 'housing_analytic_report.html', context) 
            
    else:
        form = AnalyticForm()
        context = {'form': form}
     
    return render(request, 'housing_analytic_report.html', context)

 
def score(request): 
    return render(request, 'score.html')

def about(request): 
    return render(request, 'about.html')
 