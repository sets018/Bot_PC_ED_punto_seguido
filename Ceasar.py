from Validation import Validation
from Argument import Target, Argument

# Procesos relacionados a césar
ALPHABET = list( 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789_-.áéíóúÁÉÍÓÚ?!¿¡' )

class CypherLetter:

    def __init__( self, character: str, position: int = None ) -> None:
        self.char = character
        if position is None:
          self.position = ALPHABET.index( character )
        else:
          self.position = position

    def __str__( self ) -> str:
        return self.char
    
    def __add__( self, _value: int | str ):

        if type( _value ) is int:
            position = self.position + _value
            position %= len( ALPHABET )
            char = ALPHABET[ position ]
            return CypherLetter( char, position )
        
        elif type( _value ) is str:
            return self.char + _value

        elif type( _value ) is CypherLetter:
          return self.char + _value.char

def ceasar( text: str, rotation: int ):
    rotated = [ CypherLetter( character ) + rotation if character in ALPHABET else character for character in text ]
    finalText = ''
    for char in rotated: finalText += str( char )
    rotation = ( ( rotation % len(ALPHABET) ) + len(ALPHABET) ) % len(ALPHABET) 
    key = ( CypherLetter( str( rotation // 10 ) ) + len( finalText )) + ( CypherLetter( str( rotation % 10 ) ) + len( finalText ))
    finalText += key
    return finalText

def checkText( msg, dict ):
    if msg:
        dict[ 'text' ] = msg
        return Validation( True, "¿Cual es la rotación del cifrado?" )
    return Validation( False, "Envie una cadena valida" )

def checkForInt( msg, dict ):
    try:
        dict[ 'key' ] = int( msg )
    except ValueError:
        return Validation( False, "Por favor ingrese un numero entero" )
    else:
        return Validation( True, ceasar( dict[ 'text' ], dict['key'] ) )

class CeasarArgument ( Argument ):
   
    def __init__( self, userId: int, isGroup: bool ) -> None:
        super().__init__( userId, isGroup, [ checkText, checkForInt ] )

def checkCypher( msg, dict ):
    cyphered = msg[ :len(msg) - 2 ]
    key = msg[ -2: ]
    trueKey = ''
    for digit in key:
        trueKey += str(CypherLetter( digit ) + ( -len( cyphered ) ))
    try:
        trueKey = int(trueKey)
    except ValueError:
        return Validation( True, 'La cadena no es cifrable sin una llave válida')
    else:
        decyph = ceasar( cyphered, -trueKey )
        return Validation( True, decyph[ :len(decyph)-2 ] )

class DecypherArgument ( Argument ):
    def __init__( self, userId: int, isGroup: bool ) -> None:
        super().__init__( userId, isGroup, [ checkCypher ] )