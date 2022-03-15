## Vocabulary mapping

create chunks of the vocabulary

`python src/split_vocabulary.py --vocab_path /home/jcejudo/image_tagging/data/oidv6-class-descriptions.csv --saving_path /home/jcejudo/image_tagging/data/chunks --n_chunks 20`

map to wikidata

`nohup python src/vocabulary/mapping_wikidata.py --vocab_path /home/jcejudo/image_tagging/data/chunks/vocabulary_19.csv --saving_path /home/jcejudo/image_tagging/data/chunks_wikidata/ &> wikidata.out &`


map individual chunks

`nohup python src/vocabulary/mapping_vocabularies.py --vocab_path /home/jcejudo/image_tagging/data/chunks_wikidata/vocabulary_19.csv --saving_path /home/jcejudo/image_tagging/data/chunks_aat/ --vocabulary_name aat &> mapping_aat.out &`

`nohup python src/vocabulary/mapping_vocabularies.py --vocab_path /home/jcejudo/image_tagging/data/chunks_aat/vocabulary_19.csv --saving_path /home/jcejudo/image_tagging/data/chunks_iconclass/ --vocabulary_name iconclass &> mapping_iconclass.out &` 

merge chunks

`python src/vocabulary/merge_vocabulary.py --chunks_path /home/jcejudo/image_tagging/data/chunks_iconclass --saving_path /home/jcejudo/image_tagging/data/mapped_vocabulary.csv`

analysis of total mapped vocabulary

`python src/vocabulary/analysis.py --vocab_path /home/jcejudo/image_tagging/data/entities.csv`

map to entity collection

`nohup python src/vocabulary/mapping_entity_api.py --vocab_path /home/jcejudo/image_tagging/data/mapped_vocabulary.csv --saving_path /home/jcejudo/image_tagging/data/entities.csv &> mapping_entities.out &`