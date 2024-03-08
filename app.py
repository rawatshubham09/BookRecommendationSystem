from flask import Flask,render_template, request
import numpy as np
import pickle
import logging
from datetime import date
import os

# directory names
base_dir = os.getcwd()
log_dir = os.path.join(base_dir,"log")
log_file_name = os.path.join(log_dir, "logfile" + str(date.today()) + ".log")
pickle_dir = os.path.join(base_dir,"pickle")

#logging Configuration
logging.basicConfig(filename=log_file_name,
                    format="%(asctime)s --> %(levelname)s :: %(message)s",
                    filemode='w')
logger = logging.getLogger()

# Unloading Pickle
popular_df = pickle.load(open(os.path.join(pickle_dir,"popular.pkl"),"rb"))
pt = pickle.load(open(os.path.join(pickle_dir,"pt.pkl"),"rb"))
similarity_score = pickle.load(open(os.path.join(pickle_dir,"similarity_score.pkl"),"rb"))
final_data = pickle.load(open(os.path.join(pickle_dir,"final_data.pkl"),"rb"))

app = Flask(__name__)

@app.route('/')
def index():
    """ This function will display top 50 most rated book in home screen """
    logger.info("Home page is called.")
    return render_template("main.html",
                        book_name=list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        image=list(popular_df['Image-URL-M'].values),
                        votes=list(popular_df['Num-Rating'].values),
                        rating=list(popular_df['Avg-Rating'].values)) 


@app.route('/recommend')
def recommend_ui():
    """ This Function will render recommend.html remplet """
    logger.info("Recommend page is called")
    return render_template("recommend.html")

@app.route("/recommend_book", methods=["POST"])
def recommend():
    """ This Function find most related book and display top 8 matching book using cosine similarities,
        I also include Error handling."""
    try : 
        logger.info("recmmend book rout called and data is submitted")
        user_data = request.form.get("user_input")
        logger.info("name of book : '{user_data}'")
        index = np.where(pt.index==user_data)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])),key= lambda x:x[1], reverse=True)[1:9]
        data = []
        for i in similar_items:
            item = []
            temp_df = final_data[final_data["Book-Title"] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
            
            data.append(item)

        logger.info("data is predicted and displayed")
        return render_template('recommend.html', data=data)
    except:
        logger.error("Name do not match with data base!!")
        return render_template("recommend2.html")

if __name__ == '__main__':
    app.run(debug=True)