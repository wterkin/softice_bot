from time import sleep
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
        self.assertNotEqual(self.babbler.can_process('gigachat', ''), True)

    def test_is_enabled(self):
        self.assertEqual(self.babbler.is_enabled('superchat'), True)
        self.assertNotEqual(self.babbler.is_enabled('gigachat'), True)

    def test_reload(self):
        self.assertEqual(self.babbler.reload(), True)

    def test_talk(self):
        sleep(int(self.babbler.config["babbler_period"]))
        self.assertNotEqual(self.babbler.talk('superchat', 'Трям'), "")

    def test_think(self):
        self.assertNotEqual(self.babbler.think('Трям'), "")
        self.assertNotEqual(self.babbler.think('Привет'), "")
        self.assertEqual(self.babbler.think('Кукареку'), "")
