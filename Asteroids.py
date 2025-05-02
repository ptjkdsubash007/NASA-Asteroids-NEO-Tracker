import streamlit as st
import pymysql
import pandas as pd
import datetime
#create a connection to MySQL
connection=pymysql.connect(
    host='localhost',
    user='root',
    password='@Ss952714103317',
    database='asteroids_db'
)
#create a cursor for MySQL commands
cursor=connection.cursor()
c1,c2,c3=st.columns([0.1,0.8,0.1])
with c2:
    st.title(":rocket: _:blue[NASA]_ Asteroids NEO Tracker")
    st.write(":orange-badge[Note:]The results are filtered from *:blue[10000 asteroids]* approaches from date of *:blue[2024-01-01]*")

st.divider()  # Draws a horizontal rule

#Full Table data
query="""SELECT a.id AS ID, 
        a.name AS NAME, 
        a.absolute_magnitude_h AS Magnitude, 
        a.estimated_diameter_min_km AS Min_Estimated_Diameter_km, 
        a.estimated_diameter_max_km AS Max_Estimated_Diameter_km,
        c.relative_velocity_kmph AS Asteroids_Velocity_kmph,
        c.astronomical AS Astronomical_Unit,
        c.close_approach_date AS Close_Approach_Date,
        a.is_potentially_hazardous_asteroid AS Potentially_Hazardous
        FROM asteroids a 
        LEFT JOIN close_approach c 
        ON a.id = c.neo_reference_id
        GROUP BY ID, 
        NAME,
        Magnitude, 
        Min_Estimated_Diameter_km, 
        Max_Estimated_Diameter_km,
        Asteroids_Velocity_kmph,
        Astronomical_Unit,
        Close_Approach_Date,
        Potentially_Hazardous
        ORDER BY Close_Approach_Date
        ;"""
df= pd.read_sql(query,connection)


#Minimum&Maximum values for Min. Magnitude slider
min_mag=round(min(df['Magnitude']),1)
max_mag=round(max(df['Magnitude']),1)
#Minimum&Maximum values for Min Estimated diameter(km) slider
Min_min_dia=round(min(df['Min_Estimated_Diameter_km']),1)
Max_min_dia=round(max(df['Min_Estimated_Diameter_km']),1)
#Minimum&Maximum values for Max Estimated diameter(km) slider
Min_max_dia=round(min(df['Max_Estimated_Diameter_km']),1)
Max_max_dia=round(max(df['Max_Estimated_Diameter_km']),1)
#Minimum & Maximum value for Asteroids Velocity(kmph) slider
Min_vel=round(min(df['Asteroids_Velocity_kmph']),1)
Max_vel=round(max(df['Asteroids_Velocity_kmph']),1)
#Minimum & Maximum value for Astronomical Unit slider
Min_AU=round(min(df['Astronomical_Unit']),1)
Max_AU=round(max(df['Astronomical_Unit']),1)
#Date value for Start Date date_input widget
min_date=df.iloc[0,df.columns.get_loc('Close_Approach_Date')]
#Date value for End Date date_input widget
max_date=df.iloc[-1,df.columns.get_loc('Close_Approach_Date')]


#Create a Filters
c1,c2,c3=st.columns(3,gap='large')
with c1:
    from_magnitude,to_magnitude=st.slider('Min Magnitude',min_mag,max_mag,(min_mag,max_mag))
    from_Min_ED,to_Min_ED2=st.slider('Min Estimated Diameter(km)',Min_min_dia,Max_min_dia,(Min_min_dia,Max_min_dia))
    from_Max_ED1,to_Max_ED2=st.slider('Max Estimated Diameter(km)',Min_max_dia,Max_max_dia,(Min_max_dia,Max_max_dia))


with c2:
    from_Ast_velocity,to_Ast_velocity=st.slider('Asteroids Velocity(kmph)',Min_vel,Max_vel,(Min_vel,Max_vel))
    from_AU,to_AU=st.slider('Astronomical Unit',Min_AU,Max_AU,(Min_AU,Max_AU))
    Hazardous=st.selectbox('Potentially Hazardous',['0','1'])

with c3:
    start_date=st.date_input('Start Date',min_date)   
    end_date=st.date_input('End Date',max_date)
    

filter_bt=st.button(':material/tune: Filter')
st.divider()  # Draws a horizontal rule


if filter_bt:
    st.write('### Filtered Asteroids:')
    query=f"""SELECT a.id AS ID, 
        a.name AS NAME, 
        a.absolute_magnitude_h AS Magnitude, 
        a.estimated_diameter_min_km AS Min_Estimated_Diameter_km, 
        a.estimated_diameter_max_km AS Max_Estimated_Diameter_km,
        c.relative_velocity_kmph AS Asteroids_Velocity_kmph,
        c.astronomical AS Astronomical_Unit,
        c.close_approach_date AS Close_Approach_Date,
        a.is_potentially_hazardous_asteroid AS Potentially_Hazardous
        FROM asteroids a 
        LEFT JOIN close_approach c 
        ON a.id = c.neo_reference_id
        WHERE Close_Approach_Date>='{start_date}' AND Close_Approach_Date<='{end_date}'
        GROUP BY ID, 
        NAME,
        Magnitude, 
        Min_Estimated_Diameter_km, 
        Max_Estimated_Diameter_km,
        Asteroids_Velocity_kmph,
        Astronomical_Unit,
        Close_Approach_Date,
        Potentially_Hazardous
        HAVING
        Magnitude>={from_magnitude} 
        AND Magnitude<={to_magnitude} 
        AND Min_Estimated_Diameter_km>={from_Min_ED} 
        AND Min_Estimated_Diameter_km<={to_Min_ED2}
        AND Max_Estimated_Diameter_km>={from_Max_ED1} 
        AND Max_Estimated_Diameter_km<={to_Max_ED2}
        AND Asteroids_Velocity_kmph>={from_Ast_velocity}
        AND Asteroids_Velocity_kmph<={to_Ast_velocity}
        AND Astronomical_Unit>={from_Max_ED1}
        AND Astronomical_Unit<={to_Max_ED2} 
        AND Potentially_Hazardous={Hazardous}
        ORDER BY Close_Approach_Date
        ;"""
    df= pd.read_sql(query,connection)
    df=df.drop_duplicates(keep=False)
    st.dataframe(df)
        

#print table
