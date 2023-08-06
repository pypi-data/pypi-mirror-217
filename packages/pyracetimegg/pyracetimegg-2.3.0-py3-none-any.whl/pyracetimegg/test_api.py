# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/PyRacetimeGG/blob/main/LICENSE


class TestClass:
    def __init__(self) -> None:
        from pyracetimegg.api import RacetimeGGAPI

        self.api = RacetimeGGAPI(request_per_second=3)

    def test_search_user(self):
        user = self.api.search_user(name="Nanahuse", discriminator="2723")[0]
        assert user.name == "Nanahuse"

    def test_search_user_by_term(self):
        user = self.api.search_user_by_term("Nanahuse#2723")[0]
        assert user.name == "Nanahuse"

    def test_fetch_user(self):
        user = self.api.fetch_user("xldAMBlqvY3aOP57")
        assert user.name == "Nanahuse"

    def test_fetch_category(self):
        category = self.api.fetch_category("smw")
        assert category.name == "Super Mario World"

    def test_fetch_race(self):
        category = self.api.fetch_race("smw", "comic-baby-9383")
        assert category.name == "Super Mario World"
