import redis as redis_client
import time
import os
from dotenv import load_dotenv

load_dotenv()

r = redis_client.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True
)

group = 'notification-group'
streams = ['order_completed', 'refund_order']

for stream in streams:
    try:
        r.xgroup_create(stream, group, mkstream=True)
    except:
        print(f'Group already exists for {stream}!')

while True:
    try:
        results = r.xreadgroup(group, group, {s: '>' for s in streams}, count=1, block=5000)

        if results:
            for result in results:
                stream_name = result[0]
                obj = result[1][0][1]

                if stream_name == 'order_completed':
                    print(f"Obaveštenje: Porudžbina {obj.get('pk')} je uspešno kreirana i plaćena.")
                elif stream_name == 'refund_order':
                    print(f"Obaveštenje: Porudžbina {obj.get('pk')} je refundirana.")

    except Exception as e:
        print(f"Notification consumer error: {e}")
        time.sleep(1)
