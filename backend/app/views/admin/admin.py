from http import HTTPStatus
from typing import List
from aiohttp import web
from pydantic import ValidationError

from app.db import Role
from app.models import AdminCreateUserPayload
from app.pkg.helpers import validation_error
from app.repositories import users


def setup_admin_routes(app: web.Application):
    app.router.add_post('/manage/create-user', create_user)
    app.router.add_get('/manage/users-list', users_list)


async def users_list(request):
    if request["user"].role is not Role.admin:
        return web.json_response({
            "data": {
                "error": "You have not enough permissions",
            },
            "message": "Request forbidden",
            "success": False,
        }, status=HTTPStatus.FORBIDDEN)

    async with request.app['db'].acquire() as conn:
        result = await users.list(conn)
        return web.json_response({
            "data": result,
            "message": "",
            "success": True,
        }, status=HTTPStatus.OK)


async def create_user(request):
    if request["user"].role is not Role.admin:
        return web.json_response({
            "data": {
                "error": "You have not enough permissions",
            },
            "message": "Request forbidden",
            "success": False,
        }, status=HTTPStatus.FORBIDDEN)

    data = await request.json()
    try:
        payload: AdminCreateUserPayload = AdminCreateUserPayload(**data)

        async with request.app['db'].acquire() as conn:
            try:
                result = await users.create(conn, payload)
                return web.json_response({
                    "data": result.to_json(),
                    "message": "user was added",
                    "success": True,
                }, status=HTTPStatus.CREATED)

            except Exception as e:
                return web.json_response({
                    "data": {
                        "error": str(e),
                    },
                    "message": "There some error happend",
                    "success": False,
                }, status=HTTPStatus.BAD_REQUEST)

    except ValidationError as e:
        error_messages = validation_error(e)
        return web.json_response({
            "data": error_messages,
            "message": "There some errors",
            "success": False,
        }, status=HTTPStatus.BAD_REQUEST)