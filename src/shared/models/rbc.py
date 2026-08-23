class ControllerMessageInput(BaseModel):
    model_config = DTO_CONFIG
    side_effects: ActorSideEffects
    actor_name: ActorNames
    director_now: datetime
