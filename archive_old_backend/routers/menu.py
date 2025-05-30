from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.menu import MenuItem, MenuCategory, Category, SpiceLevel
from models.user import User, UserRole
from utils.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter()

# Pydantic models for request/response
class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float
    category: Category
    image_url: Optional[str] = None
    spice_level: Optional[int] = None
    is_vegetarian: bool = False
    is_available: bool = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# Menu Category schemas
class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    display_order: int = 0

class MenuCategoryCreate(MenuCategoryBase):
    pass

class MenuCategoryUpdate(MenuCategoryBase):
    pass

class MenuCategoryResponse(MenuCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# Helper function to check if user is admin
async def is_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can perform this action"
        )
    return user

# Menu Items endpoints
@router.get("/items", response_model=List[MenuItemResponse])
async def get_menu_items(
    category: Optional[Category] = None,
    is_vegetarian: Optional[bool] = None,
    is_available: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MenuItem)
    
    if category:
        query = query.filter(MenuItem.category == category)
    if is_vegetarian is not None:
        query = query.filter(MenuItem.is_vegetarian == is_vegetarian)
    if is_available is not None:
        query = query.filter(MenuItem.is_available == is_available)
    
    return query.all()

@router.get("/items/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.post("/items", response_model=MenuItemResponse)
async def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin)
):
    db_item = MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/items/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    item: MenuItemUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin)
):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
async def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin)
):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Menu item deleted successfully"}

# Menu Categories endpoints
@router.get("/categories", response_model=List[MenuCategoryResponse])
async def get_menu_categories(db: Session = Depends(get_db)):
    return db.query(MenuCategory).order_by(MenuCategory.display_order).all()

@router.get("/categories/{category_id}", response_model=MenuCategoryResponse)
async def get_menu_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories", response_model=MenuCategoryResponse)
async def create_menu_category(
    category: MenuCategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin)
):
    db_category = MenuCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/categories/{category_id}", response_model=MenuCategoryResponse)
async def update_menu_category(
    category_id: int,
    category: MenuCategoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin)
):
    db_category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}")
async def delete_menu_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin)
):
    db_category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if there are any menu items in this category
    items_count = db.query(MenuItem).filter(MenuItem.category == db_category.name).count()
    if items_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with existing menu items"
        )
    
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"} 