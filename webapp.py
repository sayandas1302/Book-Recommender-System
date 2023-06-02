from flask import Flask, render_template, request
import pandas as pd
import pickle

# calling the import datasets and lists 
popularBooks = pd.read_csv('./Datasets/popularBooks.csv')
sim_matrix = pd.read_csv('./Datasets/sim_matrix.csv')
booksDf = pd.read_csv('./Datasets/preProcessedBooksDf.csv')

with open('./pickleFiles/freqBooks.pkl', 'rb') as file:
    freqBooks = pickle.load(file)

# function for the recommendation
def recommend(title, n):
    '''function that recommends n books similar to the book given'''
    # id of the books in the list 
    id_in_the_list = freqBooks.index(title)
    
    # id of the books similar tp the given book
    id_of_the_similar_books = sim_matrix.loc[id_in_the_list,].sort_values(ascending=False)[1:(n+1)].index
    
    # list of recommended books
    recommended_books = [freqBooks[int(x)] for x in id_of_the_similar_books]

    # informations about the books
    info = booksDf.loc[booksDf["Book-Title"].isin(recommended_books),]

    return info

# the flask app functionality 
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    suggestions = None
    bookTitle = "Choose one Book You've read"
    if request.method == 'POST':
        try: 
            bookTitle = request.form.get('bookName')
            suggestions = recommend(bookTitle, 10)
        except ValueError:
            bookTitle = "Choose one Book You've read"

    return render_template('template.html', 
                           popbook = popularBooks,
                           freqBooks = freqBooks,
                           sugg=suggestions,
                           choice=bookTitle)

if __name__ == '__main__':
    app.run(debug=True)