from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, User as TelegramUser
from aiogram.utils.exceptions import MessageCantBeEdited
from pytest_mock import MockFixture

from aiogram_carousel.carousel import CarouselHandler, BuiltCarousel, BaseCarousel


@pytest.fixture
def mock_build_carousel(mocker):
    def wrap(text: str = 'text', reply_markup: InlineKeyboardMarkup | None = None) -> MockFixture:
        return mocker.patch(
            'aiogram_carousel.carousel.CarouselHandler.build_carousel',
            return_value=BuiltCarousel(text=text, reply_markup=reply_markup),
        )

    return wrap


@pytest.fixture
def mock_tg_callback():
    def wrap(callback_data: str = '') -> AsyncMock:
        callback = AsyncMock(id=1, data=callback_data, spec=CallbackQuery)
        callback.message = AsyncMock()
        return callback

    return wrap


@pytest.fixture
def keyboard_buttons() -> list[list[InlineKeyboardButton]]:
    return [[InlineKeyboardButton(text='1', callback_data='.')]]


carousel_text = 'Test Text%'


class OnlyTextCarousel(BaseCarousel):
    def get_text(self, telegram_user: TelegramUser, page_number: int) -> str:
        return carousel_text

    def get_buttons(self, telegram_user: TelegramUser, page_number: int) -> list[list[InlineKeyboardButton]]:
        return []

    def can_turn_right(self, telegram_user: TelegramUser, page_number: int) -> bool:
        return False

    def can_turn_left(self, telegram_user: TelegramUser, page_number: int) -> bool:
        return False


@pytest.mark.asyncio
class TestCarouselHandler:
    async def test_handle_carousel_turn_should_edit_message(self, mock_build_carousel, mock_tg_callback,
                                                            keyboard_buttons):
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        mock_build_carousel(carousel_text, reply_markup)
        cb = mock_tg_callback()

        handler = CarouselHandler()
        await handler._handle_turn(cb, {'carousel_id': '_', 'page_number': '1'})

        cb.message.edit_text.assert_called_once_with(text=carousel_text, reply_markup=reply_markup)

    async def test_handle_carousel_turn_should_send_new_message(self, mock_build_carousel, mock_tg_callback,
                                                                keyboard_buttons):
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        mock_build_carousel(carousel_text, reply_markup)
        cb = mock_tg_callback()
        cb.message.edit_text = AsyncMock(side_effect=MessageCantBeEdited('text'))

        handler = CarouselHandler()
        await handler._handle_turn(cb, {'carousel_id': '_', 'page_number': '1'})

        cb.message.answer.assert_called_once_with(text=carousel_text, reply_markup=reply_markup)

    def test_build_carousel_not_existing_id(self):
        handler = CarouselHandler()

        with pytest.raises(KeyError):
            handler.build_carousel('not_existing_id', page_number=1, tg_user=Mock())

    def test_build_carousel_without_any_buttons(self):
        test_carousel = OnlyTextCarousel()
        handler = CarouselHandler()
        handler.add_carousel(test_carousel)

        build_carousel = handler.build_carousel(test_carousel.name, page_number=1, tg_user=Mock())

        assert build_carousel.text == carousel_text
        assert build_carousel.reply_markup is None

    def test_build_carousel_without_navigation_buttons(self, keyboard_buttons):
        class TestCarousel(OnlyTextCarousel):
            def get_buttons(self, telegram_user: TelegramUser, page_number: int) -> list[list[InlineKeyboardButton]]:
                return keyboard_buttons

        test_carousel = TestCarousel()
        handler = CarouselHandler()
        handler.add_carousel(test_carousel)

        build_carousel = handler.build_carousel(test_carousel.name, page_number=1, tg_user=Mock())

        assert build_carousel.text == carousel_text
        assert build_carousel.reply_markup == InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    @pytest.mark.parametrize('expected_text, next_page, turn_left, turn_right', [
        ('⬅️', 4, True, False),
        ('➡️', 6, False, True)
    ])
    def test_build_carousel_single_navigation_button(self, expected_text, next_page, turn_left, turn_right):
        class TestCarousel(OnlyTextCarousel):
            def can_turn_right(self, telegram_user: TelegramUser, page_number: int) -> bool:
                return turn_right

            def can_turn_left(self, telegram_user: TelegramUser, page_number: int) -> bool:
                return turn_left

        test_carousel = TestCarousel()
        handler = CarouselHandler()
        handler.add_carousel(test_carousel)
        expected_button = InlineKeyboardButton(
            text=expected_text,
            callback_data=CarouselHandler._carousel_callback_data.new(
                carousel_id=test_carousel.name, page_number=next_page
            )
        )

        build_carousel = handler.build_carousel(test_carousel.name, page_number=5, tg_user=Mock())

        assert build_carousel.reply_markup == InlineKeyboardMarkup(inline_keyboard=[[expected_button]])
