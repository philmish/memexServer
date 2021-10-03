from typing import Any, Union
from fastapi.exceptions import HTTPException
from memexIndexer.utils.enums import ClientResponse
from memexIndexer.api.schemas import HTTPResponse


def parse_client_response(response: ClientResponse, data: Any = None, error: Union[str, None] = None) -> HTTPResponse:
    if response is ClientResponse.SUCCESS:
        return HTTPResponse(
            data=data,
            status=200,
        )
    elif response is ClientResponse.CREATED:
        return HTTPResponse(
            data=data,
            status=201
        )
    elif response is ClientResponse.EXISTS:
        return HTTPResponse(
            data=data,
            status=409,
            erro="The item you want to create already lives under the attached ID"
        )
    elif response is ClientResponse.INVALID:
        return HTTPResponse(
            data=data,
            status=400,
            error="Invalid request"
        )
    elif response is ClientResponse.NOTFOUND:
        return HTTPResponse(
            data=data,
            status=404,
            error="Resource not found"
        )
    else:
        return HTTPResponse(
            data=data,
            status=500,
            error="Internal Server error"
        )


def parse_HTTPResponse(response: HTTPResponse):
    if response.status == 200:
        return response.data
    elif response.status == 201:
        return response.data
    elif response.status == 409:
        raise HTTPException(
            status_code=409,
            detail=response.error
            )
    elif response.status == 400:
        raise HTTPException(
            status_code=400,
            detail=response.error
            )
    elif response.status == 404:
        raise HTTPException(
            status_code=404,
            detail=response.error
            )
    else:
        raise HTTPException(
            status_code=500,
            detail=response.data
            )
