from sqlalchemy import String, Integer, Column, ForeignKey, Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base =declarative_base()



# rest_customer = Table(
#     'rest_customers',
#     Base.metadata,
#     Column('restaurant_id', ForeignKey('restaurant_id'), primary_key=True),
#     Column('customer_id', ForeignKey('customer_id'), primary_key=True),
#     extend_existing=True,
# )   

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer(), primary_key = True)
    name = Column(String())
    reg_number = Column(String())
    price = Column(Integer())
    
    
    reviews = relationship('Review', backref=backref('restaurant'))
    customers =relationship('Customer', secondary ='review', back_populates=('restaurants'))
    # customers =relationship('Customer', secondary =rest_customer, back_populates=('restaurants'))
    
    def __repr__(self):
        return f'Reataurant(id={self.id}: ' +\
            f'name={self.name}, ' +\
            f'reg_number={self.reg_number}, ' +\
            f'price={self.price})'
   
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()
 
    def all_reviews(self):
        review_collections = []
        
        for review in self.reviews:
            customer_fullname = f"{review.customer.first_name} {review.customer.last_name}"
            all_reviews = f"Review for {self.name} by {customer_fullname}: {review.star_rating} stars."
            review_collections.append(all_reviews)
            
        return review_collections
    

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    gender = Column(String())
    
    reviews = relationship('Review', backref=backref('customer'))
    restaurants =relationship('Restaurant', secondary ='review', back_populates=('customers'))
    # restaurants =relationship('Restaurant', secondary =rest_customer, back_populates=('customers'))
    
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
        review = Review(restaurant = restaurant, rating=rating)
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




engine = create_engine('sqlite:///restaurant.db', echo=True)
Base.metadata.create_all(bind=engine)
Session=sessionmaker(bind=engine)
session = Session()

customer1 = Customer(first_name="Debby", last_name="Olu", gender= "F")
customer2 = Customer(first_name="Sam", last_name="Okin", gender= "M")
customer3 = Customer(first_name="Don", last_name="Kim", gender= "M")
customer4 = Customer(first_name="Alfred", last_name="Ola", gender= "M")
customer5 = Customer(first_name="Debby", last_name="Jones", gender= "F")

session.add(customer1)
session.add(customer2)
session.add(customer3)
session.add(customer4)
session.add(customer5)

session.commit()


# Insert Restaurant values
snail_cafe = Restaurant(name="Snail Cafe", reg_number="AD34567", price=700)
stainless = Restaurant(name="Stainless Food", reg_number="AB74564", price=500)
kilmongaro = Restaurant(name="Kilmongaro", reg_number="RF45362", price=1000)
dodo_pizza = Restaurant(name="Dodo Pizza", reg_number="QT63798", price=750)
kings_bites = Restaurant(name="Kings Bites", reg_number="DD234157", price=5000)
mr_lass_kitchen = Restaurant(name="Mr. Las Kitchen", reg_number="RC012895", price=3000)

# Add session data
session.add(snail_cafe)
session.add(stainless)
session.add(kilmongaro)
session.add(dodo_pizza)
session.add(kings_bites)
session.add(mr_lass_kitchen)

session.commit()


print(customer1.full_name())