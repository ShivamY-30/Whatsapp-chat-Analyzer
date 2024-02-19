import streamlit as st
import Preprocessor, helper
import matplotlib.pyplot as plt
import emoji
import seaborn as sns

st.sidebar.title("Check")

uploaded_files = st.sidebar.file_uploader("Choose a file")
if uploaded_files is not None:
    bytes_data = uploaded_files.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)

    st.title("Whats-App Chat Statistics")
    # Draw a horizontal line
    st.markdown("---")
    df = Preprocessor.preprocessing(data)


    user_list = df['user'].unique().tolist()

    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis based on: ", user_list)
    if st.sidebar.button("Show Analysis"):

        if selected_user != 'Overall':

            st.header(f"Portfolio of : {selected_user}")
        else:
            st.header("Portfolio of All Members")

        total_msg, total_words, total_media, links_length = helper.helper_method(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Mesaages")
            st.title(total_msg)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Total Media")
            st.title(total_media)
        with col4:
            st.header("Total Number of Links")
            st.title(links_length)

        # Top users and Graph section:
        if selected_user == 'Overall':
            st.title("Most Active User")
            top_user, Percentage_df = helper.Top_user(df)
            fig, ax = plt.subplots()

            col1, col2, = st.columns(2)

            with col1:
                ax.pie( top_user.values, labels=top_user.index )
                # plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(Percentage_df)

        # WordCloud
        # df_wc = helper.wordcloud(selected_user,df)
        # fig, axis = plt.subplots()
        # axis.imshow(df_wc)
        # st.pyplot(fig)

        # Top USed Words and Graph section:
        st.title("Top Words")
        col1, col2, = st.columns(2)
        common_words = helper.most_common_Words(selected_user, df)

        with col1:
            st.dataframe(common_words)

        fig, ax = plt.subplots()
        ax.barh(common_words['Message'], common_words['Frequency'], color='blue')
        plt.ylabel("Message")
        plt.xlabel("Frequency")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)





        #TimeLine of the chat
        st.header("Dayz & Monthly & Yearly  Timeline")
        timeLine = helper.timeline_chat(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeLine['time'] , timeLine['message'] , color="red")
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)


        major_day = helper.day_most_activity(selected_user,df)
        st.title("Most Busy Dayz")
        col1 , col2 = st.columns(2)
        with col1:

            figure , axis = plt.subplots()
            axis.pie(major_day['count'] , labels =major_day['day_name'],autopct="%0.2f" )
            st.pyplot(figure)

        with col2:
             st.dataframe(major_day)


        major_month = helper.month_most_activity(selected_user,df)
        st.title("Most Busy Months")
        col1 , col2 = st.columns(2)
        with col2:
            figure , axis = plt.subplots()
            axis.bar(major_month['month'],major_month['count'] )
            plt.xticks(rotation = "vertical")
            plt.xlabel("Emojis")
            plt.ylabel("Frequency")
            st.pyplot(figure)

        with col1:
             st.dataframe(major_month)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig , ax = plt.subplots()
        ax= sns.heatmap(user_heatmap)
        st.pyplot(fig)

                #Emoji
        # st.title("Emoji Used Analysis")
        # col1, col2, = st.columns(2)
        # with col1:

        #     emoji_df = helper.emoji_founder(selected_user,df)
        #     st.dataframe(emoji_df)

        # with col2:
        #     fig, ax = plt.subplots()
        #     ax.barh(emoji_df['Emoji'], emoji_df['Frequency'], color='green')
        #     plt.xlabel("Emojis")
        #     plt.ylabel("Frequency")
        #     plt.xticks(rotation='vertical')
        #     st.pyplot(fig)


