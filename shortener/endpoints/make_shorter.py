from random import choice
from string import ascii_uppercase, digits

from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shortener import utils
from shortener.db.connection import get_session
from shortener.db.models import UrlStorage
from shortener.schemas import MakeShorterRequest, MakeShorterResponse


api_router = APIRouter(tags=["Url"])


async def get_short(session: AsyncSession) -> tuple[str, str]:
    while True:
        suffix = "".join(choice(ascii_uppercase + digits) for _ in range(5))
        exist_query = select(exists().where(UrlStorage.short_url == suffix))
        exist = await session.scalar(exist_query)
        if not exist:
            break
    short_url = utils.url_from_suffix(suffix)
    return short_url, suffix


@api_router.post(
    "/make_shorter",
    response_model=MakeShorterResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Site with this url does not exists or status code of request >= 400",
        },
    },
)
async def make_shorter(
    model: MakeShorterRequest = Body(..., example={"url": "https://yandex.ru"}),
    session: AsyncSession = Depends(get_session),
):
    """
    Логика работы ручки:

    Проверяем, что у нас еще нет сокращенного варианта урла для переданного длинного адреса
      - если он уже есть, то возвращаем его
      - если еще нет:
          1) Подбираем маленький суффикс, которого еще нет в базе;
          2) Сохраняем этот суффикс в базу;
          3) На основе этого суффикса и текущих настроек приложения генерируем полноценный урл;
          4) Возвращаем результат работы ручки: урл и secret_key для запроса дополнительной информации.
    """
    db_url_query = select(UrlStorage).where(UrlStorage.long_url == str(model.url))
    db_url = await session.scalar(db_url_query)
    exist = db_url is not None
    if exist:
        db_url.short_url = utils.url_from_suffix(db_url.short_url)
        return MakeShorterResponse.from_orm(db_url)

    if model.vip_key:
        vip_key_query = select(exists().where(UrlStorage.vip_key == model.vip_key))
        vip_key_exists = await session.scalar(vip_key_query)
        if vip_key_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VIP key already exists",
            )
        short_url = utils.url_from_suffix(model.vip_key)
        new_url = UrlStorage(long_url=str(model.url), short_url=model.vip_key, vip_key=model.vip_key)
    else:
        _, suffix = await get_short(session)
        new_url = UrlStorage(long_url=str(model.url), short_url=suffix)
    
    valid_site, message = await utils.check_website_exist(str(model.url))
    if not valid_site:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    _, suffix = await get_short(session)
    new_url = UrlStorage(long_url=str(model.url), short_url=suffix)
    session.add(new_url)
    await session.commit()
    await session.refresh(new_url)
    new_url.short_url = utils.url_from_suffix(suffix)
    return MakeShorterResponse.from_orm(new_url)
