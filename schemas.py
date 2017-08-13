# coding: utf-8

from schematics.models import Model
from schematics.types import IntType, FloatType, StringType, DateType


class Flight(Model):
    FL_DATE = DateType()
    AIRLINE_ID = IntType()
    CARRIER = StringType()
    TAIL_NUM = StringType()
    FL_NUM = IntType()
    ORIGIN_AIRPORT_ID = IntType()
    ORIGIN_AIRPORT_SEQ_ID = IntType()
    ORIGIN_CITY_MARKET_ID = IntType()
    ORIGIN = StringType()
    ORIGIN_CITY_NAME = StringType()
    ORIGIN_STATE_ABR = StringType()
    ORIGIN_STATE_FIPS = IntType()
    ORIGIN_STATE_NM = StringType()
    ORIGIN_WAC = IntType()
    DEST_AIRPORT_ID = IntType()
    DEST_AIRPORT_SEQ_ID = IntType()
    DEST_CITY_MARKET_ID = IntType()
    DEST = StringType()
    DEST_CITY_NAME = StringType()
    DEST_STATE_ABR = StringType()
    DEST_STATE_FIPS = IntType()
    DEST_STATE_NM = StringType()
    DEST_WAC = IntType()
    DEP_DELAY = FloatType()
    TAXI_OUT = FloatType()
    WHEELS_OFF = FloatType()
    WHEELS_ON = FloatType()
    TAXI_IN = FloatType()
    ARR_DELAY = FloatType()
    AIR_TIME = FloatType()
    DISTANCE = FloatType()
