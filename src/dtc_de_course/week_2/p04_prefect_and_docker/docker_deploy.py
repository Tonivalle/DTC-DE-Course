from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer

from dtc_de_course.week_2.p03_param_flow.parametrized_flow import etl_multiple_dates

docker_block = DockerContainer.load("etl-test-container")

docker_deployment = Deployment.build_from_flow(
    flow=etl_multiple_dates, name="docker-etl-flow", infrastructure=docker_block
)

if __name__ == "__main__":
    docker_deployment.apply()  # type: ignore [attr-defined]
