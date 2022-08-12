# cumulocity-health-microservice
A microservice for Cumulocity IoT that approximates the health status of a device based on the alarms raised in a short period versus the trend in the long term.
## Installation
Clone the repository, run build.sh to generate the zip to deploy to your Cumulocity tenant.
### Manual Docker Build
There may be cases script provided by Cumulocity for microservice deployment does not work with the updates and such. In that case, you can follow the guide on Cumulocity IoT Guides (https://cumulocity.com/guides/microservice-sdk/http/#hello-microservice-python) on how to build the Docker container and get it ready for deployment on the platform. List of commands required to produce the deployable .zip taken from the guide adapted to this microservice are:
```
cd docker
docker build -t cumulocity-health-microservice
cd ..
docker save cumulocity-health-microservice > "image.tar"
zip cumulocity-health-microservice cumulocity.json image.tar
```
## Usage
The microservice exposes the endpoints <tenant-url>/service/health-microservice/deviceHealth and <tenant-url>/service/health-microservice/status, where you can get the status of the microservice, or health of a device by making a GET request. Both endpoints will return a JSON using REST. 

The microservice has its own role required to get the device status registered to the platform as health read which is added automatically to available roles and configurable on Administration/User Roles tab. Users without this role will be returned 401 Unauthorized as the response when a device's health status is requested.

Authorization is handled by the microservice itself with the Cumulocity platform as suggested in the microservice guide, so request authorization header should contain Basic authorization, the rest supported by Cumulocity is not yet supported.

Device health request should always contain a source parameter with a valid deviceId.
If none were provided or the deviceId is not correct, it will return 400 Bad Request.

The request ``` GET <tenant-url>/service/health-microservice/deviceHealth?source=<device-id> ``` will return:
```
{
    "health": "<EXCELLENT || POOR || INOPERATIVE>",
    "id": "<device-id>"
}
```
This microservice has PER_TENANT deployment type, so every tenant subscribed will get its own microservice, and roles should be set for every tenant independently.
