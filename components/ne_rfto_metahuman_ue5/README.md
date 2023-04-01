
# NeRFToMetahumanUE5

This Yeager Workflow takes an input of ImageSequenceInputBaseModel, a sequence of images containing different views of the face to be processed, along with their camera parameters, and processes it to generate MetahumanUE5OutputBaseModel, the final metahuman model in Unreal Engine 5 format.

## Initial generation prompt
description: "IOs - input: 'ImageSequenceInputBaseModel: A sequence of images containing\
  \ different views\n  of the face to be processed, along with their camera parameters.'\n\
  output: 'MetahumanUE5OutputBaseModel: The final metahuman model in Unreal Engine\
  \ 5\n  format.'\n"
name: NeRFToMetahumanUE5


## Transformer breakdown
- Execute the transform of the AbstractWorkflow
- Prepare the Output BaseModel

## Parameters
[]

        