import sympy as sp
import re

from Validation import Validation
from Argument import Argument

def recursion( recurrence, domain, v0 ):

  n = sp.Symbol('n')
  f = sp.Function('f')

  terms = sp.Add.make_args( sp.sympify(recurrence) )

  msg = ''

  # - Separación según función homogénea (fh(n)) o no homogénea (fg(n))
  fh = []
  fg = []
  for term in terms:
    if term.has(f): fh.append(term)
    else: fg.append(term)

  # - Parte homogénea

  # -- Exponentes del polinómio característico
  exp = []
  for term in fh:
    # Toma los argumentos de la función para los términos que tengan f
    for expr in sp.Mul.make_args( term ):
      if expr.has(f):
        exp.append( list(expr.atoms())[1] )

  # -- Coeficientes del polinómio característico
  coef = []
  for term in fh:
    # Divide según mutliplicación
    fact = sp.Mul.make_args(term)
    # Toma el coeficiente del termino
    if len(fact) - 1: coef.append( fact[0] )
    # Si solo hay un termino, el coeficiente es 1
    else: coef.append(1)

  # -- Fromulación del polinomo característico
  Ph = n**(-min(exp))
  for i in range(len(exp)):
    Ph -= coef[i]*n**exp[i]/(n**(min(exp)))
  roots = sp.roots( sp.Poly( Ph ) )
  msg += f"Roots = {roots}"
  msg += '\n'

  # - Parte no homogénea

  # -- División según k^n
  fg = list(sp.Add.make_args(sp.simplify( sum(fg) )))

  # -- Separación según raíz y grado de polinomio de cada término
  Pg = [] # Grados
  rg = [] # Raíces (k^n)

  if not fg == [0]:
    for term in fg:
      factors = sp.Mul.make_args(term)
      if len(factors) - 1:
        rg.append(list(factors[0].atoms())[1])
        Pg.append(sp.degree(factors[1]))
      else:
        rg.append(1)
        Pg.append(sp.degree(factors[0]))

  # - No recurrencia

  # Se necesitan constantes según el dominio y los grados de los polinomios hallados
  c = []
  for i in range( domain + len(rg) + len(roots) ): c.append( sp.Symbol( f"c{i}" ) )


  cc = 0 # Variable que cuenta el número de constantes en el polinomio

  # Forma final de la funcion homogénea
  Fh = 0
  for root in roots:
    P = 0
    for i in range(roots[root]):
      P += c[cc]*n**i
      cc += 1
    Fh += P*root**n
  msg += f"Fh(n) = {Fh}"
  msg += '\n'

  # Forma final de la función no homogénea
  Fg = 0
  if rg:
    for i, root in enumerate(rg):
      P = 0
      for i in range(Pg[i] + 1):
        P += c[cc]*n**i
        cc += 1
      if root in roots:
        Fg += P*root**n*n**roots[root]
      else:
        Fg += P*root**n

  msg += f"Fg(n) = {Fg}"
  msg += '\n'

  # -- Solución sistema de ecuaciones

  # Función recursiva para obtener los v0
  def frec(x):
    result = 0
    for i in range(len(exp)):
      result += v0[ x + exp[i] ]*coef[i]
    for i in range(len(fg)):
      result += sp.lambdify( n, fg[i] )(x)
    return result

  # Se necesitan tantos valores iniciales como constantes
  for i in range( domain, cc ):
    v0.append(frec(i))

  msg += f"Dominio: {v0}"
  msg += '\n'

  # Solución del sistema de ecuaciones
  equations = []
  for i in range( cc ):
    equations.append(sp.lambdify(n, Fh + Fg - v0[i])(i))
  results = sp.solve( equations, c )
  msg += f'Coeficientes: {results}'
  msg += '\n'

  # Función no recursiva
  f = (Fh + Fg).subs( results )
  msg += f"Forma cerrada: f(n)={f}"
  msg += '\n'

  # Impresión de los primeros 25 valores
  for i in range( cc, 25 ): v0.append(frec(i))
  generated = [ str(sp.lambdify(n,f)(i)) for i in range(25) ]
  msg += f"Secuencia recursiva: {v0}"
  msg += '\n'
  msg += f"Secuencia generada: {generated}"

  return msg

def checkForRecurrence( msg: str, dict: dict ):
  charCheck = re.compile( r"[^nf()\-\+\*1-9]" )
  recCheck = re.compile( r"\(+n+ \- +[0-9]+\)" )

  msg = msg.replace(' ','')

  if charCheck.search( msg ):
    return Validation( False, 'Por favor ingrese una recurrencia valida' )
  max = 0
  for term in list( sp.Add.make_args( sp.sympify(msg) ) ):
    term = str(term)
    if ('n*f' in term) or ('n**f' in term) or ('f*(' in term) or ('f**(' in term): 
      return Validation( False, 'Por favor ingrese una recurrencia valida' )
    if 'f' in term: 
      if not recCheck.search( term ):
        return Validation( False, 'Por favor ingrese una recurrencia valida' )
      degree = int(term.replace('f(n -','').replace(')',''))
      if degree > max:
        max = degree
    
  dict['recurrence'] = msg
  dict['degree'] = max
  return Validation( True, '¿Cual es el dominio de la recurrencia?' )

def checkForInt( msg: str, dict: dict ):
  try:
      domain = int( msg )
  except ValueError:
      return Validation( False, "Por favor ingrese un numero entero" )
  else:
      if domain < dict['degree']:
        return Validation( False, "Por favor ingrese un dominio valido para la recursión" )
      dict['domain'] = domain
      return Validation( True, "¿Cuales son los valores iniciales de la función?" )

def checkForInitials( msg: str, dict: dict ):
  v0 = msg.replace( ' ', '' ).split(',')
  if len(v0) < dict['domain']:
    return Validation( False, 'No hay suficientes valores para el dominio' )
  for i, value in enumerate(v0):
    try:
      v0[i] = int(value)
    except ValueError:
      return Validation( False, f"{value} no es un número entero" )
  dict['v0'] = v0
  return Validation( True, recursion( dict['recurrence'], dict['domain'], dict['v0'] ) )
    
class RecursionArgument( Argument ):
  def __init__( self, userId: int, isGroup: bool ) -> None:
    super().__init__( userId, isGroup, [ checkForRecurrence, checkForInt, checkForInitials ] )