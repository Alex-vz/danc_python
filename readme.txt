Проект DiagramAsNativeCode (DANC)


. start_data3
cd ~/zwork1/diagrams/code


docker-compose up

docker-compose run web svg -o my.svg umlet ./data/NativeLangDiagramStruct.uxf

docker-compose run web url umlet ./data/NativeLangDiagramStruct.uxf