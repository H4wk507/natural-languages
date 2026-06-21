"""Testy szukania struktur w sekwencjach kolejnych słów."""

from natural_languages.analysis import (
    is_repetition,
    phrase_abelian_squares,
    phrase_palindromes,
    phrase_shuffle_squares,
)


class TestIsRepetition:
    def test_literal_square(self) -> None:
        assert is_repetition("abab")  # ab + ab
        assert not is_repetition("ililii")  # genuine shuffle, nie powtórzenie
        assert not is_repetition("")


class TestPhraseShuffleSquares:
    def test_finds_genuine_phrase(self) -> None:
        # "i lilii" -> "ililii" jest genuine przetasowanym kwadratem (u = "ili").
        matches = phrase_shuffle_squares([["i", "lilii"]])
        assert [m.tokens for m in matches] == [("i", "lilii")]

    def test_finds_two_word_concat(self) -> None:
        matches = phrase_shuffle_squares([["pre", "press"]])
        assert [m.phrase for m in matches] == ["pre press"]

    def test_excludes_repetitions_by_default(self) -> None:
        # "ab ab" -> "abab" to literalne powtórzenie (ww), więc domyślnie pomijane.
        assert phrase_shuffle_squares([["ab", "ab"]]) == []

    def test_can_include_repetitions(self) -> None:
        matches = phrase_shuffle_squares([["ab", "ab"]], genuine_only=False)
        assert [m.tokens for m in matches] == [("ab", "ab")]

    def test_ignores_single_tokens(self) -> None:
        # Pojedyncze słowo (nawet będące przetasowanym kwadratem) nie jest sekwencją.
        assert phrase_shuffle_squares([["abab"]]) == []

    def test_respects_max_length(self) -> None:
        assert phrase_shuffle_squares([["pre", "press"]], max_length=4) == []

    def test_sorted_by_length_desc(self) -> None:
        sentences = [["i", "lilii"], ["pre", "press"]]
        lengths = [m.length for m in phrase_shuffle_squares(sentences)]
        assert lengths == sorted(lengths, reverse=True)


class TestPhraseAbelianSquares:
    def test_finds_chiasmus(self) -> None:
        # "ab ba" -> "abba": kwadrat abelowy (połowy o równym multizbiorze), nie powtórzenie.
        matches = phrase_abelian_squares([["ab", "ba"]])
        assert [m.tokens for m in matches] == [("ab", "ba")]

    def test_excludes_repetitions_by_default(self) -> None:
        # "ab ab" -> "abab" to powtórzenie (ww), domyślnie pomijane mimo bycia abelowym.
        assert phrase_abelian_squares([["ab", "ab"]]) == []

    def test_can_include_repetitions(self) -> None:
        matches = phrase_abelian_squares([["ab", "ab"]], genuine_only=False)
        assert [m.tokens for m in matches] == [("ab", "ab")]


class TestPhrasePalindromes:
    def test_finds_palindrome(self) -> None:
        # "ko ok" -> "kook" jest palindromem.
        matches = phrase_palindromes([["ko", "ok"]])
        assert [m.phrase for m in matches] == ["ko ok"]

    def test_ignores_single_tokens(self) -> None:
        assert phrase_palindromes([["kajak"]]) == []
