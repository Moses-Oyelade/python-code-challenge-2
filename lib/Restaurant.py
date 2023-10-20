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
    
    def full_name(self):
        firstname = self.first_name 
        lastname= self.last_name
        return firstname + lastname

    def favorite_restaurant(self):
        for review in self.reviews:
            highest_rating = session.query(review.rating).order_by(
            review.rating).first()
        return highest_rating
    
    def add_review(self, restaurant, rating):
        review = Review(restaurant = restaurant, star_rating=rating)
        session.add(review)
        session.commit()
        
    def delete_reviews(restaurant):
        remove_reviews = set()
        for review in remove_reviews:
            if review.restaurant == restaurant:
                remove_reviews.append(review)
        
        for review in remove_reviews:
            session.delete(review)
            session.commit()
    
            
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer(), primary_key=True)
    rating = Column(Integer())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.full_name()}: {self.rating} stars"




engine = create_engine('sqlite:///restaurants.db', echo=True)
Base.metadata.create_all(bind=engine)
Session=sessionmaker(bind=engine)
session = Session()