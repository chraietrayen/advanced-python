"""
FASTAPI TUTORIAL - Complete Implementation
"""

# ==================== INSTALLATION ====================
# pip install fastapi uvicorn
# Run with: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# ==================== BASIC SETUP ====================
app = FastAPI(
    title="Todo API",
    description="A simple Todo API with FastAPI",
    version="1.0.0"
)

# In-memory database
todos = []

# ==================== MODELS ====================
class TodoItem(BaseModel):
    """Pydantic model for Todo items"""
    text: str  # Required field
    is_done: bool = False  # Optional field with default
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Buy groceries",
                "is_done": False
            }
        }

class TodoItemResponse(TodoItem):
    """Response model with additional fields"""
    id: int

# ==================== ROUTES ====================
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Welcome to the Todo API"}

@app.post("/todos", response_model=TodoItemResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoItem):
    """Create a new todo item"""
    new_todo = {
        "id": len(todos) + 1,
        **todo.dict()
    }
    todos.append(new_todo)
    return new_todo

@app.get("/todos", response_model=List[TodoItemResponse])
async def list_todos(limit: int = 10, offset: int = 0):
    """List todos with pagination"""
    return todos[offset:offset+limit]

@app.get("/todos/{todo_id}", response_model=TodoItemResponse)
async def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    try:
        return next(todo for todo in todos if todo["id"] == todo_id)
    except StopIteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found"
        )

@app.put("/todos/{todo_id}", response_model=TodoItemResponse)
async def update_todo(todo_id: int, updated_todo: TodoItem):
    """Update a todo item"""
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[index] = {**updated_todo.dict(), "id": todo_id}
            return todos[index]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo {todo_id} not found"
    )

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    """Delete a todo item"""
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo["id"] != todo_id]
    if len(todos) == initial_length:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo {todo_id} not found"
        )

# ==================== ERROR HANDLING ====================
@app.get("/error-demo")
async def error_demo():
    """Demo endpoint for error handling"""
    raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        detail="This is a demo error response",
        headers={"X-Error": "Demo error header"}
    )

# ==================== MAIN ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    