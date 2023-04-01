
import os
import pytest
import yaml
from pydantic import BaseModel
from pathlib import Path

from components.nerf_to_mesh_converter import NeRFToMeshConverter, NeRFToMeshConverterInputDict, NeRFToMeshConverterOutputDict

# Test cases with mocked input and expected output data:
test_cases = [
    (
        NeRFToMeshConverterInputDict(neRF_render={"test_data": [0, 1, 2]}),
        {"output_format": "fbx", "precision": 0.1},
        NeRFToMeshConverterOutputDict(mesh=Path("converted_mesh.fbx")),
    ),
    (
        NeRFToMeshConverterInputDict(neRF_render={"test_data": [3, 4, 5]}),
        {"output_format": "obj", "precision": 0.5},
        NeRFToMeshConverterOutputDict(mesh=Path("converted_mesh.obj")),
    ),
    # Add more test cases here...
]

# Use @pytest.mark.parametrize to create multiple test scenarios:
@pytest.mark.parametrize("input_data,config_data,expected_output_data", test_cases)
def test_neRF_to_mesh_converter_transform(input_data, config_data, expected_output_data):
    # Create NeRFToMeshConverter instance
    component = NeRFToMeshConverter()

    # Mock configuration values
    component.output_format = config_data["output_format"]
    component.precision = config_data["precision"]

    # Call the transform() method with mocked input data
    output_data = component.transform(input_data)

    # Assert that the output matches the expected output
    assert output_data == expected_output_data

    # Clean up generated files
    if output_data.mesh.exists():
        output_data.mesh.unlink()

# Include error handling and edge case scenarios, if applicable:
def test_invalid_output_format():
    component = NeRFToMeshConverter()
    component.output_format = "invalid_format"
    component.precision = 0.1

    # Use the "context manager" pytest.raises to test for exceptions
    with pytest.raises(ValueError, match="Invalid output_format"):
        input_data = NeRFToMeshConverterInputDict(neRF_render={"test_data": [0, 1, 2]})
        component.transform(input_data)
