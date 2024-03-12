import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the df
def load_df():
    df = pd.read_csv("df.csv", low_memory=False)
    return df

reason = {
    "springer": "Spring brings clear skies, few clouds, and partly cloudy conditions, making it an optimal time for biking. The mild temperatures and blossoming landscapes create a refreshing and invigorating atmosphere for cyclists.",
    "summer": "Summer combines mist with cloudy, broken clouds, and few clouds, providing a refreshing atmosphere for biking. The warm temperatures and occasional mist create a pleasant environment for cyclists to enjoy their rides.",
    "fall": "Fall, characterized by light snow, scattered clouds, and occasional light rain with thunderstorms, offers a cozy atmosphere for biking enthusiasts. The picturesque landscapes adorned with colorful foliage attract cyclists, despite the occasional drizzle, making it a peak season for biking activity.",
    "winter": "Heavy rain, ice pallets, thunderstorms, and mist occur alongside snow and fog, making it less favorable for biking due to the challenging and potentially dangerous conditions."
}

def get_max_reason():
    df = load_df()
    max_season = df.loc[df["cnt_daily"].idxmax(), "season_daily"]  # Get the season with maximum daily count
    return max_season

def display_monthly_traffic():
    
    all_df = load_df()
    all_df['dteday_daily'] = pd.to_datetime(all_df['dteday_daily'])

    month_df = all_df.resample('ME', on="dteday_daily").agg({
        "cnt_daily": "sum",
        "registered_daily": "sum",
        "casual_daily": "sum"
    })

    # Konversi index ke formatted date strings
    month_df.index = month_df.index.strftime('%B')

    # Rename columns
    month_df.rename(columns={
        "cnt_daily": "total user",
        "registered_daily": "registered user",
        "casual_daily": "casual user"
    }, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(month_df.index, month_df["total user"], marker='o', linewidth=2, label="Total Users")
    ax.plot(month_df.index, month_df["registered user"], marker='o', linewidth=2, label="Registered Users")
    ax.plot(month_df.index, month_df["casual user"], marker='o', linewidth=2, label="Casual Users")
    ax.set_title("Number of Users per Month", loc="center", fontsize=20)
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("Number of Users", fontsize=14)
    ax.tick_params(axis='x', labelrotation=45)  
    ax.tick_params(axis='both', labelsize=10)
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
# function to display percentag of the user
def display_percentage_by_season(total_users, registered_users, casual_users):
    registered_percentage = (registered_users / total_users) * 100
    casual_percentage = (casual_users / total_users) * 100

    st.subheader("Total Users")
    st.subheader(f"{total_users}")

    col1, col2 = st.columns(2)
    # Display percentage of users
    with col1:
        st.write("Registered Users Percentage")
        st.subheader(f"{registered_percentage:.2f}%")

    with col2:
        st.write("Casual Users Percentage")
        st.subheader(f"{casual_percentage:.2f}%")

def display_all_season_line_chart():
    df = load_df()

    df['dteday_daily'] = pd.to_datetime(df['dteday_daily'])
    df.set_index('dteday_daily', inplace=True)
    sum_user_of_season = df.groupby(by="season_daily").agg({
        "cnt_daily": "sum",
        "registered_daily": "sum",
        "casual_daily": "sum"
    })

    total = sum_user_of_season["cnt_daily"]
    registered = sum_user_of_season["registered_daily"]
    casual = sum_user_of_season["casual_daily"]

    sum_user_of_season.rename(columns={
        "cnt_daily": "total user",
        "registered_daily": "registered user",
        "casual user": "casual user"
    })

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(24, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="cnt_daily", y="season_daily", data=sum_user_of_season, hue='season_daily', palette=colors, legend=False, ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    plt.show()
    st.pyplot(fig)
    max_reason = get_max_reason()
    st.subheader("Reason")
    st.write(reason[max_reason])
    display_percentage_by_season(total.iloc[0], registered.iloc[0], casual.iloc[0])

    
# function to show season barchart
def display_season_traffic(selected_column):
    df = load_df()
    if selected_column == "spring":
        springer = df[df['season_daily'] == "springer"].agg({
            "cnt_daily": "sum",
            "registered_daily": "sum",
            "casual_daily": "sum"
        })

        total = springer["cnt_daily"]
        registered = springer["registered_daily"]
        casual = springer["casual_daily"]

        springer.rename({
            "cnt_daily": "total user",
            "registered_daily": "registered user",
            "casual_daily": "casual user"
        }, inplace=True)

        st.bar_chart(springer)
        display_percentage_by_season(total, registered, casual)

    elif selected_column == "summer":
        summer = df[df['season_daily'] == "summer"].agg({
            "cnt_daily": "sum",
            "registered_daily": "sum",
            "casual_daily": "sum"
        })

        total = summer["cnt_daily"]
        registered = summer["registered_daily"]
        casual = summer["casual_daily"]

        summer.rename({
            "cnt_daily": "total user",
            "registered_daily": "registered user",
            "casual_daily": "casual user"
        }, inplace=True)

        st.bar_chart(summer)
        display_percentage_by_season(total, registered, casual)

    elif selected_column == "fall":
        fall = df[df['season_daily'] == "fall"].agg({
            "cnt_daily": "sum",
            "registered_daily": "sum",
            "casual_daily": "sum"
        })

        total = fall["cnt_daily"]
        registered = fall["registered_daily"]
        casual = fall["casual_daily"]

        fall.rename({
            "cnt_daily": "total user",
            "registered_daily": "registered user",
            "casual_daily": "casual user"
        }, inplace=True)
        st.bar_chart(fall)
        display_percentage_by_season(total, registered, casual)

    elif selected_column == "winter":
        winter = df[df['season_daily'] == "winter"].agg({
            "cnt_daily": "sum",
            "registered_daily": "sum",
            "casual_daily": "sum"
        })
        
        total = winter["cnt_daily"]
        registered = winter["registered_daily"]
        casual = winter["casual_daily"]

        winter.rename({
            "cnt_daily": "total user",
            "registered_daily": "registered user",
            "casual_daily": "casual user"
        }, inplace=True)
        st.bar_chart(winter)
        display_percentage_by_season(total, registered, casual)
    
def weather_conditions(select_option):
    if select_option == "spring":
        st.header("Weather condition of this season")
        st.subheader("Clear, few clouds, partly cloudy, partly cloudy.")
    elif select_option == "summer":
        st.header("Weather condition of this season")
        st.subheader("Mist and cloudy, mist and broken clouds, mist and few clouds, mist.")
    elif select_option == "fall":
        st.header("Weather condition of this season")
        st.subheader("Light snow, light rain plus thunderstorm and scattered clouds, light rain and scattered clouds.")
    elif select_option == "winter":
        st.header("Weather condition of this season")
        st.subheader("Heavy rain plus ice pallets plus thunderstorm and mist, snow and fog.")

def main():
    # Title
    st.header('', divider='rainbow')
    st.title('Traffic Biker Behavior')
    st.header('', divider='rainbow')
    # Sidebar options
    selected_option = st.sidebar.selectbox('Select Season:', ["spring", "summer", "fall", "winter"])

    # Display all traffic
    display_monthly_traffic()
    st.subheader("Amount user per season")
    # Display the reason for the maximum traffic
    display_all_season_line_chart()
    
    # Display traffic based on season
    st.header('', divider='rainbow')
    st.header("Biker behavior in each season")
    st.header('', divider='rainbow')

    display_season_traffic(selected_option)
    weather_conditions(selected_option)


if __name__ == "__main__":
    main()



