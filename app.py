from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
book = pickle.load(open('book.pkl','rb'))
pivot = pickle.load(open('pivot.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           Author = list(popular_df['Book-Author'].values),
                           Img = list(popular_df['Image-URL-M'].values),
                           Votes = list(popular_df['num_rating'].values),
                           Ratings = list(popular_df['avg_rating'].values))


@app.route('/recommend')
def recommend():
    return render_template('recommender.html')


@app.route('/recommend_books',methods = ['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    try:
        index = np.where(pivot.index==user_input)[0][0]
        similar_item =sorted(list(enumerate(similarity_score[index])),key =lambda x:x[1],reverse = True)[1:6]
        data = []
        for i in similar_item:
            item = []
           #print(pivot.index[i[0]])
            temp_df =book[book['Book-Title']==pivot.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
            data.append(item)
        print(data)
        
    except:
        print(f'There is no such book name :{user_input} ')

    return render_template('/recommender.html',data = data)
if __name__ == '__main__':
    app.run(debug=True)