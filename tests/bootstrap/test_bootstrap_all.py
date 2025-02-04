import pytest
from _pytest.tmpdir import TempPathFactory
from approvaltests.pytest.py_test_namer import PyTestNamer
from utils.approvals import verify
from utils.click_invoker import invoke
from utils.proc_mock import ProcMock


def test_bootstrap_all_empty(tmp_path_factory: TempPathFactory):
    cwd = tmp_path_factory.mktemp("cwd")

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output)


def test_bootstrap_all_env(tmp_path_factory: TempPathFactory):
    cwd = tmp_path_factory.mktemp("cwd")
    (cwd / ".env.template").touch()

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output)


def test_bootstrap_all_poetry(tmp_path_factory: TempPathFactory, proc_mock: ProcMock):
    cwd = tmp_path_factory.mktemp("cwd")
    (cwd / "poetry.toml").touch()

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output)


@pytest.mark.parametrize(
    "mock_os_dependency",
    [
        pytest.param("Windows", id="windows"),
        pytest.param("Linux", id="linux"),
        pytest.param("Darwin", id="macOS"),
    ],
    indirect=["mock_os_dependency"],
)
def test_bootstrap_all_npm(
    proc_mock: ProcMock, tmp_path_factory: TempPathFactory, request: pytest.FixtureRequest, mock_os_dependency: None
):
    cwd = tmp_path_factory.mktemp("cwd")
    (cwd / "package.json").touch()

    # proc_mock.set_output("npm install", ["<<Installed npm packages>>"])
    # proc_mock.set_output("npm.cmd install", ["<<Installed npm.cmd packages on Windows>>"])

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output, namer=PyTestNamer(request))


def test_bootstrap_all_poetry_via_pyproject(tmp_path_factory: TempPathFactory, proc_mock: ProcMock):
    cwd = tmp_path_factory.mktemp("cwd")
    (cwd / "pyproject.toml").write_text("[tool.poetry]", encoding="utf-8")

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output)


def test_bootstrap_all_skip_dirs(tmp_path_factory: TempPathFactory):
    cwd = tmp_path_factory.mktemp("cwd")
    (cwd / ".venv").mkdir()
    (cwd / "__pycache__").mkdir()
    (cwd / "node_modules").mkdir()
    (cwd / "file.txt").touch()
    (cwd / "empty_dir").mkdir()
    (cwd / "boring_dir").mkdir()
    (cwd / "boring_dir" / "file.txt").touch()
    (cwd / "double_nested_dir").mkdir()
    (cwd / "double_nested_dir" / "nest1").mkdir()
    (cwd / "double_nested_dir" / "nest2").mkdir()
    (cwd / "double_nested_dir" / "nest2" / "file.txt").touch()

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output)


def test_bootstrap_all_sub_dir(tmp_path_factory: TempPathFactory, proc_mock: ProcMock):
    cwd = tmp_path_factory.mktemp("cwd")
    (cwd / "empty_dir").mkdir()
    (cwd / "live_dir").mkdir()
    (cwd / "live_dir" / ".env.template").touch()
    (cwd / "live_dir" / "poetry.toml").touch()

    result = invoke(
        "bootstrap all",
        cwd=cwd,
    )

    assert result.exit_code == 0
    verify(result.output)
