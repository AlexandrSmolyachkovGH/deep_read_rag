"""User's routers."""

from pathlib import Path as _Path
from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.connections.pg_conn import get_pg_session
from app.core.exceptions.custom_exceptions import ServiceException
from app.core.temp_file_handler.dir_creation import get_tmp_dir_path
from app.schemes.documents import (
    CreateDocReq,
    CreateDocResp,
    GetDocResp,
)
from app.schemes.rag import RagResponse
from app.schemes.users import (
    CreateUserReq,
    CreateUserResp,
    GetUserReq,
    GetUserResp,
)
from app.services.ask_service import ask_service
from app.services.documents import doc_service
from app.services.users import user_service

user_router = APIRouter(
    prefix="/users",
    tags=[
        "users",
    ],
)


@user_router.post(
    "/",
    response_model=CreateUserResp,
    status_code=status.HTTP_201_CREATED,
    description="Create new user.",
)
async def create_user(
    create_data: Annotated[CreateUserReq, Body()],
    session: Annotated[AsyncSession, Depends(get_pg_session)],
) -> CreateUserResp:
    """Create new user."""
    try:
        user = await user_service.create_user(
            create_data=create_data,
            session=session,
        )

    except ServiceException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return CreateUserResp.model_validate(user)


@user_router.get(
    "/",
    response_model=GetUserResp,
    status_code=status.HTTP_200_OK,
    description="Get user or lazy create.",
)
async def get_user(
    get_user_data: Annotated[GetUserReq, Query()],
    session: Annotated[AsyncSession, Depends(get_pg_session)],
) -> GetUserResp:
    """Get user by email."""
    try:
        user = await user_service.get_user(
            get_user_data=get_user_data,
            session=session,
        )

    except ServiceException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Undefined server side error.",
        ) from exc

    return GetUserResp.model_validate(user)


@user_router.post(
    "/{user_id}/documents/",
    response_model=CreateDocResp,
    status_code=status.HTTP_201_CREATED,
    description="Create user document.",
)
async def create_user_document(
    user_id: Annotated[UUID, Path(...)],
    file: Annotated[UploadFile, File()],
    session: Annotated[AsyncSession, Depends(get_pg_session)],
    tmp_dir: Annotated[_Path, Depends(get_tmp_dir_path)],
) -> CreateDocResp:
    """Create user document."""
    try:
        create_data = CreateDocReq(
            user_id=user_id,
            file_name=file.filename,
        )
        doc = await doc_service.create_doc(
            create_data=create_data,
            file=file,
            session=session,
            tmp_dir=tmp_dir,
        )

    except ServiceException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Undefined server side error.",
        ) from exc

    return CreateDocResp.model_validate(doc)


@user_router.get(
    "/{user_id}/documents/",
    response_model=list[GetDocResp],
    status_code=status.HTTP_200_OK,
    description="Get user documents.",
)
async def get_user_documents(
    user_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_pg_session)],
) -> list[GetDocResp]:
    """Get user documents."""
    try:
        docs = await doc_service.get_docs(
            user_id=user_id,
            session=session,
        )

    except ServiceException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Undefined server side error.",
        ) from exc

    return [GetDocResp.model_validate(doc) for doc in docs]


@user_router.get(
    "/{user_id}/documents/{document_id}/",
    response_model=GetDocResp,
    status_code=status.HTTP_200_OK,
    description="Get user document.",
)
async def get_user_document(
    user_id: Annotated[UUID, Path(...)],
    document_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_pg_session)],
) -> GetDocResp:
    """Get user document."""
    try:
        doc = await doc_service.get_doc(
            user_id=user_id,
            document_id=document_id,
            session=session,
        )

    except ServiceException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Undefined server side error.",
        ) from exc

    return GetDocResp.model_validate(doc)


@user_router.post(
    "/{user_id}/ask/",
    response_model=RagResponse,
    status_code=status.HTTP_200_OK,
    description="Receive AI response following RAG pipline.",
)
async def ask_ai(
    user_id: Annotated[UUID, Path(...)],
    question: Annotated[str, Body()],
) -> RagResponse:
    """Receive AI response following RAG pipline."""
    response: RagResponse = await ask_service.ask_ai(
        user_id=user_id,
        question=question,
    )

    return response
