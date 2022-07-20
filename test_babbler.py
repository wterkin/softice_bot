from unittest import TestCase
import json
import babbler


class CTestBabbler(TestCase):
    def setUp(self) -> None:
        with open('config.sample.json', "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)

        self.babbler = babbler.CBabbler(self.config, self.config["windows_data_folder"])

    def test_babbler(self):
        self.assertEqual(self.babbler.babbler('superchat', '!bblr'), 'База болтуна обновлена')
        self.assertNotEqual(self.babbler.babbler('gigachat', '!bblr'), 'База болтуна обновлена')
        self.assertNotEqual(self.babbler.babbler('megachat', '!reload'), 'База болтуна обновлена')

    def test_can_process(self):
        self.assertEqual(self.babbler.can_process('superchat', ''), True)
        self.assertNotEqual(self.babbler.babbler('gigachat', ''), True)

    #
    # def test_is_this_chat_enabled(self):
    #     self.assertEqual(self.bot.is_this_chat_enabled('Ботовка'), True)
    #     self.assertEqual(self.bot.is_this_chat_enabled('Test'), False)
    #
    # # assertIn(элемент, список)
    # def test_send_help(self):
    #     self.assertNotEqual(len(self.bot.send_help('Ботовка')), 0)
    #     self.assertEqual(len(self.bot.send_help('Test1')), 0)
    #
    # def test_process_modules(self):
    #
    #     self.assertEqual(self.bot.process_modules("Ботовка", "Pet_Rovich", "Петрович",
    #                                               "!Экспекто патронум"), "")
