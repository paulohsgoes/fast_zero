from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
      username='Paulo', password='111111', email='mail@server.com'
    )
    session.add(user)
    session.commit()
    result = session.scalar(
       select(User).where(User.email == 'mail@server.com')
    )

    assert result.username == 'Paulo'
