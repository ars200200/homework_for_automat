import enum
import random
import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, UUID, String, Integer, ForeignKey, JSON, DateTime, Boolean, Float, Enum, text, update, insert, select


engine = create_engine( 
    "postgresql://ubuntu:ilovecookies@localhost:5432/mydb",
     echo = True
) 


class Base(DeclarativeBase):
    pass


class UserBaseInfo(Base):
    __tablename__ = 'user_base_info'

    user_id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    encrypted_pass = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    points = Column(Integer)
    phone_number = Column(String)
    review_count = Column(Integer)
    review_sum = Column(Integer)
    

class DriverInfo(Base):
    __tablename__ = 'driver_info'

    user_id = Column(Integer, ForeignKey(UserBaseInfo.user_id), primary_key=True)
    license_number = Column(String)
    review_count = Column(Integer)
    review_sum = Column(Integer)


class UserBankCards(Base):
    __tablename__ = 'user_bank_cards'

    user_id = Column(Integer, ForeignKey(UserBaseInfo.user_id), primary_key=True)
    bank_card_number = Column(String, primary_key=True)
    encrypted_bank_data = Column(String)


class UserReviewsInfo(Base):
    __tablename__ = 'user_reviews_info'

    review_id = Column(UUID, primary_key=True)
    user_id = Column(Integer, ForeignKey(UserBaseInfo.user_id), primary_key=True)
    reviewer_user_id = Column(Integer, ForeignKey(UserBaseInfo.user_id), primary_key=True)
    score = Column(Integer)
    created_at = Column(DateTime)
    comment = Column(String, default="")
    is_client_review = Column(Boolean)


class Cars(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, primary_key=True)
    capacity = Column(Float)
    status = Column(Integer)
    model = Column(String)
    year_of_release = Column(DateTime)


class UserCars(Base):
    __tablename__ = 'user_cars'

    user_id = Column(Integer, ForeignKey(DriverInfo.user_id), primary_key=True)
    car_id = Column(Integer, ForeignKey(Cars.car_id), primary_key=True)
    date_from = Column(DateTime)
    date_to = Column(DateTime)


class Features(Base):
    __tablename__ = 'features'

    feature = Column(String, primary_key=True)
    description = Column(String, default='')


class CarFeatures(Base):
    __tablename__ = 'car_features'

    car_id = Column(Integer, ForeignKey(Cars.car_id), primary_key=True)
    feature = Column(String, ForeignKey(Features.feature), primary_key=True)


class Tariffs(Base):
    __tablename__ = 'tariffs'

    type = Column(String, primary_key=True)
    availability = Column(Integer)


class CarTypes(Base):
    __tablename__ = 'car_types'

    car_id = Column(Integer, ForeignKey(Cars.car_id), primary_key=True)
    type = Column(String, ForeignKey(Tariffs.type), primary_key=True)


class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(UUID, primary_key=True)
    price = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String)
    number_of_points_awarded = Column(Integer)
    promo = Column(String)


class EOrderStatus(enum.Enum):
    waiting = 'WAITING'
    accepted = 'ACCEPTED'
    rejected = 'REJECTED'
    canceled = 'CANCELED'
    finished = 'FINISHED'


class OrderInfo(Base):
    __tablename__ = 'order_info'

    order_id = Column(UUID, primary_key=True)
    client_user_id = Column(Integer, ForeignKey(UserBaseInfo.user_id))
    driver_user_id = Column(Integer, ForeignKey(DriverInfo.user_id))
    created_at = Column(DateTime)
    order_status = Column(Enum(EOrderStatus))
    map_coordinates = Column(JSON)
    payment_id = Column(UUID, ForeignKey(Payment.payment_id))
    tariff_type = Column(String, ForeignKey(Tariffs.type))


# Base.metadata.create_all(engine)


def create_users(count: int = 32):
    with engine.connect() as conn:
        for i in range(count):
            conn.execute(insert(UserBaseInfo).values(
                login=f'login_{i}_{random.randint(0, 9999999)}',
                encrypted_pass=f'encrypted_pass_{i}',
                email=f'email_{i}',
                name=f'name_{i}',
                surname=f'surname_{i}',
                points=10 * random.randrange(1, 16),
                phone_number=f'phone_number_{i}',
                review_count=random.randrange(1, 5),
                review_sum=random.randrange(1, 5),
            ))
        conn.commit()


def create_driver_users(count: int = 16):
    with engine.connect() as conn:
        for i in range(count):
            result = conn.execute(insert(UserBaseInfo).values(
                login=f'driver_login_{i}_{random.randint(0, 9999999)}',
                encrypted_pass=f'encrypted_pass_{i}',
                email=f'email_{i}',
                name=f'name_{i}',
                surname=f'surname_{i}',
                points=10 * random.randrange(1, 16),
                phone_number=f'phone_number_{i}',
                review_count=random.randrange(1, 5),
                review_sum=random.randrange(1, 5),
            ).returning(UserBaseInfo.user_id))
            
            conn.execute(insert(DriverInfo).values(
                user_id=result.fetchone()[0],
                license_number=f'license_number_{random.randint(0, 9999999)}',
                review_count=random.randint(0, 9999999),
                review_sum=random.randint(0, 9999999)
            ))
            
        conn.commit()


