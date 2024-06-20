import argparse

from server.extra.server import app
import uvicorn

parser = argparse.ArgumentParser()
parser.add_argument('-rd', '--round_duration', type=int,  default=30)
parser.add_argument('-p', '--port', type=int, default=8000, help="The port on which the api will be accessible.")
parser.add_argument('-ho', '--host', default="localhost", help="The host on which the api will be accessible.")
args = parser.parse_args()

round_duration = args.round_duration
print(f"Round duration is set at {round_duration}")

uvicorn.run(app, host=args.host, port=args.port)
