

import streamlit as st
import pymysql
import pandas as pd

connection=pymysql.connect(
    host='localhost',
    user='root',
    password='@Ss952714103317',
    database='asteroids_db'
)
cursor=connection.cursor()
c1,c2,c3=st.columns([0.1,0.8,0.1])
with c2:
    st.title(":rocket: _:blue[NASA]_ Asteroids NEO Tracker")
    st.write(":orange-badge[Note:]The results are filtered from *:blue[10000 asteroids]* approaches from date of *:blue[2024-01-01]*")


options=st.selectbox('Select the query:',["Select the query",
                                  "1. Count how many times each asteroid has approached Earth",
                                  "2. Average velocity of each asteroid over multiple approaches",
                                  "3. List top 10 fastest asteroids",
                                  "4. Find potentially hazardous asteroids that have approached Earth more than 3 times",
                                  "5. Find the month with the most asteroid approaches",
                                  "6. Get the asteroid with the fastest ever approach speed",
                                  "7. Sort asteroids by maximum estimated diameter (descending)",
                                  "8. Asteroids whose closest approach is getting nearer over time",
                                  "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
                                  "10. List names of asteroids that approached Earth with velocity > 50,000 km/h",
                                  "11. Count how many approaches happened per month",
                                  "12. Find asteroid with the highest brightness",
                                  "13. Get number of hazardous vs non-hazardous asteroids",
                                  "14. Find asteroids that passed closer than the Moon along with their close approach date and distance",
                                  "15. Find asteroids that came within 0.05 AU",
                                  "16. Count how many approaches happened per day",
                                  "17. Find asteroid with the least brightness",
                                  "18. Find Top 10 close approaches asteroids near earth",
                                  "19. Find Top 10 asteroids with most count of approaches to Earth",
                                  "20. Find Top 10 potentially hazardous asteroids with most count of approaches to Earth"
                                  ])


# 1. Count how many times each asteroid has approached Earth


if options=="1. Count how many times each asteroid has approached Earth":
    
    query = """SELECT name NAME,
                COUNT(id) as No_of_Approaches 
                FROM asteroids 
                GROUP BY name;"""
    df = pd.read_sql(query, connection)
    st.write("Table of each asteroid's number of approaches to earth:")
    st.dataframe(df)
    

# 2. Average velocity of each asteroid over multiple approaches

elif options=="2. Average velocity of each asteroid over multiple approaches":
    
    query = """SELECT a.name as NAME, 
                AVG(c.relative_velocity_kmph) as Average_velocity 
                FROM asteroids a
                INNER JOIN close_approach c on c.neo_reference_id=a.id 
                GROUP BY a.name
                ORDER BY Average_velocity
                DESC;"""
    df = pd.read_sql(query, connection)
    st.write("Table of average velocity of each asteroid's approaches to earth:")
    st.dataframe(df)

# 3. List top 10 fastest asteroids

elif options=="3. List top 10 fastest asteroids":
    
    query = """SELECT a.name as NAME, 
                c.relative_velocity_kmph as Average_velocity 
                FROM asteroids a
                INNER JOIN close_approach c on c.neo_reference_id=a.id 
                ORDER BY c.relative_velocity_kmph
                DESC LIMIT 10;"""
    df = pd.read_sql(query, connection)
    st.write("Table of Top 10 fastest asteroids approaches to earth:")
    st.dataframe(df)

# 4. Find potentially hazardous asteroids that have approached Earth more than 3 times

