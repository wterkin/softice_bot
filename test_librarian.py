from unittest import TestCase
import json
import librarian


class CTestLibrarian(TestCase):

    def setUp(self) -> None:
        with open('config.sample.json', "r", encoding="utf-8") as json_file:
            self.config = json.load(json_file)
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.config["windows_data_folder"])
        self.librarian.reload()

    def test_can_process(self):
        self.assertEqual(self.librarian.can_process('superchat', '!хк'), True)
        self.assertEqual(self.librarian.can_process('megachat', '!цт'), True)
        self.assertEqual(self.librarian.can_process('gigachat', '!цт'), False)
        self.assertEqual(self.librarian.can_process('megachat', '!хквс'), False)

    def test_execute_hokku_commands(self):
        self.assertEqual(self.librarian.execute_hokku_commands("username", "usertitle",
                                                               ["!хк"]))

    def test_execute_quotes_commands(self):
        self.fail()

    def test_get_help(self):
        self.fail()

    def test_get_hint(self):
        self.fail()

    def test_is_enabled(self):
        self.fail()

    def test_is_master(self):
        self.fail()

    def test_librarian(self):
        self.fail()

    def test_reload(self):
        self.fail()
