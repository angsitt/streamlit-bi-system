import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from streamlit_option_menu import option_menu
from WebScrapper import IndeedScrapper
from DBConnection import DBConnection
from credentials import DB_USERNAME, DB_PASSWORD
from transformers import pipeline
from wordcloud import WordCloud, STOPWORDS

hide_menu = """
<style>
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
</style>
"""

SERVER = 'localhost, 1433'
DATABASE = 'epam_reviews'

menu = st.sidebar
st.markdown(hide_menu, unsafe_allow_html=True)

with menu:
    selected = option_menu(
        menu_title='Menu',
        options=['Home', 'Web-scrapper', 'EDA', 'English Reviews', 'Russian Reviews'],
        icons=['house', 'code-slash', 'search', 'chat-square-dots', 'chat-square-dots'],
        menu_icon='bar-chart',
        default_index=0
    )

if selected == 'Home':
    header = st.container()
    with header:
        st.title('EPAM Systems Reviews Sentiment Analysis')

elif selected == 'Web-scrapper':

    def parse_source(source):
        if source == 'Indeed.com':
            st.info(f'{source} web-scrapping started...')
            indeedScrapper = IndeedScrapper()
            status = indeedScrapper.parse()
            if 'Error' not in status:
                st.success(status)
            else:
                st.error(status)
            dataset = st.container()
            with dataset:
                st.header('Indeed Reviews Preview')
                st.text('TOP-10 records are displayed')
                reviews_df = pd.read_csv('indeed_reviews.csv', sep=';')
                st.write(reviews_df.head(10))
        elif source == 'Dreamjob.ru':
            st.write(source)
        elif source == 'careerbliss.com':
            st.write(source)
        elif source == 'habr.com':
            st.write(source)

    header = st.container()
    with header:
        st.title('Reviews Web-scrapping')

    st.write("To start web-scrapping it's necessary to choose one of the available company review web-sites.")
    source_to_parse = st.selectbox('Select Source', ('Indeed.com', 'Dreamjob.ru', 'careerbliss.com', 'habr.com'))
    parse_btn = st.button('Parse')
    if parse_btn:
        parse_source(source_to_parse)

if selected == 'EDA':
    header = st.container()
    with header:
        st.title('Exploratory Data Analysis')

    with st.header('1. Upload your CSV data'):
        uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

    # Pandas Profiling Report
    if uploaded_file is not None:
        @st.cache
        def load_csv():
            csv = pd.read_csv(uploaded_file, sep=';')
            return csv

        df = load_csv()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
    else:
        st.info('Awaiting for CSV file to be uploaded.')

elif selected == 'English Reviews':

    def sentiment_analysis(df):
        sent_pipeline = pipeline("sentiment-analysis")
        df['sentiment'] = df['review'].apply(lambda x: sent_pipeline(x)[0]['label'])
        with DBConnection(SERVER, DATABASE, DB_USERNAME, DB_PASSWORD) as db:
            db.update_sentiment(df)

    header = st.container()
    dataset = st.container()
    visualizations = st.container()

    with header:
        st.title('Reviews Sentiment Analysis')
        st.text('The purpose of the analysis:\n'
                '- estimate EPAM Systems as an employer;\n'
                '- define strengths and weaknesses of EPAM HR-brand.')

    with dataset:
        st.header('EPAM Systems Reviews')
        pd.set_option('display.max_columns', None)
        with DBConnection(SERVER, DATABASE, DB_USERNAME, DB_PASSWORD) as db:
            sql_query = 'SELECT r.id, r.title, r.review, r.advantage, r.disadvantage, r.score, r.review_date ' \
                        'FROM hr_brand.reviews r ' \
                        'WHERE r.review is not NULL AND r.lang = \'eng\' and r.sentiment is NULL ' \
                        'ORDER BY r.review_date DESC'
            df = db.read_sql_to_df(sql_query)
            df_main = db.read_reviews_to_df('eng')
        if df_main.shape[0] == 0:
            st.info('There is no data in the database. '
                    'Please go to "Web-scrapper" and parse the data from available web-source to start analysis.')
        else:
            st.info(f'There are {df.shape[0]} reviews that could be processed.')
            if df.shape[0] != 0:
                analyze_btn = st.button('Analyze')
                if analyze_btn:
                    st.info('Sentiment Analysis started...')
                    sentiment_analysis(df)
                    st.success('Sentiment Analysis executed successfully!')
                    with DBConnection(SERVER, DATABASE, DB_USERNAME, DB_PASSWORD) as db:
                        df = db.read_reviews_to_df('eng')
                    st.write(df)
            else:
                st.write(df_main)

            with visualizations:
                st.header('Data Visualization')
                st.text('Score Distribution')
                ax = df['score'].value_counts().sort_index()
                st.bar_chart(ax)

                st.text('Strengths')
                positive_text = " ".join(cat for cat in df.advantage.dropna())
                # Creating word_cloud with text as argument in .generate() method
                wordcloud = WordCloud(collocations=False).generate(positive_text)
                # Display the generated Word Cloud
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.show()
                st.pyplot()

                st.text('Weaknesses')
                negative_text = " ".join(cat for cat in df.disadvantage.dropna())
                # Creating word_cloud with text as argument in .generate() method
                wordcloud = WordCloud(collocations=False).generate(negative_text)
                # Display the generated Word Cloud
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.show()
                st.pyplot()

elif selected == 'Russian Reviews':
    header = st.container()
    dataset = st.container()
    visualizations = st.container()

    with header:
        st.title('Reviews Sentiment Analysis')
        st.text('The purpose of the analysis:\n'
                '- estimate EPAM Systems as an employer;\n'
                '- define strengths and weaknesses.')

    with dataset:
        st.header('EPAM Systems Reviews')
        st.text('10 the most recent reviews are displayed')
        pd.set_option('display.max_columns', None)
        df = pd.read_csv('dreamjob_reviews.csv', sep=';')
        st.write(df)

        st.text('Частота слов')
        text = " ".join(cat for cat in df.review.dropna())
        # Creating word_cloud with text as argument in .generate() method
        wordcloud = WordCloud(collocations=False).generate(text)
        # Display the generated Word Cloud
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()