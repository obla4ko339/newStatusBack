from typing import List, Optional
from fastapi import APIRouter, HTTPException,File,UploadFile
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.sites import crud_create_sites,crud_get_sites,crud_get_sites_user_id,crud_get_sites_search,crud_get_site_id,crud_update_data
from src.crud.loading import loading_file, get_pay_phone

import csv;
import io;
from datetime import datetime, timezone

router = APIRouter(prefix="/loading", tags=["sites"])



class LoadingFile(BaseModel):
    id: str
    filename: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
 
@router.post("/file1c")
async def upload_file(
    file: UploadFile = File(...), 
): 
    
    content = await file.read()
    parseData = parse_csv(content)
    result = await loading_file(parseData)
    return result
    # print(parseData) 
    # try:
    #     sites = Sites()
    #     data = await sites.getSite()
    #     return data
    # except DoesNotExist:
    #     raise HTTPException(status_code=404, detail="Object not found")



class GetPayPhone(BaseModel):
    phone: str
@router.post("/get_pay_phone")
async def upload_file(
    phone: GetPayPhone, 
): 
    res = await get_pay_phone(phone.phone)
    return dict(res)
    
    
    # print(parseData) 
    # try:
    #     sites = Sites()
    #     data = await sites.getSite()
    #     return data
    # except DoesNotExist:
    #     raise HTTPException(status_code=404, detail="Object not found")




def parse_csv(content):

    content_str = content.decode('utf-8-sig')
    csv_file = io.StringIO(content_str)

    fieldnames = ['phone', 'dogovor', 'dolg', 'pay', 'pre_pay', 'bill_status']
    reader = csv.DictReader(csv_file, fieldnames=fieldnames, delimiter=';')
    results = []
    for row in reader:
        if row is None:
            del row[None]
        if row['pay'] == '':
            row['pay'] = None 
        if row['phone']:
            row['phone'] = row['phone'].lstrip("+")
        # row['date'] = 'NOW()'
        row['user_loading'] = 20
        results.append(row)

    # print(results)
    return results
 