def create_tariffs(count: int = 16):
    with engine.connect() as conn:
        for i in range(count):
            conn.execute(insert(Tariffs).values(
                type=f'type_{i}',
                availability=random.randint(1, 5)
            ))
            
        conn.commit()


def create_features(count: int = 16):
    with engine.connect() as conn:
        for i in range(count):
            conn.execute(insert(Features).values(
                feature=f'feature_{i}',
                description=f'some description {i}'
            ))
            
        conn.commit()


def create_cars(count: int = 16):
    with engine.connect() as conn:
        for i in range(count):
            conn.execute(insert(Cars).values(
                capacity=random.randint(1, 100) / 10.0, 
                status=random.randint(1, 10), 
                model=f'model_{i}', 
                year_of_release=datetime.now(), 
            ))
            
        conn.commit()


def create_car_types():
    with engine.connect() as conn:
        cars = {car[0] for car in conn.execute(select(Cars)).all()}
        types = [type[0] for type in conn.execute(select(Tariffs)).all()]

        for car in cars:
            car_types = random.sample(types, random.randint(1, len(types)))
            for type in car_types:
                conn.execute(insert(CarTypes).values(
                    car_id=car,
                    type=type
                ))
            
        conn.commit()


def create_car_features():
    with engine.connect() as conn:
        cars = {car[0] for car in conn.execute(select(Cars)).all()}
        features = [feature[0] for feature in conn.execute(select(Features)).all()]

        for car in cars:
            car_features = random.sample(features, random.randint(1, len(features)))
            for feature in car_features:
                conn.execute(insert(CarFeatures).values(
                    car_id=car,
                    feature=feature
                ))
            
        conn.commit()
        

def create_car_payment(count : int = 16):
    with engine.connect() as conn:
        for i in range(count):
            conn.execute(insert(Payment).values(
                payment_id=uuid.uuid4(),
                price=random.randint(1, 99999) / 100.0,
                payment_method=f'payment_method_{i}',
                payment_status=f'payment_status_{i}',
                number_of_points_awarded=random.randint(1, 5),
                promo=f'promo_{i}'
            ))
            
        conn.commit()


def create_order_info(count : int = 16):
    with engine.connect() as conn:
        users = [user[0] for user in conn.execute(select(UserBaseInfo)).all()]
        drivers = [user[0] for user in conn.execute(select(DriverInfo)).all()]
        payments = [pay[0] for pay in conn.execute(select(Payment)).all()]
        tariff_types = [type[0] for type in conn.execute(select(Tariffs)).all()]

        for i in range(count):
            user = random.sample(users, 1)[0]
            driver = random.sample(drivers, 1)[0]
            conn.execute(insert(OrderInfo).values(
                order_id=uuid.uuid4(),
                client_user_id=user,
                driver_user_id=driver,
                created_at=datetime.now(),
                order_status=random.choice(list(EOrderStatus)).value,
                map_coordinates='{}',
                payment_id=random.sample(payments, 1)[0],
                tariff_type=random.sample(tariff_types, 1)[0]
            ))
            
        conn.commit()
        

def create_user_cars():
    with engine.connect() as conn:
        drivers = [user[0] for user in conn.execute(select(DriverInfo)).all()]
        cars = [car[0] for car in conn.execute(select(Cars)).all()]

        for driver in drivers:
            driver_cars = random.sample(cars, random.randint(1, len(cars)))
            for car in driver_cars:
                conn.execute(insert(UserCars).values(
                    user_id=driver,
                    car_id=car,
                    date_from=datetime.now(),
                    date_to=datetime.now()
                ))
            
        conn.commit()


def create_user_bank_cards():
    with engine.connect() as conn:
        users = [user[0] for user in conn.execute(select(UserBaseInfo)).all()]

        for user in users:
            conn.execute(insert(UserBankCards).values(
                user_id=user,
                bank_card_number=f'tinkoff_{uuid.uuid4()}',
                encrypted_bank_data=f'abracadabra_{uuid.uuid4()}'
            ))
        
        conn.commit()


def create_user_reviews_info(count : int = 16):
    with engine.connect() as conn:
        users = [user[0] for user in conn.execute(select(UserBaseInfo)).all()]

        for i in range(count):
            couple = random.sample(users, 2)
            conn.execute(insert(UserReviewsInfo).values(
                review_id=uuid.uuid4(),
                user_id=couple[0],
                reviewer_user_id=couple[1],
                score=random.randint(1, 500),
                created_at=datetime.now(),
                is_client_review=True
            ))
        
        conn.commit()


if __name__ == '__main__':
    with engine.connect() as conn:
        conn.execute(text(open('tables_creation.sql', 'r').read()))
        conn.commit()

    create_users()
    create_driver_users()
    create_tariffs()
    create_features()
    create_cars()
    create_car_features()
    create_car_types()
    create_car_payment()
    create_order_info()
    create_user_cars()
    create_user_bank_cards()
    create_user_reviews_info()
