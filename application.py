import os
import requests
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def sessionChecker():
    if 'login' in session:
        if session['login']:
            return True
    else:
        return False

def sessionBuilder(obj):
    session["userId"] = obj.id
    session["login"] = True

def apiCallReview(isbn):
    apiKey = "kPEhl0IRirjYbIIJrViYg"
    print(isbn)
    apiRes = requests.get("https://www.goodreads.com/book/review_counts.json", params={"Key":apiKey,"isbns":isbn})
    print (apiRes)
    if apiRes.status_code != 200:
        raise Exception("Error! API call unsuccessful")
    else: 
        return apiRes.json()
def maxPageVal(key=""):
    max_page = 0
    if key != "":
            counts = db.execute("SELECT count(*) as count_books from books WHERE title LIKE :key OR isbn LIKE :key OR authorname LIKE :key" , {"key":'%'+key+'%'})
            count = list(counts)[0][0]
            print(count)
            max_page = count // 10
            print(max_page)
    else:
        counts = db.execute("SELECT count(*) as count_books from books ")
        count = list(counts)[0][0]
        print(count)
        max_page = count // 10
        print(max_page)
    return max_page

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
apiKey = "kPEhl0IRirjYbIIJrViYg"
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        row = db.execute("SELECT * from users WHERE email = :email AND password = :password",{'email':email, 'password':password}).fetchone()
        if row != None:
            sessionBuilder(obj=row)
            return redirect(url_for('mhp'))
        else:
            return render_template("signin.html",message="Invalid email or password")

    if request.method == "GET":
        return render_template("signin.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        middleName = request.form.get("middleName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("pswd")
        res = db.execute("INSERT INTO users (firstname,middlename,lastname,email,password) VALUES (:firstName,:middleName,:lastName,:email,:password)", {'firstName':firstName,'middleName':middleName,'lastName':lastName,'email':email,'password':password} )
        print(type(res))
        print(f"res = {res}")
        db.commit()
        return render_template('signin.html',message="Account created! Please login to continue")

    if request.method == "GET":
        return render_template("signup.html")

@app.route("/mhp", methods=["GET", "POST"])
def mhp():
    chk = sessionChecker()
    if chk:
        if request.method == "POST":
            key = request.form.get('bookSearch')
            res = db.execute("SELECT title, isbn, authorname, year from books WHERE title LIKE :key OR isbn LIKE :key OR authorname LIKE :key LIMIT 5" , {"key":'%'+key+'%'}).fetchall()
            if res != []:
                return render_template("myMhp.html",results=res,userResponse=key)
            else:
                return render_template("myMHP.html",noresult="No books found Please check title, author name or check ISBN number and Try Again!")
        if request.method == "GET":
            return render_template("myMhp.html")
    else:
        return redirect(url_for('logout'))

@app.route("/books", methods=["GET","POST"])
@app.route("/books/<string:key>/<int:page>", methods=["GET","POST"])
@app.route("/books/<int:page>", methods=["GET","POST"])
def books(page=1,key=""):
    chk = sessionChecker()
    if chk:
        if page == 1:
            limitCount  = 10
            limitOffset = 0
        else: 
            limitCount  = 10
            limitOffset = (page-1) * 10
        if request.method == "POST":
            key = request.form.get("bookSearch")
            res = db.execute("SELECT title, isbn, authorname, year from books WHERE title LIKE :key OR isbn LIKE :key OR authorname LIKE :key LIMIT :limitCount OFFSET :limitOffset" , {"key":'%'+key+'%','limitOffset':limitOffset, 'limitCount':limitCount}).fetchall()
            
            if res != []:
                averageRating = []
                ratingsCount = []
                isbn = ""
                for row in res:
                    isbn += row.isbn + ','
                ratings = apiCallReview(isbn)
                for i in range(len(ratings["books"])):  
                    avgRate = float(ratings["books"][i]["average_rating"])
                    ratecnt = int(ratings["books"][i]["work_ratings_count"])
                    averageRating.append(avgRate)
                    ratingsCount.append(ratecnt)
                results = zip(res,averageRating,ratingsCount)
                return render_template("books.html", results=results, userResponse=key, page=page, max_page = maxPageVal(key))
            else:
                return render_template("books.html",noresult="No books found Please check title, author name or check ISBN number and Try Again!")
        else:
            if key == "":
                res = db.execute("SELECT title, isbn, authorname, year from books LIMIT :limitCount OFFSET :limitOffset",{'limitOffset':limitOffset, 'limitCount':limitCount}).fetchall()
                max_page = maxPageVal()
            else: 
                res = db.execute("SELECT title, isbn, authorname, year from books WHERE title LIKE :key OR isbn LIKE :key OR authorname LIKE :key LIMIT :limitCount OFFSET :limitOffset" , {"key":'%'+key+'%','limitOffset':limitOffset, 'limitCount':limitCount}).fetchall()
                max_page = maxPageVal(key)
            if res != []:
                averageRating = []
                ratingsCount = []
                isbn = ""
                for row in res:
                    isbn += row.isbn + ','
                ratings = apiCallReview(isbn)
                for i in range(len(ratings["books"])):  
                    avgRate = float(ratings["books"][i]["average_rating"])
                    ratecnt = int(ratings["books"][i]["work_ratings_count"])
                    averageRating.append(avgRate)
                    ratingsCount.append(ratecnt)
                    
                results = zip(res,averageRating,ratingsCount)
                
                return render_template("books.html", results=results, userResponse=key, page=page, max_page=max_page)
            else:
                return render_template("books.html",noresult="No books found Please check title, author name or check ISBN number and Try Again!")
    else:
        return redirect(url_for('logout'))

@app.route("/myReview")
def review():
    chk = sessionChecker()
    if chk:
        res = db.execute("SELECT bk.title, bk.isbn, bk.authorname, bk.year, ur.ratings, ur.review FROM books bk LEFT JOIN userreview ur ON bk.id = ur.book_id WHERE ur.user_id = :userId",{'userId':session["userId"]}).fetchall()
        if res != []:        
            return render_template("review.html", results=res)
        else:
            return render_template("review.html", noresult="No reviewed books please give review")
    else:
        return redirect(url_for('logout'))

@app.route("/bookdetail/<string:isbn>", methods=["GET","POST"])
def bookDetail(isbn):
    chk = sessionChecker()
    if chk:
        res = db.execute("SELECT id, title, description, isbn, authorname, year from books WHERE isbn = :isbn",{'isbn':isbn}).fetchone()
        if res is not None:
            ratings       = apiCallReview(isbn)
            averageRating = float(ratings["books"][0]["average_rating"])
            ratingCount   = int(ratings["books"][0]["work_ratings_count"])
            if request.method == "POST":
                comment = request.form.get("comment")
                print(request.form.get("rating"))
                rating = int(request.form.get("rating"))
                print(f"userId={session['userId']}")
                db.execute("INSERT INTO userreview(user_id, book_id, ratings, review)VALUES(:userId, :bookId, :rating, :comment)",{'userId':session["userId"],'bookId':res.id,'rating':rating,'comment':comment})
                db.commit()
                row = db.execute("SELECT bk.title, bk.description, bk.isbn, bk.authorname, bk.year, ur.ratings, ur.review FROM books bk LEFT JOIN userreview ur ON bk.id = ur.book_id WHERE bk.isbn = :isbn AND ur.user_id = :userId",{'isbn':isbn,'userId':session["userId"]}).fetchone()
                print(row)
                return render_template("bookDetail.html", result = row, rating=averageRating, ratingCount=ratingCount)

            else:
                row = db.execute("SELECT bk.title, bk.description, bk.isbn, bk.authorname, bk.year, ur.ratings, ur.review FROM books bk LEFT JOIN userreview ur ON bk.id = ur.book_id WHERE bk.isbn = :isbn AND ur.user_id = :userId",{'isbn':isbn,'userId':session["userId"]}).fetchone()
                print(row)
                if row is not None:
                    return render_template("bookDetail.html", result = row, rating=averageRating, ratingCount=ratingCount)
                else:
                    return render_template("bookDetail.html", result = res, rating=averageRating, ratingCount=ratingCount)
        else:
            return render_template("error.html", noresult="Error! records not found")
    else:
        return redirect(url_for("logout"))

@app.route("/logout")
def logout():
    session.clear()
    return render_template('signin.html',message="Please Login to Continue")


@app.route("/api/<string:isbn>")
def api(isbn):
    res = db.execute("SELECT id, title, isbn, authorname, year from books WHERE isbn = :isbn",{'isbn':isbn}).fetchone()
    if res is None:
        return jsonify({"error": "book is not available in our database"}), 404
    else:
        rate = db.execute("SELECT COUNT(ratings) as ratingcount, COUNT(review) as review, SUM(ratings) as sumrating FROM userreview WHERE book_id = :bookId",{'bookId':res.id}).fetchone()
        if rate.sumrating is not None and rate.ratingcount != 0:
            avgRate = rate.sumrating/rate.ratingcount
            averageRating = round(avgRate,2)
            ratingCount = rate.ratingcount
            reviewCount = rate.review
        else:
            averageRating = 0
            ratingCount   = 0
            reviewCount   = 0
        # print(f"ratingCount={type(rate.ratingcount)} sumRating={type(rate.sumrating)}")
        # print(f"ratingCount={rate.ratingcount} sumRating={rate.sumrating}")
        return jsonify({
            "title"        : res.title,
            "isbn"         : res.isbn,
            "author"       : res.authorname,
            "year"         : str(res.year),
            "review_count" : str(reviewCount),
            "rating_count" : str(ratingCount),
            "average_score": str(averageRating)
        }) 

