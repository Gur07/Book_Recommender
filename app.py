import streamlit as st
import pickle
import pandas as pd

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

st.set_page_config(page_title="📚 Book Recommender System", layout='wide')
st.title("📚 Personalized Book Recommender")
st.subheader("Helping You Find Your Next Favorite Read!")
st.markdown("**Made with ❤️ by Me**")


st.sidebar.header("Choose Recommendation Mode")
option = st.sidebar.radio("Select Option:", ['Top 50 Popular Books', 'Collaborative Filtering Recommendation'])

if option == 'Top 50 Popular Books':
    st.subheader("🌟 Top 50 Most Popular Books")
    
    for index, row in popular_df.iterrows():
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(row['Image-URL-M'], width=120)
        with cols[1]:
            st.write(f"**{row['Book-Title']}**")
            st.write(f"Author: {row['Book-Author']}")
            st.write(f"Publisher: {row['Publisher']}")
            st.write(f"Year: {row['Year-Of-Publication']}")
            st.write(f"Rating: {row['avg_rating']:.2f}")
        st.markdown("---")

# --- Collaborative Filtering Section ---
elif option == 'Collaborative Filtering Recommendation':
    st.subheader("🔍 Find Books Similar to Your Favorite")
    user_input = st.text_input("Enter a Book Title:")

    def recommend(book_name):
        try:
            index = pt.index.get_loc(book_name)
        except KeyError:
            return []

        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
        
        recommended_books = []
        for i in similar_items:
            book_data = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
            if not book_data.empty:
                item = {
                    'title': book_data['Book-Title'].values[0],
                    'author': book_data['Book-Author'].values[0],
                    'publisher': book_data['Publisher'].values[0],
                    'year': book_data['Year-Of-Publication'].values[0],
                    'image': book_data['Image-URL-M'].values[0]
                }
                recommended_books.append(item)
        return recommended_books

    if user_input:
        recommendations = recommend(user_input)
        if recommendations:
            st.success("Here are some books you might enjoy:")
            for rec in recommendations:
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(rec['image'], width=120)
                with cols[1]:
                    st.write(f"**{rec['title']}**")
                    st.write(f"Author: {rec['author']}")
                    st.write(f"Publisher: {rec['publisher']}")
                    st.write(f"Year: {rec['year']}")
            st.markdown("---")
        else:
            st.error("Book not found in the system. Please try another title.")

# --- Footer ---
st.markdown("""
---
Made with ❤️ by Me | Powered by Collaborative Filtering & Content Popularity Models
""")
