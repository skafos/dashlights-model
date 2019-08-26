# dashlights-model
A Turi Create object detection model for the Dashlights app. The model is trained and data is stored (for the moment) on AWS SageMaker.

## Workflow Steps

### Data Creation
Before training any model you need training data (`data_creation_pipeline.ipynb`). Here, we create synthetic data based on these two sources below:

- `Dashboards/` contains all PNG background dashboard images used for data creation.
- `Icons/` contains 12 PNG icon images used for data creation. These refer to the 12 Subaru icon classes that the model will be trained to identify

The data creation pipeline loops through all background images and pastes icon(s) in random, isolated locations. It also automatically writes out annotations data to accompany the images, making it easy to use TuriCreate for training. There are a few high level parameters you can tweak to control the creation process.

- `sizes` - this is an array of image scales that will be applied to the icons when placing on backgrounds. 1.0 represents the icon at it's natural size.
- `counts_per_size` - this is an integer controlling how many unique training images to make for each icon+background+size combination. The higher this number, the more training data gets created.

All created data will be saved in the `NewTrainingImages/` folder and then saved to a TuriCreate sframe `dashlight_images.sframe`.

### Training
Training is simple with TuriCreate. Load the data, split it into a training and testing set, configure the GPU and worker numbers, and then just wait. Training happens in `train_model.ipynb`.

This notebook creates a bunch of artifacts, none of which are persisted to git. Thankfully, AWS SageMaker notebooks have an EBS storage volume attached meaning we can persist our data right there in that environment. For each trained model, the following artifacts are created/saved:

- turicreate model
- coreml model
- testing data sframe
- testing data zipfile (for download and inspection if desired)
- model evaluation scores on testing data

Each will have a timestamp version name pre-pended to the filename. As part of the code, data is uploaded and saved to S3. 


## Future Work
A few more things need to be worked out in the future.

1. **More Steps in Data Creation.** We've added many things to the data creation pipeline to make the training data as representative of the real world as possible. However a few more steps are needed: Image rotation and scaling adjustments should be added, more background images are needed (of different dimensions too), and potentially better shots of the icons could help too.
