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



@router_in_member.get("/{id}")
def member_by_id(id:int):
    return instance.get_member_by_id(id)




@router_in_member.put("/{id}")
def update_member(id, data:dict):
    return instance.update_member(id,data)


@router_in_member.put("/{id}/deactivate")
def update_deactivate_member(id:int):
    return instance.deactivate_member(id)

@router_in_member.put("/{id}/activate")
def update_activate_member(id:int):
    return instance.activate_member(id)



