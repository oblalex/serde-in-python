#! /usr/bin/env python
# coding: utf-8

import argparse
import os

from pathlib import Path

from schemas import Flight
from utils import (
    measure, validate, format_time, format_rss, to_camel, from_camel,
)


DATA_ROOT = Path(__file__).absolute().parent


def load_args():
    parser = argparse.ArgumentParser(
        description="Serde benchmarks"
    )
    parser.add_argument(
        '-c', '--cycles',
        dest='cycles',
        type=int,
        default=10,
        help="Number of cycles for benchmarks. Default: 10",
    )
    return parser.parse_args()


def load_csv(file_name='data.csv'):
    import csv

    path = str(DATA_ROOT / file_name)
    with open(path) as f:
        reader = csv.DictReader(f)
        return [
            {
                key: value if value != '' else None
                for key, value in item.items()
            }
            for item in reader
        ]


def load_csv_and_validate(file_name='data.csv'):
    data = load_csv(file_name)
    validate(data)
    return data


def save_csv(data, file_name='data.csv', test=True):
    import csv

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    fieldnames = list(Flight.fields.keys())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    finally:
        if test:
            os.remove(path)


def load_csv_quote_nonnumeric(file_name='data.csv.quoted'):
    import csv

    path = str(DATA_ROOT / file_name)
    with open(path) as f:
        reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
        return [
            {
                key: value if value != '' else None
                for key, value in item.items()
            }
            for item in reader
        ]


def load_csv_quote_nonnumeric_and_validate(file_name='data.csv.quoted'):
    data = load_csv_quote_nonnumeric(file_name)
    validate(data)
    return data


def save_csv_quote_nonnumeric(data, file_name='data.csv.quoted', test=True):
    import csv

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    fieldnames = list(Flight.fields.keys())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'w') as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC,
            )
            writer.writeheader()
            writer.writerows(data)
    finally:
        if test:
            os.remove(path)


def load_csv_pandas(file_name='data.csv.pandas'):
    import pandas as pd

    path = str(DATA_ROOT / file_name)
    df = pd.read_csv(path)
    df = df.where((pd.notnull(df)), None)
    return df.to_dict('records')


def load_csv_pandas_and_validate(file_name='data.csv.pandas'):
    data = load_csv_pandas(file_name)
    validate(data)
    return data


def save_csv_pandas(data, file_name='data.csv.pandas', test=True):
    import csv
    import pandas as pd

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)
    df = pd.DataFrame(data)

    try:
        df.to_csv(path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    finally:
        if test:
            os.remove(path)


def load_json(file_name='data.json'):
    import json

    path = str(DATA_ROOT / file_name)
    with open(path) as f:
        return list(json.load(f))


def load_json_and_validate(file_name='data.json'):
    data = load_json(file_name)
    validate(data)
    return data


def save_json(data, file_name='data.json', test=True):
    import json

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'w') as f:
            json.dump(data, f, separators=(',', ':'))
    finally:
        if test:
            os.remove(path)


def load_ujson(file_name='data.json.u'):
    import ujson

    path = str(DATA_ROOT / file_name)
    with open(path) as f:
        return list(ujson.load(f))


def load_ujson_and_validate(file_name='data.json.u'):
    data = load_ujson(file_name)
    validate(data)
    return data


def save_ujson(data, file_name='data.json.u', test=True):
    import ujson

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'w') as f:
            ujson.dump(data, f)
    finally:
        if test:
            os.remove(path)


def load_json_lines(file_name='data.jl'):
    import json

    path = str(DATA_ROOT / file_name)
    with open(path) as f:
        return [
            json.loads(line)
            for line in f
        ]


def load_json_lines_and_validate(file_name='data.jl'):
    data = load_json_lines(file_name)
    validate(data)
    return data


def save_json_lines(data, file_name='data.jl', test=True):
    import json

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'w') as f:
            for item in data:
                f.write(json.dumps(item, separators=(',', ':')) + '\n')
    finally:
        if test:
            os.remove(path)


def load_ujson_lines(file_name='data.jl.u'):
    import ujson

    path = str(DATA_ROOT / file_name)
    with open(path) as f:
        return [
            ujson.loads(line)
            for line in f
        ]


