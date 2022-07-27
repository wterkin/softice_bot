from unittest import TestCase
import barman
import json


class CTestBarman(TestCase):
    def setUp(self) -> None:
        with open('config.sample.json', "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        self.barman: barman.CBarman = barman.CBarman(self.config, self.config["windows_data_folder"])
        self.barman.reload()

    def test_barman(self):
        self.assertNotEqual(self.barman.barman('superchat', '!пиво', 'Петрович'), '')
        self.assertNotEqual(self.barman.barman('megachat', '!beer', 'Петрович'), '')
        self.assertEqual(self.barman.barman('gigachat', '!beer', 'Петрович'), '')

        self.assertNotEqual(self.barman.barman('superchat', '!бар', 'Петрович'), '')
        self.assertNotEqual(self.barman.barman('megachat', '!bar', 'Петрович'), '')
        self.assertEqual(self.barman.barman('gigachat', '!bar', 'Петрович'), '')

        self.assertEqual(self.barman.barman('superchat', '!barreload', 'Петрович'), "Содержимое бара обновлено")
        self.assertEqual(self.barman.barman('megachat', '!barreload', 'Петрович'), "Содержимое бара обновлено")
        self.assertNotEqual(self.barman.barman('gigachat', '!barl', 'Петрович'), "Содержимое бара обновлено")

        self.assertEqual(self.barman.barman('gigachat', '!кукабарра', 'Петрович'), "")
        self.assertEqual(self.barman.barman('megachat', '!кузинатра', 'Петрович'), "")
        self.assertEqual(self.barman.barman('мяучат', '!пиво', 'Петрович'), "")
        self.assertEqual(self.barman.barman('кукучат', '!beer', 'Петрович'), "")
