from typing import Any, Callable
from telegram import Update
from telegram.ext import ContextTypes

from Validation import Validation, ValidationWithImage

class Target:
    def __init__( self, userId: int, isGroup: bool ) -> None:
        self.userId = userId
        self.isGroup = isGroup
    
    def __eq__( self, _value: object ) -> bool:
        if type( _value ) is Target:
            return _value.userId == self.userId and _value.isGroup == self.isGroup
        elif type( _value ) is tuple:
            return _value[0] == self.userId and _value[1] == self.isGroup
        return False

class Argument:

    def __init__( self,   
                 userId: int, isGroup: bool,
                 validators: list[ Callable [ [ str, dict ], Validation ] ]
    ) -> None:

        self.target: Target = Target( userId, isGroup )
        self.validators: list = validators
        self.args: dict = {}
        self.layer = 0

    def __eq__( self, item ):
        return item == self.target
    
    def __call__( self, response: str ) -> Validation:
        valid: Validation = self.validators[ self.layer ]( response, self.args )
        if valid:
            self.layer += 1
        if type( valid ) is Validation:
            return Validation( self.layer >= len( self.validators ), valid.msg )
        elif type( valid ) is ValidationWithImage:
            return valid

