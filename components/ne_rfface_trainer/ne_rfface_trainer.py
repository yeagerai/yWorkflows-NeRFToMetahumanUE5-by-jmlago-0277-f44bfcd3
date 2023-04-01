
import os
from typing import List

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent

# Replace these imports and class definitions with the appropriate ones
# representing the NeRFModel and DepthMap that would be used in this component.
from some_module import Image, NeRFModel, DepthMap


class NeRFFaceTrainerInputDict(BaseModel):
    processed_image_sequence: List[Image]


class NeRFFaceTrainerOutputDict(BaseModel):
    trained_neRF_model: NeRFModel
    generated_depth_maps: List[DepthMap]


class NeRFFaceTrainer(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.learning_rate: float = yaml_data["parameters"]["learning_rate"]
        self.num_epochs: int = yaml_data["parameters"]["num_epochs"]
        self.batch_size: int = yaml_data["parameters"]["batch_size"]

    def transform(
        self, args: NeRFFaceTrainerInputDict
    ) -> NeRFFaceTrainerOutputDict:
        # Initialize NeRF model with the given parameters
        nerf_model = NeRFModel(learning_rate=self.learning_rate)

        # Load processed image sequence
        processed_image_sequence = args.processed_image_sequence

        # Split image sequence into training and validation sets
        training_set, validation_set = self.split_image_sequence(processed_image_sequence)

        # Train NeRF model on the training set for the specified number of epochs and batch size
        nerf_model.train(training_set, num_epochs=self.num_epochs, batch_size=self.batch_size)

        # Validate NeRF model on the validation set
        nerf_model.validate(validation_set)

        # Generate depth maps using the trained NeRF model
        depth_maps = nerf_model.generate_depth_maps()

        # Return the trained NeRF model and generated depth maps
        output = NeRFFaceTrainerOutputDict(
            trained_neRF_model=nerf_model,
            generated_depth_maps=depth_maps,
        )
        return output

    def split_image_sequence(self, image_sequence: List[Image]):
        # Implement a strategy to split the image_sequence into training and validation sets
        pass


load_dotenv()
nerf_face_trainer_app = FastAPI()


@nerf_face_trainer_app.post("/transform/")
async def transform(
    args: NeRFFaceTrainerInputDict,
) -> NeRFFaceTrainerOutputDict:
    nerf_face_trainer = NeRFFaceTrainer()
    return nerf_face_trainer.transform(args)
