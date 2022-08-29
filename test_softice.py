from unittest import TestCase
import softice


class CTestSoftIceBot(TestCase):
    def setUp(self) -> None:
        self.bot = softice.CSoftIceBot()

    def test_is_master(self):
        self.assertEqual(self.bot.is_master('Pet_Rovich'), True)
        self.assertNotEqual(self.bot.is_master('User'), True)

    def test_is_this_chat_enabled(self):
        self.assertEqual(self.bot.is_this_chat_enabled('Ботовка'), True)
        self.assertEqual(self.bot.is_this_chat_enabled('Test'), False)

    def test_process_command(self):
        self.assertEqual(self.bot.process_command("config", -583831606, "Ботовка",
                                                  {"name": "Pet_Rovich", "title": "Петрович"}), True)
        print('User')
        self.assertEqual(self.bot.process_command("config", -583831606, "Ботовка",
                                                  {"name": "MegaUser", "title": "Юзер"}), False)
        self.assertEqual(self.bot.process_command("help", -583831606, "Ботовка",
                                                  {"name": "Pet_Rovich", "title": "Петрович"}), True)
        self.assertNotEqual(self.bot.process_command("вон!", -583831606, "Ботовка",
                                                     {"name": "Pet_Rovich", "title": "Петрович"}), True)

    def test_send_help(self):
        self.assertNotEqual(len(self.bot.send_help('Ботовка')), 0)
        self.assertEqual(len(self.bot.send_help('Test1')), 0)

    def test_process_modules(self):
        self.bot.message_text = "!Экспекто патронум"
        self.assertEqual(self.bot.process_modules(-583831606, "Ботовка", "Pet_Rovich", "Петрович"),
                         "Ничего не нашел.")
