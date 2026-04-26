# Movie_Recommendation
🎬 Movie Recommendation System
📌 Overview

This project is a content-based movie recommender that suggests similar movies based on features like 🎭 genres, 🧩 keywords, 👨‍🎤 cast, and 🎬 crew.
Instead of user data, it focuses on movie content similarity.

⚙️ How It Works

👉 If two movies have similar content → they get recommended together

✔️ Combines important features into a single text
✔️ Converts text into numerical vectors
✔️ Computes similarity between movies
✔️ Recommends top similar results

🧠 ML Pipeline
🔹 1. Data Preprocessing
Selected relevant columns (genres, keywords, cast, crew)
Cleaned & formatted data
Extracted director & top cast
Removed spaces for consistency
🔹 2. Feature Engineering
Combined all features into a single column: tags 🏷️
Created a textual representation of each movie
🔹 3. Text Vectorization
Used CountVectorizer 🔢
Converted text → numerical vectors
Removed stopwords
🔹 4. Stemming
Applied Porter Stemmer 🌱
Reduced words to root form (better matching)
🔹 5. Similarity Calculation
Used Cosine Similarity 📐

cos(θ)=
∥A∥∥B∥
A⋅B
	​


Measures how similar two movies are
Higher value = more similar
🔹 6. Recommendation
Input 🎥 movie name
Find similar movies
Return top 5 recommendations ⭐
🛠️ Tech Stack

🐍 Python | 📊 Pandas | 🔢 NumPy | 🤖 Scikit-learn | 🌱 NLTK

🚀 Key Learnings

✨ Feature engineering is crucial
✨ NLP helps in handling text data
✨ Cosine similarity is powerful for recommendations
✨ Built an end-to-end ML pipeline

🔗 Example
recommend("Avatar")

