#!

if ! command -v microservice ; then
    wget http://resources.cumulocity.com/examples/microservice
    chmod +x microservice
    PATH=$PATH:.
fi

microservice pack -n health-microservice

