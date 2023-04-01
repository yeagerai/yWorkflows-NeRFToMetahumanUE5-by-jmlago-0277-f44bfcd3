
import typing
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from core.workflows.abstract_workflow import AbstractWorkflow

class ImageSequenceInputBaseModel(BaseModel):
    images: typing.List[typing.Dict[str, typing.Any]]
    camera_parameters: typing.List[typing.Dict[str, typing.Any]]

class MetahumanUE5OutputBaseModel(BaseModel):
    metahuman_model: str
    unreal_engine_version: str

class NeRFToMetahumanUE5(AbstractWorkflow):
    def __init__(self) -> None:
        super().__init__()

    async def transform(
        self, args: ImageSequenceInputBaseModel, callbacks: typing.Any
    ) -> MetahumanUE5OutputBaseModel:
        results_dict = await super().transform(args=args, callbacks=callbacks)
        metahuman_model = results_dict[0].metahuman_model
        unreal_engine_version = results_dict[1].unreal_engine_version
        out = MetahumanUE5OutputBaseModel(
            metahuman_model=metahuman_model,
            unreal_engine_version=unreal_engine_version,
        )
        return out

load_dotenv()
nerf_to_metahuman_ue5_app = FastAPI()

@nerf_to_metahuman_ue5_app.post("/transform/")
async def transform(
    args: ImageSequenceInputBaseModel,
) -> MetahumanUE5OutputBaseModel:
    nerf_to_metahuman_ue5 = NeRFToMetahumanUE5()
    return await nerf_to_metahuman_ue5.transform(args, callbacks=None)
