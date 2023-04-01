
import pytest
import typing
from pydantic import BaseModel
from fastapi.testclient import TestClient
from app import nerf_to_metahuman_ue5_app, ImageSequenceInputBaseModel, MetahumanUE5OutputBaseModel

client = TestClient(nerf_to_metahuman_ue5_app)

@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        (
            ImageSequenceInputBaseModel(
                images=[
                    {"url": "https://example.com/image1.jpg", "timestamp": "2021-01-01 00:00:00"},
                    {"url": "https://example.com/image2.jpg", "timestamp": "2021-01-02 00:00:00"},
                ],
                camera_parameters=[
                    {"focal_length": 35, "sensor_width": 36, "sensor_height": 24},
                ],
            ),
            MetahumanUE5OutputBaseModel(
                metahuman_model="https://example.com/metahuman_model.fbx",
                unreal_engine_version="4.27",
            ),
        ),
        (
            ImageSequenceInputBaseModel(
                images=[
                    {"url": "https://example.com/image1.png", "timestamp": "2021-12-31 00:00:00"},
                ],
                camera_parameters=[
                    {"focal_length": 50, "sensor_width": 36, "sensor_height": 24},
                ],
            ),
            MetahumanUE5OutputBaseModel(
                metahuman_model="https://example.com/metahuman_model2.fbx",
                unreal_engine_version="5.0",
            ),
        ),
    ],
)
def test_transform(input_data: ImageSequenceInputBaseModel, expected_output: MetahumanUE5OutputBaseModel):
    response = client.post("/transform/", json=input_data.dict())
    assert response.status_code == 200
    assert response.json() == expected_output.dict()

@pytest.mark.parametrize(
    "invalid_input",
    [
        (
            ImageSequenceInputBaseModel(
                images=[
                    {"url": "https://example.com/image1.jpg", "timestamp": "not atimestamp"},
                ],
                camera_parameters=[
                    {"focal_length": 35, "sensor_width": 36, "sensor_height": 24},
                ],
            ),
        ),
        (
            ImageSequenceInputBaseModel(
                images=[
                    {"url": "not an url", "timestamp": "2021-01-01 00:00:00"},
                ],
                camera_parameters=[
                    {"focal_length": -50, "sensor_width": 36, "sensor_height": 24},
                ],
            ),
        ),
    ],
)
def test_transform_invalid_input(invalid_input: ImageSequenceInputBaseModel):
    response = client.post("/transform/", json=invalid_input.dict())
    assert response.status_code != 200
