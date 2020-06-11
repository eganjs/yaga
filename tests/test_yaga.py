from click.testing import CliRunner

from yaga import __version__, main


def test_version():
    assert __version__ == "0.1.0"


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(main, ["Joseph"])
    assert result.exit_code == 0
    assert result.output == "Hello, Joseph!\n"
