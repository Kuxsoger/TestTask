from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    EmptyFileError,
    ItemNotFoundError,
    WrongFileFormatError,
    WrongItemFormatError,
)
from app.schemas import TasksGet
from app.services import BuildsService


app = FastAPI()


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc.filename} cannot be found"},
    )


@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)},
    )


@app.exception_handler(WrongItemFormatError)
async def wrong_item_format_handler(
    request: Request, exc: WrongItemFormatError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)},
    )


@app.exception_handler(EmptyFileError)
async def empty_file_handler(request: Request, exc: EmptyFileError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)},
    )


@app.exception_handler(WrongFileFormatError)
async def wrong_file_format_handler(
    request: Request, exc: WrongFileFormatError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)}
    )


@app.post("/get_tasks")
async def get_tasks(task_request: TasksGet) -> list[str]:
    build = BuildsService.get_build(task_request.build)
    if build is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Build not found"
        )

    return BuildsService.get_tasks_for_build(build)
