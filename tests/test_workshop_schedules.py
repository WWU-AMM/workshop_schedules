#!/usr/bin/env python

"""Tests for `workshop_schedules` package."""

from typer.testing import CliRunner

from workshop_schedules import cli


def test_version():
    import workshop_schedules

    assert workshop_schedules.__version__


def test_command_line_interface():
    """Test the CLI."""
    from workshop_schedules.cli import app

    runner = CliRunner()
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert 'Usage: workshop-schedules' in result.output
    help_result = runner.invoke(app, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
