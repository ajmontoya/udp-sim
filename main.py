import argparse
import json
import random
import socket
import sys
import time


def cmdline_args() -> tuple[str, int, int, float, bool]:
    parser = argparse.ArgumentParser(prog="udpsim", description="UDP Simulator")

    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="UDP IP address",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=41234,
        help="UDP port num",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="Num seconds to run simulator",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.2,
        help="Sleep for delay seconds between UDP send",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )

    args: argparse.Namespace = parser.parse_args()
    print(args) if args.verbose else None

    return (args.address, args.port, args.timeout, args.delay, args.verbose)


def gen_rand_data(t_diff: float) -> dict:
    return {
        "vehicle": "d126",
        "escid": random.choice([0, 1, 2, 3]),
        "measurements": {
            "time": t_diff,
            "rpm": random.randint(0, 5000),
            "power": random.randint(10, 100),
            "voltage": random.uniform(0.1, 5.9),
            "temp": random.uniform(35, 45),
            "current": random.uniform(-0.01, 0.1),
        },
        "labels": ["time", "rpm", "power", "voltage", "temp", "current"],
        "uom": {
            "time": "sec",
            "rpm": "rpm",
            "power": "%",
            "voltage": "V",
            "temp": "°C",
            "current": "Amps",
        },
    }


def main() -> None:
    addr, port, timeout, delay, is_verbose = cmdline_args()

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(client) if is_verbose else None

    print("Starting simulator...")

    try:
        t_start, t_diff = time.time(), 0

        while timeout is None or t_diff < timeout:
            data = gen_rand_data(t_diff)
            print(data) if is_verbose else None

            payload = json.dumps(data).encode()
            client.sendto(payload, (addr, port))

            time.sleep(delay)
            t_diff = time.time() - t_start
    except KeyboardInterrupt:
        print("Closing socket and exiting...")
        client.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
