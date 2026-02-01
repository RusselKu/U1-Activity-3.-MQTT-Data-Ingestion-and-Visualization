docker-compose run --rm webserver airflow users create `
    --username airflow `
    --firstname Admin `
    --lastname User `
    --role Admin `
    --email admin@example.com `
    --password airflow


iniciar el db 
docker-compose run --rm webserver airflow db init

mongo
docker exec -it pipeline_chaos_to_insights-mongodb-1 mongosh -u root -p example --authenticationDatabase admin
use project_db
show collections


