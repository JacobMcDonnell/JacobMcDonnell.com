FROM golang:1.24.4-alpine3.22
MAINTAINER Jacob McDonnell <jacob@jacobmcdonnell.com>
EXPOSE 8000
WORKDIR /app
COPY . .
RUN go build
cmd ["./web"]
