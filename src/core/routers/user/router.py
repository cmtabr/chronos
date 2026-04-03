import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from core.routers.user.dependencies import (
    get_user_list_query,
    get_user_service,
)
from core.schemas.user import UserCreate, UserListQuery, UserRead, UserUpdate
from domain.models.user import UserModel
from domain.services.user import UserService

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@user_router.get("", response_model=list[UserRead])
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    query: Annotated[UserListQuery, Depends(get_user_list_query)],
) -> list[UserRead]:
    users = service.get_all_users()
    slice_ = users[query.skip : query.skip + query.limit]
    return [UserRead.model_validate(u) for u in slice_]


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    user = service.get_user_by_id(user_id)
    return UserRead.model_validate(user)


@user_router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    user = UserModel(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        name=payload.name,
        is_active=payload.is_active,
    )
    created = service.create_user(user)
    return UserRead.model_validate(created)


@user_router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    existing = service.get_user_by_id(user_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    updated = service.update_user(user_id, existing)
    return UserRead.model_validate(updated)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    service.delete_user(user_id)
