import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    #st.dataframe(df)
    # fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        num_messg,words,num_media_messg,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("Total Messages")
            st.title(f"{num_messg}")
        with col2:
            st.write("Total Words")
            st.title(f"{words}")
        with col3:
            st.write("Total Media Messages")
            st.title(f"{num_media_messg}")
        with col4:
            st.write("Total Links")
            st.title(f"{num_links}")
        #Timeline
        timeline=helper.monthly_timeline(selected_user,df)
        st.title("Monthly Timeline")
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)
        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Activity Map
        st.title('Activity Map:')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most active month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #Weeklyactivity map
        st.title("Weekly Activity Map:")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #Busy Users
        if selected_user == 'overall':
            st.title("Most Busy user:")
            x,new_df=helper.most_busy_users(df)
            fig, ax=plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # WordCloud
        st.title("Wordcloud:")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        # most common words
        most_common_words = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words[0], most_common_words[1],color='red')
        plt.xticks(rotation=90)
        st.title("Most Common Words:")
        st.pyplot(fig)
        #emoji analysis
        # Code handling the output
        most_common_emoji = helper.emoji_analysis(selected_user, df)
        st.title("Emoji Analysis:")
        if isinstance(most_common_emoji, str) and most_common_emoji == "DataFrame is empty":
            st.write("No Emoji")
        elif isinstance(most_common_emoji, str) and most_common_emoji == "No emojis found":
            st.write("No emojis found in the data")
        else:
            # Proceed with displaying the dataframe and plotting the pie chart
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(most_common_emoji)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(most_common_emoji[1],labels=most_common_emoji[0],autopct='%1.1f%%')
                st.pyplot(fig)


