from typing import Callable
import sympy as sp
from Validation import Validation
from Argument import Argument


Options = [
    'Cadenas Binarias que contengan la subcadena "10"',
    'Cadenas Binarias que contengan la subcadena "010"',
    'Cadenas Ternarias que contengan la subcadena "12"',
    'Cadenas Ternarias que contengan la subcadena "012"',
    'Cadenas Ternarias que contengan un número par de unos', 
    'Cadenas de base cinco que tengan sus caractéres en orden creciente',
    'Cadenas de base cinco que no contengan las subcadenas "01" ni "43"'
]

FGOS = {
    'Cadenas Binarias que contengan la subcadena "10"':                     "z**2/((z**2 - 2*z + 1)*(1-2*z))", 
    'Cadenas Binarias que contengan la subcadena "010"':                    "1/(z**3 - 2*z + 1)", 
    'Cadenas Ternarias que contengan la subcadena "12"':                    "1/(z*2 - 3*z + 1)",
    'Cadenas Ternarias que contengan la subcadena "012"':                   "z*3/((1 - 3*z)*(1 - 3*z + z**3))", 
    'Cadenas Ternarias que contengan un número par de unos':                "z/((1 - z)*(1 - 3*z))", 
    'Cadenas de base cinco que tengan sus caractéres en orden creciente':   "1/((1 - z)**5)",
    'Cadenas de base cinco que no contengan las subcadenas "01" ni "43"':   "1/(2*z**2 - 4*z + 1)"
}

FGOptions = 'Elija una opción:\n'
for i, FGO in enumerate( Options ):
    FGOptions += f'{i}: {FGO}\n'

def symbolicCount( fgo: str, n: int ):
    FGO = sp.parse_expr( fgo )
    z = sp.symbols('z')
    Fz = sp.Poly( FGO.series( x = z, x0 = 0, n = n + 1 ).removeO() )
    fn = Fz.all_coeffs()
    return f"Cadenas de longitud {n}: {fn[::-1][n]}"

def getOption( msg: str, dict ):
    try:
        option = Options[ int( msg ) ]
    except TypeError:
        return Validation( False, 'Por favor ingrese un índice entero' )
    except ValueError:
        return Validation( False, 'Por favor ingrese un índice entero' )
    except IndexError:
        return Validation( False, 'Por favor ingrese una opción válida' )
    else:
        dict['option'] = option
        return Validation( True, '¿Cual es la longitud de la cadena?' )

def getInt( msg: str, dict ):
    try:
        dict[ 'n' ] = int( msg )
    except ValueError:
        return Validation( False, "Por favor ingrese un numero entero" )
    else:
        return Validation( True, symbolicCount( FGOS[dict['option']], dict['n'] ) )

class SymbolicArgument( Argument ):
    def __init__(self, userId: int, isGroup: bool) -> None:
        super().__init__(userId, isGroup, [ getOption, getInt ])