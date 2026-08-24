from __future__ import annotations
import argparse,os
from azure.eventhub import EventData,EventHubProducerClient
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--path",required=True); ap.add_argument("--max-events",type=int,default=100); a=ap.parse_args(); producer=EventHubProducerClient.from_connection_string(conn_str=os.environ["EVENTHUB_CONNECTION_STRING"],eventhub_name=os.environ["EVENTHUB_NAME"]); batch=producer.create_batch(); count=0
    with open(a.path,encoding="utf-8") as f:
        for line in f:
            if count>=a.max_events: break
            try: batch.add(EventData(line.strip()))
            except ValueError: producer.send_batch(batch); batch=producer.create_batch(); batch.add(EventData(line.strip()))
            count+=1
    if len(batch)>0: producer.send_batch(batch)
    producer.close(); print(f"Published {count} events")
if __name__=="__main__": main()