def load_ujson_lines_and_validate(file_name='data.jl.u'):
    data = load_ujson_lines(file_name)
    validate(data)
    return data


def save_ujson_lines(data, file_name='data.jl.u', test=True):
    import ujson

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'w') as f:
            for item in data:
                f.write(ujson.dumps(item) + '\n')
    finally:
        if test:
            os.remove(path)


def save_msgpack(data, file_name='data.msgpack', test=True):
    import msgpack

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            f.write(msgpack.packb(data))
    finally:
        if test:
            os.remove(path)


def load_msgpack(file_name='data.msgpack'):
    import msgpack

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        return msgpack.unpackb(f.read())


def save_msgpack_utf(data, file_name='data.msgpack.utf', test=True):
    import msgpack

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            f.write(msgpack.packb(data, use_bin_type=True))
    finally:
        if test:
            os.remove(path)


def load_msgpack_utf(file_name='data.msgpack.utf'):
    import msgpack

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        return msgpack.unpackb(f.read(), encoding='utf-8')


def load_msgpack_utf_and_validate(file_name='data.msgpack.utf'):
    data = load_msgpack_utf(file_name)
    validate(data)
    return data


def save_msgpack_utf_stream(data, file_name='data.msgpack.utf.stream', test=True):
    import msgpack

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            for item in data:
                f.write(msgpack.packb(item, use_bin_type=True))
    finally:
        if test:
            os.remove(path)


def load_msgpack_utf_stream(file_name='data.msgpack.utf.stream'):
    import msgpack

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        unpacker = msgpack.Unpacker(f, encoding='utf-8')
        return list(unpacker)


def load_msgpack_utf_stream_and_validate(file_name='data.msgpack.utf.stream'):
    data = load_msgpack_utf_stream(file_name)
    validate(data)
    return data


def save_umsgpack(data, file_name='data.msgpack.u', test=True):
    import umsgpack

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            f.write(umsgpack.packb(data))
    finally:
        if test:
            os.remove(path)


def load_umsgpack(file_name='data.msgpack.u'):
    import umsgpack

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        return umsgpack.unpackb(f.read())


def load_umsgpack_and_validate(file_name='data.msgpack.u'):
    data = load_umsgpack(file_name)
    validate(data)
    return data


def load_avro(file_name='data.avro'):
    from avro.datafile import DataFileReader
    from avro.io import DatumReader

    path = str(DATA_ROOT / file_name)
    reader = DataFileReader(open(path, "rb"), DatumReader())

    try:
        return list(reader)
    finally:
        reader.close()


def save_avro(data, file_name='data.avro', test=True):
    import json

    import avro.schema

    from avro.datafile import DataFileWriter
    from avro.io import DatumWriter

    schema_path = str(DATA_ROOT / 'schemas.avsc')
    with open(schema_path) as f:
        schema = avro.schema.SchemaFromJSONData(json.load(f))

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)
    writer = DataFileWriter(open(path, "wb"), DatumWriter(), schema)

    try:
        for datum in data:
            writer.append(datum)
    finally:
        writer.close()

        if test:
            os.remove(path)


def save_avro_fast(data, file_name='data.avro.fast', test=True):
    import json

    from fastavro import writer

    schema_path = str(DATA_ROOT / 'schemas.avsc')
    with open(schema_path) as f:
        schema = json.load(f)

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as out:
            writer(out, schema, data)
    finally:
        if test:
            os.remove(path)


def load_avro_fast(file_name='data.avro.fast'):
    import json

    import fastavro as avro

    schema_path = str(DATA_ROOT / 'schemas.avsc')
    with open(schema_path) as f:
        schema = json.load(f)

    path = str(DATA_ROOT / file_name)

    with open(path, 'rb') as f:
        reader = avro.reader(f, reader_schema=schema)
        return list(reader)


def save_protobuf(data, file_name='data.proto', test=True):
    import schemas_pb2

    flight_book = schemas_pb2.FlightBook()

    for item in data:
        flight = flight_book.flights.add()

        for key, value in item.items():
            if value is not None:
                setattr(flight, key, value)

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            f.write(flight_book.SerializeToString())
    finally:
        if test:
            os.remove(path)


