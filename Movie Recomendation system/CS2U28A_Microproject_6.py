import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from PIL import ImageTk, Image
class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation App")
        self.root.geometry("400x600")

        # Connect to SQLite database
        self.conn = sqlite3.connect("movie_database.db")
        self.cursor = self.conn.cursor()

        # Create tables if not exists
        self.create_tables()

        # Create and configure main window
        self.create_main_window()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS watched_movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year INTEGER,
                rating REAL,
                genre TEXT
            )
        ''')
        self.conn.commit()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year INTEGER,
                rating REAL,
                genre TEXT
            )
        ''')
        self.conn.commit()
    

    def create_main_window(self):
        bg = Image.open( "/Users/srayasanjay/Documents/Mini project oop/bgog.png")
        bg=bg.resize((400,600))
        bg=ImageTk.PhotoImage(bg)
        label1 = tk.Label( root, image = bg) 
        label1.place(x = 0,y = 0) 
        # Buttons
        exit_button = tk.Button(self.root, text="Exit",fg="red",font=('Trebuchet',12,'bold'), command=self.on_closing)
        exit_button.pack(padx=5, pady=20,side=tk.BOTTOM)
        
        browse_button = tk.Button(self.root, text="Browse more",fg="red",font=('Trebuchet',12,'bold'), command=self.show_genres)
        browse_button.pack(padx=5, pady=20,side=tk.BOTTOM)
        
        recommendation_button = tk.Button(self.root, text="New Movies for You!",fg="red",font=('Trebuchet',12,'bold'), command=self.create_recommend_window)
        recommendation_button.pack(padx=5, pady=20,side=tk.BOTTOM)
        
        watched_list_button = tk.Button(self.root, text="Your Movies", fg="red",font=('Trebuchet',12,'bold'), command=self.open_watched_list)
        watched_list_button.pack(padx=5, pady=20,side=tk.BOTTOM)
        
        # Ensure the image is not garbage collected
        tk.Canvas.bg = bg
    
    def show_genres(self):
        # Fetch all distinct genres from the "movies" table
        genres = self.cursor.execute("SELECT DISTINCT genre FROM movies").fetchall()
        genres = [genre[0] for genre in genres]

        # Create a new window to display genres
        genres_window = tk.Toplevel(self.root)
        genres_window.geometry("400x600")
        genres_window.title("Browse Genres")
        bg4 = Image.open( "/Users/srayasanjay/Documents/Mini project oop/AlanDavid-Interstellar.png")
        bg4=bg4.resize((400,600))
        bg4=ImageTk.PhotoImage(bg4)
        label4 = tk.Label(genres_window, image = bg4) 
        label4.place(x = 0,y = 0) 

        # Combo box to display genres
        for i in genres:
            bt=tk.Button(genres_window, text=i,command=lambda g=i:self.show_movies_of(g))
            bt.pack(pady=10)
        tk.Canvas.bg4 = bg4
    def show_movies_of(self,genre):
         
        n = tk.Toplevel(self.root)
        n.geometry("400x600")
        n.title(genre)
        bg5 = Image.open( "/Users/srayasanjay/Documents/Mini project oop/bgg.png")
        bg5=bg5.resize((400,600))
        bg5=ImageTk.PhotoImage(bg5)
        label5 = tk.Label(n, image = bg5) 
        label5.place(x = 0,y = 0)
        # Fetch movies with all columns including 'genre'
        genre_movies = self.cursor.execute("""
            SELECT title, year, rating, genre
            FROM movies
            WHERE genre = ?
            AND title NOT IN (SELECT title FROM watched_movies)
            ORDER BY rating DESC
        """, (genre,)).fetchall()

        for idx, movie in enumerate(genre_movies, start=1):
            buttons_frame = tk.Frame(n)
            add_to_watched_button = tk.Button(buttons_frame, text="Add to Watched List", command=lambda m=movie: self.add_to_watched_list(m))
            add_to_wishlist_button = tk.Button(buttons_frame, text="Add to Wishlist", command=lambda m=movie: self.add_to_wishlist(m))

            add_to_watched_button.grid(row=0, column=0, padx=5)
            add_to_wishlist_button.grid(row=0, column=1, padx=5)

            # Display movie information
            movie_info_label = tk.Label(n, text=f"{idx}. {movie[0]} ({movie[1]}) - Rating: {movie[2]} - Genre: {movie[3]}")
            movie_info_label.pack(pady=5)

            # Display buttons frame
            buttons_frame.pack(pady=5)
        
        tk.Canvas.bg5 = bg5
    def on_frame_configure(self, canvas):
        # Update the Canvas scroll region to match the frame
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def create_recommend_window(self):
        
        # Create a new window for recommendations
        recommend_window = tk.Toplevel(self.root)
        recommend_window.geometry("600x400")
        recommend_window.title("Recommend")
        bg1 = Image.open( "/Users/srayasanjay/Documents/Mini project oop/popcorn-film.png")
        bg1=bg1.resize((600,400))
        bg1=ImageTk.PhotoImage(bg1)
        label1 = tk.Label( recommend_window, image = bg1) 
        label1.place(x = 0,y = 0)

        # Fetch the most watched genre from the watched_movies table
        most_watched_genre = self.cursor.execute("""
            SELECT genre, COUNT(*) as count
            FROM watched_movies
            GROUP BY genre
            ORDER BY count DESC
            LIMIT 1
        """).fetchone()

        if most_watched_genre:
            genre_to_recommend = most_watched_genre[0]
        else:
            tk.messagebox.showinfo("No Recommendation", "No movies watched yet to make a recommendation.")
            return
        
        # Fetch top 5 movies of the most watched genre with the highest ratings
        recommended_movies = self.cursor.execute("""
            SELECT title, year, rating, genre
            FROM movies
            WHERE genre = ?
            AND title NOT IN (SELECT title FROM watched_movies)
            ORDER BY rating DESC
            LIMIT 5
        """, (genre_to_recommend,)).fetchall()

        if recommended_movies:
            # Display the recommended movies with buttons in the new window
            for idx, movie in enumerate(recommended_movies, start=1):
                buttons_frame = tk.Frame(recommend_window)
                add_to_watched_button = tk.Button(buttons_frame, text="Add to Watched List", command=lambda m=movie: self.add_to_watched_list(m))
                add_to_wishlist_button = tk.Button(buttons_frame, text="Add to Wishlist", command=lambda m=movie: self.add_to_wishlist(m))

                add_to_watched_button.grid(row=0, column=0, padx=5)
                add_to_wishlist_button.grid(row=0, column=1, padx=5)

                # Display movie information
                movie_info_label = tk.Label(recommend_window, text=f"{idx}. {movie[0]} ({movie[1]}) - Rating: {movie[2]} - Genre: {genre_to_recommend}")
                movie_info_label.pack(pady=5)

                # Display buttons frame
                buttons_frame.pack(pady=5)
        else:
            tk.messagebox.showinfo("No Recommendation", f"No new movies to recommend in {genre_to_recommend}.")
        tk.Canvas.bg1 = bg1
