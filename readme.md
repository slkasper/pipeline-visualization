# Description
This is a streamlit app that I created to take data originally from a .csv file, through Underline's Redshift and transformed in dbt to a final production streamlit app for users to interactively interrogate the data 


The curated tables that I created as a result of this ELT process are used here to feed the streamlit app. I used pandas, geopandas, pydeck, and shapley to create a streamlit app that displays an interactive map with as many cities as csv files that got added to the S3 bucket.  Now, non-technical users can use this app which is internally hosted on Kubernetes to interact with the data.


Here is a quick gif of the working app in motion.
<img src="img/streamlit-run-2023-12-14-17-12-70.gif" alt="gif">


As you can see, the user can add data filters from the left sidebar to specify regions and other business specs, then hover over a specific location point to see relevant tooltip information. 


Once the filters are in place, a dataframe below is populated with the selections with information such as addresses and company names so the user (maybe a Sales Rep) can click the button below and download the dataframe for printing and taking it out on the road!


# Running the Dockerfile
To create the Dockerfile, you need to run the commands below to build your docker image.

## First create a .env file in root
After you pull down the code, create a .env file in the root folder of the repo.
Add the following:

```
REDSHIFT_HOST=aws_location
REDSHIFT_DB=your_db
REDSHIFT_PORT=your_port
REDSHIFT_USER=your_user_name
REDSHIFT_PASS=your_redshift_password
```
NOTE: dsu package needs adjustment -- REDSHIFT_PORT needs to be cast as int. For now, do this manually until in your file until the package gets corrected.

## Build the Docker image

To run this streamlit app, pull down the code and run the following in your terminal:
```bash
 $ sudo docker build --network=host -t app . --progress plain
 ```
The `--progress plain` is optional.
The sudo is also dependant on your system.  I need it on my Ubuntu system, but mac does not.

But the `--network=host` command is necessary.

This will build the docker image.

## Run the docker image
To run the image, run this command (again sudo may not be necessary for you if you are on a mac)

```bash
#$ sudo docker run --network=host -p 8501:8501 -t app 
docker run --network=host \
 -p 8501:8501 \
 -v </path/to/your>/.env:/app/.env \
 -t app
```

You should be able to check your browser for `localhost:8501` to see the streamlit app.

<!-- # Pull down the image from ghcr.io
Anyone can run this image using these instructions (in theory)

```bash
#pull down the latest image from https://github.com/nrfta/business-data-platform/pkgs/container/business-data-platform
# copy the latest image. should look like this:
docker pull ghcr.io/nrfta/business-data-platform:sha-baf0b1bf

```
Then run your image.  Remember, you need a .env file mounted as a volume when you run.  You need to use absolute pathes for it.

Note: The `--platform=linux/amd64` line is to allow M1/M2 chip (mac machine) to run.  ATM, this gives the 'watchdog' error from streamlit which should be handled with the WORKDIR in the dockerfile.  It works on a linux machine, still errors on a mac.

```bash
sudo docker run -v /path/to/your/.env:/app/.env -p 8501:8501 --platform=linux/amd64 <img_tag or sha>

#example
sudo docker run -v /Users/you/files/.env:/app/.env -p 8501:8501 --platform=linux/amd64 8f73d0387d8f
```
 -->
