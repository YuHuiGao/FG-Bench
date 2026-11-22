import json

import pytest

from evaluation.simple_check_content_recog import simple_check


def question(prediction, answer="Parking", category="Text Recognition", **alternatives):
    return {
        "Question Type": category,
        "Q": "What text is visible?",
        "A": answer,
        "Pred": prediction,
        **alternatives,
    }


@pytest.fixture
def score(tmp_path, monkeypatch):
    predictions = tmp_path / "model"
    predictions.mkdir()
    monkeypatch.chdir(tmp_path)

    def evaluate(files):
        for filename, records in files.items():
            (predictions / filename).write_text(json.dumps(records), encoding="utf-8")
        simple_check(predictions.as_posix())
        assert not (predictions / "score_text_recognition.json").exists()
        return json.loads((tmp_path / "score_text_recognition.json").read_bytes())

    return evaluate


@pytest.mark.parametrize("prediction", ["", " \t\n", ".", "。", "。.", " ."])
def test_empty_predictions_are_counted_as_incorrect(score, prediction):
    assert score({"predictions.json": [question(prediction)]}) == {"model": [0, 1]}


def test_space_does_not_match_a_gap_in_the_reference(score):
    assert score({"predictions.json": [question(" ", answer="No Parking")]}) == {"model": [0, 1]}


@pytest.mark.parametrize("prediction", [
    "Parking",
    "PARKING",
    "PARKING.",
    "Parking。",
    "The text says Parking",
    "Park",
    "  Parking  ",
])
def test_existing_matches_still_receive_credit(score, prediction):
    assert score({"predictions.json": [question(prediction)]}) == {"model": [1, 1]}


@pytest.mark.parametrize("field", ["a", "a_1", "a_2", "a_3"])
def test_alternative_answers(score, field):
    records = [question("STOP", **{field: "Stop。"})]
    assert score({"predictions.json": records}) == {"model": [1, 1]}


def test_no_matches(score):
    records = [question(prediction) for prediction in ("Walk", "Drive", "..", ".。")]
    assert score({"predictions.json": records}) == {"model": [0, 4]}


def test_mixed_predictions_keep_the_denominator(score):
    records = [question(prediction) for prediction in ("", "PARKING.", "Walk")]
    assert score({"predictions.json": records}) == {"model": [1, 3]}


def test_multiple_files_preserve_counts_and_category_filter(score):
    files = {
        "second.json": [question("Park"), question("。"), question("Run")],
        "first.json": [
            question("Parking", a="Parking", a_1="Parking"),
            question("Parking", category="Text Attribute Recognition"),
        ],
        "other_category.json": [question("Parking", category="Movement Detection")],
    }
    assert score(files) == {"model": [2, 4]}
    assert score(files) == {"model": [2, 4]}