# Existing code...
    def open_watched_list(self):
        
        # Create a new window for the watched list page
        watched_list_window=tk.Toplevel(self.root)
        watched_list_window.geometry("800x600")
        watched_list_window.title("Your Movies")
        bg2 = Image.open( "/Users/srayasanjay/Documents/Mini project oop/Movie Background Presentation.png")
        bg2=bg2.resize((800,600))
        bg2=ImageTk.PhotoImage(bg2)
        label2 = tk.Label( watched_list_window, image = bg2) 
        label2.place(x = 0,y = 0) 
  

        # Watched Movies Treeview
        self.watched_movies_tree = ttk.Treeview(watched_list_window, columns=("No.","Title", "Year", "Rating", "Genre"), show="headings")
        self.watched_movies_tree.heading("No.", text="No.")
        self.watched_movies_tree.heading("Title", text="Title")
        self.watched_movies_tree.heading("Year", text="Year")
        self.watched_movies_tree.heading("Rating", text="Rating")
        self.watched_movies_tree.heading("Genre", text="Genre")
        self.watched_movies_tree.pack(pady=10)
        self.load_watched_movies()
        self.movie_label=tk.Label(watched_list_window,text="Add new movie",bg="white",fg="black",font=('Trebuchet',12,'bold'))
        self.movie_label.pack(pady=10)
        self.movie_entry=tk.Entry(watched_list_window,bg="white",fg="black",font=('Trebuchet',12,'bold'))
        self.movie_entry.pack(pady=10)
        self.movie_entry.bind("<KeyRelease>", self.update_suggestions)
        

         # Dropdown for movie suggestions
        self.suggestion_var = tk.StringVar()
        self.movie_dropdown = ttk.Combobox(watched_list_window, textvariable=self.suggestion_var)
        self.movie_dropdown.pack(pady=10)
        self.movie_dropdown.bind("<<ComboboxSelected>>", self.add_to_watched)

        #clear database
        self.clear_b=tk.Button(watched_list_window,text="Clear your list",font=('Trebuchet',12,'bold'),bg="white",fg="black",command=self.clear_database)
        self.clear_b.pack(pady=10)

        #wishlist
        self.wishlist_head = tk.Label(watched_list_window, text="Your wishlist",font=('Trebuchet',12,'bold'),bg="white",fg="black").pack()
        self.wishlist_tree = ttk.Treeview(watched_list_window, columns=("No.", "Title", "Year", "Rating", "Genre"), show="headings")
        self.wishlist_tree.heading("No.", text="No.")
        self.wishlist_tree.heading("Title", text="Title")
        self.wishlist_tree.heading("Year", text="Year")
        self.wishlist_tree.heading("Rating", text="Rating")
        self.wishlist_tree.heading("Genre", text="Genre")
        self.wishlist_tree.pack(pady=10)

        # Load wishlist data
        self.load_wishlist()
        tk.Canvas.bg2 = bg2
    def update_suggestions(self, event):
        entered_text = self.movie_entry.get().strip()
        if entered_text:
            suggestions = self.cursor.execute("SELECT title FROM movies WHERE title LIKE ?",
                                             (f"%{entered_text}%",)).fetchall()
            self.movie_dropdown["values"] = [movie[0] for movie in suggestions]
        else:
            self.movie_dropdown["values"] = []
    def add_to_watched(self, event):
        selected_movie = self.suggestion_var.get()
        if selected_movie:
            movie_info = self.cursor.execute("SELECT * FROM movies WHERE title=?", (selected_movie,)).fetchone()
            if movie_info:
                # Insert selected movie into watched movies
                self.cursor.execute("INSERT INTO watched_movies (title, year, rating, genre) VALUES (?, ?, ?, ?)",
                                    (movie_info[1], movie_info[2], movie_info[3], movie_info[4]))
                self.conn.commit()

                # Clear entry and update watched movies display
                self.movie_entry.delete(0, tk.END)
                self.suggestion_var.set("")
                self.load_watched_movies()
    def load_watched_movies(self):
        # Clear existing data in the Treeview
        for item in self.watched_movies_tree.get_children():
            self.watched_movies_tree.delete(item)

        # Fetch data from the database and populate the Treeview
        data = self.cursor.execute("SELECT * FROM watched_movies").fetchall()
        for movie in data:
            self.watched_movies_tree.insert("", "end", values=movie)
    def load_wishlist(self):
        # Clear existing data in the Treeview
        for item in self.wishlist_tree.get_children():
            self.wishlist_tree.delete(item)

        # Fetch data from the database and populate the Treeview
        data = self.cursor.execute("SELECT * FROM wishlist").fetchall()
        for movie in data:
            self.wishlist_tree.insert("", "end", values=movie)
    def add_to_watched_list(self, movie):
        title, year, rating, genre = movie
        self.cursor.execute("INSERT INTO watched_movies (title, year, rating, genre) VALUES (?, ?, ?, ?)", (title, year, rating, genre))
        self.conn.commit()
        tk.messagebox.showinfo("Added to Watched List", f"{title} added to Watched List.")

    def add_to_wishlist(self, movie):
        title, year, rating, genre = movie
        self.cursor.execute("INSERT INTO wishlist (title, year, rating, genre) VALUES (?, ?, ?, ?)", (title, year, rating, genre))
        self.conn.commit()
        tk.messagebox.showinfo("Added to Wishlist", f"{title} added to Wishlist.")

    def clear_database(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to clear the database?")
        if confirmation:
            self.cursor.execute("DROP TABLE IF EXISTS watched_movies")
            self.conn.commit()
            # Recreate the watched_movies table
            self.create_tables()
            # Reload data
            self.load_watched_movies()
            self.movie_dropdown["values"] = []

    def on_closing(self):
        # Close the database connection before exiting
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
