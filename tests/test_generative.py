"""Testy generatywnego szukania dwuwyrazowych przetasowanych kwadratów."""

from natural_languages.analysis import (
    bucket_by_parity,
    build_bit_index,
    parity_mask,
    two_word_shuffles,
)


class TestParityMask:
    def test_anagrams_share_mask(self) -> None:
        bit = build_bit_index(["ab", "ba"])
        assert parity_mask("ab", bit) == parity_mask("ba", bit)

    def test_even_letters_cancel(self) -> None:
        bit = build_bit_index(["aab", "b"])
        # 'a' parzyście znika z maski -> "aab" ma maskę samego "b".
        assert parity_mask("aab", bit) == parity_mask("b", bit)

    def test_tangram_has_zero_mask(self) -> None:
        bit = build_bit_index(["abab"])
        assert parity_mask("abab", bit) == 0


class TestBucketByParity:
    def test_groups_same_mask(self) -> None:
        words = ["pre", "press", "xyz"]
        bit = build_bit_index(words)
        buckets = bucket_by_parity(words, bit)
        # "pre" i "press" mają tę samą maskę (s w "press" znika), "xyz" osobno.
        group = next(g for g in buckets.values() if "pre" in g)
        assert set(group) == {"pre", "press"}


class TestTwoWordShuffles:
    def test_finds_known_pair(self) -> None:
        # "pre" + "press" = "prepress", znany przetasowany kwadrat.
        pairs = two_word_shuffles(["pre", "press", "xyz"])
        found = {(p.first, p.second) for p in pairs}
        assert ("pre", "press") in found

    def test_excludes_self_pairs(self) -> None:
        # Pojedyncze słowo nie tworzy pary (ww jest kwadratem trywialnie).
        assert two_word_shuffles(["prepress"]) == []

    def test_sorted_by_length_desc(self) -> None:
        pairs = two_word_shuffles(["ab", "ba", "pre", "press", "xyz"])
        lengths = [p.length for p in pairs]
        assert lengths == sorted(lengths, reverse=True)

    def test_respects_max_length(self) -> None:
        pairs = two_word_shuffles(["pre", "press"], max_length=4)
        # "prepress" ma długość 8 > 4, więc nic nie zostaje.
        assert pairs == []
