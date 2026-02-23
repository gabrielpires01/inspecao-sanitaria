from app.services.irregularities import IrregularityService
from fastapi import Depends
from app.core.database import get_db
from app.services.users import UserService
from app.services.auth import AuthService
from app.services.establishments import EstablishmentService
from app.services.inspections import InspectionService


def get_user_service(db=Depends(get_db)) -> UserService:
    return UserService(db=db)


def get_auth_service(db=Depends(get_db)) -> AuthService:
    return AuthService(db=db)


def get_establishment_service(
    db=Depends(get_db)
) -> EstablishmentService:
    return EstablishmentService(db=db)


def get_inspection_service(
    db=Depends(get_db)
) -> InspectionService:
    return InspectionService(db=db)


def get_irregularity_service(
    db=Depends(get_db),
    inspection_service: InspectionService = Depends(get_inspection_service)
) -> IrregularityService:
    return IrregularityService(db=db, inspection_service=inspection_service)
