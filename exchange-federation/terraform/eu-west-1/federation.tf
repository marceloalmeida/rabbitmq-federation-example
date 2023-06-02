resource "rabbitmq_federation_upstream" "test" {
  name  = "test"
  vhost = rabbitmq_permissions.guest.vhost

  definition {
    uri             = format("amqp://%s:%s@%s:%s/%s", "guest", "guest", "rabbitmq-eu-central-1", 5672, rabbitmq_permissions.guest.vhost)
    prefetch_count  = 1000
    reconnect_delay = 5
    ack_mode        = "on-confirm"
    trust_user_id   = false
    max_hops        = 1
  }
}

resource "rabbitmq_policy" "test" {
  name  = "test"
  vhost = rabbitmq_permissions.guest.vhost

  policy {
    pattern  = format("^%s$", rabbitmq_exchange.test.name)
    priority = 1000
    apply_to = "exchanges"

    definition = {
      federation-upstream = rabbitmq_federation_upstream.test.name
    }
  }
}
