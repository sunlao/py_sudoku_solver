def test_controller_process(state, test_process_states):
    result = state.get_controller_process()
    assert result is None
    state.set_controller_process(test_process_states)
    result = state.get_controller_process()
    assert result == test_process_states
