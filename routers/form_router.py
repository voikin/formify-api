from typing import Annotated, List

from fastapi import APIRouter, Depends
from starlette import status

from schemas.form_schemas import NewFormRequest, AnswerToSubmit, NewForm
from services.form_service import FormService, form_service
from services.user_service import current_user

router = APIRouter(
    prefix='/api/form',
    tags=['form'],
)


@router.get('/{test_id}')
async def get_form_by_id(test_id: int, user: current_user, forms_service: Annotated[FormService, Depends(form_service)]):
    return await forms_service.get_form_by_id(test_id)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_form(user: current_user, forms_service: Annotated[FormService, Depends(form_service)], new_form: NewFormRequest):
    form_id = await forms_service.create_form(new_form.form, user.id)
    return {'id': form_id}


@router.get('/')
async def get_user_forms(user: current_user, forms_service: Annotated[FormService, Depends(form_service)]):
    return await forms_service.get_users_forms(user.id)


@router.post('/{test_id}')
async def submit_form(forms_service: Annotated[FormService, Depends(form_service)], test_id: int, answers: List[AnswerToSubmit]):
    return await forms_service.submit_form(test_id, answers)


@router.delete('/{test_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(user: current_user, test_id: int, forms_service: Annotated[FormService, Depends(form_service)]):
    await forms_service.delete_form(test_id, user.id)


@router.put('/', status_code=status.HTTP_200_OK)
async def update_form(user: current_user, form: NewForm, forms_service: Annotated[FormService, Depends(form_service)]):
    form_id = await forms_service.update_form(form, user.id)
    return {'id': form_id}
