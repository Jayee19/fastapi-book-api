# First, import the required libraries
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Define the data model for a Book using Pydantic
class Book(BaseModel):
    title: str
    author: str
    pages: int
    is_available: bool = True
    description: Optional[str] = None

# Create a list to store our books (in a real app, this would be a database)
books_db = []

# Define lifespan context manager (replaces @app.on_event("startup"))
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Add sample data when the app starts
    sample_books = [
        Book(
            title="The FastAPI Handbook",
            author="Jane Developer",
            pages=250,
            description="A comprehensive guide to FastAPI"
        ),
        Book(
            title="Python Mastery",
            author="John Coder",
            pages=400,
            description="Advanced Python programming techniques"
        )
    ]
    books_db.extend(sample_books)
    yield
    # Clean up any resources when the app shuts down
    books_db.clear()

# Create a FastAPI instance with lifespan handler
app = FastAPI(
    title="Book Library API",
    description="A simple API for managing books in a library",
    version="1.0.0",
    lifespan=lifespan
)

# --- API Routes ---

@app.get("/books", response_model=List[Book], tags=["Books"])
async def get_all_books():
    """
    Get all books in the library.
    Returns a list of all books.
    """
    return books_db

@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: int):
    """
    Get a specific book by its ID.
    Returns the book if found, raises 404 if not found.
    """
    if 0 <= book_id < len(books_db):
        return books_db[book_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
async def create_book(book: Book):
    """
    Add a new book to the library.
    Takes a Book object and adds it to the database.
    Returns the created book.
    """
    books_db.append(book)
    return book

@app.put("/books/{book_id}", response_model=Book, tags=["Books"])
async def update_book(book_id: int, updated_book: Book):
    """
    Update a book's information.
    Takes a book ID and updated Book object.
    Returns the updated book if successful, raises 404 if book not found.
    """
    if 0 <= book_id < len(books_db):
        books_db[book_id] = updated_book
        return updated_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
async def delete_book(book_id: int):
    """
    Delete a book from the library.
    Takes a book ID and removes it from the database.
    Returns nothing if successful, raises 404 if book not found.
    """
    if 0 <= book_id < len(books_db):
        books_db.pop(book_id)
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )

# Run the application
if __name__ == "__main__":
    uvicorn.run("fast_api_check:app", host="0.0.0.0", port=8000, reload=True)