from flask import Flask,render_template, request
import pandas as pd
import numpy as np
import pickle

popular_df = pickle.load(open("popular.pkl","rb"))
pt = pickle.load(open("pt.pkl","rb"))
similarity_score = pickle.load(open("similarity_score.pkl","rb"))
final_data = pickle.load(open("final_data.pkl","rb"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html",
                        book_name=list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        image=list(popular_df['Image-URL-M'].values),
                        votes=list(popular_df['Num-Rating'].values),
                        rating=list(popular_df['Avg-Rating'].values)) 

@app.route('/recommend')
def recommend_ui():

    book_name = ""
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])),key= lambda x:x[1], reverse=True)[1:9]
    data = []
    for i in similar_items:
        item = []
        temp_df = final_data[final_data["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
        data.append(item)
        
    return render_template("recommend.html" , data = data)

@app.route("/recommend_book", methods=["POST"])
def recommend():
    user_data = request.form.get("user_input")
    return str(user_data)

if __name__ == '__main__':
    app.run(debug=True)