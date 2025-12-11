import asyncio
import aiohttp

API_URL = "http://127.0.0.1:8000/api/v1/surguard"
HOST = "0.0.0.0"
PORT = 5000


async def send_event_to_server(data: str):
    """Отправляем событие в backend"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, json={"surgard": data}) as resp:
                # print(f"📤 Отправлено на {API_URL}, статус: {resp.status}")
        except Exception as e:
            print(f"⚠ Ошибка при отправке: {e}")


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    # print(f"📡 Подключение от {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                # print(f"🔌 Соединение закрыто: {addr}")
                break

            # Лог сырых байт
            # print(f"📨 RAW: {data!r}")

            # Пробуем декодировать в текст
            try:
                message = data.decode("utf-8", errors="ignore").strip()
            except UnicodeDecodeError:
                message = "<не удалось декодировать>"

            # print(f"📨 Получено от {addr}: {message}")

            # Отправляем ACK (обязательно!)
            writer.write(b"\x06")
            await writer.drain()
            # print(f"✅ Отправлен ACK -> {addr}")

            # Асинхронно отправляем данные в backend
            asyncio.create_task(send_event_to_server(message))

    except Exception as e:
        print(f"⚠ Ошибка соединения с {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    # print(f"🚀 Sur-Gard listener запущен на {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())