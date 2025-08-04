from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import NoResultFound
from ..models.models import Product
from ..schemas.schemas import ProductRequest
from ..scrapers.scraping import fetch_page, parse_page
from ..services.product import list_all_products, list_product_by_id, add_product, delete_product
from ..services.alert import create_alert
from ..telegram.notifier import notify_product_added, notify_product_deleted
from ..core.db import get_session

router = APIRouter()

@router.get("/products", response_model=list[Product])
async def get_all_products(session = Depends(get_session)):
    products = list_all_products(session)
        
    if not products:
        return HTTPException(status_code=404, detail="Products not found")
    
    return products


@router.get("/products/{id}/", response_model=Product)
async def get_product_by_id(id: int, session = Depends(get_session)):
    
    product = list_product_by_id(session, id)

    if not product:
        return HTTPException(status_code=404, detail="Product not found")

    return product

@router.post("/products/add", response_model=Product)
async def track_product(data: ProductRequest, session = Depends(get_session)):
    if not data.url:
        raise HTTPException(status_code=400, detail="Invalid URL")

    page_content = fetch_page(data.url)
    product_data = parse_page(page_content, data.url)
    product = add_product(session, product_data)

    create_alert(
        session=session,
        product_id=product.id,
        telegram_chat_id=data.telegram_chat_id,
        target_price=data.target_price
    )

    await notify_product_added(data.telegram_chat_id, product.product_name)
        
    return product_data

@router.delete("/products/{id}", status_code=status.HTTP_200_OK)
async def delete_product_by_id(id: int, session=Depends(get_session)):
    try:
        product = delete_product(session, id)
        await notify_product_deleted(product.alert.telegram_chat_id, product)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Product not found")