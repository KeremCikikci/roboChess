import berserk

GAME_ID = 'TqIKcMks2dA1'

API_TOKEN = 'lip_LaYVt0nOKwUnjEv1gJSZ'
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

berserk.clients.Board(session=session).offer_draw(GAME_ID)

#berserk.clients.Board(session=session).make_move(GAME_ID, "b2b4")