from pathlib import Path
import nonebot
from nonebot import get_driver
from .config import Config
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from mcstatus import MinecraftBedrockServer
global_config = get_driver().config
config = Config(**global_config.dict())

status = on_command("motdpe", priority=5)


@status.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    print("收到命令!!!!!!!")
    args = str(event.get_message()).strip()
    if args:
        await bot.send(event, "开始查询...")
        state["address"] = args
        result = await get_status(args)
        await status.finish(result)


@status.got("address", prompt="要查询哪个服务器?")
async def handle_address(bot: Bot, event: Event, state: T_State):
    address = state["address"]
    await bot.send(event, "开始查询...")
    await status.finish(await get_status(address))
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


async def get_status(address):
    server = MinecraftBedrockServer.lookup(address)
    status = await server.async_status()
    result = f'查询结果:\n{address}\n{status.motd} {status.version.brand}ms\n{status.players_online}/{status.players_max}'
    print(result)
    return result

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
        resolve()))
