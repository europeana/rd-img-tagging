# Image tagging

## Setup


conda activate tag_env

pip install -r requirements.txt

## Map vocabulary

redirect to readme file

## Harvest images

`nohup python src/vision/harvest.py --objects_per_provider 50 --providers_per_aggregator 30 --saving_path '/home/jcejudo/rd-img-tagging/data/evaluation_data.csv' &> harvesting.out &`

## Download images

`c python src/vision/download_images.py --input '/home/jcejudo/rd-img-tagging/data/evaluation_data.csv' --saving_dir '/home/jcejudo/projects/image_tagging_cloud/evaluation/images' &> download_images.out &`

## Upload images

`nohup python src/vision/upload_images.py --images_dir '/home/jcejudo/projects/image_tagging_cloud/evaluation/images' &> upload.out &`


## Predict images

`nohup python src/vision/predict.py --vocab 'data/vocabulary/mapped_vocabulary.csv' --data_path '/home/jcejudo/rd-img-tagging/data/evaluation_data.csv' --saving_path '/home/jcejudo/projects/image_tagging_cloud/evaluation/predictions.csv' &> predict.out &`