def load_protobuf(file_name='data.proto'):
    import schemas_pb2

    flight_book = schemas_pb2.FlightBook()

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        flight_book.ParseFromString(f.read())
        return list(flight_book.flights)


def load_protobuf_to_dicts(file_name='data.proto'):
    from schemas import Flight

    field_names = list(Flight.fields.keys())
    items = load_protobuf(file_name)

    return [
        {
            file_name: getattr(x, file_name)
            for file_name in field_names
        }
        for x in items
    ]


def save_capnp(data, file_name='data.capnp', test=True):
    import capnp
    capnp.remove_import_hook()

    schemas_path = str(DATA_ROOT / 'schemas.capnp')
    schemas = capnp.load(schemas_path)

    flight_book = schemas.FlightBook.new_message()
    flights = flight_book.init('flights', len(data))

    for i, item in enumerate(data):
        flight = flights[i]
        for key, value in item.items():
            key = to_camel(key)

            if value is None:
                try:
                    setattr(flight, key, -1)
                except capnp.lib.capnp.KjException:
                    setattr(flight, key, "")
            else:
                setattr(flight, key, value)

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            flight_book.write(f)
    finally:
        if test:
            os.remove(path)


def save_capnp_packed(data, file_name='data.capnp.packed', test=True):
    import capnp
    capnp.remove_import_hook()

    schemas_path = str(DATA_ROOT / 'schemas.capnp')
    schemas = capnp.load(schemas_path)

    count = len(data)

    flight_book = schemas.FlightBook.new_message()
    flights = flight_book.init('flights', len(data))

    for i, item in zip(range(count), data):
        flight = flights[i]
        for key, value in item.items():
            key = to_camel(key)

            if value is None:
                try:
                    setattr(flight, key, -1)
                except capnp.lib.capnp.KjException:
                    setattr(flight, key, "")
            else:
                setattr(flight, key, value)

    if test:
        file_name = "{}.{}".format(file_name, os.getpid())

    path = str(DATA_ROOT / file_name)

    try:
        with open(path, 'wb') as f:
            flight_book.write_packed(f)
    finally:
        if test:
            os.remove(path)


def load_capnp(file_name='data.capnp'):
    import capnp
    capnp.remove_import_hook()

    schemas_path = str(DATA_ROOT / 'schemas.capnp')
    schemas = capnp.load(schemas_path)

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        flight_book = schemas.FlightBook.read(
            f, traversal_limit_in_words=2 ** 61,
        )
        return list(flight_book.flights)


def load_capnp_to_dicts(file_name='data.capnp'):
    import capnp
    capnp.remove_import_hook()

    schemas_path = str(DATA_ROOT / 'schemas.capnp')
    schemas = capnp.load(schemas_path)

    path = str(DATA_ROOT / file_name)
    with open(path, 'rb') as f:
        flight_book = schemas.FlightBook.read(
            f, traversal_limit_in_words=2 ** 61,
        )
        flights = flight_book.to_dict()['flights']

    for flight in flights:
        for key in flight.keys():
            value = flight.pop(key)

            if (value == -1) or (value == ""):
                value = None

            key = from_camel(key)
            flight[key] = value

    return flights


