## To open streamlit on website you need to do this 
# 1. streamlit run Flight_Project_App.py on terminal line 
# 2. run the libraries and whatever you want to include
#3. use Ctrl + C to exit the terminal

import streamlit as st
import numpy as np
import base64
# from core import get_flights # not sure how to add this class into the final fast flight 
from fast_flights import FlightData, Passengers, create_filter, get_flights
from datetime import datetime, timedelta, date


# Mapping common city names to airport codes
city_to_airport_code = {"Phoenix": "PHX", 
                        "Denver": "DEN", 
                        "Los Angeles": "LAX", 
                        "New York": "JFK", 
                        "Salt Lake": "SLC",
                        "Atlanta": "ATL",
                        "Dallas": "DFW",
                        "Chicago": "ORD",
                        "Orlando": "MCO",
                        "Las Vegas": "LAS",
                        "Charlotte": "CLT",
                        "Miami": "MIA",
                        "Seattle": "SEA",
                        "Newark": "EWR",
                        "San Francisco": "SFO",
                        "Houston": "IAH",
                        "Boston": "BOS",
                        "Fort Lauderdale": "FLL",
                        "Minneapolis": "MSP",
                        "LaGuardia": "LGA",
                        "Detroit": "DTW",
                        "Philadelphia":	"PHL",
                        "Baltimore": "BWI",
                        "Pittsburgh":"PIT",
                        "San Diego": "SAN",
                        "Tampa": "TPA",
                        "Austin":"AUS",
                        "Raleigh": "RDU",
                        "Jacksonville":"JAX",
                        "Nashville": "BNA",
                        "Memphis":	"MEM",
                        "Oklahoma City": "OKC",
                        "Cincinnati":"CVG",
                        "Kansas City":"MCI",
                        "Hartford":	"BDL",
                        "New Orleans": "MSY",
                        "Cleveland": "CLE",
                        "Milwaukee": "MKE",
                        "Honolulu":	"HNL",
                        "Madison":	"MSN",
                        "Buffalo":	"BUF",
                        "Albany":	"ALB",
                        "Rochester":"ROC",
                        "Syracuse":	"SYR",
                        "Toledo": "TOL",
                        "Grand Rapids":	"GRR",
                        "Dayton": "DAY",
                        "Des Moines": "DSM",
                        "Lincoln": "LNK",
                        "Omaha": "OMA",
                        "Sioux Falls": "FSD",
                        "Charleston": "CHS",
                        "Columbia":	"CAE",
                        "Greenville": "GSP",
                        "Little Rock": "LIT",
                        "Birmingham": "BHM",
                        "Mobile":	"MOB",
                        "Huntsville": "HSV"
                       }

# streamlit UI
st.sidebar.title("Dashboard")

app_mode= st.sidebar.selectbox("Select Page", ["Home","Search Flights","Travel Deal Flights", "Email List", "About"])

# Main Page
if(app_mode=="Home"):
    st.markdown('''## Welcome to the U Flights!✈️''')
    image_path =  "Takeoff Flight.jpeg" 
    st.image(image_path, use_column_width=True)

    # Telling users the purpose of the app 
    st.markdown("""
**Our goal is to help Salt Lake travelers find the best flight whether they are looking for a specific location or want a getaway trip to any loaction! **

### How It Works
**There are three pages to choose from; Search Flights, Travel Deal Flights, or Subscription Page**
1. Search Flight Tab: If you have a specific location and date you want to go to. 
2. Travel Deal flights: If you just want to explore possible Travel Deal flights to the top 10 cities.
3. Subscription: You can also subscribe to our website and we will send you current deals that might interest you.

### About Us
Learn more about the mission, our story, and the team on the **About** page.
""")
# -----------------------------------------------------------------------------#
                            # Search Flights
