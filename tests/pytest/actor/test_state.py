def test_controller_process(state, startup_message, bad_message, test_process_states):
    """Assert shared actor state class
    - returns none when empty
    - returns value that was set
    - messages with different actor:behaviors cant share state
    """
    state_obj = state(startup_message)
    state_bad = state(bad_message)
    result = state_obj.get_cache()
    assert result is None
    state_obj.set_actor_domain_states(test_process_states)
    result = state_obj.get_cache()
    result_bad = state_bad.get_cache()
    assert result == test_process_states
    assert result_bad is None
