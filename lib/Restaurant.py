from sqlalchemy import String, Integer, create_engine, Column, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base =declarative_base()



rest_customer = Table(
    'rest_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurant_id'), primary_key=True),
    Column('customer_id', ForeignKey('customer_id'), primary_key=True),
    extend_existing=True,
)   

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer(), primary_key = True)
    name = Column(String())
    reg_number = Column(String())
    price = Column(Integer())
    
    
    reviews = relationship('Review', backref=backref('restaurant'))
    customers =relationship('Customer', secondary =rest_customer, back_populates=('restaurants'))
    
    def __repr__(self):
        return f'Reataurant(id={self.id}: ' +\
            f'name={self.name}, ' +\
            f'reg_number={self.reg_number}, ' +\
            f'price={self.price})'
   
    

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    gender = Column(String())
    
    reviews = relationship('Review', backref=backref('customer'))
    restaurants =relationship('Restaurant', secondary =rest_customer, back_populates=('customers'))
    
    def __repr__(self):
        return f'Customer(id={self.id}: ' +\
            f'first_name={self.first_name}, ' +\
            f'last_name={self.last_name}, ' +\
            f'gender={self.gender})'
    

            
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer(), primary_key=True)
    rating = Column(Integer())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    
   



engine = create_engine('sqlite:///restaurants.db', echo=True)
Base.metadata.create_all(bind=engine)
Session=sessionmaker(bind=engine)
session = Session()