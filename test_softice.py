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
        print("test_process_command:user ok, config")
        self.assertEqual(self.bot.process_command("config", -583831606, "superchat",
                                                  {"name": "username", "title": "usertitle"}), True)
        print("test_process_command:user wrong, config")
        self.assertEqual(self.bot.process_command("config", -583831606, "superchat",
                                                  {"name": "MegaUser", "title": "Юзер"}), False)
        print("test_process_command:user ok, help")
        self.assertEqual(self.bot.process_command("help", -583831606, "superchat",
                                                  {"name": "username", "title": "usertitle"}), True)
        print("test_process_command:user wrong, unknown command")
        self.assertNotEqual(self.bot.process_command("вон!", -583831606, "superchat",
                                                     {"name": "username", "title": "usertitle"}), True)

    def test_process_modules(self):
        self.bot.message_text = "!Экспекто патронум"
        print("test_process_modules:??")
        self.assertEqual(self.bot.process_modules(-583831606, "Ботовка", "Pet_Rovich", "Петрович"),
                         ("", False))

    def test_reload_config(self):
        # pchat_id: int, puser_name: str, puser_title: str
        print("test_reload_config:user ok")
        self.assertEqual(self.bot.reload_config(-583831606, "username", "usertitle"), True)
        print("test_reload_config:user wrong")
        self.assertEqual(self.bot.reload_config(-583831606, "user", "user"), False)
