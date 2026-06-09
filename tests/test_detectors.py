"""Testy detektorów na znanych przykładach."""

import pytest

from natural_languages.detectors import (
    AbelianSquareDetector,
    AnagramDetector,
    PalindromeDetector,
    ShuffledSquareDetector,
    SquareDetector,
)


class TestSquareDetector:
    def test_check_known_squares(self) -> None:
        detector = SquareDetector()
        assert detector.check("kankan")  # kan + kan
        assert detector.check("czacza")  # cza + cza
        assert detector.check("abab")

    def test_check_non_squares(self) -> None:
        detector = SquareDetector()
        assert not detector.check("kot")  # nieparzysta długość
        assert not detector.check("abcabd")
        assert not detector.check("")

    def test_find_whole_word(self) -> None:
        detector = SquareDetector()
        matches = detector.find("kankan")
        assert any(m.start == 0 and m.end == 6 and m.parts == ("kan", "kan") for m in matches)

    def test_find_cubes(self) -> None:
        detector = SquareDetector()
        cubes = detector.find_cubes("ababab")
        assert any(m.parts == ("ab", "ab", "ab") for m in cubes)


class TestPalindromeDetector:
    def test_check_known_palindromes(self) -> None:
        detector = PalindromeDetector()
        assert detector.check("kajak")
        assert detector.check("kayak")
        assert detector.check("anna")

    def test_check_non_palindromes(self) -> None:
        detector = PalindromeDetector()
        assert not detector.check("kot")
        assert not detector.check("tatar")  # tatar != ratat

    def test_find_includes_whole_word(self) -> None:
        detector = PalindromeDetector(min_length=2)
        matches = detector.find("kajak")
        assert any(m.word == "kajak" for m in matches)


class TestAbelianSquareDetector:
    def test_check_known_abelian_squares(self) -> None:
        detector = AbelianSquareDetector()
        assert detector.check("kryptoportyk")  # krypto / portyk — ten sam multizbiór liter
        assert detector.check("abba")  # ab / ba

    def test_check_non_abelian_squares(self) -> None:
        detector = AbelianSquareDetector()
        assert not detector.check("abcd")
        assert not detector.check("abc")  # nieparzysta długość

    def test_find_whole_word(self) -> None:
        detector = AbelianSquareDetector()
        matches = detector.find("abba")
        assert any(m.start == 0 and m.end == 4 for m in matches)


class TestAnagramDetector:
    def test_check_anagrams(self) -> None:
        detector = AnagramDetector()
        assert detector.check("kot", "tok")
        assert not detector.check("kot", "kos")

    def test_eleven_plus_two(self) -> None:
        # Klasyczny przykład: "eleven plus two" i "twelve plus one" (oba = 13).
        detector = AnagramDetector()
        assert detector.check("elevenplustwo", "twelveplusone")

    def test_find_groups(self) -> None:
        detector = AnagramDetector()
        groups = detector.find_groups(["kot", "tok", "pies", "psie", "dom"])
        sizes = sorted(len(g) for g in groups)
        assert sizes == [2, 2]  # {kot,tok}, {pies,psie}; "dom" bez pary


class TestShuffledSquareDetector:
    def test_check_known_shuffled_squares(self) -> None:
        detector = ShuffledSquareDetector()
        assert detector.check("abab")
        assert detector.check("prepress")  # p-r-e-s przeplecione: pres|pres

    def test_tangram_but_not_shuffled_square(self) -> None:
        # "abccba": każda litera parzyście (tangram), ale NIE przetasowany kwadrat.
        detector = ShuffledSquareDetector()
        assert not detector.check("abccba")

    def test_check_non_shuffled_squares(self) -> None:
        detector = ShuffledSquareDetector()
        assert not detector.check("kot")  # nieparzysta długość
        assert not detector.check("abcabd")
        assert not detector.check("")

    def test_find_whole_word(self) -> None:
        detector = ShuffledSquareDetector()
        matches = detector.find("abab")
        assert len(matches) == 1
        assert matches[0].structure_type == "shuffled_square"

    def test_length_limit(self) -> None:
        detector = ShuffledSquareDetector()
        # Długość parzysta > limit: check() zgłasza wyjątek, find() zwraca [].
        too_long = "a" * (detector.MAX_WORD_LENGTH + 2)
        with pytest.raises(ValueError):
            detector.check(too_long)
        assert detector.find(too_long) == []
