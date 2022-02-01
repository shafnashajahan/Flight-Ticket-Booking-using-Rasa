FROM python:alpine3.7

RUN python -m pip install --upgrade pip

RUN pip3 install --no-cache flask==2.0.1

RUN pip3 install --no-cache Flask-Cors==3.0.10

# RUN pip3 install --no-cache -qr requirements.txt

RUN mkdir -p /usr/src/app/chatbot/Flask

WORKDIR /usr/src/app/chatbot/Flask

COPY . /usr/src/app/chatbot/Flask

EXPOSE 5000

# RUN flask run {NOT WORKING}
# RUN python app.py

# RUN rasa run actions

# ENTRYPOINT [ "--cors", '"*"'' --enable-api ]

# docker build -t flight_flask .
# docker run -it -p 5000:5000 flight_flask python app.py