elif options=="4. Find potentially hazardous asteroids that have approached Earth more than 3 times":
    
    query = """SELECT name,
                COUNT(id) as No_of_Approaches
                FROM asteroids 
                WHERE is_potentially_hazardous_asteroid=1
                GROUP BY name 
                HAVING COUNT(id)>3
                ORDER BY No_of_Approaches DESC ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of hazardous asteroids approaches to earth more than 3 times:")
    st.dataframe(df)

# 5. Find the month with the most asteroid approaches

elif options=="5. Find the month with the most asteroid approaches":
    
    query = """SELECT DATE_FORMAT(close_approach_date, "%M %Y") as MONTH, 
                COUNT(EXTRACT(YEAR_MONTH FROM close_approach_date)) as No_of_Approaches 
                FROM close_approach 
                GROUP BY MONTH
                ORDER BY No_of_Approaches
                DESC;"""
    df = pd.read_sql(query, connection)
    month=df['MONTH'][0] #To get The most asteroids approached month
    nos=df['No_of_Approaches'][0] #To get the most number of approaches of month
    st.write("The month with most asteroid approaches is ***:green[%s]*** and Number of approaches is ***:green[%d]***" % (month,nos))

    

# 6. Get the asteroid with the fastest ever approach speed

elif options=="6. Get the asteroid with the fastest ever approach speed":
    query = """SELECT a.name as NAME, 
                c.relative_velocity_kmph as Speed_kmph 
                FROM asteroids a
                LEFT JOIN close_approach c on a.id=c.neo_reference_id
                ORDER BY Speed_kmph DESC;"""
    df = pd.read_sql(query, connection)
    NAME=df['NAME'][0] #To get The most asteroids approached month
    SPEED=df['Speed_kmph'][0] #To get the most number of approaches of month
    st.write(f"The asteroid fastest ever approaches is ***:green[{NAME}]*** and It's speed is ***:green[{SPEED:.2f}kmph]***")
    

# 7. Sort asteroids by maximum estimated diameter (descending)

elif options=="7. Sort asteroids by maximum estimated diameter (descending)":
    query = """SELECT name as NAME, estimated_diameter_max_km as MAXIMUM_DIAMETER
                FROM asteroids 
                ORDER BY MAXIMUM_DIAMETER
                DESC;"""
    df = pd.read_sql(query, connection)
    st.write("Table of asteroids maximum estimated diameter:")
    st.dataframe(df)

# 8. Asteroids whose closest approach is getting nearer over time

elif options=="8. Asteroids whose closest approach is getting nearer over time":
    query = """SELECT a.name NAME, c.close_approach_date as DATE, c.astronomical as ASTRONOMICAL_AU
                FROM asteroids a 
                LEFT JOIN close_approach c ON a.id=c.neo_reference_id
                GROUP BY NAME,DATE,ASTRONOMICAL_AU
                ORDER BY DATE
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of Asteroids approach getting nearer over time to earth:")
    st.dataframe(df)

# 9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth

elif options=="9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
    query = """SELECT a.name NAME, c.close_approach_date as DATE,c.astronomical as ASTRONOMICAL_AU, c.miss_distance_km MISS_DISTANCE_KM, c.miss_distance_lunar MISS_DISTANCE_LD
                FROM asteroids a 
                LEFT JOIN close_approach c ON a.id=c.neo_reference_id
                ORDER BY DATE
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of each asteroid along with the date and miss distance of its closest approach to Earth:")
    st.dataframe(df)

# 10. List names of asteroids that approached Earth with velocity > 50,000 km/h

elif options=="10. List names of asteroids that approached Earth with velocity > 50,000 km/h":
    query = """SELECT a.name NAME, c.relative_velocity_kmph as VELOCITY_kmph
                FROM asteroids a 
                LEFT JOIN close_approach c ON a.id=c.neo_reference_id
                GROUP BY NAME, VELOCITY_kmph
                HAVING VELOCITY_kmph>50000
                ORDER BY VELOCITY_kmph;"""
    df = pd.read_sql(query, connection)
    st.write("Table of each asteroid along with the date and miss distance of its closest approach to Earth:")
    st.dataframe(df)

# 11. Count how many approaches happened per month

elif options=="11. Count how many approaches happened per month":
    query = """SELECT DATE_FORMAT(close_approach_date, "%M %Y") as MONTH, 
                COUNT(EXTRACT(YEAR_MONTH FROM close_approach_date)) as No_of_Approaches 
                FROM close_approach 
                GROUP BY MONTH
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of asteroid approaches per month:")
    st.dataframe(df)

# 12. Find asteroid with the highest brightness

elif options=="12. Find asteroid with the highest brightness":
    query = """SELECT name NAME, absolute_magnitude_h MAGNITUDE 
                FROM asteroids
                ORDER BY MAGNITUDE
                ;"""
    df = pd.read_sql(query, connection)
    name=df['NAME'][0]
    mag=df['MAGNITUDE'][0]
    st.write(f"The highest brightness asteroid is ***:green[{name}]*** and its magnitude is ***:green[{mag:.2f}]***")
    