# -----------------------------------------------------------------------------#
elif(app_mode=="Search Flights"):
    st.header("Flight Search")

    # Input for destination airport or city name
    user_input = st.text_input("Enter the destination airport or city name:").strip().title()

    # Input for departure date
    departure_date = st.date_input("Enter the date you want to leave:")
    departure_date2 = departure_date.strftime("%Y-%m-%d")
    
    # Input for trip type
    trip_type = st.selectbox("Select trip type:", ["one-way", "round-trip"])
    
    # Include return flight if it's a round trip
    if trip_type == "round-trip":
        return_date = st.date_input("Enter the date you want to return:")
        return_date2 = return_date.strftime("%Y-%m-%d")

    # Process user input
    if st.button("Search Flights"):
        if user_input in city_to_airport_code:
            airport_name = city_to_airport_code.get(user_input, user_input)

            # Create flight data
            flight_data = [
                FlightData(
                    date=departure_date2,  # Date of departure
                    from_airport="SLC",  # Assuming departure from Salt Lake City
                    to_airport=airport_name,
                )
            ]

            # Create filter
            filter = create_filter(
                flight_data=flight_data,
                trip=trip_type,
                seat="economy",
                passengers=Passengers(adults=1, children=0),
            )
            if trip_type == "one-way":
                # Get flights with a filter
                    result = get_flights(filter)

                    # Display the filter (or use it for further processing)
                    st.write("### Flight Search Filter:")
                    # st.write(filter)  # Display the filter as JSON for demonstration
                    st.write(f"**The overall price of the flight is currently: {result.current_price}**")

                    # Exclude certain flights name and the long self transfer name.
                    excluded_names = ['Frontier', 'Spirit', 
                                    'Self transferThis trip includes tickets from multiple airlines. Missed connections may be protected by the booking provider.']
                    # Get flights with a filter
                    result = get_flights(filter)

                    # Function to check if the current price is low
                    if result.current_price == 'low': 
                        low_price_flights = [flight for flight in result.flights if flight.name not in excluded_names][:5]
                    else:
                        st.write(f"No low-priced flights found 😔 but here are other options")
                        low_price_flights = [flight for flight in result.flights if flight.name not in excluded_names][:5]

                    if low_price_flights:
                        st.write(f"### Top 5 Departure Flight details from Salt Lake City to {user_input}:") 
                        for flight in low_price_flights:
                            st.write(f"Name: {flight.name}") 
                            st.write(f"Departure: {flight.departure}") 
                            st.write(f"Arrival: {flight.arrival}") 
                            st.write(f"Duration: {flight.duration}") 
                            st.write(f"Current price: {result.current_price}") 
                            st.write(f"--------------------------")
                    else: 
                        st.write("No low-priced flights found.")
            if trip_type == "round-trip":
                if return_date2 < departure_date2: 
                    st.write(f"Please enter a date on or after {departure_date2} . Thank you")  
                else:
                    filter2 = create_filter(
                        flight_data=[
                        FlightData(
                        date=return_date2,  # Date of return
                        from_airport=airport_name, 
                        to_airport="SLC"
                        ),
                        ],
                    trip="one-way",  # Trip (round-trip, one-way)
                     seat="economy",  # Seat (economy, premium-economy, business or first)
                    passengers=Passengers(adults=1,children=0,)
                )
                    result2 = get_flights(filter2) 

                    # Get flights with a filter
                    result = get_flights(filter)

                    # Display the filter (or use it for further processing)
                    st.write("### Flight Search Filter:")
                    # st.write(filter)  # Display the filter as JSON for demonstration
                    st.write(f"**The overall price of the flight is currently: {result.current_price}**")

                    # Exclude certain flights name and the long self transfer name.
                    excluded_names = ['Frontier', 'Spirit', 
                                    'Self transferThis trip includes tickets from multiple airlines. Missed connections may be protected by the booking provider.']
                    # Get flights with a filter
                    result = get_flights(filter)

                    # Function to check if the current price is low
                    if result.current_price == 'low': 
                        low_price_flights = [flight for flight in result.flights if flight.name not in excluded_names][:5]
                    else:
                        st.write(f"No low-priced flights found 😔 but here are other options")
                        low_price_flights = [flight for flight in result.flights if flight.name not in excluded_names][:5]

                    if low_price_flights:
                        st.write(f"### Top 5 Departure Flight details from Salt Lake City to {user_input}:") 
                        for flight in low_price_flights:
                            st.write(f"Name: {flight.name}") 
                            st.write(f"Departure: {flight.departure}") 
                            st.write(f"Arrival: {flight.arrival}") 
                            st.write(f"Duration: {flight.duration}") 
                            st.write(f"Current price: {result.current_price}") 
                            st.write(f"--------------------------")
                    else: 
                        st.write("No low-priced flights found.")
                    
                    if trip_type == "round-trip":
                    # Checking return flight
                        if result2.current_price == 'low': 
                            low_price_flights = [flight for flight in result2.flights if flight.name not in excluded_names][:5]
                        else:
                            st.write(f"No return low-priced flights found 😔 but here are other options")
                            low_price_flights = [flight for flight in result2.flights if flight.name not in excluded_names][:5]

                        if low_price_flights:
                            st.write(f"### Top 5 Returning Flight details from {user_input} to Salt Lake City:") 
                            for flight in low_price_flights:
                                st.write(f"Name: {flight.name}") 
                                st.write(f"Departure: {flight.departure}") 
                                st.write(f"Arrival: {flight.arrival}") 
                                st.write(f"Duration: {flight.duration}") 
                                st.write(f"Current price: {result.current_price}")
                                st.write(f"--------------------------")
                        else: st.write("No low-priced flights found.")  
            
            #-----------------------#
                    # URL portion
            #-----------------------#

            def create_google_flights_url(from_airport, to_airport, departure_date, return_date=None):
                #Get today's date
                today = datetime.today()

                # Step 2: Parse the departure date (assuming it's in 'YYYY-MM-DD' format)
                dep_date = datetime.strptime(departure_date, "%Y-%m-%d")

                # Add 2 days to today's date
                date_ahead = today + timedelta(days=2)
                
                if dep_date == date_ahead:
                    start_char = 'w'
                else:
                    start_char= 'w'
                    # Calculate the difference in days between departure date and today
                    days_difference = (dep_date - today).days
                    
                    if days_difference == 2:
                        start_char = 'w'
                    # Generate the date string character (x, y, z, 1, 2, etc.)
                    day_offset = days_difference - 2
                    if day_offset < 24:
                    # Continue with alphabet characters
                        date_str = chr(ord(start_char) + day_offset)
                    else:
                    # Once we pass 'z', we should start numbering (i.e., '1', '2', ...)
                        date_str = str(day_offset - 24 + 1) 
        
                base_url = "https://www.google.com/travel/flights/search"
                
                # Construct the tfs parameter
                if return_date:
                    # Round-trip
                    tfs_string = f"CBwQAhooEgoyMDIzLTEwLTEwagwIAhIIL20vMGYycjZyDAgDEggvbS8wZDM1eUABSAFwAYIBCwj___________8BmAEC"
                else:
                    # One-way
                    tfs_string = f"CBwQAhojEgoyMDI1LTAzLTI{date_str}agwIAhIIL20vMGYycjZyBwgBEgNMQVhAAUgBcAGCAQsI____________AZgBAg"
        
                # Construct the full URL
                url = f"{base_url}?tfs={tfs_string}&hl=en"
                return url

            # Example usage
            from_airport = "SLC"
            to_airport = airport_name
            departure_date = departure_date2
            
            if trip_type == "one-way":
            # One-way URL
                one_way_url = create_google_flights_url(from_airport, to_airport,departure_date)
                st.write("Here is the one-way URL:", one_way_url)
            if trip_type == "round-trip":
                return_date = return_date2
            # Round-trip URL
                round_trip_url = create_google_flights_url(from_airport, to_airport, departure_date, return_date)
                st.write("Here is the round-trip URL:", round_trip_url) 
        else:
            st.write("City not found or misspelled. Please try again.")
