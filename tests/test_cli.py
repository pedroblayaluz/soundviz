"""Tests for CLI module."""

from sonicviz import cli


def test_cli_module_exists():
    """Test that cli module exists and has main function."""
    assert hasattr(cli, 'main')
    assert callable(cli.main)


def test_cli_with_help(monkeypatch, capsys):
    """Test CLI help output."""
    # Mock sys.argv to pass --help
    monkeypatch.setattr("sys.argv", ["cli", "--help"])

    try:
        cli.main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert 'type' in captured.out or 'Type' in captured.out
    assert 'input' in captured.out or 'Input' in captured.out
