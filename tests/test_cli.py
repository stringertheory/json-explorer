from pathlib import Path

from json_explorer.explore import main

FIXTURE_DIR = Path(__file__).parent.resolve() / "data"


def test_greet_cli(capsys):
    args = [FIXTURE_DIR / "example1.jsonl"]
    main(args)
    captured = capsys.readouterr()
    result = captured.out
    assert "San Juan!" in result
