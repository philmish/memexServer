from fastapi.testclient import TestClient
import pytest
from memexIndexer.api.routers.bookmarks.schemas import BookmarkBase
from memexIndexer.api.routers.books.schemas import BookBase
from memexIndexer.api.routers.emails.schemas import Email
from memexIndexer.api.routers.movies.schemas import MovieBase
from memexIndexer.api.routers.notes.schemas import NoteBase
from memexIndexer.api.schemas import ItemQuery
from memexIndexer.api.server import app


client = TestClient(app)


@pytest.mark.parametrize("endpoint", [
    ("/bookmarks/ping"),
    ("/books/ping"),
    ("/notes/ping"),
    ("/email/ping"),
    ])
def test_router_ping(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", [
    "/bookmarks/all",
    "/books/all",
    "/notes/all",
    "/email/all"
])
def test_get_all(endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint, data, item, update", [
    (
        "/bookmarks/",
        {
            "link": "https://testing.test",
            "topic": "testing",
            "notes":"This is an entry written by pytest",
        },
        BookmarkBase,
        {"notes": "Updated by pytest"}
    ),
    (
        "/books/",
        {
            "title": "Die Zauberer",
            "author": "Michael Peinkofer",
            "isbn": "978-3-492-26732-8",
            "pages": 580,
            "tags": ["api testing"]
        },
        BookBase,
        {"pages": 581}
    ),
    (
        "/email/",
        {
            "sender": "tester@testing.com",
            "subject": "Testing",
            "content": "Hello, we are still testing",
            "recieved_at": "17.09.2021 12:45"
        },
        Email,
        {"subject": "Tested"}
    ),
    (
        "/movies/",
        {
            "title": "Ran",
            "released": "1985",
            "status": "Owned",
            "runtime": 162
        },
        MovieBase,
        {"original_language": "Japanese"}
    ),
    (
        "/notes/",
        {
            "text": "This is a test note",
            "tags": ["api testing"]
        },
        NoteBase,
        {"text": "Updated by pytest"}
    )
])
def test_crud(endpoint, data, item, update):
    item_data = item(**data)
    response = client.post(
        f"{endpoint}create",
        data=item_data.json()
        )
    resp_data = response.json()
    assert response.status_code == 200
    
    for key, val in data.items():
        assert resp_data[key] == val

    query = ItemQuery(
        item_type=item_data.item_type,
        query=data
        )
    inserted = client.post(
        f"{endpoint}query",
        data=query.json()
        )
    assert inserted.status_code == 200

    id_req = client.post(
        f"{endpoint}get/id",
        data=query.json()
        )
    assert id_req.status_code == 200
    
    _id = id_req.json()["id"]
    update_query = ItemQuery(
        item_type=item_data.item_type,
        query=update
        )
    updated = client.post(
        f"{endpoint}update/{_id}",
        data=update_query.json()
        )
    assert updated.status_code == 200

    updated_data = updated.json()
    for key, val in update.items():
        assert updated_data[key] == val
    
    deleted = client.post(f"{endpoint}delete/{_id}")
    assert deleted.status_code == 200

    not_found = client.post(
        f"{endpoint}query",
        data=query.json()
        )
    assert not_found.status_code == 404









