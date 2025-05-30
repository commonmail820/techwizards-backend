from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import enum

class Category(str, enum.Enum):
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"
    BEVERAGE = "Beverage"
    SIDE = "Side"

class SpiceLevel(int, enum.Enum):
    MILD = 1
    MEDIUM = 2
    HOT = 3
    EXTRA_HOT = 4

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(Enum(Category))
    image_url = Column(String)
    spice_level = Column(Integer, nullable=True)
    is_vegetarian = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="menu_item")

class MenuCategory(Base):
    __tablename__ = "menu_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    display_order = Column(Integer, default=0) 