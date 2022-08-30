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
        # execute_hokku_commands(self, puser_name: str, puser_title: str,
        # pword_list: list, pcommand: int) -> str:
        self.assertNotEqual(len(self.librarian.execute_hokku_commands("username", "usertitle",
                                                                      ["!хк"], 0)), 0)
        hokku = "Снег согнул бамбук, / Словно мир вокруг него / Перевернулся. (Мацуо Басё)"
        self.assertEqual(self.librarian.execute_hokku_commands("username", "usertitle",
                                                               ["!хк?", "Снег"], 3), hokku)

    def test_execute_quotes_commands(self):
        self.assertNotEqual(len(self.librarian.execute_quotes_commands("username", "usertitle",
                                                                       ["!цт"], 10)), 0)
        quote = "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."
        self.assertEqual(self.librarian.execute_quotes_commands("username", "usertitle",
                                                               ["!цт?", "Мы"], 13), quote)

    def test_get_help(self):
        self.assertNotEqual(self.librarian.get_help('superchat'), "")
        self.assertNotEqual(self.librarian.get_help('megachat'), "")
        self.assertEqual(self.librarian.get_help('левочат'), "")

    def test_get_hint(self):
        self.assertNotEqual(self.librarian.get_hint('superchat'), "")
        self.assertNotEqual(self.librarian.get_hint('megachat'), "")
        self.assertEqual(self.librarian.get_hint('левочат'), "")

    def test_is_enabled(self):
        self.assertEqual(self.librarian.is_enabled('superchat'), True)
        self.assertEqual(self.librarian.is_enabled('megachat'), True)
        self.assertEqual(self.librarian.is_enabled('левочат'), False)

    def test_is_master(self):
        self.assertEqual(self.librarian.is_master('username', 'usertitle'), (True, ""))
        self.assertNotEqual(self.librarian.is_master('User', 'Юзер'), (True, ""))

    def test_librarian(self):
        pass
        # reload
        self.assertEqual(self.librarian.librarian('superchat', 'username', 'usertitle', '!lbreload'),
                         "Библиотека обновлена")
        self.assertNotEqual(self.librarian.librarian('superchat', 'User', 'Юзер', '!lbreload'), "Библиотека обновлена")
        self.assertNotEqual(self.librarian.librarian('gigachat', 'username', 'usertitle', '!lbreload'),
                            "Библиотека обновлена")
        # hint
        self.assertNotEqual(self.librarian.librarian('superchat', 'username', 'usertitle', '!библиотека'), '')
        self.assertNotEqual(self.librarian.librarian('superchat', 'username', 'usertitle', '!lib'), '')
        self.assertEqual(self.librarian.librarian('gigachat', 'username', 'usertitle', '!lib'), '')

        # hokku/quote
        self.assertNotEqual(self.librarian.librarian('superchat', 'username', 'usertitle', '!хк'), '')
        self.assertNotEqual(self.librarian.librarian('superchat', 'username', 'usertitle', '!цт'), '')
        self.assertEqual(self.librarian.librarian('gigachat', 'username', 'usertitle', '!цт'), '')
