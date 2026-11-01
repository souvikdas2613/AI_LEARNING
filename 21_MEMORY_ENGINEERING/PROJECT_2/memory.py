import json
import os
import sqlite3

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DATABASE = "memory.db"

embedding_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            assistant_message TEXT,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

    print("\nFunction create_database() - Database created successfully")


def clear_memories():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM memories")
    connection.commit()
    connection.close()

    print("\nFunction clear_memories() - Memories cleared successfully")


def create_embedding(text):
    response = embedding_client.embeddings.create(model="text-embedding-3-small", input=text)
    print("\nFunction create_embedding() - Embedding created successfully")
    return response.data[0].embedding


def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    print("\nFunction cosine_similarity() - Cosine similarity calculated successfully")
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def save_memory(user_message, assistant_message):
    text = user_message + "\n" + assistant_message
    embedding = create_embedding(text)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO memories (user_message, assistant_message, embedding)
        VALUES (?, ?, ?)
        """,
        (user_message, assistant_message, json.dumps(embedding)),
    )
    connection.commit()
    connection.close()

    print("\nFunction save_memory() - Memory saved successfully")


def list_memories():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, user_message, assistant_message, created_at
        FROM memories
        ORDER BY id
    """)
    rows = cursor.fetchall()
    connection.close()
    print("\nFunction list_memories() - Memories listed successfully")
    return [
        {"id": row[0], "user_message": row[1], "assistant_message": row[2], "created_at": row[3]}
        for row in rows
    ]


def search_semantic_memories(query, max_results=3, min_score=0.20):
    query_embedding = create_embedding(query)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT user_message, assistant_message, embedding, created_at
        FROM memories
    """)
    rows = cursor.fetchall()
    connection.close()
    results = []
    print("\nFunction search_semantic_memories() - Searching semantic memories...")
    print("Query:", query)
    print("Max results:", max_results)
    print("Min score:", min_score)

    for user_message, assistant_message, embedding_json, created_at in rows:
        memory_embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, memory_embedding)

        print("\nfor user message: ", user_message + " and query: ", query)
        print("score: ", score)
        if score >= min_score:
            results.append({
                "user_message": user_message,
                "assistant_message": assistant_message,
                "created_at": created_at,
                "score": score,
            })
    results.sort(key=lambda item: item["score"], reverse=True)
    print("\nFunction search_semantic_memories() - Semantic memories searched successfully")

    print("\nFunction search_semantic_memories() - Results:")
    print(results)
    return results[:max_results]
