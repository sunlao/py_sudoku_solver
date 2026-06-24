from pytest import raises
def test_controller_process(state, startup_message, bad_message, test_actor_domain_state):
    """Assert shared actor state class
    - returns none when empty
    - returns value that was set
    - messages with different actor:behaviors cant share state
    """
    result = state.get_cache(startup_message)
    assert result is None
    state.set_actor_domain_states(startup_message, test_actor_domain_state)
    result = state.get_cache(startup_message)
    assert result == test_actor_domain_state
    with raises(ValueError):
        state.set_actor_domain_states(bad_message, test_actor_domain_state)
    with raises(ValueError):
        _ = state.get_cache(bad_message)

    