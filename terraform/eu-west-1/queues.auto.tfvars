queues = {
  consumed-locally = {
    arguments = {
      "x-queue-type" : "classic"
    }
    routing_key = "local"
  }
  consumed-remotelly = {
    arguments = {
      "x-queue-type" : "classic"
    }
    routing_key = "remote"
  }
}
