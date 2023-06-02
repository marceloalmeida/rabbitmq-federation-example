resource "rabbitmq_exchange" "test" {
  name  = "test-exchange"
  vhost = rabbitmq_permissions.guest.vhost

  settings {
    type    = "topic"
    durable = "true"
  }
}
