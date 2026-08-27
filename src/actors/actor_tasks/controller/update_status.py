from shared.models.messages import Message
from shared.models.side_effects import ActorSideEffects
from shared.models.state import ActorDomainState, ActorDomainStates, ActorNames, ActorDomainStatus


class UpdateStatus:

    @staticmethod
    def _actor_domain_state(
        new: ActorDomainState, old: ActorDomainState
    ) -> ActorDomainState:
        if new.actor == old.actor:
            return new
        return old

    def _actor_domain_states(
        self, old: ActorDomainStates, new: ActorDomainState
    ) -> ActorDomainStates:
        return ActorDomainStates(
            states=tuple(self._actor_domain_state(new, o) for o in old.states)
        )

    @staticmethod
    def _game_done(new: ActorDomainStates) -> bool:
        return any(
            state.actor == ActorNames.GAME
            and state.status == ActorDomainStatus.DONE
            for state in new.states
        )

    @staticmethod
    def _rbc_working(new: ActorDomainStates) -> bool:
        return all(
            state.status == ActorDomainStatus.WORKING
            for state in new.states
            if state.rbc_flag
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ActorDomainState]
    ) -> None:
        old = side_effects.state.get_cache(dto)
        new = self._actor_domain_states(old, dto.content)
        side_effects.state.set_domain_actors_state(dto, new)
        if self._game_done(new) is True:
            pass # send
        if self._rbc_working(new) is False:
            pass # send
        print("**director controller: update_status end ")
