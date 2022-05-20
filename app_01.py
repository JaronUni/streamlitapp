import streamlit as st
import pandas as pd
import pickle
import geopy.distance
from datetime import date


 

st.set_page_config(
    page_title="Airbnb Price Prediciton Helper for Zurich",
    layout="wide"
    )

st.title("Airbnb Price Prediciton Helper for Zurich")

## Defining Load Functions

@st.cache()
def load_data(filename):
    data_attr = pd.read_csv(filename)
    return(data_attr.dropna())


def load_model():
    filename = "final_price_model.sav"
    loaded_model = pickle.load(open(filename, "rb"))
    return(loaded_model)


## Laod Data and Model    

att_data = load_data("sightseeing.csv")
model = load_model()


## Handling host_since calculation
def calc_days(date):
    today = date.today()
    return(today-date).days


## Helper Lists for Calculations and dummifications

#Distance Lists
att_lon_list = att_data["Latitude"].tolist()
att_lat_list = att_data["Longitude"].tolist()

#Select Lists
response_time_list = ["I don't know", "Within a day", "Within a few hours", "Within an hour"]
kreis_list = ["10","11","12","2","3","4","5","6","7","8","9"]
property_type_list = ["Boat","Entire Condo","Guest Suite", "Entire Guest House", "Entire loft","Entire rental unit", "Entire residential home","Entire serviced apartment","Entire townhouse", "Entire villa", "Private Room","Private room in bed and breakfast", "Private room in cabin", "Private room in castle", "Private room in condominium (condo)", "Private room in guest suite", "Private room in guesthouse", "Private room in hut","Private room in loft","Private room in rental unit","Private room in residential home", "Private room in serviced apartment","Private room in townhouse","Private room in villa", "Room in bed and breakfast","Room in boutique hotel", "Room in hotel", "Room in serviced apartment", "Shared room in bed and breakfast", "Shared room in hostel", "Shared room in hut", "Shared room in rental unit", "Tiny house"]
room_type_list=["Hotel room", "Private room","Shared room"]
gender_list = ["female","male","I do not want to say"]
verification_list=["E-mail","Facebook","Google","Government ID", "Identitiy manual","Jumio","KBA","Manual offline","Manual online","Offline Government ID","Phone","Reviews","Selfie","Sent ID","Work E-Mail"]

# This functions transforms the input of a select field into 1 and 0 depending on the selection
def dummify(input, options):
    input=str(input)
    if(input in options):
        index = options.index(input)
        for idx, ele in enumerate(options):
            if(idx == index):
                details_list.append(1)
            else:
                details_list.append(0)
    else:
        for ele in enumerate(options):
            details_list.append(0)

# This functions transforms the input of a multi-select field into 1 and 0 depending on the selection
def dummifyLists(input,options):
    index_list = []
    for ele in input:
        index = options.index(ele)
        index_list.append(index)
    for idx, item in enumerate(options):
        if(idx in index_list):
            details_list.append(1)
        else:
            details_list.append(0)
 
#This functions calculates the distances between the rental object and all the attractions in the sightseeing.csv file.
def calc_dist(lat, lon):
    airbnb = (lat,lon)
    dist_list = []
    for idx,ele in enumerate(att_lon_list):
        coord_attr = (att_lat_list[idx],ele)
        dist = geopy.distance.distance(coord_attr, airbnb).km
        details_list.append(dist)


### Defining the UI
st.subheader("About you as a host")
st.caption("General Information")
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([1,1,1,1])
row2_col1, row2_col2, row2_col3, row2_col4 = st.columns([1,1,1,1])
st.caption("Review Information")
row3_col1, row3_col2, row3_col3, row3_col4 = st.columns([1,1,1,1])
st.subheader("Details about your rental object")
row4_col1, row4_col2, row4_col3, row4_col4 = st.columns([2,2,1,1])
st.subheader("Availability of your rental object")
row5_col1, row5_col2,row5_col3,row5_col4 = st.columns([1,1,1,1])
row6_col1, row6_col2, = st.columns([1,1])

st.subheader("Rating")
row7_col1, row7_col2, row7_col3, row7_col4 = st.columns([1,1,1,1])
row8_col1, row8_col2, row8_col3, row8_col4 = st.columns([1,1,1,1])
st.subheader("The location of your rental object")
row9_col1, row9_col2, row9_col3, row9_col4 = st.columns([1,1,1,1])
row10_col1, row10_col2= st.columns([1,2])



superhost = row1_col1.checkbox(label="I am a superhost")
profile_pic = row1_col2.checkbox(label="I have a profile picture")
id_verified = row1_col3.checkbox(label="I am verified")
verfication_types = row1_col4.multiselect(label="Select all your verification types", options=("E-mail","Facebook","Google","Government ID", "Identitiy manual","Jumio","KBA","Manual offline","Manual online","Offline Government ID","Phone","Reviews","Selfie","Sent ID","Work E-Mail"))

host_since = row2_col1.date_input(label="I am hosting on Airbnb since:")
is_host_since = calc_days(host_since)
total_listings = row2_col2.number_input(label="Total amount of listings:",step=1)
gender = row2_col3.selectbox(label="What gender do you identify to?:", options=("female","male","I do not want to say","non-binary"))
host_response_time = row2_col4.selectbox("Select your planned response time",
                            options = ["I don't know", "Within a day", "Within a few hours", "Within an hour","A few days or more"])

