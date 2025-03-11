from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017" 
client = AsyncIOMotorClient(MONGO_URI)
db = client.library  # Database: "library"
books_collection = db.Books  # Collection: "Books"
students_collection = db.Students  # Collection: "Students"

# Get all books
@app.get("/books/")
async def get_books():
    books = await books_collection.find().to_list(100)
    return books

# Get all students
@app.get("/students/")
async def get_students():
    students = await students_collection.find().to_list(100)  # Increase limit if needed
    for student in students:
        student["_id"] = str(student["_id"])  # Convert ObjectId to string
    return students

# Issue a book to a student
@app.post("/books/issue/{serial_number}/{student_id}")
async def issue_book(serial_number: int, student_id: int):
    book = await books_collection.find_one({"_id": serial_number})
    student = await students_collection.find_one({"student_id": student_id})

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not book["is_available"]:
        raise HTTPException(
            status_code=400,
            detail=f"Book is already issued to Student ID {book['issued_to']}"
        )

    await books_collection.update_one(
        {"_id": serial_number},
        {"$set": {"is_available": False, "issued_to": student_id}}
    )

    return {"message": f"Book '{book['title']}' issued to Student ID {student_id}"}

# Return a book
@app.post("/books/return/{serial_number}")
async def return_book(serial_number: int):
    book = await books_collection.find_one({"_id": serial_number})

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book["is_available"]:
        raise HTTPException(status_code=400, detail="Book is already available")

    await books_collection.update_one(
        {"_id": serial_number},
        {"$set": {"is_available": True, "issued_to": None}}
    )

    return {"message": f"Book '{book['title']}' returned successfully"}
