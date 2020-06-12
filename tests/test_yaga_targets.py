from pathlib import Path
from textwrap import dedent

from click.testing import CliRunner

from yaga import cli


def test_no_build_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["targets"])

        assert result.exit_code == 0
        assert result.output == ""


def test_no_rules_in_single_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("BUILD").touch()

        result = runner.invoke(cli, ["targets"])

        assert result.exit_code == 0
        assert result.output == ""


def test_one_rule_in_single_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_1",
                )
                """
            )
        )

        result = runner.invoke(cli, ["targets"])

        assert result.exit_code == 0
        assert result.output == dedent(
            """\
            //:rule_1
            """
        )


def test_multiple_rules_in_single_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_1",
                )
                genrule(
                    name = "rule_2",
                )
                """
            )
        )

        result = runner.invoke(cli, ["targets"])

        assert result.exit_code == 0
        assert result.output == dedent(
            """\
            //:rule_1
            //:rule_2
            """
        )
