from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from ..models import User, Score
from datetime import datetime
from ..security import get_user
import random

#word game word generator/ generador de palabras para el juego de la palabra misteriosa
words = ['perro','gato','cama','pedo']
letters = []

words = set(words)
words = list(words)
def word_generator():
    for word in words:
        yield word
g = word_generator()
word = next(g)
rword = list(word)

#Views class/ Clase vistas
@view_defaults(renderer='../templates/home.jinja2')
class Game:
    def __init__(self, request):
        self.request = request
        self.db = self.request.dbsession
        self.letter = []

    #number game view/ vista de number game
    @view_config(route_name='number_game', renderer='../templates/number_game.jinja2')
    def number_game(self):
        username = self.request.matchdict['user']
        user = self.db.query(User).filter_by(name=username).first()
        next_url = self.request.route_url('number_game', user=username)

        # if no user no func/si no hay usuario no hay funcion
        # User validation/validacion de usuario
        if self.out_or_stay(username=username): return HTTPFound(location='/error')

        if not next_url:
            next_url = self.request.route_url('home')

        if 'form.submitted' in self.request.params:
            selected_number = self.request.params['selected_number']
            random_number = random.randint(0, 10)
            if int(selected_number) == random_number:
                win_score = 50
                score = [s for s in self.db.query(Score.user_id).all() for s in s]
                if user.id in score:
                    self.db.query(Score).filter_by(user_id=user.id).update(
                        {Score.score: Score.score+win_score, Score.date: datetime.utcnow()},
                        synchronize_session=False)
                    actual_score = self.db.query(Score).filter_by(user_id=user.id).first()
                    self.request.session.flash(f'YES! {user.name}, you have sumed 10 points and your actual score is {actual_score.score}', queue='', allow_duplicate=True)
                    return HTTPFound(location=next_url)
                else:
                    new_score = Score(score=win_score, user_id=user.id)
                    self.db.add(new_score)
            else:
                self.request.session.flash(
                    f'My number was {random_number} {user.name} you fail! jaja Try again', queue='',
                    allow_duplicate=True)

        return {'name': 'Number Game', 'user': user, 'next_url': next_url}


    #number game view/ vista de number game
    @view_config(route_name='word_game', renderer='../templates/word_game.jinja2')
    def word_game(self):
        global rword, word, letters
        len_word = len(word)
        username = self.request.matchdict['user']
        user = self.db.query(User).filter_by(name=username).first()
        next_url = self.request.route_url('word_game', user=username)

        # if no user no func/si no hay usuario no hay funcion
        # User validation/validacion de usuario
        if self.out_or_stay(username=username): return HTTPFound(location='/error')

        if not next_url:
            next_url = self.request.route_url('home')

        if 'form.submitted' in self.request.params:
            selected_letter = self.request.params['selected_letter']

            if selected_letter in rword or list(selected_letter) == list(word):
                while selected_letter in rword:
                    letters.append(selected_letter)
                    rword.remove(selected_letter)
                    self.request.session.flash(
                        f'Yes {selected_letter} is in the misterious word, continue!', queue='',
                        allow_duplicate=True)

                if list(selected_letter) == list(word) or rword == []:
                    win_score = 50
                    score = [s for s in self.db.query(Score.user_id).all() for s in s]
                    if user.id in score:
                        update_score = self.db.query(Score).filter_by(user_id=user.id).update(
                            {Score.score: Score.score + win_score, Score.date: datetime.utcnow()},
                            synchronize_session=False)
                        actual_score = self.db.query(Score).filter_by(user_id=user.id).first()
                        self.request.session.flash(
                            f'Yes {word} was the misterious word, you win 50 points! try a next word your actual score is {actual_score.score}',
                            queue='',
                            allow_duplicate=True)
                        try:
                            word = next(g)
                            rword = list(word)
                        except StopIteration:
                            pass
                        letters = []
                        return HTTPFound(location=next_url)

                    else:
                        new_score = Score(score=win_score, user_id=user.id)
                        self.db.add(new_score)
                        actual_score = self.db.query(Score).filter_by(user_id=user.id).first()
                        self.request.session.flash(
                            f'Yes {word} was the misterious word, you win 50 points!  your actual score is {actual_score.score}',
                            queue='',
                            allow_duplicate=True)
                        try:
                            word = next(g)
                            rword = list(word)
                        except StopIteration:
                            pass
                        letters = []
                return HTTPFound(location=next_url)


            if rword != [] and selected_letter not in rword:
                self.request.session.flash(
                    f'No {selected_letter} is not in the misterious word, continue!', queue='',
                    allow_duplicate=True)
                return HTTPFound(location=next_url)


        return {'name': 'Misterious word game', 'user': user, 'next_url': next_url, 'letters':letters, 'len_word':len_word}#, 'users_posts':users_posts}#, 'score':score.score}


    #pseudodecorator
    def out_or_stay(self, username=None):
        # if no user no func/si no hay usuario no hay funcion
        if self.request.user is None: return True

        # Role or username validation/validacion de rol
        user = get_user(self.request)
        if user.role != 'admin' and username is None: return True
        if user.role == 'admin' and username is None: return False
        if username != user.name: return True
        else: return False