total_reviews = row3_col1.number_input(label="Total number of reviews",step=1)
reviews_ltm = row3_col2.number_input(label="Number of reviews last year",step=1)
reviews_l30d = row3_col3.number_input(label="Number of reviews last month",step=1)
reviews_per_m = row3_col4.number_input(label="Number of reviews per month",step=1)

accommodates = row4_col1.number_input(label="How many people can stay?",step=1)
baths = row4_col2.number_input(label="How many bathrooms can be used by the guests?",step=0.5)
bedrooms = row4_col3.number_input(label="How many bedrooms do you offer?",step=1)
beds = row4_col4.number_input(label="How many beds can be used by the guetst?",step=1)
property_type = row4_col1.selectbox("Property type",
                                    ("Boat","Entire Condo","Guest Suite", "Entire Guest House", "Entire loft","Entire rental unit", "Entire residential home","Entire serviced apartment","Entire townhouse", "Entire villa", "Private Room","Private room in bed and breakfast", "Private room in cabin", "Private room in castle", "Private room in condominium (condo)", "Private room in guest suite", "Private room in guesthouse", "Private room in hut","Private room in loft","Private room in rental unit","Private room in residential home", "Private room in serviced apartment","Private room in townhouse","Private room in villa", "Room in bed and breakfast","Room in boutique hotel", "Room in hotel", "Room in serviced apartment", "Shared room in bed and breakfast", "Shared room in hostel", "Shared room in hut", "Shared room in rental unit", "Tiny house"))


room_type = row4_col2.selectbox("Room type",
                                    ("Hotel room", "Private room","Shared room","Entire home/apt"))

min_night = row5_col1.number_input(label="What is the minimum amount of nights a user has to book?", min_value=1, step=1)
max_night = row5_col2.number_input(label="What is the maximum amount of nights a user has to book?",min_value=1, step=1)
available_30 = row5_col3.number_input("How many days is your object available in the next month?",min_value=1, max_value=31, step=1)
available_365 = row5_col4.number_input(label="How many days is your object available in the next year?",min_value=1, max_value=365, step=1)

review_scores_rating = row7_col1.slider("What's your average rating?",
                                        0.00,
                                        5.00,
                                        0.00)

review_scores_accuracy = row7_col2.slider("What's your average review (accuracy)?",
                                          0.00,
                                          5.00,
                                          0.00)
review_scores_cleanliness = row7_col3.slider("What's your average rating (cleanliness)?",
                                          0.00,
                                          5.00,
                                          0.00)
review_scores_checkin = row7_col4.slider("What's your average rating (checkin)?",
                                               0.00,
                                               5.00,
                                               0.00)
review_scores_communication = row8_col1.slider("What's your average rating (communication)?",
                                               0.00,
                                               5.00,
                                               0.00)
review_scores_location = row8_col2.slider("What's your average rating (location)?",
                                               0.00,
                                               5.00,
                                               0.00)
review_scores_value = row8_col3.slider("What's your average rating (value)?",
                                               0.00,
                                               5.00,
                                               0.00)
reviews_per_month = row8_col4.number_input(label= "How many reviews per month do you have?",min_value=0,step=1)



kreis = row9_col1.number_input("Please indicate in which Kreis is your rental object located", max_value=12, min_value=1)
lat = row9_col2.number_input("Please indicate the exact latitude of the rental object", min_value=47.32767, max_value=47.43129,step=1e-6, format="%.5f")
lon = row9_col3.number_input("Please indicate exact the longitude of the rental object",min_value=8.46653, max_value=8.6048,step=1e-6, format="%.5f")

# All the user inputs are here collected and appended to the details list.

details_list = []
details_list.append(is_host_since)
details_list.append(superhost)
details_list.append(total_listings)
details_list.append(profile_pic)
details_list.append(id_verified)
details_list.append(accommodates)
details_list.append(baths)
details_list.append(bedrooms)
details_list.append(beds)
details_list.append(min_night)
details_list.append(max_night)
details_list.append(available_30)
details_list.append(available_365)
details_list.append(total_reviews)
details_list.append(reviews_ltm)
details_list.append(reviews_l30d)
details_list.append(review_scores_rating)
details_list.append(review_scores_accuracy)
details_list.append(review_scores_cleanliness)
details_list.append(review_scores_checkin)
details_list.append(review_scores_communication)
details_list.append(review_scores_location)
details_list.append(review_scores_value)
details_list.append(reviews_per_month)
if(review_scores_rating!=0 or reviews_per_month!=0):
    details_list.append(1)
else:
    details_list.append(0)
if(review_scores_accuracy!=0 or review_scores_cleanliness!=0 or review_scores_checkin!=0 or review_scores_communication!=0 or review_scores_location!=0 or review_scores_value!=0):
    details_list.append(1)
else:
    details_list.append(0)
dummify(host_response_time,response_time_list)
dummify(kreis,kreis_list)
dummify(property_type, property_type_list)
dummify(room_type,room_type_list)
dummifyLists(verfication_types, verification_list)
dummify(gender,gender_list)
calc_dist(lon,lat)

## The dataframe from all the inputs in the details_list is created here.

df = pd.DataFrame([details_list])
print(df)

## The prediction model is loaded here, and the calculations are stored in the variable prediction

model = load_model()
prediction = model.predict(df)

## The calculate button is crated here, when pressed, the result is shown.
if row10_col1.button("Start Calculation"):
    row10_col2.subheader("Our sophisticated AI recommends the following price:")
    row10_col2.markdown(f"""
  #### "<span style="color:#FF5A5F;font-size:30px">CHF {round(prediction[0],2)}</span>"  
""", unsafe_allow_html=True)


