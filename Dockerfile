
FROM python:3.12-slim

ARG OPENCV_VERSION=4.9.0

WORKDIR /opt/build

# Instala dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential cmake \
  wget unzip \
  libjpeg-dev libpng-dev libtiff-dev \
  libwebp-dev libopenjp2-7-dev \
  libtbb-dev libeigen3-dev \
  libprotobuf-dev protobuf-compiler \
  libhdf5-dev \
  tesseract-ocr tesseract-ocr-por \
  python3-dev \
  && pip install --no-cache-dir numpy

# Descarga y compila OpenCV + contrib
RUN wget -q https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip -O opencv.zip && \
  wget -q https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip -O opencv_contrib.zip && \
  unzip -qq opencv.zip -d /opt && rm opencv.zip && \
  unzip -qq opencv_contrib.zip -d /opt && rm opencv_contrib.zip && \
  cmake \
  -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-${OPENCV_VERSION}/modules \
  -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
  -D OPENCV_ENABLE_NONFREE=ON \
  -D WITH_JPEG=ON -D WITH_PNG=ON -D WITH_TIFF=ON \
  -D WITH_WEBP=ON -D WITH_OPENJPEG=ON \
  -D WITH_EIGEN=ON -D WITH_TBB=ON -D WITH_LAPACK=ON \
  -D WITH_PROTOBUF=ON \
  -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF \
  -D BUILD_opencv_python2=OFF -D BUILD_opencv_python3=ON \
  -D PYTHON3_EXECUTABLE=/usr/local/bin/python \
  -D PYTHON3_INCLUDE_DIR=/usr/local/include/python3.12/ \
  -D PYTHON3_LIBRARY=/usr/local/lib/libpython3.so \
  -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.12/site-packages/ \
  -D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.12/site-packages/numpy/core/include/ \
  /opt/opencv-${OPENCV_VERSION} && \
  make -j"$(nproc)" && make install && \
  rm -rf /opt/build/* /opt/opencv-${OPENCV_VERSION} /opt/opencv_contrib-${OPENCV_VERSION}

# Instala mediapipe (¡ahora sí!)
RUN pip install --no-cache-dir mediapipe

# Listo para tu aplicación
WORKDIR /app
COPY ./app /app

CMD ["python", "main.py"]

