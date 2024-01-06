import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import pandas as pd
import numpy as np
import seaborn as sns
from preprocessor import preprocess_text_file
from helper import stats, most_busy_user, get_wordcloud, top_com_words, fetch_message, top_emoji, time_line, daily_timeline, week_activity, month_activity, heat_map_data

# Set Streamlit page configuration
st.set_page_config(page_title="Chat Analyzer", page_icon=":speech_balloon:", layout="wide")

# Function to center-align titles
def center_align_title(title):
    return f"<h2 style='text-align:center;'>{title}</h2>"

# Streamlit app

# Sidebar
st.sidebar.markdown(center_align_title("Chat Analyzer"), unsafe_allow_html=True)

# File upload
uploaded_file = st.sidebar.file_uploader("Choose a text file", type=["txt"])

if uploaded_file is not None:
    # Preprocess the uploaded file
    df = preprocess_text_file(uploaded_file)

    # Display the processed DataFrame
    cf = df
    user_list = cf['user'].unique().tolist()
    user_list.remove("group-notification")
    user_list.sort()
    user_list = ['Overall'] + user_list
    st.sidebar.text(f"Number of users: {len(user_list)-1}")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        st.header((f"{selected_user} Analysis"))
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header(("Total Messages"))
            st.title(stats(selected_user, df)[0])

        with col2:
            st.header(("Total Words"))
            st.title(stats(selected_user, df)[1])

        with col3:
            st.header(("Total Media Shared"))
            st.title(stats(selected_user, df)[2])

        with col4:
            st.header(("Total Links Shared"))
            st.title(stats(selected_user, df)[3])

        # Timeline Graph
        st.markdown(center_align_title('Timeline Graph'), unsafe_allow_html=True)
        col_timeline1, col_timeline2 = st.columns(2)

        with col_timeline1:
            st.markdown(center_align_title("Monthly Graph"), unsafe_allow_html=True)
            fig_monthly = px.line(time_line(selected_user, df), x='time', y='message', template='plotly_dark')
            st.plotly_chart(fig_monthly)

        with col_timeline2:
            st.markdown(center_align_title("Daily Graph"), unsafe_allow_html=True)
            fig_daily = px.line(daily_timeline(selected_user, df), x='only_date', y='message', template='plotly_dark')
            st.plotly_chart(fig_daily)

        # Activity Map
        st.markdown(center_align_title("Activity Map"), unsafe_allow_html=True)
        col_activity1, col_activity2 = st.columns(2)

        with col_activity1:
            # Most Busy Months
            st.markdown(center_align_title("Most Busy Months"), unsafe_allow_html=True)
            month_data = month_activity(selected_user, df)
            month_data = month_data.sort_values(by="month")
            month_data["month"] = pd.Categorical(
                month_data["month"],
                categories=[
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ],
                ordered=True,
            )

            st.bar_chart(month_data, x="month", y="message", use_container_width=True)

        with col_activity2:
            # Most Busy Day
            st.markdown(center_align_title("Most Busy Day"), unsafe_allow_html=True)
            week_data = week_activity(selected_user, df)
            week_data = week_data.sort_values(by="dayname")
            week_data["dayname"] = pd.Categorical(
                week_data["dayname"],
                categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                ordered=True,
            )

            st.bar_chart(week_data, x="dayname", y="message", use_container_width=True)

        # Most Busy Users or Individual User Messages
        if selected_user == 'Overall':
            st.markdown(center_align_title("Most Busy Users"), unsafe_allow_html=True)
            most_busy_users, busy_user_df = most_busy_user(df)
            col_busy1, col_busy2 = st.columns(2)

            with col_busy2:
                st.bar_chart(most_busy_users, use_container_width=True)

            with col_busy1:
                st.dataframe(busy_user_df)

        else:
            st.markdown(center_align_title(f"{selected_user}'s messages in the group"), unsafe_allow_html=True)
            st.dataframe(fetch_message(df, selected_user))

        st.markdown(center_align_title("User Activity Heatmap"), unsafe_allow_html=True)
        heat_map = heat_map_data(selected_user, df)
        fig_heatmap, ax_heatmap = plt.subplots(figsize=(20, 6))

        # Assuming the index of your heatmap is the day names
        day_names_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heat_map = heat_map.reindex(day_names_order)

        sns.heatmap(heat_map, cbar_kws={'label': 'Message Count'}, annot=False, ax=ax_heatmap)
        ax_heatmap.set_xlabel('Time Range')
        ax_heatmap.set_ylabel('Days')
        st.pyplot(fig_heatmap)


        # WordCloud
        st.markdown(center_align_title("WordCloud"), unsafe_allow_html=True)
        df_wc = get_wordcloud(selected_user, df)
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(df_wc)
        st.pyplot(fig_wc)

        # Most Common Words
        st.markdown(center_align_title("Most Common Words"), unsafe_allow_html=True)
        col_common1, col_common2 = st.columns(2)
        top_words_df = top_com_words(selected_user, df)

        with col_common1:
            st.dataframe(top_words_df)

        with col_common2:
            st.bar_chart(top_words_df, x="words", y="frequency", use_container_width=True)

        # Most Common Emojis
        st.markdown(center_align_title("Most Common Emojis"), unsafe_allow_html=True)
        col_emoji1, col_emoji2 = st.columns(2)
        top_emojis_df = top_emoji(selected_user, df)

        with col_emoji1:
            st.dataframe(top_emojis_df)

        with col_emoji2:
            st.bar_chart(top_emojis_df, x="emoji", y="frequency", use_container_width=True)
