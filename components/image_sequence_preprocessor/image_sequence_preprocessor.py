
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent

class Image:
    # Implement your Image class here, or import it from another module.

class ImageSequencePreprocessorInput(BaseModel):
    raw_image_sequence: List[Image]
    raw_camera_parameters: Dict[str, Any]
    alignment_method: str = 'feature_based'
    resize_dimension: List[int] = [800, 600]
    color_correction_method: str = 'histogram_equalization'


class ImageSequencePreprocessorOutput(BaseModel):
    processed_image_sequence: List[Image]
    updated_camera_parameters: Dict[str, Any]


class ImageSequencePreprocessor(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(
        self, args: ImageSequencePreprocessorInput
    ) -> ImageSequencePreprocessorOutput:
        
        # 1. Align the raw_image_sequence
        aligned_image_sequence = self.align_images(
            args.raw_image_sequence,
            args.alignment_method
        )

        # 2. Resize the aligned_image_sequence
        resized_image_sequence = self.resize_images(
            aligned_image_sequence,
            args.resize_dimension
        )

        # 3. Perform color correction on the resized_image_sequence
        processed_image_sequence = self.color_correct_images(
            resized_image_sequence,
            args.color_correction_method
        )

        # 4. Update the camera parameters
        updated_camera_parameters = self.update_camera_parameters(
            args.raw_camera_parameters,
            args.alignment_method,
            args.resize_dimension
        )

        # 5. Return the processed_image_sequence and updated_camera_parameters
        output = ImageSequencePreprocessorOutput(
            processed_image_sequence=processed_image_sequence,
            updated_camera_parameters=updated_camera_parameters
        )
        return output
    
    def align_images(self, raw_image_sequence: List[Image], alignment_method: str) -> List[Image]:
        # Implement image alignment functionality here
        pass

    def resize_images(self, aligned_image_sequence: List[Image], resize_dimension: List[int]) -> List[Image]:
        # Implement image resizing functionality here
        pass

    def color_correct_images(self, resized_image_sequence: List[Image], color_correction_method: str) -> List[Image]:
        # Implement color correction functionality here
        pass

    def update_camera_parameters(self, raw_camera_parameters: Dict[str, Any], alignment_method: str, resize_dimension: List[int]) -> Dict[str, Any]:
        # Implement updated camera parameters functionality here
        pass

load_dotenv()
image_seq_preprocessor_app = FastAPI()


@image_seq_preprocessor_app.post("/transform/")
async def transform(
    args: ImageSequencePreprocessorInput,
) -> ImageSequencePreprocessorOutput:
    image_seq_preprocessor = ImageSequencePreprocessor()
    return image_seq_preprocessor.transform(args)
