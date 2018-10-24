from unittest import TestCase
 
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, Event, Member, Token, User
import datetime

class TestDatabase(TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite://', echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    ########
    # User #
    ########
    def test_add_wrong_user(self):
        user = User(id=1, created_at = '2')
        with self.assertRaises(Exception):
            self.session.add(user)
            self.session.commit()
        
        user = User(id=1, name = 'test', avatar = 'avatar', active = True, tokens = 'tok', created_at = datetime.datetime.now())
        with self.assertRaises(Exception):
            self.session.add(user)
            self.session.commit()

    def test_add_user(self):
        user = User(id=1, email = 'ex@example.fr', name = 'test', avatar = 'avatar', active = True, tokens = 'tok', created_at = datetime.datetime.now())
        self.session.add(user)
        self.session.commit()
        self.assertEqual(self.session.query(User).count(), 1)
        

    #########
    # Event #
    #########
    def test_add_wrong_event(self):
        event = Event(id=1, name = 'test', server = '2', date = '2')
        with self.assertRaises(Exception):
            self.session.add(event)
            self.session.commit()

    def test_add_event(self):
        event = Event(id=2, name = 'test', server = '2', date = datetime.datetime.now())
        self.session.add(event)
        self.session.commit()
        self.assertEqual(self.session.query(Event).filter(Event.id == 2).count(), 1)

    ##########
    # Member #
    ##########
    def test_add_member(self):
        member = Member(id=2, name = 'test', avatar = '2', level=0, experience=5)
        self.session.add(member)
        self.session.commit()
        self.assertEqual(self.session.query(Member).filter(Member.id == 2).count(), 1)

    #########
    # Token #
    #########
    def test_add_wrong_token(self):
        token = Token(date = '2', price = 10)
        with self.assertRaises(Exception):
            self.session.add(token)
            self.session.commit()

    def test_add_token(self):
        token = Token(date = datetime.datetime.now(), price = 10)
        self.session.add(token)
        self.session.commit()
        self.assertEqual(self.session.query(Token).count(), 1)


    def tearDown(self):
        self.session.close()