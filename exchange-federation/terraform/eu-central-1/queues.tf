resource "rabbitmq_permissions" "guest" {
  user  = "guest"
  vhost = rabbitmq_vhost.test.name

  permissions {
    configure = ".*"
    write     = ".*"
    read      = ".*"
  }
}

resource "rabbitmq_queue" "test" {
  for_each = var.queues

  name  = each.key
  vhost = rabbitmq_permissions.guest.vhost

  settings {
    durable   = true
    arguments = lookup(each.value, "arguments", {})
  }
}

resource "rabbitmq_binding" "test" {
  for_each = var.queues

  source           = rabbitmq_exchange.test.name
  vhost            = rabbitmq_vhost.test.name
  destination      = each.key
  destination_type = "queue"
  routing_key      = lookup(each.value, "routing_key", "#")

  depends_on = [
    rabbitmq_queue.test
  ]
}
