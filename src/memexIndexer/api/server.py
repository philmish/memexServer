from fastapi import FastAPI

from memexIndexer.api.routers.bookmarks.router import router as bookmarks
from memexIndexer.api.routers.books.router import router as books
from memexIndexer.api.routers.contacts.router import router as contacts
from memexIndexer.api.routers.emails.router import router as email
from memexIndexer.api.routers.movies.router import router as movies
from memexIndexer.api.routers.notes.router import router as notes
from memexIndexer.api.routers.scraped_data.router import router as scraped_data
from memexIndexer.api.routers.time_capsules.router import router as time_capsule
from memexIndexer.api.routers.todo.router import router as todo


app = FastAPI()

app.include_router(bookmarks)
app.include_router(books)
app.include_router(contacts)
app.include_router(email)
app.include_router(movies)
app.include_router(notes)
app.include_router(time_capsule)
app.include_router(todo)
app.include_router(scraped_data)

