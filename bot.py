import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN
from omdb_api import get_random_movie

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! 🎬\n"
        "Я бот, который рекомендует случайные фильмы.\n\n"
        "Используй команду:\n"
        "/random_movie <год> <жанр>"
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📌 Доступные команды:\n\n"
        "/start — приветствие\n"
        "/help — помощь\n"
        "/random_movie <год> <жанр> — получить случайный фильм\n\n"
        "Пример:\n"
        "/random_movie 2020 comedy"
    )


@router.message(Command("random_movie"))
async def random_movie_command(message: Message):
    args = message.text.split()[1:]

    if len(args) != 2:
        await message.answer("❗ Используй: /random_movie <год> <жанр>")
        return

    year, genre = args

    movie = get_random_movie(year, genre)

    if not movie:
        await message.answer("Фильм не найден 😢")
        return

    response = (
        f"🎬 {movie.get('Title')}\n"
        f"📅 Год: {movie.get('Year')}\n"
        f"⭐ Рейтинг: {movie.get('imdbRating')}\n"
        f"📝 Описание: {movie.get('Plot')}"
    )

    await message.answer(response)

@router.message()
async def unknown_message(message: Message):
    await message.answer(
        "❗ Я не понимаю эту команду.\n\n"
        "Используй /help, чтобы посмотреть доступные команды."
    )
    
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())