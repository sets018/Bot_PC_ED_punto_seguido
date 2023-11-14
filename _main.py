from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import *

import os

from Argument import *
from Ceasar import CeasarArgument, DecypherArgument
from Recursion import RecursionArgument
from Markov import ValidationWithImage, MarkovArgument
from Symbolic import SymbolicArgument, FGOptions

token = "6982268503:AAFKLWgQ1WI0F6so0-TVDTjRypHIAaj4uuY"
user = "@PuntoSeguidoBot"

targets: list[ Argument ] = []

helpText = """ ¡Bienvenido!
Este bot tiene a disposición los siguientes comandos:
/ceasar: Igresa una cadena de texto y una llave de rotación para realizar el correspondiente cifrado césar.
/decypher: Ingresa una cadena de texto cifrada por el método anterior para ver el mensaje original.
/recursion: Ingresa la recursión de una función, así como su dominio y valores iniciales y retorna su forma cerrada.
/markov: Ingresa un url estático, junto con una clave k para generar cadenas de markov con el contenido de la página.
/symbolic: Elije una de las 7 opciones de cadenas para ver cuantas cadenas de longitud ingresada cumplen con la condición
"""

# Comandos
async def start_command( update, context ):
  await update.message.reply_text( 'Conversación iniciada bipbop' )

async def help_command( update, context ):
  await update.message.reply_text( helpText )

async def ceasar_command( update, context ):
  await update.message.reply_text( '¿Cadena de texto a cifrar?' )
  targets.append( CeasarArgument( update.message.chat.id, update.message.chat.type == 'group' ) )

async def decypher_command( update, context ):
  await update.message.reply_text( '¿Cadena de texto a descifrar?' )
  targets.append( DecypherArgument( update.message.chat.id, update.message.chat.type == 'group' ) )

async def recursion_command( update, context ):
  await update.message.reply_text( '¿f(n) = ?' )
  targets.append( RecursionArgument( update.message.chat.id, update.message.chat.type == 'group' ) )

async def markov_command( update, context ):
  await update.message.reply_text( '¿Cual es la url del sitio web estático?' )
  targets.append( MarkovArgument( update.message.chat.id, update.message.chat.type == 'group' ) )

async def symbolic_command( update, context ):
  await update.message.reply_text( FGOptions )
  targets.append( SymbolicArgument( update.message.chat.id, update.message.chat.type == 'group' ) )

async def handle_msg( update, context ):
  msg_type = update.message.chat.type
  msg = update.message.text

  print( f'<{ update.message.chat.id }<>{msg_type}>: { msg }' )
  
  target = Target( update.message.chat.id, msg_type == 'group' )

  if target in targets:
    position = targets.index( target )
    result = targets[ position ]( msg )

    if result:
      targets.pop( position )
      await update.message.reply_text( 'Resultado:' )
    await update.message.reply_text( result.msg )
    print(type(result))
    if type(result) is ValidationWithImage:
      await update.message.reply_photo( open(result.img, 'rb') )
      await update.message.reply_text( result.msg2 )
      os.remove( result.img )

if __name__ == '__main__':
  print('Begin...')
  app = Application.builder().token( token ).build()

  app.add_handler( CommandHandler( 'start', start_command ) )
  app.add_handler( CommandHandler( 'ayuda', help_command ) )
  app.add_handler( CommandHandler( 'ceasar', ceasar_command ) )
  app.add_handler( CommandHandler( 'decypher', decypher_command ) )
  app.add_handler( CommandHandler( 'recursion', recursion_command ) )
  app.add_handler( CommandHandler( 'markov', markov_command ) )
  app.add_handler( CommandHandler( 'symbolic', symbolic_command ) )

  app.add_handler( MessageHandler( filters.TEXT, handle_msg ) )

  print('Loaded...')
  app.run_polling( poll_interval = 2 )
