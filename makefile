GPPFLAGS = -I/usr/local/include/modbus  -lmodbus

unit_test: unit_test.cpp
	g++ -o $@ $< $(GPPFLAGS)

fakelact: fakelact.cpp
	g++ -o $@ $< $(GPPFLAGS)

fakelact_TestClient: fakelact_TestClient.cpp
	g++ -o $@ $< $(GPPFLAGS)

clean:
	rm fakelact_TestClient
	rm fakelact
	rm *.o
