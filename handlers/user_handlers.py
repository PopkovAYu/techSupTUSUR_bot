from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
# from database.database import user_dict_template, users_db
# from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
# from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
#                                     create_edit_keyboard)
from keyboards.keyboard import create_inline_kb, create_inline__url_kb
from keyboards.start_keyboard import create_start_kb
from lexicon.lexicon_ru import LEXICON
# from utils.help_desk import send_application
# from services.file_handling import book
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from bs4 import BeautifulSoup
import requests
import os
from aiogram.types import FSInputFile
from PIL import Image


router = Router()

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'], 
                        #  reply_markup=create_inline_kb(2, 'to_support', 'knowlage_base', button_1='Кнопка 1'),
                         reply_markup=create_start_kb()
                         )
    # if message.from_user.id not in users_db:
    #     users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(F.text == 'Начать')
async def process_start_button(message: Message):
    await message.answer(text=LEXICON['start'], 
                        reply_markup=create_inline_kb(1, 'to_support', 'check', 'knowlage_base'),
                        )

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'knowlage_base' 

@router.callback_query(F.data == 'knowlage_base')
async def process_buttons_press(callback: CallbackQuery):
    if callback.message.text != LEXICON['knowlage_base']:
        await callback.message.edit_text(
            text=LEXICON['knowlage_base_choice'], 
            reply_markup=create_inline__url_kb(1, 'web_resources', 'mobile_app')
            )
    await callback.answer()

storage = MemoryStorage()
# Создаем "базу данных" пользователей
user_dict = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_name = State()        # Состояние ожидания ввода имени
    fill_email = State()         # Состояние ожидания ввода возраста
    fill_subject = State()      # Состояние ожидания выбора пола
    # upload_file = State()     # Состояние ожидания загрузки фото
    fill_message = State()   # Состояние ожидания выбора образования
    fill_sec_num = State()   # Состояние ожидания выбора получать ли новости


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
# @router.callback_query(F.data == 'to_support', StateFilter(default_state))
# async def process_start_command(message: Message):
#     await message.answer(
#         text='Этот бот демонстрирует работу FSM\n\n'
#              'Чтобы перейти к заполнению анкеты - '
#              'отправьте команду /fillform'
#     )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@router.callback_query(F.data == "to_support", StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Пожалуйста, введите ваши ФИО')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш email')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_email)



# Этот хэндлер будет срабатывать, если введен корректный email
# и переводить в состояние ввода темы обращения
@router.message(StateFilter(FSMFillForm.fill_email),
            lambda x: '@' and '.' in x.text)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем email в хранилище по ключу "email"
    await state.update_data(email=message.text)
    # # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите тему вашего обращения'
        # reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_subject)


# Этот хэндлер будет срабатывать, если введеная тема
# и переводить в состояние ожидания ввода сообщения
@router.message(StateFilter(FSMFillForm.fill_subject))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенную тему в хранилище по ключу "subject"
    await state.update_data(subject=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите описание вашей проблемы')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_message)

# Получить сообщение и вывести из машины состояний
@router.message(StateFilter(FSMFillForm.fill_message))
async def process_message_sent(message: Message, state: FSMContext):
    # Cохраняем введенное сообщение в хранилище по ключу "message"
    await state.update_data(message=message.text)
    r = requests.get('https://help.tusur.ru/index.php?a=add&category=17')
    user_dict[message.from_user.id] = user_dict.get(message.from_user.id, {})
    user_dict[message.from_user.id]['cookies'] = user_dict[message.from_user.id].get('cookies', r.cookies.get_dict())
    soup = BeautifulSoup(r.text, 'html.parser')
    token = soup.find(attrs={'name': 'token'})
    user_dict[message.from_user.id]['token'] = user_dict[message.from_user.id].get('token', token['value'])
    mysecnum = soup.find('img', {'name': 'secimg'})
    sec_num = str(mysecnum).split('?')[-1].split('\"')[0]
    img_data = requests.get(f'https://help.tusur.ru/{mysecnum["src"]}.png', cookies=user_dict[message.from_user.id]['cookies']).content
    with open(f'captcha_{sec_num}.png', 'wb') as captcha:
        captcha.write(img_data)
    background = Image.new('RGBA', (150, 100), (255, 0, 0, 0))
    image = Image.open(f'captcha_{sec_num}.png')
    background.paste(image, (0, 30))
    background.save(f'captcha_{sec_num}.png')
    photo = FSInputFile(f'captcha_{sec_num}.png')
    await message.answer_photo(photo, caption='Введите число с картинки')
    try:
        os.remove(f'captcha_{sec_num}.png')
    except OSError:
        pass
    await state.set_state(FSMFillForm.fill_sec_num)




@router.message(StateFilter(FSMFillForm.fill_sec_num))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенную тему в хранилище по ключу "subject"
    await state.update_data(sec_num=message.text)
    token = user_dict[message.from_user.id]['token']
    cookies = user_dict[message.from_user.id]['cookies']
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()
    user_dict[message.from_user.id]['token'] = token
    user_dict[message.from_user.id]['cookies'] = cookies
    # Завершаем машину состояний
    await state.clear()
    data = {
        "name": user_dict[message.from_user.id]['name'],
        "email": user_dict[message.from_user.id]['email'],
        "subject": user_dict[message.from_user.id]['subject'],
        "message": user_dict[message.from_user.id]['message'],
        "mysecnum": user_dict[message.from_user.id]['sec_num'],
        "token": user_dict[message.from_user.id]['token'],
        "category": 17,
        "hx": 3,
        "hy": ''
        }
    r2 = requests.post('https://help.tusur.ru/submit_ticket.php?submit=1', data=data,  cookies=user_dict[message.from_user.id]['cookies'])
    soup_2 = BeautifulSoup(r2.text, 'html.parser')
    app_id = soup_2.find(attrs={'class': 'btn btn-full'})
    app_id_user = app_id["href"].split("=")[-1].split("\n")[0]
    
    # Отправляем в чат сообщение о выходе из машины состояний
    await message.answer(text=f'{app_id_user}')
        
    
    
# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@router.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        await message.answer(f'{user_dict}')
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить - '
            'отправьте команду /fillform'
        )


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')