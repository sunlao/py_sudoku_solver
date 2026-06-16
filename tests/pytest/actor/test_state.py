from shared.models.constants import ActorBehaviors

def test_controller_process(state, test_process_states):
    result = state.get_cached(ActorBehaviors.CONTROLLER_START_UP)
    assert result is None
    state.set_controller_process(ActorBehaviors.CONTROLLER_START_UP, test_process_states)
    result = state.get_cached(ActorBehaviors.CONTROLLER_START_UP)
    assert result == test_process_states
