# First create a .env file in root
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

# Build the Docker image

To run this streamlit app, pull down the code and run the following in your terminal:
```bash
 $ sudo docker build --network=host -t app . --progress plain
 ```
The `--progress plain` is optional.
The sudo is also dependant on your system.  I need it on my Ubuntu system, but mac does not.

But the `--network=host` command is necessary.

This will build the docker image.

# Run the docker image
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
