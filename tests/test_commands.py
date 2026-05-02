from commands import restart, run_task


def test_restart_command():
    assert restart() is None


def test_run_task():
    res = run_task('debug_task')
    assert res is None
