# Covid-19 tracker around the world

The project aims to provide an efficient solution for analyzing and visualizing data on covid-19 that can be found on https://github.com/CSSEGISandData/COVID-19. To achieve this, we're utilizing a technology stack that includes Elastic Search, Kibana, and Cassandra, all orchestrated using Docker Compose to implement the pipeline below:

![HomeView](images/archtecture.PNG)

## Prerequisites
    - Docker
    - Docker Compose

## Installation
    1- Clone the repository: git clone https://github.com/SanaHassen/Elastic-Search-Project.git
    2- Navigate to the project directory then cd src
    3- Build Python image and start the containers: docker-compose up --build

> In our case, we chose to launch Cassandra, Elasticsearch, and Python in the first place. Once Python's job is successfully done, we launch the Kibana container to minimize resource consumption.

## Usage 
After the containerized services are running, you can access the different services:

### Cassandra
You can access Cassandra at `localhost:9042`. You can use the cqlsh command-line tool to interact with the Cassandra database. After applying transformations to the COVID-19 data, it is stored in Cassandra.

### Elasticsearch
You can access Elasticsearch at `http://localhost:9200`. You can use tools like curl or Postman to interact with the Elasticsearch API. The image below demonstrates the indexing of COVID-19 data in Elasticsearch within the `covid` index.

![HomeView](images/postman.png)

### Kibana
You can access Kibana at http://localhost:5601. You can use Kibana to visualize and analyze your data in Elasticsearch.

For example, we have created the dashboard below, which includes:
- Different metrics about confirmed, recovered, and death cases.
- A map showing the spread of COVID-19 in countries around the world.
- Various charts and graphs.

![HomeView](images/dashboard.png)

## Configuration
You can customize the configuration of the application and the Elasticsearch, Kibana, and Cassandra containers by modifying the environment variables in the docker-compose.yml file.

## Acknowledgments
Thanks to the Docker, Elasticsearch, Kibana, and Cassandra communities for providing such great tools!









