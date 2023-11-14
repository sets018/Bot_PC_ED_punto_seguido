import requests
from bs4 import BeautifulSoup
import re
import random
from nltk import ngrams
import nltk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Validation import Validation, ValidationWithImage
from Argument import Target, Argument

def getUrl( msg, dict ):
  
    checkUrl = re.compile( r"https?://\S+" )
    # Valida que sea una url
    if not checkUrl.match( msg ):
        return Validation( False, 'Ingrese una url válida' )
    
    # Se accede a la url ingresada
    response = requests.get( msg )
    # Si se puede ingresar a la url, se extrae el texto utilizando la libreria bs4
    if not (response.status_code == 200):
        return Validation( False, f"No se ha podido acceder a la pagina con la url ingresada, error code: {response.status_code}" )
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Se extrae solo el texto que esta dentro de los tags que contienen texto que esta dentro de un parrafo
    # all_text = soup.get_text(separator=' ', strip=True)
    all_text = ' '.join([p.get_text() for p in soup.find_all('p')])
    if ( len(all_text) <= 1000 ):
       return Validation( False, "Por favor ingrese un url valido de un sitio web estatico" )
    
    response = f"Texto original extraido de : {msg}"
    response += '\n'
    if len( all_text ) > 3500:
       response += all_text[:3500]
    else:
       response += all_text
    response += '\n\n'
    response += '¿Cual es el orden del modelo de markov (k)?'

    dict['url'] = msg
    dict['text'] = all_text

    return Validation( True, response )

def getMarkovOrder( msg, dict ):
    try:
        order = int( msg )
    except ValueError:
        return Validation( False, "Por favor ingrese un numero entero" )
    else:
        if order > 10:
            return Validation( False, 'Por favor ingrese un orden menor o igual a 10' )
        dict[ 'order' ] = order
        dict[ 'option' ] = None
        return Validation( True, '¿Desea ver el texto generado o el histograma de las frecuencias de las k tuplas de caractéres?' )
    
def get_markov_chain(k, words):
  markov_chain, n_words = {}, len(words)
  for i in range(n_words - k):
    curr_state = ()
    for j in range(i, i + k):
      curr_state = curr_state + (words[j],)
    if (i == 0):
      first_state = curr_state
    word_after = words[j + 1]
    if curr_state not in markov_chain.keys():
      markov_chain[curr_state] = []
    markov_chain[curr_state].append(word_after)
  return markov_chain, first_state

def get_words(plain_text):
  plain_text = plain_text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
  words = plain_text.split(' ')
  words = [word for word in words if word not in ['', ' ', '  ', '  ']]
  return words

def get_fake_text(markov_chain, curr_state, n, k):
  fake_text = list(curr_state)
  markov_keys = [list(key) for key in markov_chain.keys()]
  for i in range(n - k):
    try:
      next_word = random.choice(markov_chain[curr_state])
      fake_text.append(next_word)
      curr_state = ()
      for j in range(len(fake_text) - k, len(fake_text)):
        curr_state = curr_state + (fake_text[j],)
    except KeyError:
        curr_state = tuple(markov_keys[0]) 
  fake_text_string = ' '.join(fake_text)
  return fake_text_string
    
def isHistogramOrText( msg: str, dctionary ):

    if dctionary['option'] != 'texto':

        msg = msg.lower()
        dctionary['option'] = msg
        match dctionary['option']:
            case 'histograma':
                ngram_freq = nltk.FreqDist(ngrams( get_words( dctionary['text'] ) , dctionary['order']))
                freq_dist = {', '.join(key): value for key, value in dict(ngram_freq).items()}
                df_freq_dist = pd.DataFrame(pd.Series(dict(freq_dist))).reset_index()
                df_freq_dist = df_freq_dist.rename(columns={'index': 'k-grama', 0: 'frecuencia'})
                df_freq_dist['k-grama'] = df_freq_dist['k-grama'].astype(str)
                df_freq_dist = df_freq_dist.sort_values(by='frecuencia', ascending=False).head(10)
                fig, ax = plt.subplots(figsize=(15,10))
                sns.barplot(data=df_freq_dist, y='k-grama', x='frecuencia',palette='crest', ax=ax)
                ax.set_xlabel('Frecuencia')
                ax.set_title(f"Histograma de distribucion de frecuencias de los {dctionary['order']}-gramas")
                ax.grid(axis='x')
                ax.tick_params(axis='y', labelsize=10)
                sns.despine()
                plt.tight_layout()
                salt = str(random.randint(0,100000))
                fname = 'plot'+salt+'.png'
                plt.savefig( fname )
                return ValidationWithImage( False, 'Gráfico resultante', fname, 'Ingrese otra opción' )
            case 'texto':
                return Validation( False, '¿Cual es la cantidad de caractéres que debe tener el texto generado?' )
            case 'salir':
                return Validation( True, 'Ha decidido salir' )
            case _:
                return Validation( False, 'Ingrese una opción válida' )
    else:
        try:
            n = int(msg)
        except ValueError:
            return Validation( False, "Por favor ingrese un numero entero" )
        else:
            dctionary['option'] = None

            words = get_words( dctionary['text'] )
            markov_model, first_state = get_markov_chain( dctionary['order'], words )
            fake_text = get_fake_text(markov_model, first_state, n, dctionary['order'])
            if len(fake_text) > 4000:
               fake_text = fake_text[:4000]
            return Validation( False, fake_text )
        
class MarkovArgument( Argument ):
    def __init__(self, userId: int, isGroup: bool) -> None:
        super().__init__(userId, isGroup, [ getUrl, getMarkovOrder, isHistogramOrText ])