# -----------------------------------------------------------------------------#
                            # About the Flight Deal
# -----------------------------------------------------------------------------#

elif(app_mode=="Travel Deal Flights"):       
    st.header("Travel Deal Flights on sale 😊")

    #creating start and end date for users
    start_date = datetime.now() + timedelta(days=60) # 2 months from now (can change this)
    end_date = datetime.now() + timedelta(days=90) # 3 months from now (can change this)
    start_date_good = start_date.strftime("%B %d, %Y")
    end_date_good = end_date.strftime("%B %d, %Y")

    st.write("The travel deal looks at designated loaction in Salt Lake at a time period from " + str(start_date_good) + " to " 
             + str(end_date_good) + " of the top 12 US locations that are most traveled to")
    def generate_date_range(start_date, end_date): 
        delta = end_date - start_date 
        return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]
    
    # top 10 location people like to travel to
    top_airport_dest = ["JFK", "HNL", "SFO", "SAN", "IAD", "MSY", "SEA", "ORD", "MIA", "LAS", "BNA", "BOS"]

# Map airport codes to location names
    airport_mapping = {
        "JFK": "New York",
        "HNL": "Honolulu",
        "SFO": "San Francisco",
        "SAN": "San Diego",
        "IAD": "Washington, D.C.",
        "MSY": "New Orleans",
        "SEA": "Seattle",
        "ORD": "Chicago",
        "MIA": "Miami",
        "LAS": "Las Vegas",
        "BNA": "Nashville",
        "BOS": "Boston"
    }

    # Create a list of location names for the select box
    location_names = [airport_mapping[code] for code in top_airport_dest]

    # Create the select box
    selected_location = st.selectbox("Select a destination:", location_names)

    # Retrieve the corresponding airport code
    selected_code = list(airport_mapping.keys())[list(airport_mapping.values()).index(selected_location)]

    # Display the selected airport code
    st.write(f"Checking flights to: {selected_location} ({selected_code})")
    
    # Calculate dates 2 to 3 months away 
    start_date = datetime.now() + timedelta(days=60) # 1 months from now (can change this)
    end_date = datetime.now() + timedelta(days=90) # 2 months from now (can change this)

    # Generate a list of dates between start_date and end_date 
    date_range = generate_date_range(start_date, end_date)

