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
        self.fail()

    def test_execute_hokku_commands(self):
        self.fail()

    def test_execute_quotes_commands(self):
        self.fail()

    def test_find_in_book(self):
        self.fail()

    def test_get_command(self):
        self.fail()

    def test_get_help(self):
        self.fail()

    def test_get_hint(self):
        self.fail()

    def test_is_enabled(self):
        self.fail()

    def test_librarian(self):
        self.fail()

    def test_load_book_from_file(self):
        self.fail()

    def test_quote(self):
        self.fail()

    def test_reload(self):
        self.fail()

    def test_save_book(self):
        self.fail()
