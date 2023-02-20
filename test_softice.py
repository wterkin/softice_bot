from unittest import TestCase
import softice


class CTestSoftIceBot(TestCase):
    def setUp(self) -> None:
        self.bot = softice.CSoftIceBot()
        # global CONFIG_FILE_NAME
        # CONFIG_FILE_NAME = "config.sample.json"
        self.bot.load_config("config.sample.json")

    def test_is_master(self):
        self.assertEqual(self.bot.is_master('username'), True)
        self.assertNotEqual(self.bot.is_master('User'), True)

    def test_is_this_chat_enabled(self):
        self.assertEqual(self.bot.is_this_chat_enabled('superchat'), True)
        self.assertEqual(self.bot.is_this_chat_enabled('supermegachat'), False)

    def test_process_command(self):
        self.assertEqual(self.bot.process_command("config", -583831606, "superchat",
                                                  {"name": "username", "title": "usertitle"}), True)
        self.assertEqual(self.bot.process_command("config", -583831606, "superchat",
                                                  {"name": "MegaUser", "title": "Юзер"}), False)
        self.assertEqual(self.bot.process_command("help", -583831606, "superchat",
                                                  {"name": "username", "title": "usertitle"}), True)
        self.assertNotEqual(self.bot.process_command("вон!", -583831606, "superchat",
                                                     {"name": "username", "title": "usertitle"}), True)

    def test_process_modules(self):
        self.bot.message_text = "!Экспекто патронум"
        self.assertEqual(self.bot.process_modules(-583831606, "Ботовка", "Pet_Rovich", "Петрович"),
                         ("", False))

    def test_reload_config(self):
        # pchat_id: int, puser_name: str, puser_title: str
        self.assertEqual(self.bot.reload_config(-583831606, "username", "usertitle"), True)
        self.assertEqual(self.bot.reload_config(-583831606, "user", "user"), False)