def main():
    args = load_args()
    data = load_csv_pandas('source.csv')

    # CSV pandas
    save_csv_pandas(data, test=False)

    time, rss = measure(args.cycles, save_csv_pandas, data)
    print('save_csv_pandas', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_csv_pandas)
    print('load_csv_pandas', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_csv_pandas_and_validate)
    print('load_csv_pandas_and_validate', format_time(time), format_rss(rss))

    # CSV default
    save_csv(data, test=False)

    time, rss = measure(args.cycles, save_csv, data)
    print('save_csv', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_csv)
    print('load_csv', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_csv_and_validate)
    print('load_csv_and_validate', format_time(time), format_rss(rss))

    # CSV quote_nonnumeric
    save_csv_quote_nonnumeric(data, test=False)

    time, rss = measure(args.cycles, save_csv_quote_nonnumeric, data)
    print('save_csv_quote_nonnumeric', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_csv_quote_nonnumeric)
    print('load_csv_quote_nonnumeric', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_csv_quote_nonnumeric_and_validate)
    print('load_csv_quote_nonnumeric_and_validate', format_time(time), format_rss(rss))

    # JSON default
    save_json(data, test=False)

    time, rss = measure(args.cycles, save_json, data)
    print('save_json', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_json)
    print('load_json', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_json_and_validate)
    print('load_json_and_validate', format_time(time), format_rss(rss))

    # uJSON default
    save_ujson(data, test=False)

    time, rss = measure(args.cycles, save_ujson, data)
    print('save_ujson', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_ujson)
    print('load_ujson', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_ujson_and_validate)
    print('load_ujson_and_validate', format_time(time), format_rss(rss))

    # JSON lines
    save_json_lines(data, test=False)

    time, rss = measure(args.cycles, save_json_lines, data)
    print('save_json_lines', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_json_lines)
    print('load_json_lines', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_json_lines_and_validate)
    print('load_json_lines_and_validate', format_time(time), format_rss(rss))

    # uJSON lines
    save_ujson_lines(data, test=False)

    time, rss = measure(args.cycles, save_ujson_lines, data)
    print('save_ujson_lines', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_ujson_lines)
    print('load_ujson_lines', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_ujson_lines_and_validate)
    print('load_ujson_lines_and_validate', format_time(time), format_rss(rss))

    # msgpack
    save_msgpack(data, test=False)

    time, rss = measure(args.cycles, save_msgpack, data)
    print('save_msgpack', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_msgpack)
    print('load_msgpack', format_time(time), format_rss(rss))

    # msgpack utf
    save_msgpack_utf(data, test=False)

    time, rss = measure(args.cycles, save_msgpack_utf, data)
    print('save_msgpack_utf', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_msgpack_utf)
    print('load_msgpack_utf', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_msgpack_utf_and_validate)
    print('load_msgpack_utf_and_validate', format_time(time), format_rss(rss))

    # msgpack utf stream
    save_msgpack_utf_stream(data, test=False)

    time, rss = measure(args.cycles, save_msgpack_utf_stream, data)
    print('save_msgpack_utf_stream', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_msgpack_utf_stream)
    print('load_msgpack_utf_stream', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_msgpack_utf_stream_and_validate)
    print('load_msgpack_utf_stream_and_validate', format_time(time), format_rss(rss))

    # umsgpack
    save_umsgpack(data, test=False)

    time, rss = measure(args.cycles, save_umsgpack, data)
    print('save_umsgpack', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_umsgpack)
    print('load_umsgpack', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_umsgpack_and_validate)
    print('load_umsgpack_and_validate', format_time(time), format_rss(rss))

    # avro
    save_avro(data, test=False)

    time, rss = measure(args.cycles, save_avro, data)
    print('save_avro', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_avro)
    print('load_avro', format_time(time), format_rss(rss))

    # avro fast
    save_avro_fast(data, test=False)

    time, rss = measure(args.cycles, save_avro_fast, data)
    print('save_avro_fast', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_avro_fast)
    print('load_avro_fast', format_time(time), format_rss(rss))

    # protobuf
    save_protobuf(data, test=False)

    time, rss = measure(args.cycles, save_protobuf, data)
    print('save_protobuf', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_protobuf)
    print('load_protobuf', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_protobuf_to_dicts)
    print('load_protobuf_to_dicts', format_time(time), format_rss(rss))

    # capnp
    save_capnp(data, test=False)
    save_capnp_packed(data, test=False)

    time, rss = measure(args.cycles, save_capnp, data)
    print('save_capnp', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, save_capnp_packed, data)
    print('save_capnp_packed', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_capnp)
    print('load_capnp', format_time(time), format_rss(rss))

    time, rss = measure(args.cycles, load_capnp_to_dicts)
    print('load_capnp_to_dicts', format_time(time), format_rss(rss))


if __name__ == '__main__':
    main()
