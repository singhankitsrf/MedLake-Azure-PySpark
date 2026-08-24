# Streaming Design

Azure Event Hubs is consumed through its Kafka-compatible endpoint from Spark Structured Streaming. The design exposes partition/offset metadata, durable checkpointing, append-only Bronze storage, secret retrieval rather than hard-coded credentials, and independently scalable batch/streaming paths.
