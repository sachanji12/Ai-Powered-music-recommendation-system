import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pygame

# Initialize pygame for playing music
pygame.mixer.init()

# Sample dataset: Song features (In practice, this should be more extensive)
data = {
    'Song': ['Song1', 'Song2', 'Song3', 'Song4', 'Song5','Song6', 'Song7', 'Song8', 'Song9', 'Song10', 'Song11'],
    'Genre': ['Pop', 'Rock', 'Pop', 'Jazz', 'Rock','Pop', 'Rock', 'Pop', 'Jazz', 'Rock','Jazz'],
    'Tempo': [120, 140, 128, 100, 135 ,125 ,122 ,126 ,120 ,138 ,133],  # Example feature: tempo
    'Energy': [0.8, 0.6, 0.75, 0.5, 0.7 , 0.9 ,1 , 0.87, 0.82, 0.92,0.78],  # Example feature: energy
}

# Create DataFrame
df = pd.DataFrame(data)

# Create a simple content-based recommendation engine using song features
def recommend_songs(genre, tempo, energy):
    # Use the NearestNeighbors algorithm to recommend songs based on features
    features = df[['Tempo', 'Energy']]
    model = NearestNeighbors(n_neighbors=4)  # Find 3 similar songs
    model.fit(features)
    
    # Query song features from user input
    query = np.array([[tempo, energy]])
    
    # Find nearest songs
    distances, indices = model.kneighbors(query)
    
    recommended_songs = df.iloc[indices[0]]['Song'].tolist()
    return recommended_songs

# Play a song (this assumes you have MP3 files named 'Song1.mp3', etc.)
def play_song(song_name):
    try:
        pygame.mixer.music.load(f'{song_name}.mp3')  # Make sure to have the song files
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"Could not play {song_name}: {str(e)}")

# Pause the song
def pause_song():
    pygame.mixer.music.pause()

# Unpause the song (resume)
def unpause_song():
    pygame.mixer.music.unpause()

# Stop the song
def stop_song():
    pygame.mixer.music.stop()

# GUI setup
class MusicRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Music Recommendation System")
        
        # Genre input
        self.genre_label = tk.Label(root, text="Enter Genre (e.g., Pop, Rock, Jazz):")
        self.genre_label.pack(pady=5)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.pack(pady=5)
        
        # Tempo input
        self.tempo_label = tk.Label(root, text="Enter Tempo (BPM):")
        self.tempo_label.pack(pady=5)
        self.tempo_entry = tk.Entry(root)
        self.tempo_entry.pack(pady=5)
        
        # Energy input
        self.energy_label = tk.Label(root, text="Enter Energy (0 to 1):")
        self.energy_label.pack(pady=5)
        self.energy_entry = tk.Entry(root)
        self.energy_entry.pack(pady=5)
        
        # Recommendation Button
        self.recommend_button = tk.Button(root, text="Get Recommendations", command=self.get_recommendations)
        self.recommend_button.pack(pady=10)
        
        # Play Button
        self.play_button = tk.Button(root, text="Play", command=self.play_current_song, state=tk.DISABLED)
        self.play_button.pack(pady=5)
        
        # Pause Button
        self.pause_button = tk.Button(root, text="Pause", command=pause_song, state=tk.DISABLED)
        self.pause_button.pack(pady=5)
        
        # Resume Button
        self.resume_button = tk.Button(root, text="Resume", command=unpause_song, state=tk.DISABLED)
        self.resume_button.pack(pady=5)
        
        # Next Button
        self.next_button = tk.Button(root, text="Next", command=self.play_next_song, state=tk.DISABLED)
        self.next_button.pack(pady=5)
        
        # Recommendations display
        self.recommendations_label = tk.Label(root, text="Recommended Songs will appear here.")
        self.recommendations_label.pack(pady=10)

        # Variable to hold the current song and index
        self.current_song = None
        self.recommended_songs = []
        self.current_song_index = 0

    def get_recommendations(self):
        try:
            genre = self.genre_entry.get()
            tempo = float(self.tempo_entry.get())
            energy = float(self.energy_entry.get())
            
            # Get recommendations
            self.recommended_songs = recommend_songs(genre, tempo, energy)
            
            # Display recommendations
            recommendations_text = "\n".join(self.recommended_songs)
            self.recommendations_label.config(text=f"Recommended Songs:\n{recommendations_text}")
            
            # Enable play button and store the first song in the list
            if self.recommended_songs:
                self.current_song = self.recommended_songs[0]
                self.play_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.NORMAL)
                self.resume_button.config(state=tk.NORMAL)
                self.next_button.config(state=tk.NORMAL)
                self.current_song_index = 0
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for Tempo and Energy.")
    
    def play_current_song(self):
        if self.current_song:
            play_song(self.current_song)
    
    def play_next_song(self):
        if self.current_song_index + 1 < len(self.recommended_songs):
            # Stop current song and play the next one
            stop_song()
            self.current_song_index += 1
            self.current_song = self.recommended_songs[self.current_song_index]
            play_song(self.current_song)
        else:
            messagebox.showinfo("End of Recommendations", "No more songs to play.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicRecommenderApp(root)
    root.mainloop()
