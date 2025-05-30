from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.order import Order, OrderItem, OrderStatus, PaymentStatus, PaymentMethod
from models.menu import MenuItem
from models.user import User, UserRole
from utils.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter()

# Pydantic models for request/response
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    special_instructions: Optional[str] = None

class OrderItemResponse(OrderItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    unit_price: float
    total_price: float

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    special_instructions: Optional[str] = None
    is_takeout: bool = False
    table_number: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    special_instructions: Optional[str] = None

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    payment_status: PaymentStatus
    payment_method: Optional[PaymentMethod]
    created_at: datetime
    updated_at: datetime
    special_instructions: Optional[str]
    is_takeout: bool
    table_number: Optional[int]
    items: List[OrderItemResponse]

# Helper function to check if user is staff (admin or worker)
async def is_staff(user: User = Depends(get_current_user)):
    if user.role not in [UserRole.ADMIN, UserRole.WORKER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff members can perform this action"
        )
    return user

# Order endpoints
@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    status: Optional[OrderStatus] = None,
    payment_status: Optional[PaymentStatus] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Order)
    
    # Regular users can only see their own orders
    if user.role == UserRole.CUSTOMER:
        query = query.filter(Order.user_id == user.id)
    
    if status:
        query = query.filter(Order.status == status)
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)
    
    return query.order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user has permission to view this order
    if user.role == UserRole.CUSTOMER and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Calculate total amount and validate menu items
    total_amount = 0
    order_items = []
    
    for item in order.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail=f"Menu item {menu_item.name} is not available")
        
        item_total = menu_item.price * item.quantity
        order_items.append(
            OrderItem(
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                unit_price=menu_item.price,
                total_price=item_total,
                special_instructions=item.special_instructions
            )
        )
        total_amount += item_total

    # Create order
    db_order = Order(
        user_id=user.id,
        total_amount=total_amount,
        special_instructions=order.special_instructions,
        is_takeout=order.is_takeout,
        table_number=order.table_number,
        payment_method=order.payment_method,
        items=order_items
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Only staff can update order status
    if order_update.status or order_update.payment_status:
        if user.role not in [UserRole.ADMIN, UserRole.WORKER]:
            raise HTTPException(status_code=403, detail="Only staff can update order status")
    
    # Regular users can only update their own orders
    if user.role == UserRole.CUSTOMER and db_order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    
    # Update order
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Only admin can delete orders
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin can delete orders")
    
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}

# Staff-only endpoints
@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    _: User = Depends(is_staff),
    db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/{order_id}/payment", response_model=OrderResponse)
async def update_payment_status(
    order_id: int,
    payment_status: PaymentStatus,
    _: User = Depends(is_staff),
    db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.payment_status = payment_status
    db.commit()
    db.refresh(db_order)
    return db_order 