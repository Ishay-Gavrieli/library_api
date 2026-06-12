from fastapi import APIRouter
from database.member_db import Members


instance = Members()


router_in_member = APIRouter()



@router_in_member.post("")
def create_member(data:dict):
    return instance.create(data)


@router_in_member.get("")
def all_members():
    return instance.get_all_members()