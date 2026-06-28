from shared.models.messages import Message
from shared.models.side_effects import ActorSideEffects
from shared.models.state import ActorDomainState, ActorDomainStates


class UpdateStatus:

    @staticmethod
    def _pick_state(
        new: ActorDomainState, current: ActorDomainState
    ) -> ActorDomainState:
        if new.actor == current.actor:
            return new
        return current

    def _xform_actor_domain_states(
        self, ads: ActorDomainStates, new: ActorDomainState
    ) -> ActorDomainStates:
        return ActorDomainStates(
            states=tuple(self._pick_state(new, s) for s in ads.states)
        )

    async def director(
        self, side_effects: ActorSideEffects, dto: Message[ActorDomainState]
    ) -> None:
        ads = side_effects.state.get_cache(dto)
        new_ads = self._xform_actor_domain_states(ads, dto.content)
        side_effects.state.set_actor_domain_states(dto, new_ads)
