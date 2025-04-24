"""
PYTHON WEB DEVELOPMENT MEGADEMO
Combining Pydantic, Requests, FastAPI, and Streamlit
"""

# ==================== IMPORTS ====================
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
import requests
import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Optional
import uvicorn

# ==================== PYDANTIC MODELS ====================
class User(BaseModel):
    """Pydantic model for user data validation"""
    name: str
    email: str
    age: int
    
    @field_validator('age')
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be ≥ 18")
        return value

class TodoItem(BaseModel):
    """Model for FastAPI todo items"""
    text: str
    is_done: bool = False

# ==================== FASTAPI SETUP ====================
app = FastAPI(title="MegaDemo API")
todos = []

@app.post("/todos", response_model=TodoItem)
async def create_todo(item: TodoItem):
    """Create new todo item"""
    todos.append(item)
    return item

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    """Get all todos"""
    return todos

# ==================== STREAMLIT APP ====================
def streamlit_app():
    """Streamlit frontend for the demo"""
    st.title("Python Web Dev MegaDemo")
    st.write("This app combines Pydantic, Requests, FastAPI and Streamlit")
    
    tab1, tab2, tab3 = st.tabs(["Pydantic", "Requests", "FastAPI"])
    
    with tab1:
        st.header("Pydantic Demo")
        name = st.text_input("Name")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=0)
        
        if st.button("Validate"):
            try:
                user = User(name=name, email=email, age=age)
                st.success(f"Valid user: {user}")
            except ValueError as e:
                st.error(f"Validation error: {e}")
    
    with tab2:
        st.header("Requests Demo")
        url = st.text_input("Enter API URL", "https://jsonplaceholder.typicode.com/todos/1")
        
        if st.button("Fetch Data"):
            try:
                response = requests.get(url, timeout=5)
                st.json(response.json())
            except Exception as e:
                st.error(f"Request failed: {e}")
    
    with tab3:
        st.header("FastAPI Integration")
        todo_text = st.text_input("New Todo")
        
        if st.button("Add Todo"):
            try:
                response = requests.post(
                    "http://localhost:8000/todos",
                    json={"text": todo_text, "is_done": False}
                )
                st.success("Todo added!")
            except Exception as e:
                st.error(f"API Error: {e}")
        
        if st.button("Show Todos"):
            try:
                todos = requests.get("http://localhost:8000/todos").json()
                st.table(pd.DataFrame(todos))
            except Exception as e:
                st.error(f"Fetch Error: {e}")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    import threading
    
    # Start FastAPI server in a separate thread
    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8000)
    
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Run Streamlit app
    streamlit_app()