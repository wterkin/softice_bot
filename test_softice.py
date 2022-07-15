from unittest import TestCase
import softice


class CTestSoftIceBot(TestCase):
    def setUp(self) -> None:
        self.bot = softice.CSoftIceBot()

    def test_is_this_chat_enabled(self):
        self.assertEqual(self.bot.is_this_chat_enabled('Ботовка'), True)
        self.assertEqual(self.bot.is_this_chat_enabled('Test'), False)

    def test_send_help(self):
        self.assertNotEqual(len(self.bot.send_help('Ботовка')), 0)
        self.assertEqual(len(self.bot.send_help('Test1')), 0)

    def test_process_modules(self):

        self.assertEqual(self.bot.process_modules("Ботовка", "Pet_Rovich", "Петрович",
                                                  "!Экспекто патронум"), "")
