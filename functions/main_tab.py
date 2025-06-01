from aiogram import Router
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from database.pnds import Database, UsersDatabase, InterDatabase
from aiogram.types import InputMediaPhoto, InputMediaVideo
from aiogram import Bot
import os 
from ast import literal_eval

load_dotenv()
router = Router()
db = Database() 
usr_db = UsersDatabase()
acts_db = InterDatabase()
bot = Bot(os.getenv('TOKEN'))

class Movements(CallbackData, prefix = '1'):
    placement: str
    level: int

async def tabs(level,stage="main_table"):
    if level == 0:
        builder=InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Закупка рекламы", callback_data=Movements(placement="buy", level = 1).pack()))
        builder.row(InlineKeyboardButton(text = "Канал под ключ с нуля", callback_data=Movements(placement="fullstack_buy", level = 1).pack()))
        builder.row(InlineKeyboardButton(text = "Telegram Ads", callback_data=Movements(placement="tg_ads", level = 1).pack()))
        builder.row(InlineKeyboardButton(text="Консультация", callback_data=Movements(placement="consulting", level = 1).pack()))
        return builder.as_markup()
    if db.pic_exists(f'{stage}_{level+1}') and db.desc_exists(f'{stage}_{level+1}'):
        builder=InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Назад",callback_data=Movements(placement=stage,level=level-1).pack()))
        builder.add(InlineKeyboardButton(text="Далее",callback_data=Movements(placement=stage,level=level+1).pack()))
        return builder.as_markup()
    else: 
        builder=InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Назад",callback_data=Movements(placement=stage,level=level-1).pack()))
        builder.row(InlineKeyboardButton(text="На главную",callback_data=Movements(placement=stage,level=0).pack()))
        return builder.as_markup()

@router.message(Command("start"))
async def id_command(message: Message):
    if usr_db.user_exists(message.from_user.id) == False:
        for each in literal_eval(os.getenv('ADMIN')):
            print(each)
            await bot.send_message(each, text=f'🧳<b>Новый запуск бота</b>\n\n<b>Пользователь:</b> {message.from_user.first_name}_{message.from_user.last_name} (@{message.from_user.username})\n<b>ID:</b> {message.from_user.id}', parse_mode='HTML')
        usr_db.add_user(message.from_user.id, f'{message.from_user.first_name}_{message.from_user.last_name}')
        await message.answer_photo(photo=db.get_pic("main_table"),caption=db.get_desc("main_table"),
        parse_mode='HTML', reply_markup=await tabs(0)
        )
    else:
        await message.answer_photo(photo=db.get_pic("main_table"),caption=db.get_desc("main_table"),
        parse_mode='HTML', reply_markup=await tabs(0)
        )
    
@router.callback_query(Movements.filter())
async def movements_handler(callback: CallbackQuery, callback_data: Movements):
    if callback_data.level == 0:
            await callback.message.edit_media(InputMediaPhoto(media=db.get_pic("main_table"),caption=db.get_desc("main_table"),
        parse_mode='HTML'), reply_markup=await tabs(0)
    )
    else:
        media = db.get_pic(f'{callback_data.placement}_{callback_data.level}')
        if media == "None":
            acts_db.add_visit(f'{callback_data.placement}_{callback_data.level}')
            await callback.message.delete()
            await bot.send_message(chat_id = callback.message.chat.id, text=db.get_desc(f'{callback_data.placement}_{callback_data.level}'), parse_mode='HTML', reply_markup=await tabs(callback_data.level,callback_data.placement), disable_web_page_preview=True)
        elif callback_data.placement == "buy" and callback_data.level==2:
            acts_db.add_visit(f'{callback_data.placement}_{callback_data.level}')
            await callback.message.edit_media(InputMediaVideo(media=db.get_pic(f'{callback_data.placement}_{callback_data.level}'), caption=db.get_desc(f'{callback_data.placement}_{callback_data.level}'), parse_mode='HTML'),reply_markup=await tabs(callback_data.level,callback_data.placement))
        else:
            acts_db.add_visit(f'{callback_data.placement}_{callback_data.level}')
            await callback.message.edit_media(InputMediaPhoto(media=db.get_pic(f'{callback_data.placement}_{callback_data.level}'), caption=db.get_desc(f'{callback_data.placement}_{callback_data.level}'), parse_mode='HTML'),reply_markup=await tabs(callback_data.level,callback_data.placement))
