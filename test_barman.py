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
        self.assertNotEqual(self.barman.barman('superchat', '!пиво', 'Юзер'), '')
        self.assertNotEqual(self.barman.barman('megachat', '!beer', 'Юзер'), '')
        self.assertEqual(self.barman.barman('gigachat', '!beer', 'Юзер'), '')

        self.assertNotEqual(self.barman.barman('superchat', '!бар', 'Юзер'), '')
        self.assertNotEqual(self.barman.barman('megachat', '!bar', 'Юзер'), '')
        self.assertEqual(self.barman.barman('gigachat', '!bar', 'Юзер'), '')

        self.assertEqual(self.barman.barman('superchat', '!barreload', 'Юзер'), "Содержимое бара обновлено")
        self.assertEqual(self.barman.barman('megachat', '!barreload', 'Юзер'), "Содержимое бара обновлено")
        self.assertNotEqual(self.barman.barman('gigachat', '!barl', 'Юзер'), "Содержимое бара обновлено")

        self.assertEqual(self.barman.barman('gigachat', '!кукабарра', 'Юзер'), "")
        self.assertEqual(self.barman.barman('megachat', '!кузинатра', 'Юзер'), "")
        self.assertEqual(self.barman.barman('мяучат', '!пиво', 'Юзер'), "")
        self.assertEqual(self.barman.barman('кукучат', '!beer', 'Юзер'), "")

    def test_serve_client(self):
        self.assertNotEqual(self.barman.serve_client('Юзер', 'пиво'), "")
        self.assertNotEqual(self.barman.serve_client('Юзер', 'beer'), "")
        self.assertEqual(self.barman.serve_client('Юзер', 'кузинатра'), "")

    def test_can_process(self):
        self.assertEqual(self.barman.can_process('superchat', '!beer'), True)
        self.assertEqual(self.barman.can_process('megachat', '!пиво'), True)
        self.assertEqual(self.barman.can_process('gigachat', '!кукабарра'), False)

    def test_get_help(self):
        self.assertNotEqual(self.barman.get_help('superchat'), "")
        self.assertNotEqual(self.barman.get_help('megachat'), "")
        self.assertEqual(self.barman.get_help('левочат'), "")

    def test_get_hint(self):
        self.assertNotEqual(self.barman.get_hint('superchat'), "")
        self.assertNotEqual(self.barman.get_hint('megachat'), "")
        self.assertEqual(self.barman.get_hint('левочат'), "")

    def test_is_enabled(self):
        self.assertEqual(self.barman.is_enabled('superchat'), True)
        self.assertEqual(self.barman.is_enabled('megachat'), True)
        self.assertEqual(self.barman.is_enabled('левочат'), False)