# Exclude certain flights name and the long self transfer name.
    excluded_names = ['Frontier', 'Spirit', 
            'Self transferThis trip includes tickets from multiple airlines. Missed connections may be protected by the booking provider.']

    def is_not_excluded(flight): 
        return flight.name not in excluded_names 
        
    low_price_flights2 = []

# Iterate through the date range and apply the filter
    for best_date in date_range:
    # Define the filter for Departure 
        filter3 = create_filter(
            flight_data=[
                FlightData(
                    date=best_date,  # Date of departure
                    from_airport="SLC", 
                    to_airport=selected_code
                ),
            ],
            trip="one-way",  # Trip (round-trip, one-way)
            seat="economy",  # Seat (economy, premium-economy, business or first)
            passengers=Passengers(
                adults=1,
                children=0,
            )
        )
        result3 = get_flights(filter3)

        # looking at low current price for user  
        if result3.current_price == 'low': 
            st.write(f"Low price found for {selected_location} on {best_date}!")
            low_price_flights2.extend([flight for flight in result3.flights if is_not_excluded(flight)][:5]) 
            break 
    
    if result3.current_price != 'low':
            st.write(f"No low price found for {selected_location}")
            low_price_flights2.extend([flight for flight in result3.flights if is_not_excluded(flight)][:5])
        # Remove duplicates if any 
    low_price_flights2 = list({flight.name: flight for flight in low_price_flights2}.values())


    if low_price_flights2:
        st.write(f"### Top Departing Flight details from Salt Lake to {selected_location}:") 
        for flight in low_price_flights2:
            st.write(f"Name: {flight.name}") 
            st.write(f"Departure: {flight.departure}") 
            st.write(f"Arrival: {flight.arrival}") 
            st.write(f"Duration: {flight.duration}") 
            st.write(f"Current price: {result3.current_price}")
            st.write(f"Actual price: {flight.price}") 
            st.write(f"--------------------------")
    else: 
        st.write("No low departing priced flights found.")

    def string_to_datetime_date(date_string):
        try:
            # Attempt to parse the date string using the default format
            date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
            return date_obj
        except ValueError:
            # Handle potential errors in date string format
            print(f"Invalid date format: {date_string}")
            return None
        
    best_date2 = string_to_datetime_date(best_date)
    return_date_range = [(best_date2 + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 11)]
            
    low_return_price_flights = []

    for return_date in return_date_range:
        filter_return = create_filter(
            flight_data=[
                # Include more if it's not a one-way trip
                FlightData(
                    date=return_date,  # Date of return
                    from_airport=selected_code, 
                    to_airport="SLC"
                ),
                # ... include more for round trips
            ],
            trip="one-way",  # Trip (round-trip, one-way)
            seat="economy",  # Seat (economy, premium-economy, business or first)
            passengers=Passengers(
                adults=1,
                children=0,
            )
        )
        result_return = get_flights(filter_return)
        if result_return.current_price == 'low': 
            st.write(f"**Low return price found for {selected_location} on {return_date}!**")
            low_return_price_flights.extend([flight for flight in result_return.flights if is_not_excluded(flight)][:5]) 
            break 
    if result_return.current_price != 'low':
        st.write(f"No low return price found for {selected_location}")
        low_return_price_flights.extend([flight for flight in result_return.flights if is_not_excluded(flight)][:5])

    # Remove duplicates if any 
    low_return_price_flights = list({flight.name: flight for flight in low_return_price_flights}.values())

    if low_return_price_flights:
        st.write(f"### Top Returning Flight details from {selected_location} to Salt Lake:") 
        for flight in low_return_price_flights:
            st.write(f"Name: {flight.name}") 
            st.write(f"Departure: {flight.departure}") 
            st.write(f"Arrival: {flight.arrival}") 
            st.write(f"Duration: {flight.duration}") 
            st.write(f"Current price: {result3.current_price}") 
            st.write(f"Actual price: {flight.price}") 
            st.write(f"--------------------------")
    else: 
        st.write("No low return priced flights found.")

    def create_google_flights_url(from_airport, to_airport, departure_date, return_date=None):
                #Get today's date
                today = datetime.today()

                # Step 2: Parse the departure date (assuming it's in 'YYYY-MM-DD' format)
                dep_date = datetime.strptime(departure_date, "%Y-%m-%d")

                # Add 2 days to today's date
                date_ahead = today + timedelta(days=2)
                
                if dep_date == date_ahead:
                    start_char = 'w'
                else:
                    start_char= 'w'
                    # Calculate the difference in days between departure date and today
                    days_difference = (dep_date - today).days
                    
                    if days_difference == 2:
                        start_char = 'w'
                    # Generate the date string character (x, y, z, 1, 2, etc.)
                    day_offset = days_difference - 2
                    if day_offset < 24:
                    # Continue with alphabet characters
                        date_str = chr(ord(start_char) + day_offset)
                    else:
                    # Once we pass 'z', we should start numbering (i.e., '1', '2', ...)
                        date_str = str(day_offset - 24 + 1) 
        
                base_url = "https://www.google.com/travel/flights/search"
                
                # Construct the tfs parameter
                if return_date:
                    # Round-trip
                    tfs_string = f"CBwQAhojEgoyMDI1LTA1LTA1agcIARIDU0xDcgwIAhIIL20vMHJoNmsaIxIKMjAyNS0wNS0xMmoMCAISCC9tLzByaDZrcgcIARIDU0xDQAFIAXABggELCP___________wGYAQE&hl=en&gl=us&client=safari&curr=USD"
        
                # Construct the full URL
                url = f"{base_url}?tfs={tfs_string}&hl=en"
                return url

    #  Defining Variable
    from_airport = "SLC"
    to_airport = selected_code
    departure_date = best_date
    return_date = return_date
            
    round_trip_url = create_google_flights_url(from_airport, to_airport, departure_date, return_date)
    st.write("Here is the round-trip URL:", round_trip_url) 
