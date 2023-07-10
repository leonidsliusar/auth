1. Запустить из папки с проектом (где находится сам docker-compose.yml)
         
         docker compose up

2. Идем на http://0.0.0.0:8000/


3. Документация на http://0.0.0.0:8000/docs


4. Verify code пока что выводится в консоль


5. Чтобы закрыть и удалить все (контейнеры, образы)
    
        docker compose down --rmi all

6. Чтобы не удалять образ

        docker compose down

7. Посмотреть образы в терминале 

         docker images

8. Посмотреть контейнеры


      docker ps - запущенные
      docker ps -a - незапущенные
