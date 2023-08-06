from pydantic import BaseModel


class KafkaEvent(BaseModel):

    def to_str(self) -> str:
        pass
