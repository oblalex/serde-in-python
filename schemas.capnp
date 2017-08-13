@0xe04fc9f2d73ea4a8;

struct Flight {
  flDate @0 :Text;
  airlineId @1 :UInt32;
  carrier @2 :Text;
  tailNum @3 :Text;
  flNum @4 :UInt32;
  originAirportId @5 :UInt32;
  originAirportSeqId @6 :UInt32;
  originCityMarketId @7 :UInt32;
  origin @8 :Text;
  originCityName @9 :Text;
  originStateAbr @10 :Text;
  originStateFips @11 :UInt32;
  originStateNm @12 :Text;
  originWac @13 :UInt32;
  destAirportId @14 :UInt32;
  destAirportSeqId @15 :UInt32;
  destCityMarketId @16 :UInt32;
  dest @17 :Text;
  destCityName @18 :Text;
  destStateAbr @19 :Text;
  destStateFips @20 :UInt32;
  destStateNm @21 :Text;
  destWac @22 :UInt32;
  depDelay @23 :Float32;
  taxiOut @24 :Float32;
  wheelsOff @25 :Float32;
  wheelsOn @26 :Float32;
  taxiIn @27 :Float32;
  arrDelay @28 :Float32;
  airTime @29 :Float32;
  distance @30 :Float32;
}


struct FlightBook {
  flights @0 :List(Flight);
}
