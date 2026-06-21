"""Testy wyszukiwania rekordów (najdłuższych struktur) na znanych przykładach."""

from natural_languages.analysis import (
    best_records,
    is_shuffled_square,
    longest_abelian_square,
    longest_palindrome,
    longest_shuffled_square,
    longest_square,
    split_sentences,
)
from natural_languages.detectors import ShuffledSquareDetector


class TestLongestPalindrome:
    def test_whole_string(self) -> None:
        # "Kobyła ma mały bok" bez spacji jest palindromem (13 liter).
        assert longest_palindrome("kobylamalybok") == "kobylamalybok"

    def test_embedded(self) -> None:
        assert longest_palindrome("xxkajakyy") == "kajak"

    def test_even_length(self) -> None:
        assert longest_palindrome("abccba") == "abccba"

    def test_none_below_min_length(self) -> None:
        assert longest_palindrome("ab") == ""
        assert longest_palindrome("") == ""


class TestLongestSquare:
    def test_embedded_square(self) -> None:
        assert longest_square("abcabcd") == "abcabc"

    def test_whole_square(self) -> None:
        assert longest_square("aabbaabb") == "aabbaabb"

    def test_prefers_longest_period(self) -> None:
        # "aa" (okres 1) oraz "abab" (okres 2) — wygrywa dłuższy kwadrat.
        assert longest_square("aaabab") == "abab"

    def test_none(self) -> None:
        assert longest_square("abc") == ""


class TestLongestAbelianSquare:
    def test_whole(self) -> None:
        assert longest_abelian_square("abba") == "abba"
        assert longest_abelian_square("kryptoportyk") == "kryptoportyk"

    def test_embedded(self) -> None:
        assert longest_abelian_square("xabbay") == "abba"

    def test_none(self) -> None:
        assert longest_abelian_square("abc") == ""


class TestShuffledSquare:
    def test_is_shuffled_square_known(self) -> None:
        assert is_shuffled_square("abab")
        assert is_shuffled_square("prepress")
        assert is_shuffled_square("zzabab")  # u = "zab"

    def test_is_shuffled_square_negative(self) -> None:
        assert not is_shuffled_square("abccba")  # tangram, ale NIE shuffle square
        assert not is_shuffled_square("kot")
        assert not is_shuffled_square("")

    def test_consistent_with_detector(self) -> None:
        # Nowy recognizer musi zgadzać się z istniejącym detektorem na krótkich słowach.
        detector = ShuffledSquareDetector()
        for word in ["abab", "prepress", "abccba", "abcabd", "aabbccaabbcc"]:
            assert is_shuffled_square(word) == detector.check(word)

    def test_longest_embedded(self) -> None:
        assert longest_shuffled_square("xyabab") == "abab"

    def test_longest_respects_max_length(self) -> None:
        # Okno dłuższe niż max_length jest pomijane mimo bycia shuffle square.
        assert longest_shuffled_square("abab", max_length=2) == ""


class TestBestRecords:
    def test_keeps_longest_per_structure(self) -> None:
        records = best_records(["kajak", "rotor", "kankan"])
        assert records["palindrome"].match == "kajak"  # 5 > 5? remis -> pierwszy dłuższy
        assert records["palindrome"].length == 5
        assert records["square"].match == "kankan"
        assert records["square"].source == "kankan"

    def test_empty_input(self) -> None:
        assert best_records([]) == {}


class TestSplitSentences:
    def test_splits_on_terminators(self) -> None:
        assert split_sentences("Ala ma kota. Kot ma Alę! Czy na pewno?") == [
            "Ala ma kota",
            "Kot ma Alę",
            "Czy na pewno",
        ]
