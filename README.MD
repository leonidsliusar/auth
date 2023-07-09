1. Запустить из папки с проектом (где находится сам docker-compose.yml)
         
         docker compose up -d

2. Идем на http://0.0.0.0:8000/


3. Документация на http://0.0.0.0:8000/docs


4. Чтобы закрыть и удалить все (контейнеры, образы)
    
        docker compose down --rmi all

5. Чтобы не удалять образ

        docker compose down

6. Посмотреть образы в терминале 

         docker images

7. Посмотреть контейнеры


      docker ps - запущенные
      docker ps -a - незапущенные
