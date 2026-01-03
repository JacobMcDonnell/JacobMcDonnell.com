FROM golang:1.25.5-alpine3.23
MAINTAINER Jacob McDonnell <jacob@jacobmcdonnell.com>
EXPOSE 8000
WORKDIR /app
COPY . .
RUN go build
cmd ["./web"]