# -----------------------------------------------------------------------------#
                            # Email List
# -----------------------------------------------------------------------------#
elif(app_mode=="Email List"):
    st.header("Thank you for joining our email list! ")
    # library needed for email
    import smtplib
    from email.message import EmailMessage

    def send_confirmation_email(to_email, user_name):
        # Replace with your own email and app password
        sender_email = "email@gmail.com"
        sender_password = "password"  # testing

        msg = EmailMessage()
        msg['Subject'] = "Welcome to UFlights! ✈️"
        msg['From'] = sender_email
        msg['To'] = to_email

        msg.set_content(f"""
        Hello {user_name},

        Thank you for subscribing to UFlights! We’re excited to have you onboard. 
        Stay tuned for exclusive flight deals, tips, and updates.

        Safe travels,
        The UFlights Team
        """)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


    # Input for email list
    user_input_name = st.text_input("Please enter your name").strip().title()
    user_input_email = st.text_input("Please enter your email address:").strip().title()
    if user_input_name and user_input_email: 
        st.write(f"""Hello, {user_input_name}  we are so glad you can join our email list. You will recieve an 
    email shortly confirming that you have subscribe to UFlights.✈️""")
        if send_confirmation_email(user_input_email, user_input_name):
            st.success("Confirmation email sent successfully! 📧")
        else:
            st.error("Oops! Something went wrong while sending the email.")
    else:
        st.warning("Please enter both your name and email address.")
# -----------------------------------------------------------------------------#
                            # About Page
# -----------------------------------------------------------------------------#
elif(app_mode=="About"):
    # Write about the Mission
    st.header("Our Mission")
    st.write("""Our mission is to revolutionize the way travelers experience air travel from Salt Lake by providing a seamless 
    intuitive app that simplifies flight booking, real-time updates, and personalized travel recommendations.
    We are committed to enhancing every journey with innovative features that save time, and 
    empower users to make informed decisions. By prioritizing user convenience and connectivity, we aim to create a smarter, 
    more enjoyable travel experience for everyone. """)
    # Write about the Story
    st.header("Our Story")
    st.write("""U Flights started in 2025, as a frequent traveler frustrated by the lack of a simple solution 
    for flight management, I built an app that simplifies every step of the journey. Today, I'm dedicated to making 
    air travel smarter, smoother, and more enjoyable for everyone, one flight at a time.""")
    # Write about Meeting the team
    st.header("Meet the Team")
    image_path2 =  "Baby_Chris.jpeg" 
    st.image(image_path2, use_column_width=True)
    st.write("Chris James | CEO")
    