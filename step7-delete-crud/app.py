from flask import Flask, request, render_template, redirect, url_for
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Web App Configuration
app = Flask(__name__)

# Database Connection Configuration
def get_db_connection():
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=5432,
            database=os.getenv("DB_NAME")
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies;")
            movies = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template("home.html", movie_list=movies)
    except Exception as e:
        print(f"Error fetching movies: {e}")
    return render_template("home.html", movie_list=[])

@app.route('/movies/add')
def add_movie():
    return render_template("editmovie.html", movie=None)

@app.route('/movies/edit/<int:movie_id>')
def edit_movie(movie_id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies WHERE id = %s;", (movie_id,))
            movie = cursor.fetchone()
            cursor.close()
            conn.close()
            return render_template("editmovie.html", movie=movie)
    except Exception as e:
        print(f"Error editing movie: {e}")
    return redirect(url_for('home'))

@app.route('/movies/persist', methods=['POST'])
def persist_movie():
    movie_id = request.form.get('id', 0)
    movie_id = int(movie_id) if movie_id and movie_id.isdigit() else 0
    title = request.form['title']
    year = request.form['year']
    director = request.form['director']

    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            if movie_id == 0:
                cursor.execute("INSERT INTO movies (title, director, year) VALUES (%s, %s, %s);", 
                               (title, director, year))
            else:
                cursor.execute("UPDATE movies SET title = %s, director = %s, year = %s WHERE id = %s;", 
                               (title, director, year, movie_id))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error persisting movie: {e}")

    return redirect(url_for('home'))

@app.route('/movie/delete/<int:movie_id>')
def delete_movie(movie_id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM movies WHERE id = %s;", (movie_id,))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error deleting movie: {e}")

    return redirect(url_for('home'))

# Azure Web App requires a specific port
port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)