
import os
import yaml
from pathlib import Path
from pydantic import BaseModel

from core.abstract_component import AbstractComponent

class NeRFToMeshConverterInputDict(BaseModel):
    neRF_render: object


class NeRFToMeshConverterOutputDict(BaseModel):
    mesh: Path


class NeRFToMeshConverter(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.output_format: str = yaml_data["parameters"]["output_format"]
        self.precision: float = yaml_data["parameters"]["precision"]

    def transform(self, args: NeRFToMeshConverterInputDict) -> NeRFToMeshConverterOutputDict:
        precision = self.precision
        output_format = self.output_format

        # Convert NeRF render to a mesh representation using the precision parameter
        # (Implementation details for converting the NeRF render to a mesh should be added here)

        # Export the mesh to specified output_format (either .fbx or .obj)
        mesh_output_filepath = Path(f"converted_mesh.{output_format}")

        # Save mesh to specified format
        # (Implementation details for saving the mesh in .fbx or .obj format should be added here)

        return NeRFToMeshConverterOutputDict(mesh=mesh_output_filepath)


