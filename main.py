import argparse
from enum import IntEnum
import json
from pprint import pprint
import random
import socket
import sys
import time


class Config(IntEnum):
    SINGLE = 1
    CROSS_02 = 2
    CROSS_13 = 3
    ALL_4 = 4


def cmdline_args() -> tuple[str, int, int, int, int, list[int], float, bool]:
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
        default=1,
        help="Num seconds to run simulator",
    )
    parser.add_argument(
        "--power",
        type=int,
        default=20,
        help="ESC power level as a percentage [10-100]",
    )
    parser.add_argument(
        "--config",
        type=int,
        default=4,
        help="Test configuration [1: single, 2: cross_02, 3: cross_13, 4: all_4]",
    )
    parser.add_argument(
        "--steps",
        type=int,
        nargs="*",
        help="Stepwise power intervals",
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

    return (
        args.address,
        args.port,
        args.timeout,
        args.power,
        args.config,
        args.steps,
        args.delay,
        args.verbose,
    )


def gen_rand_data(
    testid: float, ts_idx: int, count: int, power: int, config: Config, step: bool
) -> dict:
    return {
        "vehicle": "d126",
        "testid": testid,
        "escid": count,
        "params": {
            "power": power,
            "config": config.value,
            "step": step,
        },
        "measurements": {
            "time": ts_idx,
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
    addr, port, timeout, power, config, steps, delay, is_verbose = cmdline_args()

    print(
        f"address: {addr}, port: {port}, timeout: {timeout}, power: {power}, config: {config}, step: {steps}, delay: {delay}, is verbose: {is_verbose}"
    )

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(client) if is_verbose else None

    print("Starting simulator...")

    try:
        t_start, t_diff = time.time(), 0
        count, ts_idx = 0, 1
        cfg = Config(config)

        if steps:
            for powerStep in steps:
                data = gen_rand_data(t_start, ts_idx, count, powerStep, cfg, powerStep)

                payload = json.dumps(data).encode()
                client.sendto(payload, (addr, port))
                pprint(payload) if is_verbose else None

                time.sleep(delay)

                if count < 3:
                    count += 1
                else:
                    count = 0
                    ts_idx += 1
        else:
            while timeout is None or t_diff < timeout:
                data = gen_rand_data(t_start, ts_idx, count, power, cfg, None)

                payload = json.dumps(data).encode()
                client.sendto(payload, (addr, port))
                pprint(payload) if is_verbose else None

                time.sleep(delay)
                t_diff = time.time() - t_start

                if count < 3:
                    count += 1
                else:
                    count = 0
                    ts_idx += 1

    except KeyboardInterrupt:
        print("Closing socket and exiting...")
        client.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