# 13. Get number of hazardous vs non-hazardous asteroids
elif options=="13. Get number of hazardous vs non-hazardous asteroids":
    query="""SELECT COUNT(CASE WHEN is_potentially_hazardous_asteroid=1 THEN 1 END) AS HAZARDOUS,
            COUNT(CASE WHEN is_potentially_hazardous_asteroid=0 THEN 1 END) AS NON_HAZARDOUS
            FROM asteroids
            ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of numbers of harzardous vs non-harzardous asteroids:")
    st.dataframe(df)
    

# 14. Find asteroids that passed closer than the Moon along with their close approach date and distance
elif options=="14. Find asteroids that passed closer than the Moon along with their close approach date and distance":
    query=""" SELECT a.name NAME, c.miss_distance_lunar DISTANCE_LD, c.miss_distance_km DISTANCE_KM
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_reference_id
            GROUP BY NAME,DISTANCE_LD,DISTANCE_KM
            HAVING DISTANCE_LD<1
            ORDER BY DISTANCE_LD
            ;"""
    df=pd.read_sql(query,connection)
    st.dataframe(df)

# 15. Find asteroids that came within 0.05 AU
elif options=="15. Find asteroids that came within 0.05 AU":
    query = """SELECT a.name NAME, c.astronomical as ASTRONOMICAL_AU
                FROM asteroids a 
                LEFT JOIN close_approach c ON a.id=c.neo_reference_id
                GROUP BY NAME, ASTRONOMICAL_AU
                HAVING ASTRONOMICAL_AU<0.05
                ORDER BY ASTRONOMICAL_AU
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of Asteroids approach getting nearer over time to earth:")
    st.dataframe(df)

# 16. Count how many approaches happened per day
elif options=="16. Count how many approaches happened per day":
    query = """SELECT close_approach_date as DATE, 
                COUNT(close_approach_date) as No_of_Approaches 
                FROM close_approach 
                GROUP BY DATE
                ORDER BY DATE
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of asteroid approaches per month:")
    st.dataframe(df)

# 17. Find asteroid with the least brightness

elif options=="17. Find asteroid with the least brightness":
    query = """SELECT name NAME, absolute_magnitude_h MAGNITUDE 
                FROM asteroids
                ORDER BY MAGNITUDE
                DESC
                ;"""
    df = pd.read_sql(query, connection)
    name=df['NAME'][0]
    mag=df['MAGNITUDE'][0]
    st.write(f"The least brightness asteroid is ***:green[{name}]*** and its magnitude is ***:green[{mag:.2f}]***")
    
# 18. Find Top 10 close approaches asteroids near earth
elif options=="18. Find Top 10 close approaches asteroids near earth":
    query=""" SELECT a.name NAME, c.miss_distance_km DISTANCE_KM
            FROM asteroids a
            JOIN close_approach c ON a.id = c.neo_reference_id
            GROUP BY NAME,DISTANCE_KM
            HAVING DISTANCE_KM
            ORDER BY DISTANCE_KM LIMIT 10
            ;"""
    df=pd.read_sql(query,connection)
    st.write("Table of Top 10 close approaches asteroids near earth:")
    st.dataframe(df)

# 19. Find Top 10 asteroids with most count of approaches to Earth
if options=="19. Find Top 10 asteroids with most count of approaches to Earth":
    query = """SELECT name NAME,
                COUNT(id) as No_of_Approaches 
                FROM asteroids 
                GROUP BY name
                ORDER BY No_of_Approaches
                DESC LIMIT 10
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of Top 10 asteroids with most count of approaches to Earth:")
    st.dataframe(df)

# 20. Find Top 10 potentially hazardous asteroids with most count of approaches to Earth
if options=="20. Find Top 10 potentially hazardous asteroids with most count of approaches to Earth":
    query = """SELECT name NAME,
                COUNT(id) as No_of_Approaches 
                FROM asteroids 
                WHERE is_potentially_hazardous_asteroid=1
                GROUP BY name
                ORDER BY No_of_Approaches
                DESC LIMIT 10
                ;"""
    df = pd.read_sql(query, connection)
    st.write("Table of Top 10 potentially hazardous asteroids with most count of approaches to Earth:")
    st.dataframe(df)

else:
    st.success(":rotating_light: :red[No queries selected :point_up:]")
    
