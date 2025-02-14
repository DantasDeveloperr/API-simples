import BaseModel # type: ignore

class UserSchema(BaseModel):
    id : int
    name : str
    email : str

    class config :
        orm_mode = True