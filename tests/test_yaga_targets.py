from os import chdir
from pathlib import Path
from textwrap import dedent

from click.testing import CliRunner

from yaga import cli


def test_no_workspace_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["targets"])

        assert result.output == dedent(
            """\
            Error: Could not find directory containing WORKSPACE file
            """
        )
        assert result.exit_code == 1


def test_no_build_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

        result = runner.invoke(cli, ["targets"])

        assert result.output == ""
        assert result.exit_code == 0


def test_no_rules_in_single_file(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

        Path("BUILD").touch()

        result = runner.invoke(cli, ["targets"])

        assert result.output == ""
        assert result.exit_code == 0


def test_one_rule_in_single_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

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

        assert result.output == dedent(
            """\
            //:rule_1
            """
        )
        assert result.exit_code == 0


def test_multiple_rules_in_single_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

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

        assert result.output == dedent(
            """\
            //:rule_1
            //:rule_2
            """
        )
        assert result.exit_code == 0


def test_multiple_empty_files_in_directory_tree():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

        Path("BUILD").touch()

        subdirectory = Path("subdirectory")
        subdirectory.mkdir()
        (subdirectory / "BUILD").touch()

        sub_subdirectory = subdirectory / "sub-subdirectory"
        sub_subdirectory.mkdir()
        (sub_subdirectory / "BUILD").touch()

        result = runner.invoke(cli, ["targets"])

        assert result.output == ""
        assert result.exit_code == 0


def test_multiple_rules_in_directory_tree():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

        Path("BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_1",
                )
                """
            )
        )

        subdirectory = Path("subdirectory")
        subdirectory.mkdir()
        (subdirectory / "BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_2",
                )
                """
            )
        )

        sub_subdirectory = subdirectory / "sub-subdirectory"
        sub_subdirectory.mkdir()
        (sub_subdirectory / "BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_3",
                )
                """
            )
        )

        result = runner.invoke(cli, ["targets"])

        assert result.output == dedent(
            """\
            //:rule_1
            //subdirectory:rule_2
            //subdirectory/sub-subdirectory:rule_3
            """
        )
        assert result.exit_code == 0


def test_multiple_rules_in_directory_tree_from_subdirectory():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("WORKSPACE").touch()

        Path("BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_1",
                )
                """
            )
        )

        subdirectory = Path("subdirectory")
        subdirectory.mkdir()
        (subdirectory / "BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_2",
                )
                """
            )
        )

        sub_subdirectory = subdirectory / "sub-subdirectory"
        sub_subdirectory.mkdir()
        (sub_subdirectory / "BUILD").write_text(
            dedent(
                """\
                genrule(
                    name = "rule_3",
                )
                """
            )
        )

        chdir(subdirectory)

        result = runner.invoke(cli, ["targets"])

        assert result.output == dedent(
            """\
            //:rule_1
            //subdirectory:rule_2
            //subdirectory/sub-subdirectory:rule_3
            """
        )
        assert result.exit_code == 0
