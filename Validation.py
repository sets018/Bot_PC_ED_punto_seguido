class Validation:
    def __init__( self, valid: bool, msg: str ) -> None:
        self.valid = valid
        self.msg = msg
    
    def __bool__( self ) -> bool:
        return self.valid

class ValidationWithImage( Validation ):
    def __init__(self, valid: bool, msg: str, img, msg2: str) -> None:
        self.img = img
        self.msg2 = msg2
        super().__init__(valid, msg)